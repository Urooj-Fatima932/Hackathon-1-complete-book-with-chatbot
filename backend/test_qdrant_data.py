"""
Simple test to verify Qdrant collection has data
"""
import asyncio
from qdrant_client import AsyncQdrantClient
from src.core.config import settings


async def test_qdrant_data():
    print("Testing Qdrant collection for data...")
    
    # Initialize Qdrant client
    client = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False
    )
    
    collection_name = "document_chunks"
    
    try:
        # Get collection info
        collection_info = await client.get_collection(collection_name)
        print(f"Collection '{collection_name}' exists")
        print(f"Points count: {collection_info.points_count}")
        
        if collection_info.points_count > 0:
            print("[SUCCESS] Qdrant collection has data!")
            print(f"Total points in collection: {collection_info.points_count}")
            
            # Sample a few points to verify
            records, _ = await client.scroll(
                collection_name=collection_name,
                limit=2,
                with_payload=True,
                with_vectors=False
            )
            
            if records:
                print(f"Sample records: {len(records)}")
                for i, record in enumerate(records):
                    print(f"  Record {i+1}: ID={record.id}, Payload keys={list(record.payload.keys())}")
        else:
            print("[ISSUE] Qdrant collection is still empty!")
            
    except Exception as e:
        print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_qdrant_data())