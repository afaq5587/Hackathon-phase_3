# Data Model: AI-Powered Todo Chatbot

**Feature**: 001-ai-chatbot-frontend
**Date**: 2025-12-20
**Database**: Neon Serverless PostgreSQL

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           users (Phase 2)                            │
│  Managed by Better Auth - not modified in Phase 3                   │
├─────────────────────────────────────────────────────────────────────┤
│  id (PK)          │ string    │ Unique user identifier              │
│  email            │ string    │ User email                          │
│  name             │ string    │ Display name                        │
│  created_at       │ timestamp │ Account creation time               │
└─────────────────────────────────────────────────────────────────────┘
           │
           │ 1:N
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                              tasks                                   │
│  Existing from Phase 2 - extended for Phase 3                       │
├─────────────────────────────────────────────────────────────────────┤
│  id (PK)          │ integer   │ Auto-increment task ID              │
│  user_id (FK)     │ string    │ References users.id                 │
│  title            │ string    │ Task title (1-200 chars, required)  │
│  description      │ text      │ Task description (optional)         │
│  completed        │ boolean   │ Completion status (default: false)  │
│  created_at       │ timestamp │ Task creation time                  │
│  updated_at       │ timestamp │ Last modification time              │
└─────────────────────────────────────────────────────────────────────┘
           │
           │ (same user)
           │
┌─────────────────────────────────────────────────────────────────────┐
│                          conversations                               │
│  NEW for Phase 3 - Chat session management                          │
├─────────────────────────────────────────────────────────────────────┤
│  id (PK)          │ integer   │ Auto-increment conversation ID      │
│  user_id (FK)     │ string    │ References users.id                 │
│  created_at       │ timestamp │ Conversation start time             │
│  updated_at       │ timestamp │ Last activity time                  │
└─────────────────────────────────────────────────────────────────────┘
           │
           │ 1:N
           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            messages                                  │
│  NEW for Phase 3 - Individual chat messages                         │
├─────────────────────────────────────────────────────────────────────┤
│  id (PK)          │ integer   │ Auto-increment message ID           │
│  conversation_id  │ integer   │ References conversations.id (FK)    │
│  user_id (FK)     │ string    │ References users.id (denormalized)  │
│  role             │ enum      │ 'user' | 'assistant'                │
│  content          │ text      │ Message text content                │
│  tool_calls       │ jsonb     │ MCP tools invoked (nullable)        │
│  created_at       │ timestamp │ Message timestamp                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Entity Definitions

### Task (existing, from Phase 2)

**Purpose**: Represents a todo item belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | integer | PK, auto-increment | Unique task identifier |
| user_id | string | FK → users.id, NOT NULL | Owner of the task |
| title | varchar(200) | NOT NULL | Task title (FR-011) |
| description | text | nullable | Optional task details |
| completed | boolean | NOT NULL, default false | Completion status (FR-013) |
| created_at | timestamp | NOT NULL, default now() | Creation timestamp |
| updated_at | timestamp | NOT NULL, default now() | Last update timestamp |

**Indexes**:
- `idx_tasks_user_id` on (user_id) - Filter tasks by user
- `idx_tasks_user_completed` on (user_id, completed) - Filter by status

**Validation Rules**:
- title: 1-200 characters, non-empty after trim
- description: max 1000 characters (optional)
- user_id: must exist in users table

### Conversation (new for Phase 3)

**Purpose**: Represents a chat session for a user. Supports FR-016 to FR-019.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | integer | PK, auto-increment | Unique conversation identifier |
| user_id | string | FK → users.id, NOT NULL | Owner of the conversation |
| created_at | timestamp | NOT NULL, default now() | Session start time |
| updated_at | timestamp | NOT NULL, default now() | Last activity time |

**Indexes**:
- `idx_conversations_user_id` on (user_id) - List user's conversations
- `idx_conversations_user_updated` on (user_id, updated_at DESC) - Get most recent

**Validation Rules**:
- user_id: must exist in users table
- updated_at: must be >= created_at

### Message (new for Phase 3)

**Purpose**: Represents a single message in a conversation. Supports FR-016 to FR-019.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | integer | PK, auto-increment | Unique message identifier |
| conversation_id | integer | FK → conversations.id, NOT NULL | Parent conversation |
| user_id | string | FK → users.id, NOT NULL | For user isolation queries |
| role | varchar(20) | NOT NULL, check in ('user', 'assistant') | Message sender type |
| content | text | NOT NULL | Message text content |
| tool_calls | jsonb | nullable | MCP tools invoked (for assistant messages) |
| created_at | timestamp | NOT NULL, default now() | Message timestamp |

**Indexes**:
- `idx_messages_conversation_id` on (conversation_id) - List conversation messages
- `idx_messages_conversation_created` on (conversation_id, created_at ASC) - Chronological order

**Validation Rules**:
- content: non-empty string
- role: must be 'user' or 'assistant'
- tool_calls format (when present):
  ```json
  [
    {
      "tool": "add_task",
      "arguments": {"user_id": "...", "title": "..."},
      "result": {"task_id": 1, "status": "created", "title": "..."}
    }
  ]
  ```

## SQLModel Definitions

### Task Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Conversation Model

```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Model

```python
from typing import List, Any

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    role: str = Field(max_length=20)  # 'user' | 'assistant'
    content: str
    tool_calls: Optional[List[dict]] = Field(default=None, sa_column_kwargs={"type_": "JSONB"})
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## State Transitions

### Task States

```
[created] ──complete_task──► [completed]
    │                            │
    │◄────────uncomplete────────┘
    │
    ▼
[deleted] (removed from database)
```

### Conversation States

```
[active] ───────────────► [inactive]
   │                          │
   │ (on new message)         │ (no activity for X time)
   │◄─────────────────────────┘
```

## Query Patterns

### Get User's Tasks (list_tasks MCP tool)

```sql
-- All tasks
SELECT * FROM tasks WHERE user_id = :user_id ORDER BY created_at DESC;

-- Pending tasks
SELECT * FROM tasks WHERE user_id = :user_id AND completed = false ORDER BY created_at DESC;

-- Completed tasks
SELECT * FROM tasks WHERE user_id = :user_id AND completed = true ORDER BY created_at DESC;
```

### Get Conversation History (for agent context)

```sql
SELECT m.role, m.content, m.tool_calls, m.created_at
FROM messages m
WHERE m.conversation_id = :conversation_id
ORDER BY m.created_at ASC;
```

### Get Most Recent Conversation (for returning users)

```sql
SELECT id FROM conversations
WHERE user_id = :user_id
ORDER BY updated_at DESC
LIMIT 1;
```

## User Isolation (Constitution Principle V)

All queries MUST include user_id filter to ensure data isolation:

| Entity | Isolation Method |
|--------|------------------|
| Task | WHERE user_id = :authenticated_user_id |
| Conversation | WHERE user_id = :authenticated_user_id |
| Message | JOIN conversations ON user_id = :authenticated_user_id |

**Security Note**: Even though messages have user_id denormalized, always verify through conversation ownership for defense in depth.
