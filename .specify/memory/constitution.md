<!-- Sync Impact Report:
Version change: 0.0.0 -> 1.0.0
Modified principles: None (initial creation)
Added sections: Global Writing Standards, Global Code Standards, RAG & AI Standards, Translation Standards, Frontend/UX Standards, Backend Standards, Authentication Standards, Personalization (Context7) Standards, Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs: None
-->
# AI-Native Book with Integrated RAG Chatbot, Context7 Personalization, Urdu Translation, and Better Auth Login System. Constitution

## Core Principles

### Clarity
All writing must be simple, beginner-friendly, and structured for step-by-step understanding.

### Accuracy
All technical explanations, architecture, and code examples must be valid, tested, and aligned with industry best practices.

### Consistency
All chapters must follow the same tone, formatting, structure, and explanation depth.

### Reusability
All agents, subagents, and skills must be reusable across the book and future projects.

### AI-Safety
No hallucinated facts or code. All AI output must strictly follow source content and verified knowledge.

### Maintainability
All code must be clean, modular, and easy to update.

## Global Writing Standards

- Tone: Friendly, clear, supportive, beginner-focused.
- Format for every chapter:
  1. Introduction
  2. Concepts Breakdown
  3. Architecture/Workflow
  4. Step-by-Step Implementation
  5. Example Code
  6. Visual Explanation (if needed)
  7. Summary
- Reading Level: Beginner to intermediate (grade 9–12).
- No jargon without explanation.
- All diagrams must follow a consistent visual style.
- All explanations must be actionable, not theoretical.

## Global Code Standards

- All code must be runnable, complete, and tested.
- Must follow best practices:
  - TypeScript: strict typing, modern syntax, clean interfaces.
  - Python: readable functions, modular files, Pydantic (if needed).
- No placeholder code unless explicitly marked.
- Every code block must include comments explaining key logic.
- Folder structure must follow clean architecture principles.

## RAG & AI Standards

- Chatbot must answer *only* from book content unless user provides custom text.
- RAG pipeline must include embeddings, vector indexing, similarity search.
- Chatbot must support “answer from selected text only.”
- No hallucinations: model must decline when answer is not in book.
- Subagents must inherit all global tone, accuracy, and explanation rules.
- All AI output must be deterministic under temperature ≤ 0.2.
- Rewritten chapters must stay aligned with original meaning.
- No assumptions: use only stored user background data.

## Translation Standards

- Urdu translation must focus on clarity and meaning.
- Roman Urdu must use simple phonetic spelling understandable by beginners.
- Avoid overly hard Urdu vocabulary.
- Maintain formatting (headings, code blocks, lists).
- Never translate code.

## Frontend/UX Standards

- All chapters must include buttons at the top:
  - “Personalize for me”
  - “Translate to Urdu”
  - “Translate to Roman Urdu”
- Output must be clean, readable, and free of visual noise.
- All pages must render correctly on GitHub Pages.

## Backend Standards

- FastAPI must be used for all backend services.
- Qdrant Cloud (Free Tier) for vector database.
- Neon Serverless Postgres for user profiles + logs.
- OpenAI Agents/ChatKit SDK for RAG responses and routing.
- Must support:
  - Full chapter retrieval
  - Selected text retrieval
  - User-personalized retrieval

## Authentication Standards

- Use Better Auth for signup and login.
- During signup, collect:
  - Software skills
  - Hardware details
  - Programming background
  - Learning goals
- All API routes requiring personalization must be protected.

## Personalization (Context7) Standards

- Personalization can adjust tone, complexity, and examples.
- Personalization cannot change factual correctness.
- Must respect user profile stored from Better Ath Integrated RAG Chatbot, Context7 Personalization, Urdu Translation, and Better Auth Login System.

## Constraints

- The entire book must be deployable on GitHub Pages.
- Code examples must be runnable on a fresh environment.
- No step can depend on paid databases or services except OpenAI APIs.
- All text must follow this Constitution.
- All agents and subagents must obey the Constitution automatically.

## Success Criteria

- Book is published and fully working.
- Integrated RAG chatbot embedded and functional.
- “Answer based on selected text” works reliably.
- Personalization works based on stored user profile.
- Urdu and Roman Urdu translations work for every chapter.
- Auth system fully functional with Better Auth.
- All chapters consistent in formatting, tone, and teaching quality.
- No hallucinations, broken code, or inconsistent writing.

## Governance

All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
