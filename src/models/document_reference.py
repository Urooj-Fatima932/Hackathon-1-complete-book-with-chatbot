from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base
import uuid


class DocumentReference(Base):
    __tablename__ = "document_references"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    document_chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id"), nullable=False)
    relevance_score = Column(Integer, nullable=True)  # e.g., 0-100 score
    citation_metadata = Column(JSON, nullable=True)  # Additional metadata about the reference
    created_at = Column(DateTime(timezone=True), server_default=func.now())