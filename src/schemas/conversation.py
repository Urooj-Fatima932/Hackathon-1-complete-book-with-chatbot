from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from .base import BaseSchema


class ConversationBase(BaseSchema):
    session_id: str
    title: Optional[str] = None
    is_active: bool = True


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class Conversation(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageBase(BaseSchema):
    conversation_id: UUID
    role: str  # 'user', 'assistant', 'system'
    content: str
    tokens_count: Optional[int] = 0
    sources: Optional[List[Dict[str, Any]]] = Field(default=None)
    is_streaming_complete: bool = False


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    is_streaming_complete: Optional[bool] = None


class Message(MessageBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True