# src/services/user_service.py
import json
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.user import User
from .base import BaseService

class UserService(BaseService):
    """Service for handling user-related operations"""
    
    async def get_or_create_user(self, session_id: str) -> User:
        """Get existing user or create a new one"""
        user = await self.get_user_by_session_id(session_id)
        if not user:
            user = await self.create_user(session_id)
        return user

    async def get_user_by_session_id(self, session_id: str) -> Optional[User]:
        """Get a user by their session ID"""
        result = await self.db.execute(
            select(User).where(User.session_id == session_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, session_id: str) -> User:
        """Create a new user"""
        user = User(
            session_id=session_id,
            preferences={"theme": "light", "language": "en"}  # Default preferences
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_preferences(self, session_id: str) -> Optional[Dict]:
        """Get user preferences"""
        user = await self.get_user_by_session_id(session_id)
        if user:
            return user.preferences or {}
        return None

    async def update_user_preferences(self, session_id: str, preferences: Dict) -> Dict:
        """Update user preferences"""
        user = await self.get_or_create_user(session_id)
        if not user.preferences:
            user.preferences = {}
        
        # Update existing preferences with new ones
        user.preferences.update(preferences)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user.preferences or {}

    async def create_default_preferences(self, session_id: str) -> Dict:
        """Create default preferences for a user"""
        user = await self.get_or_create_user(session_id)
        user.preferences = {"theme": "light", "language": "en"}
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user.preferences