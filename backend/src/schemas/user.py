from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from .base import BaseSchema


class UserBase(BaseSchema):
    session_id: str
    preferences: Optional[Dict[str, Any]] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    preferences: Optional[Dict[str, Any]] = None


class User(UserBase):
    id: UUID
    created_at: datetime
    last_active: Optional[datetime] = None

    class Config:
        from_attributes = True