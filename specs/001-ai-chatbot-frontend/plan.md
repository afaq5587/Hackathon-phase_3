# Implementation Plan: AI-Powered Todo Chatbot with Beautiful Frontend

**Branch**: `001-ai-chatbot-frontend` | **Date**: 2025-12-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot-frontend/spec.md`

## Summary

Build an AI-powered conversational chatbot interface that enables users to manage their todo tasks through natural language. The system uses OpenAI Agents SDK with MCP tools for task operations, persists conversations to Neon PostgreSQL, and provides a beautiful ChatKit-based frontend. All 26 functional requirements from the spec will be addressed through this architecture.

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript/JavaScript (Frontend - Next.js 16+)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK (Python), SQLModel, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (Desktop + Mobile responsive)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**:
- Chat interface loads in <2 seconds (SC-004)
- Task operations complete in <10 seconds (SC-001)
- Task list retrieval in <3 seconds (SC-002)
- Loading indicator within 1 second (SC-008)
**Constraints**:
- Stateless backend (per Constitution Principle II)
- JWT authentication required on all endpoints (Constitution Principle V)
- MCP tools must follow standard schema (Constitution Principle III)
**Scale/Scope**: Single-user sessions, conversation persistence, 5 MCP tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| I. Spec-Driven Development | All implementation follows Specify → Plan → Tasks → Implement | PASS - Following SDD workflow |
| II. Stateless Architecture | Chat endpoint stateless, all state in database | PASS - Design uses DB persistence |
| III. MCP-Native Tool Design | 5 tools: add_task, list_tasks, complete_task, delete_task, update_task | PASS - All tools planned |
| IV. Agent-First Conversation | OpenAI Agents SDK orchestrates chat, 7-step flow | PASS - Architecture follows flow |
| V. Authentication Continuity | JWT validation on all endpoints, user isolation | PASS - JWT middleware planned |
| VI. Monorepo Structure | /frontend, /backend, /specs directories | PASS - Structure defined below |

**Gate Status**: ALL PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-frontend/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.md     # MCP tool schemas
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py           # Task SQLModel (FR-011 to FR-015)
│   │   ├── conversation.py   # Conversation SQLModel (FR-016 to FR-019)
│   │   └── message.py        # Message SQLModel (FR-016 to FR-019)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py   # Chat orchestration (FR-007 to FR-010)
│   │   ├── task_service.py   # Task CRUD operations
│   │   └── conversation_service.py  # Conversation management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py           # POST /api/{user_id}/chat endpoint
│   │   ├── auth.py           # JWT middleware (FR-020 to FR-022)
│   │   └── deps.py           # Dependency injection
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py         # MCP server setup
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── add_task.py       # MCP tool (Constitution III)
│   │       ├── list_tasks.py     # MCP tool (Constitution III)
│   │       ├── complete_task.py  # MCP tool (Constitution III)
│   │       ├── delete_task.py    # MCP tool (Constitution III)
│   │       └── update_task.py    # MCP tool (Constitution III)
│   ├── agent/
│   │   ├── __init__.py
│   │   └── todo_agent.py     # OpenAI Agents SDK agent definition
│   ├── db.py                 # Database connection (Neon)
│   ├── config.py             # Environment configuration
│   └── main.py               # FastAPI app entry point
├── tests/
│   ├── contract/
│   │   └── test_chat_api.py
│   ├── integration/
│   │   ├── test_chat_flow.py
│   │   └── test_mcp_tools.py
│   └── unit/
│       ├── test_task_service.py
│       └── test_conversation_service.py
├── requirements.txt
├── pyproject.toml
└── CLAUDE.md                 # Backend-specific Claude instructions

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Landing/redirect
│   │   ├── chat/
│   │   │   └── page.tsx      # Chat interface page (FR-001 to FR-006)
│   │   └── api/
│   │       └── auth/         # Better Auth routes
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatContainer.tsx    # Main chat wrapper (FR-001)
│   │   │   ├── MessageList.tsx      # Message history display (FR-002)
│   │   │   ├── MessageBubble.tsx    # Individual message (FR-024)
│   │   │   ├── ChatInput.tsx        # Input field + send (FR-005, FR-006)
│   │   │   └── TypingIndicator.tsx  # Loading state (FR-003)
│   │   └── ui/
│   │       └── Button.tsx
│   ├── lib/
│   │   ├── api.ts            # API client for backend
│   │   ├── auth.ts           # Better Auth client setup
│   │   └── hooks/
│   │       └── useChat.ts    # Chat state management
│   └── styles/
│       └── globals.css       # Tailwind + custom styles (FR-023 to FR-026)
├── tests/
│   └── components/
│       └── ChatInput.test.tsx
├── package.json
├── tailwind.config.js
├── next.config.js
└── CLAUDE.md                 # Frontend-specific Claude instructions

# Root level
├── CLAUDE.md                 # Root Claude instructions (references AGENTS.md)
├── docker-compose.yml        # Local development setup
├── .env.example              # Environment template
└── README.md                 # Project documentation
```

**Structure Decision**: Web application monorepo with `/frontend` (Next.js + ChatKit) and `/backend` (FastAPI + MCP). This follows Constitution Principle VI and hackathon requirements for Phase 3.

## Complexity Tracking

> No constitution violations detected. Standard web application architecture.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| MCP Integration | In-process MCP server | Simplest approach for single-service deployment |
| Agent Framework | OpenAI Agents SDK | Mandated by hackathon requirements |
| State Management | Database-only | Enforced by Constitution Principle II |

## Requirements Coverage Matrix

| Requirement | Implementation Component | User Story |
|-------------|-------------------------|------------|
| FR-001 | ChatContainer.tsx | US6 |
| FR-002 | MessageList.tsx, MessageBubble.tsx | US6 |
| FR-003 | TypingIndicator.tsx | US6 |
| FR-004 | Tailwind responsive classes | US6 |
| FR-005 | ChatInput.tsx | US6 |
| FR-006 | ChatInput.tsx (onKeyDown) | US6 |
| FR-007 | todo_agent.py + MCP tools | US1, US2 |
| FR-008 | todo_agent.py (system prompt) | US1-US5 |
| FR-009 | todo_agent.py (fallback handling) | Edge cases |
| FR-010 | todo_agent.py (intent mapping) | US1 |
| FR-011 | add_task.py MCP tool | US1 |
| FR-012 | list_tasks.py MCP tool | US2 |
| FR-013 | complete_task.py MCP tool | US3 |
| FR-014 | delete_task.py MCP tool | US4 |
| FR-015 | update_task.py MCP tool | US5 |
| FR-016 | conversation_service.py, Message model | US7 |
| FR-017 | chat_service.py (history fetch) | US7 |
| FR-018 | chat_service.py (auto-create) | US7 |
| FR-019 | todo_agent.py (context building) | US7 |
| FR-020 | auth.py middleware | Security |
| FR-021 | All MCP tools (user_id filter) | Security |
| FR-022 | deps.py (JWT validation) | Security |
| FR-023 | globals.css, Tailwind config | US6 |
| FR-024 | MessageBubble.tsx variants | US6 |
| FR-025 | Button.tsx, ChatInput.tsx states | US6 |
| FR-026 | Tailwind config (contrast) | US6 |
