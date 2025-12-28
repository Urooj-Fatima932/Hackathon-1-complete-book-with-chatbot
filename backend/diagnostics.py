"""
Diagnostic script to check the health of the chatbot system
This script will test each component individually to identify where failures occur.
"""
import asyncio
import logging
import traceback
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def check_imports() -> Dict[str, Any]:
    """Check if all required modules can be imported"""
    logger.info("Checking imports...")
    results = {}
    
    modules_to_test = [
        ("SQLAlchemy components", lambda: __import__("sqlalchemy")),
        ("Async SQLAlchemy", lambda: __import__("sqlalchemy.ext.asyncio")),
        ("FastAPI", lambda: __import__("fastapi")),
        ("Pydantic", lambda: __import__("pydantic")),
        ("UUID", lambda: __import__("uuid")),
        ("Cohere client", lambda: __import__("cohere")),
        ("Qdrant client", lambda: __import__("qdrant_client")),
    ]
    
    for name, import_func in modules_to_test:
        try:
            import_func()
            results[name] = {"status": "success", "error": None}
            logger.info(f"✓ {name} - OK")
        except Exception as e:
            results[name] = {"status": "failed", "error": str(e)}
            logger.error(f"✗ {name} - Error: {str(e)}")
    
    return results

async def check_config() -> Dict[str, Any]:
    """Check if configuration is properly loaded"""
    logger.info("Checking configuration...")
    results = {}
    
    try:
        from src.core.config import settings
        results["config_load"] = {"status": "success", "error": None}
        logger.info("✓ Configuration loaded")
        
        # Check required settings
        required_settings = [
            ("Cohere API Key", settings.cohere_api_key, "COHERE_API_KEY should be set in .env"),
            ("Qdrant URL", settings.qdrant_url, "QDRANT_URL should be set in .env"),
            ("Database URL", settings.database_url, "DATABASE_URL should be set in .env"),
            ("Secret Key", settings.secret_key, "SECRET_KEY should be set in .env"),
        ]
        
        for name, value, description in required_settings:
            if value:
                results[name] = {"status": "success", "error": None}
                logger.info(f"✓ {name} - OK")
            else:
                results[name] = {"status": "missing", "error": description}
                logger.error(f"✗ {name} - {description}")
                
    except Exception as e:
        results["config_load"] = {"status": "failed", "error": str(e)}
        logger.error(f"✗ Configuration - Error: {str(e)}")
        traceback.print_exc()
    
    return results

async def check_database_connection() -> Dict[str, Any]:
    """Check if database connection works"""
    logger.info("Checking database connection...")
    results = {}
    
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        from src.core.config import settings
        
        engine = create_async_engine(settings.database_url)
        
        async with engine.begin() as conn:
            # Test connection by getting version - need to use text() for raw SQL
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            results["db_connection"] = {"status": "success", "error": None}
            logger.info("✓ Database connection - OK")

            # Test if tables exist by querying the conversations table
            try:
                result = await conn.execute(text("SELECT COUNT(*) FROM conversations LIMIT 1"))
                results["table_exists"] = {"status": "success", "error": None}
                logger.info("✓ Conversations table exists - OK")
            except Exception as table_error:
                results["table_exists"] = {"status": "missing", "error": str(table_error)}
                logger.error(f"x Conversations table - Error: {str(table_error)}")
                
    except Exception as e:
        results["db_connection"] = {"status": "failed", "error": str(e)}
        logger.error(f"✗ Database connection - Error: {str(e)}")
        traceback.print_exc()
    
    return results

async def check_cohere_connection() -> Dict[str, Any]:
    """Check if Cohere API connection works"""
    logger.info("Checking Cohere API connection...")
    results = {}
    
    try:
        import cohere
        from src.core.config import settings
        
        # Create a simple client to test
        client = cohere.AsyncClient(settings.cohere_api_key)
        
        # Test the connection by making a simple call (using embed API as it's safer)
        try:
            response = await client.embed(
                texts=["test"],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            results["cohere_connection"] = {"status": "success", "error": None}
            logger.info("✓ Cohere API connection - OK")
        except Exception as embed_error:
            results["cohere_connection"] = {"status": "failed", "error": str(embed_error)}
            logger.error(f"✗ Cohere API connection - Error: {str(embed_error)}")
            
    except Exception as e:
        results["cohere_connection"] = {"status": "failed", "error": str(e)}
        logger.error(f"✗ Cohere client initialization - Error: {str(e)}")
        traceback.print_exc()
    
    return results

async def check_qdrant_connection() -> Dict[str, Any]:
    """Check if Qdrant connection works"""
    logger.info("Checking Qdrant connection...")
    results = {}
    
    try:
        from qdrant_client import AsyncQdrantClient
        from src.core.config import settings
        
        client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        
        # Test connection by listing collections
        collections = await client.get_collections()
        results["qdrant_connection"] = {"status": "success", "error": None}
        logger.info(f"✓ Qdrant connection - OK, found {len(collections.collections)} collection(s)")
        
        # Check if document_chunks collection exists
        collection_names = [col.name for col in collections.collections]
        if "document_chunks" in collection_names:
            results["document_chunks_collection"] = {"status": "success", "error": None}
            logger.info("✓ document_chunks collection exists - OK")
        else:
            results["document_chunks_collection"] = {"status": "missing", "error": "Collection 'document_chunks' not found"}
            logger.warning("✗ document_chunks collection - Not found")
            
    except Exception as e:
        results["qdrant_connection"] = {"status": "failed", "error": str(e)}
        logger.error(f"✗ Qdrant connection - Error: {str(e)}")
        traceback.print_exc()
    
    return results

async def check_model_instantiation() -> Dict[str, Any]:
    """Check if services can be instantiated without errors"""
    logger.info("Checking service instantiation...")
    results = {}
    
    try:
        from sqlalchemy.ext.asyncio import AsyncSession
        from src.services.conversation_service import ConversationService
        from unittest.mock import AsyncMock
        
        # Create a mock db session for testing instantiation
        mock_db = AsyncMock(spec=AsyncSession)
        
        try:
            # Try to instantiate ConversationService - this was the original error
            service = ConversationService(mock_db)
            results["conversation_service"] = {"status": "success", "error": None}
            logger.info("✓ ConversationService instantiation - OK")
        except Exception as service_error:
            results["conversation_service"] = {"status": "failed", "error": str(service_error)}
            logger.error(f"✗ ConversationService instantiation - Error: {str(service_error)}")
            
    except Exception as e:
        results["model_instantiation"] = {"status": "failed", "error": str(e)}
        logger.error(f"✗ Service instantiation setup - Error: {str(e)}")
        traceback.print_exc()
    
    return results

async def run_diagnostics():
    """Run all diagnostic checks"""
    logger.info("Starting chatbot diagnostics...")
    
    all_results = {}
    
    all_results["imports"] = await check_imports()
    all_results["config"] = await check_config()
    all_results["database"] = await check_database_connection()
    all_results["cohere"] = await check_cohere_connection()
    all_results["qdrant"] = await check_qdrant_connection()
    all_results["models"] = await check_model_instantiation()
    
    logger.info("Diagnostics complete!")
    
    # Print summary
    print("\n" + "="*50)
    print("DIAGNOSTICS SUMMARY")
    print("="*50)
    
    total_checks = 0
    failed_checks = 0
    
    for category, results in all_results.items():
        print(f"\n{category.upper()}:")
        for check_name, result in results.items():
            total_checks += 1
            status = result["status"]
            if status == "failed":
                failed_checks += 1
                print(f"  ✗ {check_name}: {result['error']}")
            else:
                print(f"  ✓ {check_name}: OK")
    
    print(f"\nSUMMARY: {total_checks-failed_checks}/{total_checks} checks passed")
    
    if failed_checks > 0:
        print(f"\nIMPORTANT: {failed_checks} check(s) failed. These are likely causing your chatbot issues.")
    else:
        print(f"\nALL CHECKS PASSED! Your chatbot should work correctly.")
    
    return all_results

if __name__ == "__main__":
    asyncio.run(run_diagnostics())