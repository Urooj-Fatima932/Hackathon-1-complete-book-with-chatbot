# src/services/embedding_service.py
from typing import List
import traceback
import cohere
from ..core.config import settings
from ..core.logging_config import embedding_logger

class EmbeddingService:
    """Service for handling text embeddings using Cohere"""

    def __init__(self):
        embedding_logger.debug("Initializing EmbeddingService")
        try:
            self.client = cohere.AsyncClient(settings.cohere_api_key)
            self.model = "embed-english-v3.0"
            embedding_logger.info(f"EmbeddingService initialized with model: {self.model}")
        except Exception as e:
            embedding_logger.error(f"Failed to initialize EmbeddingService: {str(e)}")
            raise

    async def create_embeddings(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """Create embeddings for a list of texts"""
        embedding_logger.info(f"Creating embeddings for {len(texts)} texts, input_type: {input_type}")
        try:
            response = await self.client.embed(
                texts=texts,
                model=self.model,
                input_type=input_type
            )
            embeddings = [embedding for embedding in response.embeddings]
            embedding_logger.info(f"Successfully created {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            embedding_logger.error(f"Error creating embeddings: {type(e).__name__}")
            embedding_logger.error(f"Error message: {str(e)}")
            embedding_logger.error(f"Traceback:\n{traceback.format_exc()}")
            raise

    async def create_query_embedding(self, text: str) -> List[float]:
        """Create embedding for a query text"""
        embedding_logger.debug(f"Creating query embedding for text: '{text[:50]}...'")
        try:
            embeddings = await self.create_embeddings([text], input_type="search_query")
            return embeddings[0] if embeddings else []
        except Exception as e:
            embedding_logger.error(f"Failed to create query embedding: {str(e)}")
            return []

    async def create_document_embedding(self, text: str) -> List[float]:
        """Create embedding for a document text"""
        embedding_logger.debug(f"Creating document embedding for text: '{text[:50]}...'")
        try:
            embeddings = await self.create_embeddings([text], input_type="search_document")
            return embeddings[0] if embeddings else []
        except Exception as e:
            embedding_logger.error(f"Failed to create document embedding: {str(e)}")
            return []