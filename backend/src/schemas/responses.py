from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from .conversation import Message
from .document import Document


class ChatResponse(BaseModel):
    message_id: UUID
    conversation_id: UUID
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StreamingResponseData(BaseModel):
    token: Optional[str] = None
    sources: Optional[List[Dict[str, str]]] = None
    done: Optional[bool] = None
    message_id: Optional[UUID] = None
    conversation_id: Optional[UUID] = None


class ChatStartResponse(BaseModel):
    conversation_id: UUID
    session_id: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuerySelectionResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    status: str
    message: str


class DocumentIngestionResponse(BaseModel):
    document_id: UUID
    chunks_processed: int
    status: str


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]


class UserPreferencesResponse(BaseModel):
    theme: Optional[str] = "light"
    chat_position: Optional[str] = "bottom-right"
    default_view: Optional[str] = "expanded"
    last_active_conversation: Optional[str] = None


class UpdatePreferencesResponse(BaseModel):
    theme: str
    chat_position: str
    default_view: str
    updated_at: datetime


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime