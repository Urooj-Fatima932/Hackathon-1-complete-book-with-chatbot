# src/services/conversation_service.py
import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from ..models.conversation import Conversation, Message
from ..models.user import User
from .base import BaseService

class ConversationService(BaseService):
    """Service for handling conversation-related operations"""

    async def create_conversation(self, session_id: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        if not session_id:
            session_id = str(uuid.uuid4())

        conversation = Conversation(
            session_id=session_id,
            title="New Conversation",  # Will be updated with first message
            is_active=True
        )

        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """Get a conversation by its ID"""
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def get_conversation_by_session(self, session_id: str) -> Optional[Conversation]:
        """Get active conversation by session ID"""
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.session_id == session_id)
            .where(Conversation.is_active == True)
        )
        return result.scalar_one_or_none()

    async def update_conversation_title(self, conversation_id: uuid.UUID, title: str):
        """Update the title of a conversation based on the first message"""
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.title = title
            await self.db.commit()
            await self.db.refresh(conversation)
        return conversation

    async def deactivate_conversation(self, conversation_id: uuid.UUID):
        """Deactivate a conversation (soft delete)"""
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.is_active = False
            await self.db.commit()
            await self.db.refresh(conversation)
        return conversation

    async def create_user_message(self, conversation_id: uuid.UUID, content: str) -> Message:
        """Create a user message in a conversation"""
        message = Message(
            conversation_id=conversation_id,
            role="user",
            content=content
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def create_ai_message(self, conversation_id: uuid.UUID, content: str, sources: list = None) -> Message:
        """Create an AI message in a conversation"""
        if sources is None:
            sources = []

        message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            sources=sources
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages_by_conversation(self, conversation_id: uuid.UUID) -> list:
        """Get all messages in a conversation"""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return result.scalars().all()

    # Implementation of abstract methods from BaseService
    async def create(self, *args, **kwargs) -> Any:
        """Create a new entity - specific implementation for conversation"""
        session_id = kwargs.get('session_id')
        return await self.create_conversation(session_id)

    async def get_by_id(self, entity_id: str) -> Any:
        """Get entity by ID - for ConversationService, this gets a conversation"""
        conversation_id = uuid.UUID(entity_id)
        return await self.get_conversation_by_id(conversation_id)

    async def update(self, entity_id: str, **kwargs) -> Any:
        """Update entity - for ConversationService, this updates a conversation"""
        conversation_id = uuid.UUID(entity_id)
        title = kwargs.get('title')
        if title:
            return await self.update_conversation_title(conversation_id, title)
        return None

    async def delete(self, entity_id: str) -> bool:
        """Delete entity - for ConversationService, this deactivates a conversation"""
        conversation_id = uuid.UUID(entity_id)
        conversation = await self.get_conversation_by_id(conversation_id)
        if conversation:
            await self.deactivate_conversation(conversation_id)
            return True
        return False