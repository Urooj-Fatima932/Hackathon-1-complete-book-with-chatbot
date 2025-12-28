"""Test script for intent classification"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.intent_classifier import IntentClassifier

async def test_intent_classification():
    classifier = IntentClassifier()

    test_cases = [
        ("Hi", "greeting"),
        ("Hello!", "greeting"),
        ("How are you?", "greeting"),
        ("Good morning", "greeting"),
        ("Who are you?", "identity"),
        ("What can you do?", "identity"),
        ("What are you?", "identity"),
        ("What is photosynthesis?", "textbook_question"),
        ("Explain quantum physics", "textbook_question"),
        ("What is the capital of Pakistan?", "off_topic"),
        ("Who is the president of USA?", "off_topic"),
        ("What's the weather today?", "off_topic"),
    ]

    print("=" * 60)
    print("INTENT CLASSIFICATION TEST")
    print("=" * 60)

    for message, expected_intent in test_cases:
        intent = await classifier.classify_intent(message)
        status = "[OK]" if intent == expected_intent else "[FAIL]"
        print(f"{status} '{message}' -> {intent} (expected: {expected_intent})")

        # Show actual response
        if intent == "greeting":
            response = classifier.get_greeting_response(message)
        elif intent == "identity":
            response = classifier.get_identity_response()
        elif intent == "off_topic":
            response = classifier.get_off_topic_response()
        else:
            response = "Would use RAG pipeline..."

        print(f"  Response: {response[:80]}...")
        print()

if __name__ == "__main__":
    asyncio.run(test_intent_classification())
