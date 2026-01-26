from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
import uuid
import asyncio
import traceback
from ..services.chat_service import ChatService
from ..services.conversation_service import ConversationService
from ..core.database import get_db
from ..core.config import settings
from ..schemas.responses import MessageResponse
from ..core.logging_config import api_logger

router = APIRouter()

class StartConversationRequest(BaseModel):
    initial_message: Optional[str] = None

class StartConversationResponse(BaseModel):
    id: str
    session_id: str

class SendMessageRequest(BaseModel):
    message: str

class QuerySelectionRequest(BaseModel):
    selected_text: str
    question: str

@router.post("/start", response_model=StartConversationResponse)
async def start_conversation(
    request: StartConversationRequest = None,
    db=Depends(get_db)
):
    """Start a new conversation"""
    api_logger.info("=" * 80)
    api_logger.info("Starting new conversation")
    try:
        conversation_service = ConversationService(db)
        conversation = await conversation_service.create_conversation()

        api_logger.info(f"Conversation created successfully - ID: {conversation.id}, Session: {conversation.session_id}")

        return StartConversationResponse(
            id=str(conversation.id),
            session_id=conversation.session_id
        )
    except Exception as e:
        api_logger.error(f"Failed to create conversation: {str(e)}")
        api_logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")

@router.post("/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message_request: SendMessageRequest,
    request: Request,
    db=Depends(get_db)
):
    """Send a message and get a streaming response"""
    api_logger.info("=" * 80)
    api_logger.info(f"Received message for conversation: {conversation_id}")
    api_logger.info(f"User message: {message_request.message[:100]}..." if len(message_request.message) > 100 else f"User message: {message_request.message}")

    try:
        # Validate conversation ID
        api_logger.debug(f"Validating conversation ID: {conversation_id}")
        try:
            conv_uuid = UUID(conversation_id)
            api_logger.debug(f"Conversation ID validated: {conv_uuid}")
        except ValueError as e:
            api_logger.error(f"Invalid conversation ID format: {conversation_id} - {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

        # Initialize chat service (reuse pre-initialized services if available)
        api_logger.debug("Initializing ChatService")
        chat_service = ChatService(db)

        # Use pre-initialized services from app.state if available (faster!)
        if hasattr(request.app.state, 'embedding_service'):
            api_logger.debug("Using pre-initialized services (fast path)")
            chat_service.embedding_service = request.app.state.embedding_service
            chat_service.retrieval_service = request.app.state.retrieval_service

        # Create the user message
        api_logger.info("Creating user message in database")
        user_message = await chat_service.create_user_message(
            conversation_id=conv_uuid,
            content=message_request.message
        )
        api_logger.info(f"User message created - ID: {user_message.id}")

        # Create streaming generator
        async def generate_stream():
            try:
                api_logger.info("Starting AI response generation (streaming)")

                # Generate the full response first
                response_content = await chat_service.generate_response_sync(
                    conversation_id=conv_uuid,
                    user_message=user_message
                )
                api_logger.info(f"AI response generated - Length: {len(response_content)} chars")

                # Stream the response character by character for typewriter effect
                for char in response_content:
                    yield char
                    await asyncio.sleep(0.002)  # Very fast typewriter effect

                # Save the complete message to database after streaming
                api_logger.info("Saving AI message to database")
                await chat_service.create_ai_message(
                    conversation_id=conv_uuid,
                    content=response_content,
                    sources=[]
                )
                api_logger.info("Message processing completed successfully")
                api_logger.info("=" * 80)

            except Exception as e:
                api_logger.error("=" * 80)
                api_logger.error(f"ERROR in streaming generation")
                api_logger.error(f"Error type: {type(e).__name__}")
                api_logger.error(f"Error message: {str(e)}")
                api_logger.error(f"Full traceback:\n{traceback.format_exc()}")
                api_logger.error("=" * 80)
                yield f"\n\nError: {str(e)}"

        return StreamingResponse(
            generate_stream(),
            media_type="text/plain"
        )

    except HTTPException:
        raise
    except Exception as e:
        api_logger.error("=" * 80)
        api_logger.error(f"ERROR in send_message endpoint")
        api_logger.error(f"Conversation ID: {conversation_id}")
        api_logger.error(f"User message: {message_request.message}")
        api_logger.error(f"Error type: {type(e).__name__}")
        api_logger.error(f"Error message: {str(e)}")
        api_logger.error(f"Full traceback:\n{traceback.format_exc()}")
        api_logger.error("=" * 80)
        raise HTTPException(
            status_code=500,
            detail=f"Sorry, I encountered an error while processing your request. Please try again. Error: {str(e)}"
        )

@router.post("/{conversation_id}/query-selection")
async def query_selection(
    conversation_id: str,
    query_request: QuerySelectionRequest,
    request: Request,
    db=Depends(get_db)
):
    """Query based on selected text from documentation"""
    api_logger.info("=" * 80)
    api_logger.info(f"Received selection query for conversation: {conversation_id}")
    api_logger.info(f"Selected text: {query_request.selected_text[:100]}...")
    api_logger.info(f"Question: {query_request.question}")

    try:
        # Validate conversation ID
        try:
            conv_uuid = UUID(conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

        # Initialize chat service
        chat_service = ChatService(db)

        # Use pre-initialized services if available
        if hasattr(request.app.state, 'embedding_service'):
            chat_service.embedding_service = request.app.state.embedding_service
            chat_service.retrieval_service = request.app.state.retrieval_service

        # Create user message combining question and selection
        combined_message = f"{query_request.question}\n\nSelected text: {query_request.selected_text}"
        user_message = await chat_service.create_user_message(
            conversation_id=conv_uuid,
            content=combined_message
        )

        # Query using the selected text
        response_text, sources = await chat_service.query_selected_text(
            selected_text=query_request.selected_text,
            context=query_request.question
        )

        # Add source information to response
        if sources:
            sources_text = "\n\n---\n📚 **Related sections from your textbook:**\n"
            for i, source in enumerate(sources[:3], 1):
                sources_text += f"\n{i}. Relevance: {source['relevance_score']:.2f}"

            response_text = response_text + sources_text

        # Save AI message
        await chat_service.create_ai_message(
            conversation_id=conv_uuid,
            content=response_text,
            sources=sources
        )

        # Return as plain text
        return StreamingResponse(
            iter([response_text]),
            media_type="text/plain"
        )

    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"ERROR in query_selection endpoint: {str(e)}")
        api_logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing selection query: {str(e)}"
        )