from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys and External Services
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    database_url: str
    neon_db_url: Optional[str] = None  # Add this field to avoid validation error

    # Application Settings
    app_name: str = "Docusaurus Chatbot API"
    debug: bool = False
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # RAG Configuration
    chunk_size: int = 512
    chunk_overlap: int = 50
    retrieval_limit: int = 20
    rerank_top_k: int = 5

    # Performance settings
    response_timeout: int = 25  # seconds
    embedding_batch_size: int = 10

    class Config:
        env_file = ".env"


settings = Settings()