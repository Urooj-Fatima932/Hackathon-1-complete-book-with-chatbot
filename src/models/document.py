from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base
import uuid


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, nullable=False, unique=True)
    source_type = Column(String, nullable=True)  # e.g., 'markdown', 'html', 'api_doc'
    metadata_ = Column("metadata", JSON, nullable=True)  # Using metadata_ to avoid conflict with metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    embedding_vector_id = Column(String, nullable=True)  # Reference to vector ID in Qdrant


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)  # Sequential index within document
    embedding_vector_id = Column(String, nullable=True)  # Reference to vector ID in Qdrant
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())