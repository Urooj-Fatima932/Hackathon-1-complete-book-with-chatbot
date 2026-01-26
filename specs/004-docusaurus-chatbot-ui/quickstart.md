# Quickstart Guide: Docusaurus Chatbot Implementation

## Overview

This guide provides step-by-step instructions to set up the RAG chatbot for your Docusaurus documentation site. The implementation includes a FastAPI backend with Cohere integration and a React frontend that integrates seamlessly with your Docusaurus site.

## Prerequisites

- Node.js 18+ (for Docusaurus)
- Python 3.11+
- Git
- API keys for:
  - Cohere (for embeddings and chat)
  - Qdrant (vector database)
  - Neon Postgres (SQL database)

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install fastapi uvicorn python-multipart pydantic psycopg2-binary asyncpg sqlalchemy qdrant-client cohere-toolkit python-dotenv
```

### 2. Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=postgresql+asyncpg://username:password@db.neon.tech/dbname
NEON_DB_URL=your_neon_db_url
SECRET_KEY=your_secret_key
DEBUG=false
```

### 3. Initialize Database

```bash
# Create tables and setup the database
python -m src.core.init_db
```

### 4. Run the Backend Server

```bash
# Start the FastAPI server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://localhost:8000`.

## Frontend Integration with Docusaurus

### 1. Install Frontend Dependencies

```bash
cd my-website
npm install framer-motion react-markdown remark-gfm
```

### 2. Configure Tailwind CSS

Update your `tailwind.config.js` to synchronize with Docusaurus themes:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./static/**/*.{js,jsx,ts,tsx}",
    "./node_modules/@docusaurus/core/lib/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: ['class', '[data-theme="dark"]'], // This syncs with Docusaurus theme
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 3. Create Chatbot Components

Create the following components in `my-website/src/components/`:

1. `ChatbotPopup.jsx` - Main container for the chatbot UI
2. `FloatingActionButton.jsx` - The floating button that opens the chat
3. `ChatWindow.jsx` - The main chat interface
4. `MessageBubble.jsx` - Individual message components

### 4. Integrate with Docusaurus Root

Swizzle the Docusaurus Root component to persist the chatbot across all pages:

```bash
cd my-website
npx docusaurus swizzle @docusaurus/Root
```

This creates a `src/theme/Root.js` file where you can inject the chatbot component at the root level:

```jsx
import React from 'react';
import ChatbotPopup from '../components/ChatbotPopup';

export default function Root({children}) {
  return (
    <>
      {children}
      <ChatbotPopup />
    </>
  );
}
```

## Configuration

### Backend Configuration

Review and adjust configurations in `backend/src/core/config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    database_url: str
    
    # RAG configuration
    chunk_size: int = 512
    chunk_overlap: int = 50
    retrieval_limit: int = 20
    rerank_top_k: int = 5
    
    # Performance settings
    response_timeout: int = 25  # seconds
    
    class Config:
        env_file = ".env"
```

### Frontend Configuration

Update the chatbot configuration in your component files:

```js
// API endpoints
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Chat settings
const CHAT_CONFIG = {
  maxMessageLength: 2000,
  enableTextSelection: true,
  themeSyncEnabled: true,
  streamingEnabled: true,
};
```

## Testing the Integration

### 1. Test Backend Endpoints

Verify the backend is working by testing the health endpoint:

```bash
curl http://localhost:8000/health
```

### 2. Test Document Ingestion

Test ingesting a sample document:

```bash
curl -X POST http://localhost:8000/api/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Documentation",
    "content": "This is a sample documentation content...",
    "url": "/docs/sample",
    "metadata": {"author": "test", "tags": ["test"]}
  }'
```

### 3. Run Docusaurus

Start your Docusaurus site to see the integrated chatbot:

```bash
cd my-website
npm run start
```

## Deployment

### 1. Backend Deployment

Deploy the FastAPI backend to your preferred cloud platform:

- **Railway**: `npx @railway/cli up`
- **Heroku**: Use the Python buildpack
- **AWS/GCP**: Containerize with Docker

### 2. Frontend Deployment

Deploy your Docusaurus site as you normally would:

```bash
npm run build
# Then deploy the `build/` folder to your hosting service
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your backend allows requests from your frontend origin
2. **Database Connection**: Verify your Neon Postgres connection string is correct
3. **Vector Database**: Confirm Qdrant is properly configured and accessible
4. **API Keys**: Double-check all API keys are set in environment variables

### Testing the Integration

Use the following test endpoints to verify functionality:

- Health check: `GET /health`
- Document ingestion: `POST /api/documents/ingest`
- Chat: `POST /api/chat/{conversation_id}/message`

## Next Steps

1. Customize the chatbot UI to match your documentation site
2. Add analytics to track chatbot usage
3. Implement advanced features like conversation history export
4. Set up monitoring and alerting for the backend services