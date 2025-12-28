from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
from .config import settings
import uuid


class VectorDBService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Set to True in production if gRPC is available
        )
        self.collection_name = "document_embeddings"
        self.vector_size = 1024  # Cohere embed-english-v3.0 has 1024 dimensions
        
    async def create_collection(self):
        """
        Create the collection for document embeddings if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection with 1024-dim vectors (for Cohere embeddings)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
    
    async def upsert_vectors(self, vectors: List[Dict], document_ids: List[str]):
        """
        Upsert vectors to Qdrant with document metadata
        """
        points = []
        for i, (vector, doc_id) in enumerate(zip(vectors, document_ids)):
            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "document_id": doc_id
                    }
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    async def search_vectors(self, query_vector: List[float], top_k: int = 10) -> List[Dict]:
        """
        Search for similar vectors in Qdrant
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        # Format results to include document_id and score
        formatted_results = []
        for result in results:
            formatted_results.append({
                "document_id": result.payload.get("document_id"),
                "score": result.score,
                "vector_id": result.id
            })
        
        return formatted_results
    
    async def delete_vectors(self, vector_ids: List[str]):
        """
        Delete vectors from Qdrant by their IDs
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=vector_ids
            )
        )
    
    async def get_vector_by_id(self, vector_id: str) -> Optional[Dict]:
        """
        Retrieve a specific vector by its ID
        """
        records = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[vector_id]
        )
        
        if records:
            record = records[0]
            return {
                "id": record.id,
                "vector": record.vector,
                "payload": record.payload
            }
        
        return None

# Global instance
vector_db_service = VectorDBService()