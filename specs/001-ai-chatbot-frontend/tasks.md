# Tasks: AI-Powered Todo Chatbot with Beautiful Frontend

**Input**: Design documents from `/specs/001-ai-chatbot-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend: Python FastAPI
- Frontend: Next.js TypeScript

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

- [ ] T001 Create monorepo directory structure with backend/ and frontend/ directories per plan.md
- [ ] T002 [P] Initialize Python backend with UV and create pyproject.toml in backend/
- [ ] T003 [P] Initialize Next.js 16+ frontend with TypeScript in frontend/
- [ ] T004 [P] Create .env.example with DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- [ ] T005 [P] Create backend/CLAUDE.md with backend-specific development guidelines
- [ ] T006 [P] Create frontend/CLAUDE.md with frontend-specific development guidelines
- [ ] T007 [P] Create docker-compose.yml for local development environment
- [ ] T008 [P] Install backend dependencies: fastapi, uvicorn, sqlmodel, openai, mcp, python-jose in backend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Models

- [ ] T009 Create database connection module in backend/src/db.py with Neon PostgreSQL async support
- [ ] T010 Create environment configuration in backend/src/config.py (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY)
- [ ] T011 [P] Create Task SQLModel in backend/src/models/task.py per data-model.md
- [ ] T012 [P] Create Conversation SQLModel in backend/src/models/conversation.py per data-model.md
- [ ] T013 [P] Create Message SQLModel in backend/src/models/message.py per data-model.md
- [ ] T014 Create models __init__.py exporting all models in backend/src/models/__init__.py
- [ ] T015 Create database migration script for conversations and messages tables in backend/migrations/

### Authentication & Security

- [ ] T016 Implement JWT validation middleware in backend/src/api/auth.py (verify BETTER_AUTH_SECRET)
- [ ] T017 Create dependency injection for authenticated user in backend/src/api/deps.py
- [ ] T018 Implement user_id path parameter validation (must match JWT user) in backend/src/api/deps.py

### Core Services

- [ ] T019 Create TaskService with CRUD operations in backend/src/services/task_service.py
- [ ] T020 Create ConversationService in backend/src/services/conversation_service.py
- [ ] T021 Create services __init__.py exporting all services in backend/src/services/__init__.py

### FastAPI App Setup

- [ ] T022 Create FastAPI application entry point in backend/src/main.py with CORS, routers
- [ ] T023 Create API router structure in backend/src/api/__init__.py

### Frontend Foundation

- [ ] T024 [P] Configure Tailwind CSS with custom theme in frontend/tailwind.config.js
- [ ] T025 [P] Create global styles with WCAG AA contrast colors in frontend/src/styles/globals.css
- [ ] T026 [P] Setup Better Auth client in frontend/src/lib/auth.ts
- [ ] T027 [P] Create API client with JWT header injection in frontend/src/lib/api.ts
- [ ] T028 Create root layout with authentication check in frontend/src/app/layout.tsx
- [ ] T029 Create landing page with auth redirect in frontend/src/app/page.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by typing natural language messages to the chatbot

**Independent Test**: Send "Add a task to buy groceries" and verify task appears in database with correct title

**FR Coverage**: FR-007, FR-008, FR-010, FR-011

### MCP Tools for US1

- [ ] T030 [P] [US1] Create MCP server setup in backend/src/mcp/server.py
- [ ] T031 [P] [US1] Create add_task MCP tool in backend/src/mcp/tools/add_task.py per mcp-tools.md schema
- [ ] T032 [US1] Create MCP tools __init__.py registering add_task in backend/src/mcp/tools/__init__.py

### Agent for US1

- [ ] T033 [US1] Create todo_agent with system prompt for task creation intent in backend/src/agent/todo_agent.py
- [ ] T034 [US1] Implement agent response generation with friendly confirmations in backend/src/agent/todo_agent.py

### Chat Service for US1

- [ ] T035 [US1] Create ChatService with message storage in backend/src/services/chat_service.py
- [ ] T036 [US1] Implement 7-step conversation flow (receive, fetch history, build context, store user msg, run agent, store response, return) in backend/src/services/chat_service.py

### Chat API Endpoint

- [ ] T037 [US1] Create POST /api/{user_id}/chat endpoint in backend/src/api/chat.py per chat-api.yaml
- [ ] T038 [US1] Implement request validation (non-empty message) in backend/src/api/chat.py
- [ ] T039 [US1] Implement conversation auto-creation for new sessions in backend/src/api/chat.py

### Frontend Chat Interface (Basic)

- [ ] T040 [P] [US1] Create ChatInput component with text field and send button in frontend/src/components/chat/ChatInput.tsx
- [ ] T041 [P] [US1] Create MessageBubble component with user/assistant styling in frontend/src/components/chat/MessageBubble.tsx
- [ ] T042 [US1] Create MessageList component displaying conversation in frontend/src/components/chat/MessageList.tsx
- [ ] T043 [US1] Create ChatContainer orchestrating chat flow in frontend/src/components/chat/ChatContainer.tsx
- [ ] T044 [US1] Create useChat hook for state management in frontend/src/lib/hooks/useChat.ts
- [ ] T045 [US1] Create chat page integrating ChatContainer in frontend/src/app/chat/page.tsx

**Checkpoint**: User Story 1 complete - users can create tasks via natural language

---

## Phase 4: User Story 2 - View and List Tasks via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can ask to see their tasks and get filtered lists (all/pending/completed)

**Independent Test**: Ask "Show me all my tasks" and verify correct task list displays

**FR Coverage**: FR-007, FR-008, FR-012

### MCP Tools for US2

- [ ] T046 [US2] Create list_tasks MCP tool with status filter in backend/src/mcp/tools/list_tasks.py per mcp-tools.md schema
- [ ] T047 [US2] Register list_tasks tool in backend/src/mcp/tools/__init__.py
- [ ] T048 [US2] Update todo_agent to handle list intents ("show", "what's pending") in backend/src/agent/todo_agent.py

### Agent Response Formatting

- [ ] T049 [US2] Implement task list formatting in agent responses (numbered list with status) in backend/src/agent/todo_agent.py

**Checkpoint**: User Stories 1 AND 2 complete - users can create and view tasks via chat

---

## Phase 5: User Story 3 - Mark Tasks Complete via Chat (Priority: P2)

**Goal**: Users can mark tasks as complete by ID or name via conversation

**Independent Test**: Create a task, then say "Mark task 1 as complete" and verify status changes

**FR Coverage**: FR-007, FR-008, FR-013

### MCP Tools for US3

- [ ] T050 [US3] Create complete_task MCP tool in backend/src/mcp/tools/complete_task.py per mcp-tools.md schema
- [ ] T051 [US3] Register complete_task tool in backend/src/mcp/tools/__init__.py
- [ ] T052 [US3] Update todo_agent to handle complete intents ("mark complete", "done", "finished") in backend/src/agent/todo_agent.py

### Error Handling for US3

- [ ] T053 [US3] Implement "task not found" friendly error with offer to show tasks in backend/src/mcp/tools/complete_task.py

**Checkpoint**: User Story 3 complete - users can mark tasks complete via chat

---

## Phase 6: User Story 4 - Delete Tasks via Chat (Priority: P2)

**Goal**: Users can delete tasks by ID or name via conversation

**Independent Test**: Create a task, then say "Delete task 1" and verify task is removed

**FR Coverage**: FR-007, FR-008, FR-014

### MCP Tools for US4

- [ ] T054 [US4] Create delete_task MCP tool in backend/src/mcp/tools/delete_task.py per mcp-tools.md schema
- [ ] T055 [US4] Register delete_task tool in backend/src/mcp/tools/__init__.py
- [ ] T056 [US4] Update todo_agent to handle delete intents ("delete", "remove", "cancel") in backend/src/agent/todo_agent.py

### Error Handling for US4

- [ ] T057 [US4] Implement "task not found" friendly error in backend/src/mcp/tools/delete_task.py

**Checkpoint**: User Story 4 complete - users can delete tasks via chat

---

## Phase 7: User Story 5 - Update Tasks via Chat (Priority: P2)

**Goal**: Users can modify task titles or descriptions via conversation

**Independent Test**: Create a task, then say "Change task 1 to 'Buy fruits'" and verify title updates

**FR Coverage**: FR-007, FR-008, FR-015

### MCP Tools for US5

- [ ] T058 [US5] Create update_task MCP tool in backend/src/mcp/tools/update_task.py per mcp-tools.md schema
- [ ] T059 [US5] Register update_task tool in backend/src/mcp/tools/__init__.py
- [ ] T060 [US5] Update todo_agent to handle update intents ("change", "update", "rename") in backend/src/agent/todo_agent.py

### Error Handling for US5

- [ ] T061 [US5] Implement validation for empty updates and "task not found" in backend/src/mcp/tools/update_task.py

**Checkpoint**: User Story 5 complete - users can update tasks via chat

---

## Phase 8: User Story 6 - Beautiful Chat Interface (Priority: P3)

**Goal**: Polished, modern UI with responsive design and visual feedback

**Independent Test**: Load chat interface, verify visual elements render correctly on mobile and desktop

**FR Coverage**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-023, FR-024, FR-025, FR-026

### Visual Components

- [ ] T062 [P] [US6] Create TypingIndicator component with animation in frontend/src/components/chat/TypingIndicator.tsx
- [ ] T063 [P] [US6] Create Button component with hover/focus states in frontend/src/components/ui/Button.tsx
- [ ] T064 [US6] Enhance MessageBubble with distinct user (right, blue) vs AI (left, gray) styling in frontend/src/components/chat/MessageBubble.tsx
- [ ] T065 [US6] Add Enter key submission handler to ChatInput in frontend/src/components/chat/ChatInput.tsx

### Responsive Design

- [ ] T066 [US6] Add responsive breakpoints (320px-1920px) to ChatContainer in frontend/src/components/chat/ChatContainer.tsx
- [ ] T067 [US6] Configure Tailwind responsive utilities for chat layout in frontend/tailwind.config.js

### Loading States

- [ ] T068 [US6] Integrate TypingIndicator display during API calls in frontend/src/components/chat/ChatContainer.tsx
- [ ] T069 [US6] Add optimistic UI updates for immediate feedback in frontend/src/lib/hooks/useChat.ts

### Accessibility

- [ ] T070 [US6] Ensure WCAG AA color contrast in all chat components in frontend/src/styles/globals.css
- [ ] T071 [US6] Add aria labels and keyboard navigation support in frontend/src/components/chat/ChatInput.tsx

**Checkpoint**: User Story 6 complete - chat interface is polished and responsive

---

## Phase 9: User Story 7 - Conversation Persistence (Priority: P3)

**Goal**: Chat history persists across page refreshes and browser sessions

**Independent Test**: Have a conversation, refresh the page, verify messages appear

**FR Coverage**: FR-016, FR-017, FR-018, FR-019

### Backend Persistence

- [ ] T072 [US7] Implement conversation history fetch on chat load in backend/src/services/conversation_service.py
- [ ] T073 [US7] Implement get most recent conversation for returning users in backend/src/services/conversation_service.py
- [ ] T074 [US7] Add GET /api/{user_id}/conversations endpoint in backend/src/api/chat.py
- [ ] T075 [US7] Add GET /api/{user_id}/conversations/{id}/messages endpoint in backend/src/api/chat.py

### Frontend Persistence

- [ ] T076 [US7] Load conversation history on chat page mount in frontend/src/lib/hooks/useChat.ts
- [ ] T077 [US7] Store conversation_id in session for continuity in frontend/src/lib/hooks/useChat.ts
- [ ] T078 [US7] Display historical messages on page load in frontend/src/components/chat/MessageList.tsx

**Checkpoint**: User Story 7 complete - conversations persist across sessions

---

## Phase 10: Edge Cases & Error Handling

**Purpose**: Handle all edge cases defined in spec

**FR Coverage**: FR-009

- [ ] T079 Implement empty message validation with "Please type a message" response in backend/src/api/chat.py
- [ ] T080 Implement unclear intent fallback in agent: "I'm not sure what you'd like me to do..." in backend/src/agent/todo_agent.py
- [ ] T081 Implement session expiry redirect with message in frontend/src/lib/auth.ts
- [ ] T082 Implement AI service unavailable error handling in backend/src/services/chat_service.py
- [ ] T083 Add error boundary for frontend chat errors in frontend/src/components/chat/ChatContainer.tsx

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting all user stories

- [ ] T084 [P] Update README.md with Phase 3 setup instructions
- [ ] T085 [P] Create backend API documentation in backend/docs/api.md
- [ ] T086 Run quickstart.md validation checklist
- [ ] T087 Verify all 26 functional requirements are implemented
- [ ] T088 Verify all 10 success criteria are met
- [ ] T089 Performance optimization: add database indexes per data-model.md
- [ ] T090 Security review: verify user isolation in all MCP tools and endpoints

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──────────────────────────────────────────────────────────┐
     │                                                                     │
     ▼                                                                     │
Phase 2 (Foundational) ◄── BLOCKS ALL USER STORIES                        │
     │                                                                     │
     ├──────────────────┬──────────────────┬──────────────────┐           │
     ▼                  ▼                  ▼                  ▼           │
Phase 3 (US1)     Phase 4 (US2)      [Can run in parallel after Phase 2]  │
  MVP Core          MVP Core                                              │
     │                  │                                                  │
     ├──────────────────┤                                                  │
     ▼                  ▼                                                  │
Phase 5 (US3)     Phase 6 (US4)     Phase 7 (US5)                         │
  Complete          Delete            Update                              │
     │                  │                │                                 │
     └──────────────────┴────────────────┴─────────────────────────────────┤
                                                                           │
Phase 8 (US6) ◄── Enhances existing UI from US1-US5                        │
  Beautiful UI                                                             │
     │                                                                     │
     ▼                                                                     │
Phase 9 (US7) ◄── Requires backend services from earlier phases            │
  Persistence                                                              │
     │                                                                     │
     ▼                                                                     │
Phase 10 (Edge Cases)                                                      │
     │                                                                     │
     ▼                                                                     │
Phase 11 (Polish) ◄── Final phase, depends on all stories complete         │
```

### User Story Dependencies

| User Story | Depends On | Can Start After |
|------------|------------|-----------------|
| US1 (Task Creation) | Phase 2 only | Phase 2 complete |
| US2 (List Tasks) | Phase 2 only | Phase 2 complete (parallel with US1) |
| US3 (Complete Task) | US1, US2 | Phase 4 complete |
| US4 (Delete Task) | US1, US2 | Phase 4 complete (parallel with US3) |
| US5 (Update Task) | US1, US2 | Phase 4 complete (parallel with US3, US4) |
| US6 (Beautiful UI) | US1 minimum | Phase 3 complete |
| US7 (Persistence) | US1 minimum | Phase 3 complete |

### Parallel Opportunities

```bash
# Phase 1 - All setup tasks can run in parallel:
T002, T003, T004, T005, T006, T007, T008

# Phase 2 - Models can run in parallel:
T011, T012, T013

# Phase 2 - Frontend foundation can run in parallel:
T024, T025, T026, T027

# Phase 3 (US1) - MCP tools can start in parallel:
T030, T031

# Phase 3 (US1) - Frontend components can run in parallel:
T040, T041

# Phase 8 (US6) - Visual components can run in parallel:
T062, T063

# Phase 11 - Documentation can run in parallel:
T084, T085
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Task Creation)
4. Complete Phase 4: User Story 2 (List Tasks)
5. **STOP and VALIDATE**: Test both stories independently
6. Deploy/demo MVP - users can create and view tasks via chat

### Incremental Delivery

1. MVP (US1 + US2) → Deploy → 200 points hackathon checkpoint
2. Add US3, US4, US5 → All CRUD via chat → Full functionality
3. Add US6 → Beautiful UI → Polish
4. Add US7 → Persistence → Complete Phase 3

### Task Count Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| Phase 1: Setup | 8 | 7 |
| Phase 2: Foundational | 21 | 8 |
| Phase 3: US1 (Create) | 16 | 4 |
| Phase 4: US2 (List) | 4 | 0 |
| Phase 5: US3 (Complete) | 4 | 0 |
| Phase 6: US4 (Delete) | 4 | 0 |
| Phase 7: US5 (Update) | 4 | 0 |
| Phase 8: US6 (UI) | 10 | 2 |
| Phase 9: US7 (Persist) | 7 | 0 |
| Phase 10: Edge Cases | 5 | 0 |
| Phase 11: Polish | 7 | 2 |
| **TOTAL** | **90** | **23** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All file paths are relative to repository root
- Backend paths: backend/src/...
- Frontend paths: frontend/src/...
