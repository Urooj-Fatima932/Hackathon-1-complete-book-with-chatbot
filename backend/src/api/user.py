from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import uuid
from ..services.user_service import UserService
from ..core.database import get_db
from ..core.config import settings

router = APIRouter()

class ThemePreference(BaseModel):
    theme: str  # 'light' or 'dark'

class UserPreferenceRequest(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    # Add other preferences as needed

class UserPreferenceResponse(BaseModel):
    theme: str
    language: str
    # Add other preferences as needed

@router.get("/", response_model=UserPreferenceResponse)
async def get_user_preferences(
    session_id: str,
    db=Depends(get_db)
):
    """Get user preferences"""
    user_service = UserService(db)
    preferences = await user_service.get_user_preferences(session_id)
    
    if not preferences:
        # Create default preferences if they don't exist
        preferences = await user_service.create_default_preferences(session_id)
    
    return UserPreferenceResponse(
        theme=preferences.get('theme', 'light'),
        language=preferences.get('language', 'en')
    )

@router.put("/", response_model=UserPreferenceResponse)
async def update_user_preferences(
    session_id: str,
    request: UserPreferenceRequest,
    db=Depends(get_db)
):
    """Update user preferences"""
    user_service = UserService(db)
    updated_preferences = await user_service.update_user_preferences(
        session_id,
        request.dict(exclude_unset=True)
    )
    
    return UserPreferenceResponse(
        theme=updated_preferences.get('theme', 'light'),
        language=updated_preferences.get('language', 'en')
    )