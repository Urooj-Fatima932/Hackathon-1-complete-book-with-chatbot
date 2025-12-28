"""
Quick test to check if Qdrant has data
"""
import asyncio
from qdrant_client import AsyncQdrantClient
from src.core.config import settings


async def check_qdrant():
    """Check if Qdrant collection has data"""
    print("Connecting to Qdrant...")

    client = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False
    )

    collection_name = "document_chunks"

    try:
        # Get collection info
        collection_info = await client.get_collection(collection_name)
        print(f"\nCollection: {collection_name}")
        print(f"Points count: {collection_info.points_count}")
        print(f"Vectors count: {collection_info.vectors_count}")

        if collection_info.points_count == 0:
            print("\n⚠️  WARNING: Collection is EMPTY!")
            print("You need to run: python backend/scripts/ingest_docs.py")
        else:
            print(f"\n✓ Collection has {collection_info.points_count} document chunks")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(check_qdrant())
