# src/services/chat_service.py
import asyncio
import traceback
from typing import List, Tuple, Generator
import cohere
from ..core.config import settings
from ..services.conversation_service import ConversationService
from ..services.embedding_service import EmbeddingService
from ..services.retrieval_service import RetrievalService
from ..core.database import get_db
from ..models.conversation import Message
from ..core.logging_config import service_logger
from ..utils.intent_classifier import IntentClassifier


class ChatService:
    """Main service for handling chat functionality"""

    def __init__(self, db, app_state=None):
        service_logger.debug("Initializing ChatService")
        self.db = db
        self.conversation_service = ConversationService(db)
        self.app_state = app_state
        self.intent_classifier = IntentClassifier()

    def _get_cohere_client(self):
        """Get or create Cohere client."""
        if self.app_state and hasattr(self.app_state, 'cohere_client'):
            return self.app_state.cohere_client
        return cohere.AsyncClient(settings.cohere_api_key)

    def _get_embedding_service(self):
        """Get or create embedding service."""
        if self.app_state and hasattr(self.app_state, 'embedding_service'):
            return self.app_state.embedding_service
        from ..services.embedding_service import EmbeddingService
        return EmbeddingService()

    def _get_retrieval_service(self):
        """Get or create retrieval service."""
        if self.app_state and hasattr(self.app_state, 'retrieval_service'):
            return self.app_state.retrieval_service
        from ..services.retrieval_service import RetrievalService
        return RetrievalService()

    async def create_user_message(self, conversation_id: str, content: str) -> Message:
        """Create a user message in the conversation"""
        return await self.conversation_service.create_user_message(conversation_id, content)

    async def create_ai_message(self, conversation_id: str, content: str, sources: list = None) -> Message:
        """Create an AI message in the conversation"""
        return await self.conversation_service.create_ai_message(conversation_id, content, sources)

    async def generate_response_sync(self, conversation_id: str, user_message: Message) -> str:
        """Generate a response synchronously (for non-streaming)"""
        service_logger.info(f"Generating response for conversation {conversation_id}")
        service_logger.debug(f"User message ID: {user_message.id}, Content length: {len(user_message.content)}")

        try:
            # Step 1: Classify intent (FAST - no API call!)
            service_logger.info("Classifying user intent...")
            intent = self.intent_classifier.classify_intent(user_message.content)
            service_logger.info(f"Detected intent: {intent}")

            # Step 2: Handle based on intent
            if intent == "greeting":
                service_logger.info("Handling greeting intent")
                return self.intent_classifier.get_greeting_response(user_message.content)

            elif intent == "identity":
                service_logger.info("Handling identity intent")
                return self.intent_classifier.get_identity_response()

            elif intent == "off_topic":
                service_logger.info("Handling off-topic intent")
                return self.intent_classifier.get_off_topic_response()

            # Step 3: For textbook questions, use RAG pipeline
            service_logger.info("Processing as textbook question - using RAG pipeline")

            # Retrieve relevant context from documents
            service_logger.info("Retrieving context from knowledge base...")
            context_docs = await self.retrieval_service.search_and_rerank(
                query=user_message.content,
                search_top_k=settings.retrieval_limit,
                rerank_top_k=settings.rerank_top_k
            )

            # Format the context from retrieved documents
            context_text = "\n\n".join([doc["content"] for doc in context_docs])

            # Prepare the prompt with context
            if context_text:
                prompt = f"""You are a helpful assistant that answers questions ONLY based on the provided context from the textbook. If the answer is not in the context, say "I couldn't find this information in the textbook."

Context from textbook:
{context_text}

Question: {user_message.content}

Answer (based ONLY on the context above):"""
            else:
                prompt = f"""I apologize, but I couldn't find relevant information in the textbook to answer your question: {user_message.content}

Please try rephrasing your question or ask about topics covered in the textbook."""
            service_logger.debug(f"Prompt length: {len(prompt)} chars")

            # Generate response using Cohere Chat API
            service_logger.info("Calling Cohere Chat API")

            # If no context, return early without calling API
            if not context_text:
                service_logger.warning("No context found - returning fallback message")
                return prompt

            try:
                response = await self.cohere_client.chat(
                    model="command-r-plus-08-2024",
                    message=prompt,
                    max_tokens=500,  # Increased for better answers
                    temperature=0.3  # Lower temperature for more accurate, context-focused answers
                )
                service_logger.info("Cohere API call successful")
                service_logger.debug(f"Response text length: {len(response.text) if response.text else 0}")

                result = response.text if response.text else "I couldn't find a good answer to your question."

                # Add source information if context was used
                if context_docs and result:
                    sources_text = "\n\n---\n📚 **Sources from your textbook:**\n"
                    for i, doc in enumerate(context_docs[:3], 1):  # Show top 3 sources
                        title = doc.get("title", "Untitled")
                        url = doc.get("url", "")
                        score = doc.get("score", 0)

                        # Create clickable link if URL exists
                        if url:
                            sources_text += f"\n{i}. [{title}]({url}) (Relevance: {score:.2f})"
                        else:
                            sources_text += f"\n{i}. {title} (Relevance: {score:.2f})"

                    result = result + sources_text

                service_logger.info(f"Generated response: {len(result)} chars, {len(context_docs)} sources")
                return result

            except Exception as cohere_error:
                service_logger.error(f"Cohere API error: {type(cohere_error).__name__}")
                service_logger.error(f"Cohere error message: {str(cohere_error)}")
                service_logger.error(f"Cohere error traceback:\n{traceback.format_exc()}")
                raise

        except Exception as e:
            service_logger.error(f"Error in generate_response_sync: {type(e).__name__}")
            service_logger.error(f"Error message: {str(e)}")
            service_logger.error(f"Full traceback:\n{traceback.format_exc()}")
            raise

    async def generate_response_stream(self, conversation_id: str, user_message: Message) -> Generator[str, None, None]:
        """Generate a response with streaming"""
        service_logger.info(f"Generating streaming response for conversation {conversation_id}")

        # Retrieve relevant context from documents
        context_docs = await self.retrieval_service.search_and_rerank(
            query=user_message.content,
            search_top_k=settings.retrieval_limit,
            rerank_top_k=settings.rerank_top_k
        )

        # Format the context from retrieved documents
        context_text = "\n\n".join([doc["content"] for doc in context_docs])

        # Prepare the prompt with context (same improved prompt)
        if context_text:
            prompt = f"""You are a helpful assistant that answers questions ONLY based on the provided context from the textbook. If the answer is not in the context, say "I couldn't find this information in the textbook."

Context from textbook:
{context_text}

Question: {user_message.content}

Answer (based ONLY on the context above):"""
        else:
            service_logger.warning("No context found for streaming response")
            yield f"I apologize, but I couldn't find relevant information in the textbook to answer your question: {user_message.content}\n\nPlease try rephrasing your question or ask about topics covered in the textbook."
            return

        # Use Cohere chat endpoint for streaming
        service_logger.info("Starting Cohere streaming response")
        async with self.cohere_client.chat_stream(
            model="command-r-plus-08-2024",
            message=prompt,
            temperature=0.3
        ) as stream:
            async for event in stream:
                if event.event_type == "text-generation":
                    yield event.text

    async def query_selected_text(self, selected_text: str, context: str = "") -> Tuple[str, List[dict]]:
        """Handle query based on selected text"""
        # Retrieve relevant context from documents based on selected text
        context_docs = await self.retrieval_service.search_and_rerank(
            query=selected_text,
            search_top_k=settings.retrieval_limit,
            rerank_top_k=settings.rerank_top_k
        )

        # Format the context from retrieved documents
        context_text = "\n\n".join([doc["content"] for doc in context_docs])

        # Prepare the prompt with both selected text and any additional context
        if context_text:
            prompt = f"Selected text: {selected_text}\n\nAdditional context: {context}\n\nBased on the selected text and documentation, please provide relevant information:"
        else:
            prompt = f"Selected text: {selected_text}\n\nAdditional context: {context}\n\nPlease provide information about this selection:"

        # Generate response using Cohere Chat API (replaces deprecated generate API)
        response = await self.cohere_client.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            max_tokens=500,
            temperature=0.7
        )

        response_text = response.text if response.text else "I couldn't find relevant information."

        # Format sources
        sources = [
            {
                "id": doc["id"],
                "content": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"],
                "document_id": doc["document_id"],
                "relevance_score": doc["score"]
            }
            for doc in context_docs
        ]

        return response_text, sources
