# Data Model: Docusaurus Chatbot UI

## Overview

This document defines the entities, relationships, and data structures required for the RAG chatbot implementation within the Docusaurus documentation site.

## Core Entities

### 1. Document

**Description**: Represents a documentation page or content chunk that can be indexed for retrieval

**Fields**:
- `id` (UUID): Unique identifier for the document
- `title` (String): Title of the documentation page
- `content` (Text): The actual content of the document
- `url` (String): URL path to the original documentation page
- `source_type` (Enum): Type of source (e.g., 'markdown', 'html', 'api_doc')
- `metadata` (JSON): Additional metadata about the document
- `created_at` (DateTime): When the document was first indexed
- `updated_at` (DateTime): When the document was last updated
- `embedding_vector_id` (String): Reference to the vector ID in Qdrant

**Validation Rules**:
- `title` must not be empty
- `url` must be a valid URL path
- `content` length must be within reasonable limits (max 100,000 characters)
- `embedding_vector_id` must exist in vector database

### 2. DocumentChunk

**Description**: Represents a smaller, indexed piece of a larger document for retrieval

**Fields**:
- `id` (UUID): Unique identifier for the chunk
- `document_id` (UUID): Reference to the parent document
- `content` (Text): The chunked content
- `chunk_index` (Integer): Sequential index of this chunk within the document
- `embedding_vector_id` (String): Reference to the vector ID in Qdrant
- `token_count` (Integer): Number of tokens in this chunk
- `created_at` (DateTime): When the chunk was created

**Validation Rules**:
- `content` must not be empty
- `chunk_index` must be non-negative
- `token_count` must be positive
- Must reference a valid document

### 3. Conversation

**Description**: Represents a single chat session between user and AI

**Fields**:
- `id` (UUID): Unique identifier for the conversation
- `session_id` (String): Session identifier for client-side tracking
- `title` (String): Auto-generated title based on first message
- `created_at` (DateTime): When conversation started
- `updated_at` (DateTime): When conversation was last updated
- `is_active` (Boolean): Whether the conversation is currently active

**Validation Rules**:
- `session_id` must be present
- `created_at` must be before `updated_at`

### 4. Message

**Description**: Represents a single message within a conversation

**Fields**:
- `id` (UUID): Unique identifier for the message
- `conversation_id` (UUID): Reference to the parent conversation
- `role` (Enum): Role of the message ('user', 'assistant', 'system')
- `content` (Text): The message content
- `created_at` (DateTime): When the message was created
- `tokens_count` (Integer): Number of tokens in the message
- `sources` (JSON): Array of document sources referenced in the response
- `is_streaming_complete` (Boolean): Whether streaming is complete for AI responses

**Validation Rules**:
- `role` must be one of the allowed values
- `content` must not be empty
- Must reference a valid conversation
- `tokens_count` must be non-negative

### 5. User

**Description**: Represents the documentation site visitor/user

**Fields**:
- `id` (UUID): Unique identifier for the user
- `session_id` (String): Session identifier (for anonymous users)
- `preferences` (JSON): User preferences including theme settings
- `created_at` (DateTime): When the user's session started
- `last_active` (DateTime): When the user was last active

**Validation Rules**:
- `session_id` must be present for all users
- `created_at` must be before `last_active`

### 6. DocumentReference

**Description**: Links AI responses to the source documents they reference

**Fields**:
- `id` (UUID): Unique identifier for the reference
- `message_id` (UUID): Reference to the AI message
- `document_chunk_id` (UUID): Reference to the source chunk
- `relevance_score` (Float): Relevance score from the retrieval process
- `citation_metadata` (JSON): Additional citation information

**Validation Rules**:
- Must reference a valid message and document chunk
- `relevance_score` must be between 0 and 1

## Relationships

```
User (1) --- (m) Conversation
Conversation (1) --- (m) Message
Message (1) --- (m) DocumentReference
Document (1) --- (m) DocumentChunk
DocumentReference (m) --- (1) DocumentChunk
```

## State Transitions

### Conversation States
- `active`: Conversation is currently in progress
- `completed`: Conversation has ended normally
- `archived`: Conversation is no longer active but stored for reference

### Message States
- `pending`: Message is being processed
- `complete`: Message is fully generated/received
- `error`: Message generation/reception failed

## Indexes and Performance Considerations

### Required Indexes:
1. **Document**: Index on `url` for fast lookup by page URL
2. **DocumentChunk**: Index on `document_id` for efficient document relationships
3. **Conversation**: Index on `session_id` and `updated_at` for session management
4. **Message**: Index on `conversation_id` and `created_at` for chronological ordering
5. **User**: Index on `session_id` for session tracking

### Performance Notes:
- Document and DocumentChunk tables will be primarily read-heavy
- Conversation and Message tables will have mixed read/write patterns
- Consider partitioning large tables by date for better performance
- Vector similarity searches handled by Qdrant, not Postgres