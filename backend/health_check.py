"""
Health check script to verify all chatbot components are working
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.config import settings
from src.core.database import engine
from qdrant_client import QdrantClient
import cohere


async def check_health():
    print("=" * 60)
    print("CHATBOT HEALTH CHECK")
    print("=" * 60)

    all_ok = True

    # 1. Check Configuration
    print("\n1. Checking Configuration...")
    try:
        print(f"   App Name: {settings.app_name}")
        print(f"   Debug Mode: {settings.debug}")
        print(f"   Database URL: {settings.database_url[:30]}...")
        print(f"   Qdrant URL: {settings.qdrant_url}")
        print(f"   Cohere API Key: {settings.cohere_api_key[:10]}...")
        print("   ✓ Configuration: LOADED")
    except Exception as e:
        print(f"   ✗ Configuration: FAILED - {str(e)}")
        all_ok = False

    # 2. Check Cohere API
    print("\n2. Checking Cohere API...")
    try:
        client = cohere.Client(settings.cohere_api_key)
        # Test with a simple embedding call
        response = client.embed(
            texts=["test"],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        if response.embeddings and len(response.embeddings[0]) == 1024:
            print("   ✓ Cohere API: CONNECTED")
            print(f"   ✓ Embeddings: Working (dimension: 1024)")
        else:
            print("   ✗ Cohere API: Unexpected response")
            all_ok = False
    except Exception as e:
        print(f"   ✗ Cohere API: FAILED - {str(e)}")
        all_ok = False

    # 3. Check Qdrant
    print("\n3. Checking Qdrant...")
    try:
        qdrant = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        collections = qdrant.get_collections()
        print(f"   ✓ Qdrant: CONNECTED")
        print(f"   Collections found: {len(collections.collections)}")

        if collections.collections:
            for col in collections.collections:
                info = qdrant.get_collection(col.name)
                print(f"     - {col.name}: {info.points_count} points")

                # Check if our expected collection exists
                if col.name == "document_chunks":
                    if info.points_count > 0:
                        print(f"   ✓ Collection 'document_chunks' has data")
                    else:
                        print(f"   ⚠ Collection 'document_chunks' is EMPTY")
                        print(f"     You need to ingest documents!")
        else:
            print("   ⚠ No collections found")
            print("     You need to create collections and ingest documents!")

    except Exception as e:
        print(f"   ✗ Qdrant: FAILED - {str(e)}")
        all_ok = False

    # 4. Check Database
    print("\n4. Checking Database...")
    try:
        async with engine.connect() as conn:
            print("   ✓ Database: CONNECTED")

            # Check if tables exist
            from sqlalchemy import text
            result = await conn.execute(text("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]

            if tables:
                print(f"   Tables found: {len(tables)}")
                for table in tables:
                    print(f"     - {table}")

                expected_tables = ['conversations', 'messages', 'documents', 'document_chunks']
                missing = [t for t in expected_tables if t not in tables]
                if missing:
                    print(f"   ⚠ Missing tables: {missing}")
                    print(f"     Run: python init_db_new.py")
                else:
                    print(f"   ✓ All expected tables exist")
            else:
                print("   ⚠ No tables found")
                print("     Run: python init_db_new.py")

    except Exception as e:
        print(f"   ✗ Database: FAILED - {str(e)}")
        all_ok = False

    # 5. Check Log Directory
    print("\n5. Checking Logs...")
    try:
        log_dir = Path(__file__).parent / "logs"
        if log_dir.exists():
            log_files = list(log_dir.glob("chatbot_*.log"))
            print(f"   ✓ Log directory exists: {log_dir}")
            print(f"   Log files found: {len(log_files)}")
            if log_files:
                latest = max(log_files, key=lambda p: p.stat().st_mtime)
                print(f"   Latest: {latest.name}")
        else:
            print(f"   ⚠ Log directory will be created on first run")
    except Exception as e:
        print(f"   ✗ Logs: FAILED - {str(e)}")

    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ ALL CHECKS PASSED - Chatbot is ready!")
    else:
        print("✗ SOME CHECKS FAILED - See errors above")
        print("\nQuick fixes:")
        print("  - Cohere: Check COHERE_API_KEY in .env")
        print("  - Qdrant: docker start qdrant")
        print("  - Database: Check PostgreSQL is running")
        print("  - Tables: python init_db_new.py")
    print("=" * 60)

    return all_ok


if __name__ == "__main__":
    result = asyncio.run(check_health())
    sys.exit(0 if result else 1)
