from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import settings

# Async engine
engine = create_async_engine(
    settings.database_url,
    echo=True,              # True only in dev
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300
)

# Async session maker (SQLAlchemy 2.x style)
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
