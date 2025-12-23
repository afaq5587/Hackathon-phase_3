---
description: Create SQLModel database model with proper fields, validation, and relationships
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse model requirements** from user input:
   - Model name (entity name)
   - Table name
   - Fields with types and constraints
   - Relationships to other models
   - Indexes needed for performance
   - Validation rules

2. **Verify project structure**:
   - Check `backend/src/models/` directory exists
   - Review data model specification in `specs/*/data-model.md` (if exists)
   - Check existing models for patterns
   - Verify database configuration in `backend/src/db.py`

3. **Create model file**:
   - File location: `backend/src/models/{entity}.py`
   - Use snake_case for filename
   - One primary model per file
   - Include related schemas (Create, Update, Read)

4. **Implement SQLModel structure**:
   ```python
   """
   {Entity} SQLModel for {project}.

   Per data-model.md: {brief description}
   """

   from datetime import datetime
   from typing import Optional

   from sqlmodel import Field, SQLModel


   class {Entity}Base(SQLModel):
       """Base {entity} fields for create/update operations."""

       field1: str = Field(
           max_length=200,
           description="Field description"
       )
       field2: Optional[str] = Field(
           default=None,
           max_length=1000,
           description="Optional field"
       )


   class {Entity}Create({Entity}Base):
       """Schema for creating a new {entity}."""
       pass


   class {Entity}Update(SQLModel):
       """Schema for updating an existing {entity}."""

       field1: Optional[str] = Field(default=None, max_length=200)
       field2: Optional[str] = Field(default=None, max_length=1000)


   class {Entity}(BaseEntity}, table=True):
       """
       {Entity} database model.

       Indexes:
       - idx_{table}_{field} on (field) - {purpose}
       """

       __tablename__ = "{table_name}"

       id: Optional[int] = Field(default=None, primary_key=True)
       user_id: str = Field(index=True, description="Owner user ID")
       created_at: datetime = Field(default_factory=datetime.utcnow)
       updated_at: datetime = Field(default_factory=datetime.utcnow)


   class {Entity}Read({Entity}Base):
       """Schema for reading {entity} (API response)."""

       id: int
       user_id: str
       created_at: datetime
       updated_at: datetime
   ```

5. **Define model fields with proper types**:
   - **Primary Key**: `id: Optional[int] = Field(default=None, primary_key=True)`
   - **String**: `name: str = Field(max_length=200)`
   - **Optional String**: `description: Optional[str] = Field(default=None)`
   - **Boolean**: `completed: bool = Field(default=False)`
   - **Integer**: `count: int = Field(default=0, ge=0)`
   - **Float**: `price: float = Field(ge=0.0)`
   - **DateTime**: `created_at: datetime = Field(default_factory=datetime.utcnow)`
   - **Enum**: Use Python Enum with `sa_column=Column(Enum(...))`
   - **JSON**: `metadata: dict = Field(default_factory=dict, sa_column=Column(JSON))`

6. **Add field validation and constraints**:
   - Use `max_length` for string length limits
   - Use `ge` (>=) and `le` (<=) for numeric ranges
   - Use `regex` for pattern validation
   - Add `description` for documentation
   - Set `nullable=False` for required fields
   - Set `unique=True` for unique constraints
   - Use `index=True` for frequently queried fields

7. **Add user isolation field**:
   - **CRITICAL**: Always include `user_id: str = Field(index=True)`
   - Index user_id for performance
   - Never allow direct user_id modification via API
   - Use in all queries to enforce data isolation

8. **Add timestamp fields**:
   - `created_at: datetime = Field(default_factory=datetime.utcnow)`
   - `updated_at: datetime = Field(default_factory=datetime.utcnow)`
   - Update `updated_at` in service layer on modifications
   - Use UTC timezone (utcnow)

9. **Define relationships** (if needed):
   ```python
   from sqlmodel import Relationship

   class Task(SQLModel, table=True):
       # Fields...
       tags: List["Tag"] = Relationship(back_populates="task")

   class Tag(SQLModel, table=True):
       # Fields...
       task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")
       task: Optional[Task] = Relationship(back_populates="tags")
   ```

10. **Add indexes for performance**:
    - Document indexes in model docstring
    - Index foreign keys automatically
    - Add composite indexes for common queries:
      ```python
      __table_args__ = (
          Index('idx_tasks_user_completed', 'user_id', 'completed'),
      )
      ```

11. **Create Pydantic schemas**:
    - **{Entity}Base**: Shared fields for create/read
    - **{Entity}Create**: Fields for creating (no id, timestamps)
    - **{Entity}Update**: All fields optional for partial updates
    - **{Entity}**: Full database model with table=True
    - **{Entity}Read**: Fields returned in API responses

12. **Register model** in `backend/src/models/__init__.py`:
    ```python
    from .{entity} import {Entity}, {Entity}Create, {Entity}Update, {Entity}Read

    __all__ = [
        "{Entity}",
        "{Entity}Create",
        "{Entity}Update",
        "{Entity}Read",
        # ... other models
    ]
    ```

13. **Testing checklist**:
    - [ ] Model has primary key (id)
    - [ ] Model has user_id for isolation
    - [ ] Model has timestamps (created_at, updated_at)
    - [ ] Required fields marked properly
    - [ ] String fields have max_length
    - [ ] Numeric fields have validation (ge, le)
    - [ ] Indexes defined for performance
    - [ ] Relationships configured correctly
    - [ ] All schemas created (Base, Create, Update, Read)
    - [ ] Model registered in __init__.py
    - [ ] Docstring describes purpose and indexes

## Example Model Implementations

### Simple Entity (Task)
```python
"""
Task SQLModel for Todo Chatbot.

Represents a todo item belonging to a user.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base task fields."""

    title: str = Field(
        max_length=200,
        description="Task title (1-200 chars, required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional)"
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class Task(TaskBase, table=True):
    """
    Task database model.

    Indexes:
    - idx_tasks_user_id on (user_id)
    - idx_tasks_user_completed on (user_id, completed)
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="Owner of the task")
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRead(TaskBase):
    """Schema for reading a task (API response)."""

    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### Entity with Relationships (Conversation & Message)
```python
"""
Conversation and Message models for chat history.
"""

from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


# Conversation Model
class ConversationBase(SQLModel):
    """Base conversation fields."""
    pass  # Conversations have no user-editable fields


class ConversationCreate(ConversationBase):
    """Schema for creating conversation."""
    pass


class Conversation(ConversationBase, table=True):
    """
    Conversation database model.

    Indexes:
    - idx_conversations_user_id on (user_id)
    - idx_conversations_updated on (user_id, updated_at DESC)
    """

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="Owner user ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    """Schema for reading conversation."""

    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


# Message Model
class MessageBase(SQLModel):
    """Base message fields."""

    role: str = Field(
        max_length=20,
        description="Message role: 'user' or 'assistant'"
    )
    content: str = Field(
        min_length=1,
        description="Message content"
    )


class MessageCreate(MessageBase):
    """Schema for creating message."""
    pass


class Message(MessageBase, table=True):
    """
    Message database model.

    Indexes:
    - idx_messages_conversation on (conversation_id, created_at)
    """

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    """Schema for reading message."""

    id: int
    conversation_id: int
    created_at: datetime
```

### Entity with Enum and Validation
```python
"""
Task model with priority and due date.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import Field, SQLModel


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(SQLModel):
    """Base task fields."""

    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)


class TaskCreate(TaskBase):
    """Schema for creating task."""
    pass


class TaskUpdate(SQLModel):
    """Schema for updating task."""

    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class Task(TaskBase, table=True):
    """
    Task database model with priority and due date.

    Indexes:
    - idx_tasks_user_priority on (user_id, priority)
    - idx_tasks_due_date on (user_id, due_date) WHERE completed = FALSE
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Override priority with SQL Enum column
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        sa_column=Column(SQLEnum(TaskPriority))
    )


class TaskRead(TaskBase):
    """Schema for reading task."""

    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

## Example Usage

```bash
# Create a simple model
/backend.model Create Task model with title, description, completed, user_id

# Create model with relationships
/backend.model Create Tag model with name, color, and relationship to Tasks

# Create model with enum
/backend.model Create Task model with priority enum (low, medium, high, urgent)
```

## Best Practices

- Always include `user_id` for data isolation
- Always include timestamps (`created_at`, `updated_at`)
- Use `Optional[int]` for primary key id
- Set `max_length` on all string fields
- Use `default` or `default_factory` for optional fields
- Index frequently queried fields
- Create separate schemas for Create, Update, and Read
- Document indexes in model docstring
- Use descriptive field descriptions
- Validate constraints at database level
- Use UTC for all timestamps
- Follow naming conventions (PascalCase for classes, snake_case for tables)

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (model implementation work)
2) Generate Title: 3–7 words describing the model created
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
