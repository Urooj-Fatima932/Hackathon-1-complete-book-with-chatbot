import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy", 
        "message": "Docusaurus Chatbot API is running"
    }

def test_start_conversation():
    """Test starting a new conversation"""
    response = client.post("/api/chat/start")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "session_id" in data

def test_chat_message_flow():
    """Test a complete chat message flow"""
    # Start a conversation
    conv_response = client.post("/api/chat/start")
    assert conv_response.status_code == 200
    conv_data = conv_response.json()
    conversation_id = conv_data["id"]
    
    # Send a message
    msg_response = client.post(
        f"/api/chat/{conversation_id}/message",
        json={"message": "Hello, how are you?"}
    )
    assert msg_response.status_code == 200
    msg_data = msg_response.json()
    assert "id" in msg_data
    assert "content" in msg_data
    assert msg_data["role"] == "assistant"