"""
Script to initialize the database tables
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# Import settings and base
from src.core.config import settings
from src.models.base import Base

# Import all models to register them with SQLAlchemy (avoiding circular imports)
# Import each model module directly to register with SQLAlchemy
import src.models.conversation
import src.models.document
import src.models.user
import src.models.document_reference


async def init_db():
    """Initialize the database tables"""
    # Create async engine
    engine = create_async_engine(settings.database_url)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())