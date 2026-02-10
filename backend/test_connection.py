import asyncio
import os
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models

# Force reload environment variables
from dotenv import load_dotenv
import importlib
import sys

# Clear any cached modules
if 'src.core.config' in sys.modules:
    del sys.modules['src.core.config']

load_dotenv(dotenv_path='.env', override=True)

# Get settings from environment
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print(f"Qdrant URL: {qdrant_url}")
print(f"Qdrant API Key present: {bool(qdrant_api_key)}")

async def test_connection():
    try:
        # Initialize Qdrant client
        client = AsyncQdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=False
        )
        
        print("Attempting to connect to Qdrant...")
        
        # Try to get collections
        collections = await client.get_collections()
        print(f"Successfully connected! Collections: {[c.name for c in collections.collections]}")
        
        # Try to create collection
        collection_name = "document_chunks"
        try:
            await client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' created successfully!")
        except Exception as e:
            print(f"Collection creation failed (might already exist): {e}")
            
    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(test_connection())