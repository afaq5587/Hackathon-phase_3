"""
Chat Service for Phase 3 Todo Chatbot.

Implements the 7-step conversation flow per Constitution Principle IV:
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent
4. Store user message in database
5. Run agent with MCP tools
6. Store assistant response in database
7. Return response to client
"""

from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.message import Message
from .conversation_service import ConversationService

if TYPE_CHECKING:
    from ..agent.todo_agent import TodoAgent


class ChatService:
    """
    Service for handling chat interactions.

    Orchestrates the conversation flow between user, agent, and database.
    """

    def __init__(self, db: AsyncSession):
        """Initialize with database session."""
        self.db = db
        self.conversation_service = ConversationService(db)

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Process a chat message through the 7-step flow.

        Args:
            user_id: Authenticated user ID
            message: User's natural language message
            conversation_id: Optional existing conversation ID

        Returns:
            {
                conversation_id: int,
                response: str,
                tool_calls: list[dict] | None
            }

        Raises:
            Exception: If AI service is unavailable
        """
        # Step 1: Message already received via API

        # Step 2 & 3: Get or create conversation, fetch history
        conversation = await self.conversation_service.get_or_create_conversation(
            user_id, conversation_id
        )

        # Fetch conversation history for context
        history_messages = await self.conversation_service.get_messages(
            user_id, conversation.id, limit=20  # Last 20 messages for context
        )

        # Build conversation history for agent
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages
        ]

        # Step 4: Store user message
        await self.conversation_service.add_message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        # Step 5: Run agent with MCP tools
        try:
            # Import here to avoid circular import
            from ..agent.todo_agent import TodoAgent
            agent = TodoAgent(self.db, user_id)
            response_text, tool_calls = await agent.run(
                message=message,
                conversation_history=conversation_history,
            )
        except Exception as e:
            # Handle AI service unavailable (FR-082)
            print(f"ERROR in ChatService: {str(e)}")  # Visible in uvicorn logs
            response_text = "I'm having trouble connecting right now. Please try again in a moment."
            tool_calls = []

        # Step 6: Store assistant response
        await self.conversation_service.add_message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            tool_calls=tool_calls if tool_calls else None,
        )

        # Step 7: Return response
        return {
            "conversation_id": conversation.id,
            "response": response_text,
            "tool_calls": tool_calls if tool_calls else None,
        }
