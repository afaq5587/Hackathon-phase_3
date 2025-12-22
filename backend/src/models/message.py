"""
Message SQLModel for Phase 3 Todo Chatbot.

Per data-model.md: Represents a single message in a conversation.
NEW for Phase 3 - Individual chat messages.
Supports FR-016 to FR-019.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class MessageRole(str, Enum):
    """Message sender type."""

    USER = "user"
    ASSISTANT = "assistant"


class MessageBase(SQLModel):
    """Base message fields."""

    role: str = Field(max_length=20, description="'user' | 'assistant'")
    content: str = Field(description="Message text content")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""

    tool_calls: Optional[list[dict[str, Any]]] = None


class Message(MessageBase, table=True):
    """
    Message database model.

    Indexes:
    - idx_messages_conversation_id on (conversation_id) - List conversation messages
    - idx_messages_conversation_created on (conversation_id, created_at ASC) - Chronological order

    tool_calls format (when present):
    [
        {
            "tool": "add_task",
            "arguments": {"user_id": "...", "title": "..."},
            "result": {"task_id": 1, "status": "created", "title": "..."}
        }
    ]
    """

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(index=True, description="Parent conversation")
    user_id: str = Field(index=True, description="For user isolation queries")
    tool_calls: Optional[list[dict[str, Any]]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="MCP tools invoked (for assistant messages)",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRead(MessageBase):
    """Schema for reading a message (API response)."""

    id: int
    conversation_id: int
    user_id: str
    tool_calls: Optional[list[dict[str, Any]]] = None
    created_at: datetime
