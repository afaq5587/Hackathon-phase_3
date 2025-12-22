"""
Conversation SQLModel for Phase 3 Todo Chatbot.

Per data-model.md: Represents a chat session for a user.
NEW for Phase 3 - Chat session management.
Supports FR-016 to FR-019.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ConversationBase(SQLModel):
    """Base conversation fields."""

    pass


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""

    pass


class Conversation(ConversationBase, table=True):
    """
    Conversation database model.

    Indexes:
    - idx_conversations_user_id on (user_id) - List user's conversations
    - idx_conversations_user_updated on (user_id, updated_at DESC) - Get most recent
    """

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="Owner of the conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationRead(ConversationBase):
    """Schema for reading a conversation (API response)."""

    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
