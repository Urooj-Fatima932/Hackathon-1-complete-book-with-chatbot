"""
Test the retrieval service to ensure it's working with the fixed search method
"""
import asyncio
from src.services.retrieval_service import RetrievalService


async def test_retrieval():
    """Test document retrieval"""
    print("Initializing Retrieval Service...")
    retrieval_service = RetrievalService()

    # Test query
    test_query = "What is ROS2?"
    print(f"\nTesting query: '{test_query}'")
    print("=" * 60)

    # Search and rerank
    results = await retrieval_service.search_and_rerank(
        query=test_query,
        search_top_k=10,
        rerank_top_k=3
    )

    print(f"\nRetrieved {len(results)} documents:\n")

    for i, doc in enumerate(results, 1):
        print(f"{i}. Score: {doc['score']:.4f}")
        print(f"   Title: {doc.get('title', 'N/A')}")
        print(f"   Content preview: {doc['content'][:150]}...")
        print()

    if len(results) > 0:
        print("✓ SUCCESS! Retrieval is working correctly!")
        print("The chatbot will now answer using book content.")
    else:
        print("✗ FAILED! No documents retrieved.")


if __name__ == "__main__":
    asyncio.run(test_retrieval())
