"""
SQLModel database models for Phase 3 Todo Chatbot.

Exports all models for easy importing:
    from src.models import Task, Conversation, Message
"""

from .conversation import (
    Conversation,
    ConversationBase,
    ConversationCreate,
    ConversationRead,
)
from .message import Message, MessageBase, MessageCreate, MessageRead, MessageRole
from .task import Task, TaskBase, TaskCreate, TaskRead, TaskUpdate

__all__ = [
    # Task models
    "Task",
    "TaskBase",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    # Conversation models
    "Conversation",
    "ConversationBase",
    "ConversationCreate",
    "ConversationRead",
    # Message models
    "Message",
    "MessageBase",
    "MessageCreate",
    "MessageRead",
    "MessageRole",
]
