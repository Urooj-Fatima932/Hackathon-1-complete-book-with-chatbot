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
    query_request: QuerySelectionRequest,
    request: Request,
    db=Depends(get_db)
):
    """Query based on selected text from documentation"""
    chat_service = ChatService(db, app_state=request.app.state)

    # Process the selected text and return a response
    response_content, sources = await chat_service.query_selected_text(
        selected_text=query_request.selected_text,
        context=query_request.context
    )

    return QuerySelectionResponse(
        response=response_content,
        sources=sources
    )