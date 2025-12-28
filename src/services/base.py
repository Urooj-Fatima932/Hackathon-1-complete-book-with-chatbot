# src/services/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

class BaseService(ABC):
    """Base service class providing common functionality for all services"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, *args, **kwargs) -> Any:
        """Create a new entity"""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Any:
        """Get an entity by its ID"""
        pass

    @abstractmethod
    async def update(self, entity_id: str, **kwargs) -> Any:
        """Update an entity with the given fields"""
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete an entity by its ID"""
        pass