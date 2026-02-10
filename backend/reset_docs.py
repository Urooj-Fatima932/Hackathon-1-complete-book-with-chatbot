"""
Script to clear existing documents and re-ingest them into Qdrant
"""
import asyncio
import sys
from pathlib import Path
from typing import List, Tuple
import uuid

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Force reload environment variables before importing settings
from dotenv import load_dotenv
load_dotenv(override=True)

from src.core.config import settings
from src.core.database import AsyncSessionLocal
from src.models.document import Document, DocumentChunk
from src.services.embedding_service import EmbeddingService
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
import cohere


async def clear_existing_documents():
    """Clear all existing documents from both database and Qdrant"""
    print("Clearing existing documents...")
    
    # Clear from database
    async with AsyncSessionLocal() as db_session:
        try:
            from sqlalchemy import delete
            
            # Delete document chunks first (due to foreign key constraint)
            stmt = delete(DocumentChunk)
            await db_session.execute(stmt)
            
            # Then delete documents
            stmt = delete(Document)
            await db_session.execute(stmt)
            
            await db_session.commit()
            print("[OK] Database cleared")
        except Exception as e:
            print(f"[ERROR] Error clearing database: {e}")
            await db_session.rollback()
            raise
    
    # Clear from Qdrant
    try:
        qdrant_client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        
        collection_name = "document_chunks"
        
        # Delete all points in the collection
        await qdrant_client.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[]
                )
            )
        )
        print("[OK] Qdrant collection cleared")
    except Exception as e:
        print(f"[ERROR] Error clearing Qdrant: {e}")
        raise


def main():
    """Main function to clear and re-ingest documents"""
    print("Starting document reset process...")
    
    # Clear existing documents
    asyncio.run(clear_existing_documents())
    
    # Now run the ingestion script
    print("\nNow running ingestion script...")
    import subprocess
    import os
    
    # Change to backend directory and run the ingestion script
    result = subprocess.run([
        sys.executable, 
        str(Path(__file__).parent / "scripts" / "ingest_docs.py")
    ], cwd=Path(__file__).parent, capture_output=True, text=True)
    
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print(f"Return code: {result.returncode}")


if __name__ == "__main__":
    main()