# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot-frontend
**Date**: 2025-12-20

## Prerequisites

Before starting, ensure you have:

- [ ] Phase 2 codebase with working authentication (Better Auth)
- [ ] Node.js 18+ installed
- [ ] Python 3.13+ installed
- [ ] UV package manager installed
- [ ] Neon PostgreSQL database (from Phase 2)
- [ ] OpenAI API key

## Environment Setup

### 1. Clone and Navigate

```bash
cd phase_3
```

### 2. Create Environment File

Create `.env` in the project root:

```env
# Database (from Phase 2)
DATABASE_URL=postgresql://user:password@your-neon-host/dbname?sslmode=require

# Authentication (from Phase 2)
BETTER_AUTH_SECRET=your-shared-secret-key

# OpenAI (new for Phase 3)
OPENAI_API_KEY=sk-your-openai-api-key

# ChatKit (for production deployment)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

### 3. Install Backend Dependencies

```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Database Migration

Run migrations to add Phase 3 tables (conversations, messages):

```bash
cd backend
python -m alembic upgrade head
```

Or manually create tables:

```sql
-- conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    user_id VARCHAR NOT NULL REFERENCES users(id),
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);
```

## Running Locally

### Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Expected output:
```
▲ Next.js 16.x
- Local:        http://localhost:3000
- Ready in 2.1s
```

## Verification Checklist

### Backend Verification

1. **Health Check**
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status": "ok"}
   ```

2. **API Docs**
   - Open http://localhost:8000/docs
   - Should show Swagger UI with `/api/{user_id}/chat` endpoint

3. **MCP Tools Loaded**
   - Check server logs for:
     ```
     INFO: Registered MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
     ```

### Frontend Verification

1. **Landing Page**
   - Open http://localhost:3000
   - Should redirect to login if not authenticated

2. **Chat Interface**
   - After login, navigate to /chat
   - Should see:
     - Message input at bottom
     - Send button
     - Empty conversation area

3. **Authentication Flow**
   - Login with Phase 2 credentials
   - Should receive JWT and access chat

### End-to-End Test

1. Log in to the application
2. Navigate to chat interface
3. Type: "Add a task to test the chatbot"
4. Expected:
   - Loading indicator appears
   - AI responds: "I've added 'test the chatbot' to your task list!"
   - Task appears in database
5. Type: "Show me my tasks"
6. Expected:
   - AI lists the task you just created

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check BETTER_AUTH_SECRET matches frontend/backend |
| OpenAI API Error | Verify OPENAI_API_KEY is valid and has credits |
| Database Connection | Check DATABASE_URL and Neon dashboard |
| CORS Errors | Ensure backend allows frontend origin |
| Chat not responding | Check backend logs for agent/MCP errors |

### Debug Mode

Enable verbose logging:

```bash
# Backend
LOG_LEVEL=DEBUG uvicorn src.main:app --reload

# Frontend
DEBUG=* npm run dev
```

### Check Database State

```sql
-- View recent conversations
SELECT * FROM conversations ORDER BY created_at DESC LIMIT 5;

-- View recent messages
SELECT m.*, c.user_id
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
ORDER BY m.created_at DESC LIMIT 10;

-- View tasks
SELECT * FROM tasks ORDER BY created_at DESC LIMIT 5;
```

## Success Criteria Validation

| Criteria | How to Test |
|----------|-------------|
| SC-001: Task creation <10s | Time from send to confirmation |
| SC-002: Task list <3s | Time to display after "show tasks" |
| SC-003: 90% intent recognition | Test 10 varied commands |
| SC-004: Interface load <2s | Browser DevTools Network tab |
| SC-005: Conversation persists | Refresh page, check history |
| SC-006: Responsive 320-1920px | Chrome DevTools device mode |

## Next Steps

After successful setup:

1. Run `/sp.tasks` to generate implementation tasks
2. Start with P1 user stories (task creation, listing)
3. Test each feature against acceptance scenarios
4. Deploy to Vercel (frontend) once local tests pass

## References

- [Spec](./spec.md) - Feature specification
- [Plan](./plan.md) - Implementation plan
- [Data Model](./data-model.md) - Database schema
- [API Contract](./contracts/chat-api.yaml) - OpenAPI spec
- [MCP Tools](./contracts/mcp-tools.md) - Tool schemas
