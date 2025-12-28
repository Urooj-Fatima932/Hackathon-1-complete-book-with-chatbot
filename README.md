# Docusaurus Chatbot UI

A production-ready, theme-aware RAG chatbot integrated into Docusaurus documentation sites.

## Features

- Floating Action Button (FAB) for easy access to the chat interface
- Collapsible chat window with smooth animations
- Text selection integration for contextual queries
- Theme synchronization with Docusaurus dark/light mode
- Streaming AI responses with typing effect
- Markdown rendering for formatted content

## Tech Stack

- **Frontend**: React 18+, Docusaurus v3+, Framer Motion, Tailwind CSS, React Markdown
- **Backend**: FastAPI, Python 3.11
- **AI Services**: Cohere for RAG functionality
- **Vector DB**: Qdrant for document embeddings
- **SQL DB**: Neon Postgres for metadata
- **Architecture**: Docusaurus Root swizzling for persistent integration

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env .env.local
   # Edit .env.local with your API keys and settings
   ```

5. Start the backend server:
   ```bash
   python -m uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to the Docusaurus site:
   ```bash
   cd my-website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

## API Endpoints

- `POST /api/chat/start` - Start a new conversation
- `POST /api/chat/{conversation_id}/message` - Send a message
- `POST /api/query-selection` - Query based on selected text
- `GET/PUT /api/user/preferences` - Manage user preferences

## Architecture

The implementation follows the planned architecture with:

- Frontend components in `my-website/src/components/`
- React hooks in `my-website/src/hooks/`
- API routes in `backend/src/api/`
- Service layer in `backend/src/services/`
- Database models in `backend/src/models/`

## Configuration

The app respects the Docusaurus theme settings by watching for `[data-theme]` attribute changes and adapting the chat interface accordingly.

## Deployment

For production deployment:

1. Build the Docusaurus site: `npm run build`
2. Deploy the backend service to a cloud provider
3. Update the API base URL in frontend services
4. Configure environment variables for production