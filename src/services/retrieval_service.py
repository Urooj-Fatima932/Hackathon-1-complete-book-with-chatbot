# src/services/retrieval_service.py
from typing import List, Tuple
import traceback
import cohere
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from ..core.config import settings
from ..core.vector_db import vector_db_service
from ..core.logging_config import retrieval_logger


class RetrievalService:
    """Service for handling document retrieval using Qdrant and Cohere"""

    def __init__(self):
        retrieval_logger.debug("Initializing RetrievalService")
        # Initialize Qdrant client using settings
        try:
            retrieval_logger.debug(f"Connecting to Qdrant at: {settings.qdrant_url}")
            self.qdrant_client = AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False
            )
            retrieval_logger.debug("Qdrant client initialized successfully")
        except Exception as e:
            retrieval_logger.error(f"Failed to initialize Qdrant client: {str(e)}")
            raise

        try:
            self.cohere_client = cohere.AsyncClient(settings.cohere_api_key)
            retrieval_logger.debug("Cohere client initialized for retrieval")
        except Exception as e:
            retrieval_logger.error(f"Failed to initialize Cohere client for retrieval: {str(e)}")
            raise

        self.collection_name = "document_chunks"
        retrieval_logger.info(f"RetrievalService initialized with collection: {self.collection_name}")

    async def search_documents(self, query: str, top_k: int = 20) -> List[dict]:
        """Search for relevant documents using vector similarity"""
        retrieval_logger.info(f"Searching documents - Query: '{query[:100]}...', top_k: {top_k}")

        try:
            # Get embedding for the query
            retrieval_logger.debug("Getting query embedding")
            query_embedding = await self._get_query_embedding(query)

            if not query_embedding:
                retrieval_logger.error("Failed to generate query embedding - empty result")
                return []

            retrieval_logger.debug(f"Query embedding generated - dimensions: {len(query_embedding)}")

            # Search in Qdrant
            retrieval_logger.info(f"Searching Qdrant collection: {self.collection_name}")
            try:
                search_results = await self.qdrant_client.query_points(
                    collection_name=self.collection_name,
                    query=query_embedding,
                    limit=top_k
                )
                retrieval_logger.info(f"Qdrant search returned {len(search_results.points)} results")
            except Exception as qdrant_error:
                retrieval_logger.error(f"Qdrant search failed: {type(qdrant_error).__name__}")
                retrieval_logger.error(f"Qdrant error message: {str(qdrant_error)}")
                retrieval_logger.error(f"Qdrant error traceback:\n{traceback.format_exc()}")
                return []

            # Format results
            results = []
            for idx, hit in enumerate(search_results.points):
                results.append({
                    "id": str(hit.id),
                    "content": hit.payload.get("content", ""),
                    "document_id": hit.payload.get("document_id"),
                    "chunk_index": hit.payload.get("chunk_index"),
                    "title": hit.payload.get("title", "Untitled"),
                    "url": hit.payload.get("url", ""),
                    "score": hit.score
                })
                retrieval_logger.debug(f"Result {idx+1}: score={hit.score:.4f}, title='{hit.payload.get('title', 'N/A')}', content_len={len(hit.payload.get('content', ''))}")

            retrieval_logger.info(f"Formatted {len(results)} search results")
            return results

        except Exception as e:
            retrieval_logger.error(f"Error in search_documents: {type(e).__name__}")
            retrieval_logger.error(f"Error message: {str(e)}")
            retrieval_logger.error(f"Full traceback:\n{traceback.format_exc()}")
            return []

    async def rerank_documents(self, query: str, documents: List[dict], top_k: int = 5) -> List[dict]:
        """Rerank documents using Cohere's rerank functionality"""
        retrieval_logger.info(f"Reranking {len(documents)} documents, top_k: {top_k}")

        if not documents:
            retrieval_logger.warning("No documents to rerank")
            return []

        try:
            # Prepare documents for reranking
            documents_text = [doc["content"] for doc in documents]
            retrieval_logger.debug(f"Prepared {len(documents_text)} documents for reranking")

            # Rerank using Cohere
            retrieval_logger.info("Calling Cohere rerank API")
            try:
                rerank_response = await self.cohere_client.rerank(
                    model="rerank-english-v3.0",  # Updated from v2.0 (sunset Dec 2025)
                    query=query,
                    documents=documents_text,
                    top_n=top_k
                )
                retrieval_logger.info(f"Rerank API returned {len(rerank_response.results)} results")
            except Exception as cohere_error:
                retrieval_logger.error(f"Cohere rerank API failed: {type(cohere_error).__name__}")
                retrieval_logger.error(f"Cohere error message: {str(cohere_error)}")
                retrieval_logger.error(f"Cohere error traceback:\n{traceback.format_exc()}")
                retrieval_logger.warning(f"Falling back to original top {top_k} documents")
                return documents[:top_k]

            # Format reranked results
            reranked_results = []
            for idx, rank in enumerate(rerank_response.results):
                original_doc = documents[rank.index]
                reranked_results.append({
                    "id": original_doc["id"],
                    "content": original_doc["content"],
                    "document_id": original_doc["document_id"],
                    "chunk_index": original_doc["chunk_index"],
                    "title": original_doc.get("title", "Untitled"),
                    "url": original_doc.get("url", ""),
                    "score": rank.relevance_score
                })
                retrieval_logger.debug(f"Reranked {idx+1}: relevance={rank.relevance_score:.4f}, title='{original_doc.get('title', 'N/A')}', original_index={rank.index}")

            retrieval_logger.info(f"Reranking completed - returning {len(reranked_results)} documents")
            return reranked_results

        except Exception as e:
            retrieval_logger.error(f"Error in rerank_documents: {type(e).__name__}")
            retrieval_logger.error(f"Error message: {str(e)}")
            retrieval_logger.error(f"Full traceback:\n{traceback.format_exc()}")
            retrieval_logger.warning(f"Falling back to original top {top_k} documents")
            return documents[:top_k]

    async def search_and_rerank(self, query: str, search_top_k: int = 20, rerank_top_k: int = 5) -> List[dict]:
        """Search documents and rerank the results"""
        retrieval_logger.info(f"Starting search_and_rerank - search_top_k: {search_top_k}, rerank_top_k: {rerank_top_k}")
        retrieval_logger.debug(f"Query: '{query}'")

        # First, search in vector database
        search_results = await self.search_documents(query, top_k=search_top_k)

        if not search_results:
            retrieval_logger.warning("No search results found - skipping reranking")
            return []

        # Then, rerank the results
        reranked_results = await self.rerank_documents(query, search_results, top_k=rerank_top_k)

        retrieval_logger.info(f"search_and_rerank completed - returning {len(reranked_results)} documents")
        return reranked_results

    async def _get_query_embedding(self, query: str, retry_count: int = 0) -> List[float]:
        """Get embedding for a query with retry logic"""
        retrieval_logger.debug(f"Getting query embedding for: '{query[:50]}...' (attempt {retry_count + 1})")
        max_retries = 3

        try:
            response = await self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            retrieval_logger.debug(f"Query embedding generated successfully - dim: {len(response.embeddings[0])}")
            return response.embeddings[0]
        except Exception as e:
            retrieval_logger.error(f"Error getting query embedding (attempt {retry_count + 1}): {type(e).__name__}")
            retrieval_logger.error(f"Error message: {str(e)}")

            # Retry with exponential backoff
            if retry_count < max_retries:
                import asyncio
                wait_time = 2 ** retry_count  # 1s, 2s, 4s
                retrieval_logger.warning(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
                return await self._get_query_embedding(query, retry_count + 1)

            retrieval_logger.error(f"All retries exhausted. Traceback:\n{traceback.format_exc()}")
            return []

    async def add_document_chunk(self, chunk_id: str, content: str, document_id: str, chunk_index: int):
        """Add a document chunk to the vector database"""
        try:
            # Get embedding for the content
            embedding = await self._get_document_embedding(content)

            # Prepare the point to insert
            point = models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "content": content,
                    "document_id": document_id,
                    "chunk_index": chunk_index
                }
            )

            # Insert into Qdrant
            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        except Exception as e:
            print(f"Error adding document chunk: {e}")

    async def _get_document_embedding(self, content: str) -> List[float]:
        """Get embedding for a document chunk"""
        try:
            response = await self.cohere_client.embed(
                texts=[content],
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings[0]
        except Exception as e:
            print(f"Error getting document embedding: {e}")
            return []