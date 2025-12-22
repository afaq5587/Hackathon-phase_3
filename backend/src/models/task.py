"""
Task SQLModel for Phase 3 Todo Chatbot.

Per data-model.md: Represents a todo item belonging to a user.
Existing from Phase 2, extended for Phase 3.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base task fields shared between create/update/read operations."""

    title: str = Field(max_length=200, description="Task title (1-200 chars, required)")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Task description (optional)"
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
    - idx_tasks_user_id on (user_id) - Filter tasks by user
    - idx_tasks_user_completed on (user_id, completed) - Filter by status
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
