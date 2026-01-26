# Implementation Tasks: Docusaurus Chatbot UI

## Feature Overview

Deploy a production-ready, theme-aware RAG chatbot within a Docusaurus site using React frontend components, FastAPI backend with Cohere for RAG functionality, vector storage in Qdrant, and Neon Postgres for metadata. The solution includes a floating action button, collapsible chat window, text selection integration, and streaming responses with Markdown rendering.

**Feature Branch**: `004-docusaurus-chatbot-ui`

**User Stories Priority Order**:
- [US1] Access Chat Interface via FAB (P1) - Foundational
- [US2] Engage in Conversational Exchange (P1) - Core functionality 
- [US3] Query Selected Text Context (P2) - Enhanced interaction
- [US4] Experience Consistent Theme Integration (P3) - Visual consistency

## Dependencies

**User Story Dependencies**:
- US1 (P1) is foundational and required for all other stories
- US2 (P1) builds on US1
- US3 (P2) can be implemented after US1
- US4 (P3) is independent but benefits from US1

**Implementation Order**: Setup → Foundational → US1 → US2 → US3 → US4 → Polish

## Parallel Execution Examples

**Per-User Story**:
- For US1: UI components (FAB, ChatWindow) can be developed in parallel with backend API endpoints
- For US2: Message rendering UI can be developed alongside backend chat services
- For US3: Text selection logic can be implemented parallel to query API development
- For US4: Theme configuration can be implemented alongside component styling

## Implementation Strategy

**MVP Scope (US1 + US2)**: Basic FAB with chat window and simple conversation flow
**Incremental Delivery**: Each user story adds a complete, independently testable feature
**Phase Approach**: Setup → Foundational → User Stories → Polish

---

## Phase 1: Setup (Project Initialization)

### Goal
Initialize project structure and configure development environment with required dependencies and tools.

- [X] T001 Create backend project structure in `backend/` directory
- [X] T002 [P] Setup backend dependencies in `backend/requirements.txt` (FastAPI, Pydantic, asyncpg, SQLAlchemy, qdrant-client, cohere, python-dotenv)
- [X] T003 [P] Setup frontend dependencies in `my-website/package.json` (framer-motion, react-markdown, remark-gfm)
- [X] T004 Setup backend configuration model `backend/src/core/config.py` with Pydantic settings
- [X] T005 Create `.env` template file for API keys (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL)
- [X] T006 [P] Initialize Git repository with proper `.gitignore` for backend, frontend, and sensitive files
- [X] T007 Create initial database migration files for Neon Postgres
- [X] T008 Setup basic FastAPI app structure with CORS middleware in `backend/src/main.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

### Goal
Implement foundational backend services and database models required by all user stories.

- [X] T009 Create database models in `backend/src/models/`: Document, DocumentChunk, Conversation, Message
- [X] T010 [P] Create database models: User, DocumentReference in `backend/src/models/`
- [X] T011 Implement async database connection service in `backend/src/core/database.py` using asyncpg
- [X] T012 Create Qdrant client service in `backend/src/core/vector_db.py` for vector operations
- [X] T013 [P] Implement database utility functions for basic CRUD operations in `backend/src/core/db_utils.py`
- [X] T014 Setup Qdrant collection for document embeddings with 1024-dim vectors
- [X] T015 Create Pydantic schemas for all models in `backend/src/schemas/`
- [X] T016 [P] Implement API response models for all endpoints in `backend/src/schemas/responses.py`
- [X] T017 Create service layer base classes in `backend/src/services/base.py`
- [X] T018 Setup logging and monitoring configuration in `backend/src/core/logging.py`

---

## Phase 3: User Story 1 - Access Chat Interface via FAB (Priority: P1)

### Goal
Implement floating action button that opens chat window, providing access to the chat interface.

### Independent Test Criteria
Can be fully tested by clicking the floating action button and verifying that the chat window opens with correct dimensions and styling, delivering a seamless transition from the documentation to the chat experience.

- [X] T019 [P] Create FloatingActionButton component in `my-website/src/components/FloatingActionButton.jsx`
- [X] T020 [P] Create ChatWindow component in `my-website/src/components/ChatWindow.jsx`
- [X] T021 Implement FAB click handler to toggle chat window visibility
- [X] T022 [P] Style FAB and ChatWindow with Tailwind CSS (position bottom-right, 56px circular, 400px width, 600px max height)
- [X] T023 Add smooth animations using Framer Motion for open/close transitions
- [X] T024 Implement state management for chat window open/closed state using React hooks
- [X] T025 Create useChatState hook in `my-website/src/hooks/useChatState.js` for chat UI state
- [X] T026 Implement state persistence across page navigations using localStorage or similar
- [X] T027 Add proper accessibility attributes (aria labels, keyboard navigation) to FAB and ChatWindow
- [X] T028 [US1] Test: Verify FAB appears at bottom-right of viewport on all documentation pages
- [X] T029 [US1] Test: Verify clicking FAB opens ChatWindow with smooth animation
- [X] T030 [US1] Test: Verify clicking FAB again closes ChatWindow and returns to initial state

---

## Phase 4: User Story 2 - Engage in Conversational Exchange (Priority: P1)

### Goal
Implement messaging functionality allowing users to send questions and receive AI responses with typing effect.

### Independent Test Criteria
Can be fully tested by entering a query and receiving a response, delivering the primary value proposition of the chatbot.

- [X] T031 Create MessageBubble component in `my-website/src/components/MessageBubble.jsx`
- [X] T032 [P] Style MessageBubble with different alignments: right-aligned for user, left-aligned for AI
- [X] T033 Implement message input field and send button in ChatWindow footer
- [X] T034 Create API service in `my-website/src/services/chatService.js` for chat endpoints
- [X] T035 [US2] Create ChatService in `backend/src/services/chat_service.py` for conversation logic
- [X] T036 [US2] Create EmbeddingService in `backend/src/services/embedding_service.py` for text processing
- [X] T037 [US2] Create RetrievalService in `backend/src/services/retrieval_service.py` for document search
- [X] T038 [US2] Implement POST /api/chat/{conversation_id}/message endpoint in `backend/src/api/chat.py`
- [X] T039 [US2] Implement streaming response functionality using FastAPI StreamingResponse
- [X] T040 [P] Implement real-time token display with typing effect in frontend message display
- [X] T041 Create ConversationService in `backend/src/services/conversation_service.py`
- [X] T042 [P] Implement message history in ChatWindow with auto-scroll to latest message
- [X] T043 [US2] Implement POST /api/chat/start endpoint for new conversations
- [X] T044 [P] Integrate Cohere Command-R+ for generating AI responses
- [X] T045 [P] Implement react-markdown rendering for formatted content (bold, code, lists)
- [X] T046 [US2] Test: Verify sending a message creates proper user bubble alignment on right
- [X] T047 [US2] Test: Verify AI response appears with typing effect and proper left alignment
- [X] T048 [US2] Test: Verify formatted content (bold, code, lists) renders correctly

---

## Phase 5: User Story 3 - Query Selected Text Context (Priority: P2)

### Goal
Implement text selection detection that shows contextual UI hint when user selects text in documentation.

### Independent Test Criteria
Can be fully tested by selecting text and observing the contextual UI hint, delivering enhanced accessibility to the chatbot for specific content queries.

- [X] T049 Create useTextSelection hook in `my-website/src/hooks/useTextSelection.js`
- [X] T050 Implement global mouseup event listener to detect text selection
- [X] T051 [P] Create contextual hint UI element that appears above input field
- [X] T052 Add logic to extract selected text content and position
- [X] T053 [P] Implement "Ask about selection" button that includes selected text in query
- [X] T054 [US3] Create POST /api/query-selection endpoint in `backend/src/api/query.py`
- [X] T055 [US3] Update ChatService to handle selected text context in messages
- [X] T056 Create visual feedback for text selection (highlight or temporary border)
- [X] T057 [P] Implement debouncing for selection detection to avoid performance issues
- [X] T058 [US3] Integrate selected text as system prompt context in Cohere calls
- [X] T059 [US3] Test: Verify selecting text shows contextual hint UI above input field
- [X] T060 [US3] Test: Verify clicking hint includes selected text in new query
- [X] T061 [US3] Test: Verify selected text context improves query relevance

---

## Phase 6: User Story 4 - Experience Consistent Theme Integration (Priority: P3)

### Goal
Implement theme synchronization so chat interface matches documentation site's light/dark mode.

### Independent Test Criteria
Can be tested by toggling between themes and verifying the chat interface adapts appropriately, delivering consistent visual branding.

- [X] T062 Update `tailwind.config.js` to use `darkMode: ['class', '[data-theme="dark"]']`
- [X] T063 [P] Implement dark mode variants for FAB component using Tailwind dark: prefix
- [X] T064 [P] Implement dark mode variants for ChatWindow component
- [X] T065 [P] Implement dark mode variants for MessageBubble component
- [X] T066 Create theme context in `my-website/src/contexts/ThemeContext.js`
- [X] T067 [P] Update MessageBubble styling to use Tailwind color classes that respect theme
- [X] T068 [P] Implement theme detection that watches for [data-theme] attribute changes
- [X] T069 [US4] Create GET /api/user/preferences endpoint for theme settings
- [X] T070 [US4] Create PUT /api/user/preferences endpoint to update theme preferences
- [X] T071 [US4] Implement theme preference storage in User model
- [X] T072 [US4] Test: Verify chat interface uses light theme colors when documentation is light
- [X] T073 [US4] Test: Verify chat interface uses dark theme colors when documentation is dark
- [X] T074 [US4] Test: Verify theme switch happens automatically when documentation theme changes

---

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Implement additional features, error handling, performance optimizations, and deployment configurations.

- [X] T075 Add comprehensive error handling for API calls and network issues
- [X] T076 [P] Implement loading states and skeleton UI for better UX
- [X] T077 Add rate limiting to API endpoints to prevent abuse
- [X] T078 [P] Implement proper validation for all API request bodies using Pydantic
- [X] T079 Add caching layer for frequently accessed embeddings and responses
- [X] T080 [P] Add comprehensive logging throughout the application
- [X] T081 Implement graceful degradation when AI services are unavailable
- [X] T082 [P] Add unit and integration tests for backend services
- [X] T083 [P] Add component tests for React components using React Testing Library
- [X] T084 Create health check endpoint at `/health` in FastAPI
- [X] T085 [P] Implement proper cleanup for event listeners to prevent memory leaks
- [X] T086 Add proper documentation for all API endpoints using FastAPI auto docs
- [X] T087 [P] Configure production-ready settings for deployment (env variables, security headers)
- [X] T088 Update docusaurus.config.js to include chatbot integration
- [X] T089 [P] Implement swizzling of Docusaurus Root component to inject ChatbotPopup
- [X] T090 Create README.md with setup instructions and project overview
- [X] T091 [P] Add performance monitoring for response times and AI service usage
- [X] T092 Test end-to-end user flows across all user stories
- [X] T093 Verify all functional requirements from spec are implemented (FR-001 to FR-010)