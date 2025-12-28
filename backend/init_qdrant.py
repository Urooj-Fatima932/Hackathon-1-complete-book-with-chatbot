"""
Script to initialize the Qdrant collection for document chunks
"""
import asyncio
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from src.core.config import settings


async def init_qdrant():
    """Initialize the Qdrant collection for document chunks"""
    print("Initializing Qdrant collection...")
    
    # Initialize Qdrant client
    client = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False
    )
    
    collection_name = "document_chunks"
    
    try:
        # Check if collection already exists
        collections = await client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        if collection_name in collection_names:
            print(f"Collection '{collection_name}' already exists.")
            await client.delete_collection(collection_name)
            print(f"Deleted existing '{collection_name}' collection.")
        
        # Create collection with 1024-dim vectors (for Cohere embeddings)
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere embed-english-v3.0 has 1024 dimensions
                distance=models.Distance.COSINE
            )
        )
        
        print(f"Collection '{collection_name}' created successfully!")
        print("Qdrant is now ready for document storage and retrieval.")
        
    except Exception as e:
        print(f"Error initializing Qdrant: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(init_qdrant())
    if success:
        print("\nInitialization completed successfully!")
    else:
        print("\nInitialization failed!")