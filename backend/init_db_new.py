"""
Script to initialize the database tables
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

# Create a fresh Base to avoid conflicts
Base = declarative_base()

# Import models after Base is defined to register with this specific Base
from src.models.conversation import Conversation, Message  # noqa: F401
from src.models.document import Document, DocumentChunk  # noqa: F401
from src.models.user import User  # noqa: F401
from src.models.document_reference import DocumentReference  # noqa: F401


async def init_db():
    """Initialize the database tables"""
    from src.core.config import settings

    # Create async engine
    engine = create_async_engine(settings.database_url)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())