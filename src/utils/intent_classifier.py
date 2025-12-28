# src/utils/intent_classifier.py
import re
from typing import Literal
from ..core.logging_config import service_logger

IntentType = Literal["greeting", "textbook_question", "off_topic", "identity"]

class IntentClassifier:
    """Classifies user intent using fast pattern matching"""

    def __init__(self):
        # Greeting patterns (very common, respond instantly)
        self.greeting_patterns = [
            r'\b(hi|hello|hey|greetings|hola|howdy)\b',
            r'\b(good\s*(morning|afternoon|evening|day))\b',
            r'\b(how\s*(are|r)\s*(you|u))\b',
            r'^(yo|sup|wassup|whats\s*up)$',
        ]

        # Identity patterns (asking about the bot)
        self.identity_patterns = [
            r'\b(who|what)\s*(are|r)\s*(you|u)\b',
            r'\bwhat\s*can\s*you\s*do\b',
            r'\bwhat\s*(is|are)\s*your\s*(purpose|function|capabilities)\b',
            r'\btell\s*me\s*about\s*(yourself|you)\b',
            r'\byour\s*capabilities\b',
            r'\bwhat\s*do\s*you\s*do\b',
        ]

        # Off-topic patterns (general knowledge, unrelated to textbook)
        self.off_topic_patterns = [
            r'\b(capital|president|prime minister|government|country|city)\b',
            r'\b(weather|temperature|forecast|climate)\b',
            r'\b(sports|football|cricket|basketball|game|match)\b',
            r'\b(news|current events|today\'?s)\b',
            r'\b(movie|film|tv show|series|entertainment)\b',
            r'\btell\s*(me\s*)?(a\s*)?(joke|story)\b',
            r'\b(recipe|cooking|food|restaurant)\b',
            r'\b(stock|market|price|bitcoin|crypto)\b',
        ]

    def classify_intent(self, user_message: str) -> IntentType:
        """
        Fast pattern-based classification (no LLM call!)
        - greeting: Hi, Hello, How are you, etc.
        - identity: Who are you, What can you do, etc.
        - off_topic: General knowledge questions
        - textbook_question: Everything else (uses RAG)
        """
        message_lower = user_message.lower().strip()
        service_logger.debug(f"Classifying intent for: {message_lower[:50]}")

        # Check greeting patterns (FASTEST - most common)
        for pattern in self.greeting_patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                service_logger.info(f"Detected intent: greeting (pattern match)")
                return "greeting"

        # Check identity patterns
        for pattern in self.identity_patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                service_logger.info(f"Detected intent: identity (pattern match)")
                return "identity"

        # Check off-topic patterns
        for pattern in self.off_topic_patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                service_logger.info(f"Detected intent: off_topic (pattern match)")
                return "off_topic"

        # Default to textbook question (uses RAG)
        service_logger.info(f"Detected intent: textbook_question (default)")
        return "textbook_question"

    def get_greeting_response(self, user_message: str) -> str:
        """Return appropriate greeting response"""
        message_lower = user_message.lower()

        if any(word in message_lower for word in ["hi", "hello", "hey", "greetings"]):
            return "Hello! 👋 I'm your textbook assistant. I'm here to help you understand the content in your textbook. What would you like to know?"
        elif any(word in message_lower for word in ["how are you", "how r u", "how are u"]):
            return "I'm doing great, thank you for asking! I'm here and ready to help you with any questions about your textbook. What would you like to learn today?"
        elif any(word in message_lower for word in ["good morning", "morning"]):
            return "Good morning! ☀️ Ready to explore your textbook together? What topic would you like to discuss?"
        elif any(word in message_lower for word in ["good evening", "evening"]):
            return "Good evening! 🌙 I'm here to help you with your textbook. What can I assist you with?"
        elif any(word in message_lower for word in ["good afternoon", "afternoon"]):
            return "Good afternoon! I'm ready to help you understand your textbook better. What questions do you have?"
        else:
            return "Hello! I'm your textbook assistant. How can I help you understand the material today?"

    def get_identity_response(self) -> str:
        """Return response about chatbot identity"""
        return """I'm an AI-powered textbook assistant, designed to help you understand and learn from your textbook content.

Here's what I can do:
📚 Answer questions about topics covered in your textbook
💡 Explain concepts and provide clarifications
🔍 Help you find relevant information from the textbook
📖 Provide context-based explanations

I focus specifically on the content available in your textbook. If you have questions about topics covered in the book, feel free to ask!"""

    def get_off_topic_response(self) -> str:
        """Return response for off-topic questions"""
        return """I appreciate your question, but I'm specifically designed to help with your textbook content. I can only answer questions related to the topics covered in your textbook.

If you have questions about the material in your textbook, I'd be happy to help! What would you like to learn from the textbook?"""
