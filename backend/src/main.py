from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat import router as chat_router
from .api.query import router as query_router
from .api.user import router as user_router
from .core.config import settings
from .core.logging_config import root_logger
from .services.embedding_service import EmbeddingService
from .services.retrieval_service import RetrievalService
import cohere
from qdrant_client import AsyncQdrantClient
import asyncio


def create_app() -> FastAPI:
    root_logger.info("Creating FastAPI application")

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
    app.include_router(query_router, prefix="/api/query", tags=["query"])
    app.include_router(user_router, prefix="/api/user", tags=["user"])

    root_logger.info("API routers registered")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "message": "Docusaurus Chatbot API is running"}

    @app.on_event("startup")
    async def startup_event():
        root_logger.info("="*80)
        root_logger.info("APPLICATION STARTUP")
        root_logger.info(f"App Name: {settings.app_name}")
        root_logger.info(f"Debug Mode: {settings.debug}")
        root_logger.info(f"Database URL: {settings.database_url[:30]}...")
        root_logger.info(f"Qdrant URL: {settings.qdrant_url}")

        # Pre-initialize services to avoid cold start on first request
        root_logger.info("Pre-initializing services...")
        try:
            # Initialize Cohere client
            app.state.cohere_client = cohere.AsyncClient(settings.cohere_api_key)
            root_logger.info("[OK] Cohere client initialized")

            # Initialize Qdrant client
            app.state.qdrant_client = AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False
            )
            root_logger.info("[OK] Qdrant client initialized")

            # Initialize embedding service
            app.state.embedding_service = EmbeddingService()
            root_logger.info("[OK] Embedding service initialized")

            # Initialize retrieval service
            app.state.retrieval_service = RetrievalService()
            root_logger.info("[OK] Retrieval service initialized")

            root_logger.info("All services pre-initialized successfully!")
        except Exception as e:
            root_logger.error(f"Error pre-initializing services: {e}")

        root_logger.info("="*80)

    @app.on_event("shutdown")
    async def shutdown_event():
        root_logger.info("APPLICATION SHUTDOWN")

    return app


app = create_app()
# Note: Hugging Face Spaces uses Docker CMD to run the app
# Do not use if __name__ == "__main__" block to avoid port conflicts
