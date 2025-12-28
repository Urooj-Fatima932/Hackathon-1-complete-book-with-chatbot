from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
import uuid
from ..services.chat_service import ChatService
from ..services.conversation_service import ConversationService
from ..core.database import get_db
from ..core.config import settings

router = APIRouter()

class QuerySelectionRequest(BaseModel):
    selected_text: str
    context: Optional[str] = ""

class QuerySelectionResponse(BaseModel):
    response: str
    sources: List[dict]

@router.post("/selection", response_model=QuerySelectionResponse)
async def query_selection(
    request: QuerySelectionRequest,
    db=Depends(get_db)
):
    """Query based on selected text from documentation"""
    chat_service = ChatService(db)
    
    # Process the selected text and return a response
    response_content, sources = await chat_service.query_selected_text(
        selected_text=request.selected_text,
        context=request.context
    )
    
    return QuerySelectionResponse(
        response=response_content,
        sources=sources
    )