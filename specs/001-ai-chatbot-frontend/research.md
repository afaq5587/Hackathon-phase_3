# Research: AI-Powered Todo Chatbot with Beautiful Frontend

**Feature**: 001-ai-chatbot-frontend
**Date**: 2025-12-20
**Status**: Complete

## Overview

This document captures research findings and architectural decisions for the Phase 3 AI-Powered Todo Chatbot implementation.

---

## 1. OpenAI Agents SDK Integration

### Decision
Use OpenAI Agents SDK with function calling to orchestrate the AI chatbot. The agent receives natural language input, determines intent, and invokes MCP tools.

### Rationale
- Mandated by hackathon Phase 3 requirements
- Provides built-in function calling for tool invocation
- Handles conversation context management
- Supports streaming responses for better UX

### Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| LangChain | Not specified in hackathon requirements |
| Raw OpenAI API | Lacks agent orchestration features |
| Anthropic Claude API | Hackathon requires OpenAI stack |

### Implementation Notes
```python
# Agent setup pattern
from openai import OpenAI
from agents import Agent, Runner

agent = Agent(
    name="todo_assistant",
    instructions="You are a helpful todo list assistant...",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)
```

---

## 2. MCP Server Architecture

### Decision
Implement MCP server in-process within the FastAPI application using the Official MCP SDK (Python). Tools are registered and invoked through the Agents SDK integration.

### Rationale
- Simplest deployment model for Phase 3
- Constitution Principle III mandates MCP tools
- In-process reduces latency vs separate MCP server
- Official MCP SDK provides standardized tool schemas

### Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| Separate MCP server process | Added complexity for Phase 3 scope |
| Custom tool implementation | Doesn't follow MCP standard |
| REST-only tools | Constitution requires MCP protocol |

### Tool Schema Pattern
Each MCP tool follows this interface per Constitution:
```python
@mcp_tool
async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Create a new task for the user."""
    # Returns: {"task_id": int, "status": "created", "title": str}
```

---

## 3. Stateless Chat Architecture

### Decision
Implement fully stateless chat endpoint. All conversation state persists to Neon PostgreSQL. Each request reconstructs context from database.

### Rationale
- Constitution Principle II mandates statelessness
- Enables horizontal scaling for Phase 4/5
- Server restarts don't lose conversation state
- Any backend instance can handle any request

### Conversation Flow (7 Steps per Constitution IV)
1. Receive user message via POST /api/{user_id}/chat
2. Fetch conversation history from database
3. Build message array for agent (system prompt + history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Store assistant response in database
7. Return response to client

### State Storage
| Data | Storage | Retrieval |
|------|---------|-----------|
| Conversation metadata | conversations table | By user_id + conversation_id |
| Message history | messages table | By conversation_id, ordered by created_at |
| Task data | tasks table | By user_id |

---

## 4. OpenAI ChatKit Frontend

### Decision
Use OpenAI ChatKit for the chat UI, customized with Tailwind CSS for visual polish.

### Rationale
- Specified in hackathon requirements
- Provides ready-made chat components
- Handles message rendering, input, typing indicators
- Can be styled with Tailwind for "beautiful" requirement

### Integration Pattern
```tsx
// ChatKit integration with custom styling
import { Chat } from '@openai/chatkit';

export function ChatInterface({ userId }) {
  return (
    <Chat
      endpoint={`/api/${userId}/chat`}
      className="custom-chat-container"
    />
  );
}
```

### Customization Areas
- Message bubble styling (FR-024)
- Loading/typing indicator (FR-003)
- Responsive layout (FR-004)
- Color scheme and contrast (FR-026)

---

## 5. JWT Authentication Flow

### Decision
Reuse Better Auth JWT setup from Phase 2. Backend validates JWT on every request. User ID extracted from token and matched against URL parameter.

### Rationale
- Constitution Principle V requires authentication continuity
- Phase 2 already has Better Auth infrastructure
- JWT enables stateless auth verification
- Shared secret between frontend and backend

### Validation Flow
```python
# Backend JWT validation
async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
    return payload["user_id"]

# URL parameter match
@router.post("/api/{user_id}/chat")
async def chat(user_id: str, current_user: str = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(403, "Forbidden")
```

---

## 6. Database Schema Design

### Decision
Three tables: tasks (existing from Phase 2), conversations (new), messages (new). All include user_id for isolation.

### Rationale
- Separates concerns: tasks vs chat state
- Enables conversation history reconstruction
- Supports multiple conversations per user
- User isolation built into schema

### Schema Overview
```sql
-- Existing from Phase 2
tasks (id, user_id, title, description, completed, created_at, updated_at)

-- New for Phase 3
conversations (id, user_id, created_at, updated_at)
messages (id, conversation_id, user_id, role, content, created_at)
```

---

## 7. Error Handling Strategy

### Decision
Implement graceful error handling with user-friendly messages. Agent fallback for unrecognized intents.

### Rationale
- FR-009 requires graceful handling of ambiguous requests
- Edge cases in spec define expected error responses
- SC-009 requires user-friendly error messages

### Error Categories
| Error Type | Response |
|------------|----------|
| Task not found | "I couldn't find task {id}. Want me to show your current tasks?" |
| Unclear intent | "I'm not sure what you'd like me to do. You can ask me to add, list, complete, delete, or update tasks." |
| Auth failure | HTTP 401/403 with generic message |
| AI service unavailable | "I'm having trouble connecting right now. Please try again in a moment." |
| Empty message | "Please type a message to continue." |

---

## 8. Performance Considerations

### Decision
Optimize for success criteria timing requirements through caching, efficient queries, and streaming.

### Targets (from Success Criteria)
| Metric | Target | Approach |
|--------|--------|----------|
| Interface load | <2s | Code splitting, lazy loading |
| Task operation | <10s | Direct DB queries, no N+1 |
| Task list retrieval | <3s | Indexed queries by user_id |
| Feedback display | <1s | Optimistic UI updates |

### Query Optimization
- Index on messages(conversation_id, created_at)
- Index on tasks(user_id, completed)
- Index on conversations(user_id, updated_at)

---

## Summary

All technical decisions align with:
- Constitution principles (I-VI)
- Hackathon Phase 3 requirements
- Feature specification (26 functional requirements)
- Success criteria (10 measurable outcomes)

No unresolved clarifications remain. Ready for Phase 1 design artifacts.
