# Implementation Plan: Docusaurus Chatbot UI

**Branch**: `004-docusaurus-chatbot-ui` | **Date**: Wednesday, December 17, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-docusaurus-chatbot-ui/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy a production-ready, theme-aware RAG chatbot within a Docusaurus site using React frontend components, FastAPI backend with Cohere for RAG functionality, vector storage in Qdrant, and Neon Postgres for metadata. The solution includes a floating action button, collapsible chat window, text selection integration, and streaming responses with Markdown rendering.

## Technical Context

**Language/Version**: Python 3.11 (Backend), JavaScript/TypeScript (Frontend), Node 18+
**Primary Dependencies**: FastAPI, React (v18+), Cohere SDK, Qdrant client, Neon Postgres client, Tailwind CSS, Framer Motion
**Storage**: Neon Postgres for document metadata and Qdrant for vector embeddings
**Testing**: pytest for backend, Jest/React Testing Library for frontend components
**Target Platform**: Docusaurus v3+ documentation sites, React-based, cross-browser compatible
**Project Type**: Web application with frontend and backend components
**Performance Goals**: Response time under 2.5 seconds, sub-1 second UI transitions, 95% uptime
**Constraints**: <200ms p95 for UI interactions, 2.5s max for AI responses, compatible with Docusaurus swizzling
**Scale/Scope**: Supports 1000+ concurrent users with proper connection pooling, handles documentation sites with 500+ pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gates from constitution:**
- ✅ RAG & AI Standards: Chatbot must answer from documentation content, includes embeddings and vector indexing
- ✅ Frontend/UX Standards: Clean, readable UI components with proper accessibility
- ✅ Backend Standards: Using FastAPI for backend services, Qdrant for vector DB, Neon Postgres for metadata
- ✅ Performance Goals: 2.5s max for AI responses as specified in requirements
- ✅ Global Code Standards: Code must be clean, modular, and well-documented

## Project Structure

### Documentation (this feature)

```text
specs/004-docusaurus-chatbot-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── checklists/          # Quality validation checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── chat.py
│   │   ├── document.py
│   │   └── user.py
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   │   └── chat_service.py
│   ├── api/
│   │   ├── chat.py
│   │   ├── ingest.py
│   │   └── query.py
│   └── core/
│       ├── config.py
│       └── dependencies.py
├── requirements.txt
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatbotPopup.jsx
│   │   ├── FloatingActionButton.jsx
│   │   ├── ChatWindow.jsx
│   │   └── MessageBubble.jsx
│   ├── hooks/
│   │   ├── useChatState.js
│   │   └── useTextSelection.js
│   └── styles/
│       └── chatbot.css
└── package.json

my-website/
├── src/
│   ├── pages/
│   ├── components/
│   └── theme/
│       └── Root.js          # Docusaurus Root swizzle for chatbot integration
├── docusaurus.config.js
├── tailwind.config.js
├── babel.config.js
└── package.json
```

**Structure Decision**: Web application structure with separate backend and frontend components. The Docusaurus site integrates the chatbot through a Root swizzle component that wraps the entire site, ensuring the chatbot persists during navigation. The backend provides FastAPI endpoints for chat functionality, ingestion, and retrieval, while the frontend provides React components that manage state and UI interactions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Docusaurus Root Swizzling | Needed to persist chatbot across all documentation pages | Direct component integration would break on page navigation |
| Multiple storage systems (Neon + Qdrant) | Vector store required for semantic search, SQL for metadata | Single store would compromise either search performance or metadata operations |