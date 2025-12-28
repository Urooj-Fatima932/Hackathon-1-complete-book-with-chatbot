from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from .base import BaseSchema


class DocumentBase(BaseSchema):
    title: str
    content: str
    url: str
    source_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias='metadata_')
    embedding_vector_id: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Document(DocumentBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentChunkBase(BaseSchema):
    document_id: UUID
    content: str
    chunk_index: int
    embedding_vector_id: Optional[str] = None
    token_count: Optional[int] = 0


class DocumentChunkCreate(DocumentChunkBase):
    pass


class DocumentChunk(DocumentChunkBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentReferenceBase(BaseSchema):
    message_id: UUID
    document_chunk_id: UUID
    relevance_score: Optional[float] = None
    citation_metadata: Optional[Dict[str, Any]] = None


class DocumentReferenceCreate(DocumentReferenceBase):
    pass


class DocumentReference(DocumentReferenceBase):
    id: UUID

    class Config:
        from_attributes = True