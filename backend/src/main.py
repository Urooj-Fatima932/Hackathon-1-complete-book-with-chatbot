from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat import router as chat_router
from .api.query import router as query_router
from .api.user import router as user_router
from .core.config import settings
from .core.logging_config import root_logger
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

        # Lazy initialization - services will initialize on first request
        # This prevents startup timeouts when external services are unreachable
        root_logger.info("Services will initialize lazily on first request")
        root_logger.info("="*80)

    async def get_services():
        """Lazily initialize and return services."""
        if not hasattr(app.state, 'cohere_client'):
            root_logger.info("Initializing Cohere client...")
            app.state.cohere_client = cohere.AsyncClient(settings.cohere_api_key)
        if not hasattr(app.state, 'qdrant_client'):
            root_logger.info("Initializing Qdrant client...")
            app.state.qdrant_client = AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False
            )
        if not hasattr(app.state, 'embedding_service'):
            from .services.embedding_service import EmbeddingService
            app.state.embedding_service = EmbeddingService()
        if not hasattr(app.state, 'retrieval_service'):
            from .services.retrieval_service import RetrievalService
            app.state.retrieval_service = RetrievalService()
        return app.state

    @app.on_event("shutdown")
    async def shutdown_event():
        root_logger.info("APPLICATION SHUTDOWN")

    return app


app = create_app()

