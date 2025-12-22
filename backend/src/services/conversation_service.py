"""
Conversation Service for Phase 3 Todo Chatbot.

Provides conversation and message management with user isolation.
Supports FR-016 to FR-019 for conversation persistence.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import (
    Conversation,
    ConversationCreate,
    Message,
    MessageCreate,
)


class ConversationService:
    """Service for conversation and message operations with user isolation."""

    def __init__(self, db: AsyncSession):
        """Initialize with database session."""
        self.db = db

    async def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for user.

        Args:
            user_id: Owner of the conversation

        Returns:
            Created conversation with ID
        """
        conversation = Conversation(user_id=user_id)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversation(
        self, user_id: str, conversation_id: int
    ) -> Optional[Conversation]:
        """
        Get conversation by ID with user isolation.

        Args:
            user_id: Owner to filter by
            conversation_id: Conversation ID to find

        Returns:
            Conversation if found and owned by user, None otherwise
        """
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_most_recent_conversation(
        self, user_id: str
    ) -> Optional[Conversation]:
        """
        Get most recent conversation for returning users.

        Per data-model.md query pattern:
        SELECT id FROM conversations WHERE user_id = :user_id
        ORDER BY updated_at DESC LIMIT 1;

        Args:
            user_id: Owner to filter by

        Returns:
            Most recent conversation or None
        """
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_conversations(
        self, user_id: str, limit: int = 10
    ) -> list[Conversation]:
        """
        List user's conversations.

        Args:
            user_id: Owner to filter by
            limit: Maximum conversations to return

        Returns:
            List of conversations ordered by most recent first
        """
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def add_message(
        self,
        user_id: str,
        conversation_id: int,
        role: str,
        content: str,
        tool_calls: Optional[list[dict[str, Any]]] = None,
    ) -> Message:
        """
        Add a message to conversation.

        Also updates conversation's updated_at timestamp.

        Args:
            user_id: Owner of the conversation
            conversation_id: Target conversation
            role: 'user' or 'assistant'
            content: Message text content
            tool_calls: Optional MCP tools invoked

        Returns:
            Created message with ID
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
        )
        self.db.add(message)

        # Update conversation timestamp
        conversation = await self.get_conversation(user_id, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages(
        self,
        user_id: str,
        conversation_id: int,
        limit: int = 50,
    ) -> list[Message]:
        """
        Get conversation messages in chronological order.

        Per data-model.md query pattern:
        SELECT m.role, m.content, m.tool_calls, m.created_at
        FROM messages m WHERE m.conversation_id = :conversation_id
        ORDER BY m.created_at ASC;

        Args:
            user_id: Owner to filter by (for security)
            conversation_id: Conversation to get messages from
            limit: Maximum messages to return

        Returns:
            List of messages in chronological order
        """
        # First verify conversation ownership
        conversation = await self.get_conversation(user_id, conversation_id)
        if not conversation:
            return []

        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_or_create_conversation(
        self, user_id: str, conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get existing conversation or create new one.

        Used by chat endpoint for auto-creation per FR-039.

        Args:
            user_id: Owner of the conversation
            conversation_id: Optional existing conversation ID

        Returns:
            Existing or new conversation
        """
        if conversation_id:
            conversation = await self.get_conversation(user_id, conversation_id)
            if conversation:
                return conversation

        # Create new conversation
        return await self.create_conversation(user_id)
