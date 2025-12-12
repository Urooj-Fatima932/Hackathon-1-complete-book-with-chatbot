---
id: 1
title: Initialize Project Constitution
stage: constitution
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: cli_user
command: /sp.constitution
labels: [documentation,governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:

---

## Prompt

Project: AI-Native Book with Integrated RAG Chatbot, Context7 Personalization, Urdu Translation, and Better Auth Login System.

Core Principles:
- Clarity: All writing must be simple, beginner-friendly, and structured for step-by-step understanding.
- Accuracy: All technical explanations, architecture, and code examples must be valid, tested, and aligned with industry best practices.
- Consistency: All chapters must follow the same tone, formatting, structure, and explanation depth.
- Reusability: All agents, subagents, and skills must be reusable across the book and future projects.
- AI-Safety: No hallucinated facts or code. All AI output must strictly follow source content and verified knowledge.
- Maintainability: All code must be clean, modular, and easy to update.

Global Writing Standards:
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

Global Code Standards:
- All code must be runnable, complete, and tested.
- Must follow best practices:
  - TypeScript: strict typing, modern syntax, clean interfaces.
  - Python: readable functions, modular files, Pydantic (if needed).
- No placeholder code unless expllean, readable, and free of visual noise.
- All pages must render correctly on GitHub Pages.

Backend Standards:
- FastAPI must be used for all backend services.
- Qdrant Cloud (Free Tier) for vector database.
- Neon Serverless Postgres for user profiles + logs.
- OpenAI Agents/ChatKit SDK for RAG responses and routing.
- Must support:
  - Full chapter retrieval
  - Selected text retrieval
  - User-personalized retrieval

Authentication Standards:
- Use Better Auth for signup and login.
- During signup, collect:
  - Software skills
  - Hardware details
  - Programming background
  - Learning goals
- All API routes requiring personalization must be protected.

Constraints:
- The entire book must be deployable on GitHub Pages.
- Code examples must be runnable on a fresh environment.
- No step can depend on paid databases or services except OpenAI APIs.
- All text must follow this Constitution.
- All agents and subagents must obey the Constitution automatically.

Success Criteria:
- Book is published and fully working.
- Integrated RAG chatbot embedded and functional.
- “Answer based on selected text” works reliably.
- Personalization works based on stored user profile.
- Urdu and Roman Urdu translations work for every chapter.
- Auth system fully functional with Better Auth.
- All chapters consistent in formatting, tone, and teaching quality.
- No hallucinations, broken code, or inconsistent writing.

## Response snapshot

The project constitution has been updated to version 1.0.0. This is the initial creation of the constitution, incorporating all the principles and standards provided in the user's prompt. The `.specify/memory/constitution.md` file has been written.

## Outcome

- ✅ Impact: Successfully initialized the project constitution.
- 🧪 Tests: No tests run for constitution update.
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Review and update other templates based on the new constitution.
- 🧠 Reflection: Successfully parsed user input, filled constitution template, and generated initial version. Need to follow up on template consistency.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
