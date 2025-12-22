"""
Chat API endpoints for Phase 3 Todo Chatbot.

Per chat-api.yaml:
- POST /api/{user_id}/chat - Send chat message and get AI response
- GET /api/{user_id}/conversations - List user's conversations
- GET /api/{user_id}/conversations/{conversation_id}/messages - Get conversation messages
"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models import ConversationRead, MessageRead
from ..services import ChatService, ConversationService
from .deps import validate_user_id_match

router = APIRouter()


# Request/Response schemas per chat-api.yaml
class ChatRequest(BaseModel):
    """Chat request schema."""

    conversation_id: Optional[int] = Field(
        default=None,
        description="Existing conversation ID (creates new if not provided)",
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's natural language message",
    )


class ToolCall(BaseModel):
    """MCP tool call schema."""

    tool: str
    arguments: dict[str, Any]
    result: Optional[Any] = None


class ChatResponse(BaseModel):
    """Chat response schema."""

    conversation_id: int
    response: str
    tool_calls: Optional[list[ToolCall]] = None


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str
    message: str


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        503: {"model": ErrorResponse, "description": "AI service unavailable"},
    },
)
async def send_chat_message(
    request: ChatRequest,
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
):
    """
    Send chat message and get AI response.

    Implements: FR-007 to FR-019

    Conversation Flow (per Constitution Principle IV):
    1. Receive user message
    2. Fetch conversation history from database
    3. Build message array for agent
    4. Store user message in database
    5. Run agent with MCP tools
    6. Store assistant response in database
    7. Return response to client
    """
    # Validate non-empty message (FR-009)
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "validation_error", "message": "Message cannot be empty"},
        )

    # Process message through ChatService (7-step flow)
    chat_service = ChatService(db)

    try:
        result = await chat_service.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "service_unavailable",
                "message": "I'm having trouble connecting right now. Please try again in a moment.",
            },
        )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        tool_calls=result.get("tool_calls"),
    )


@router.get(
    "/{user_id}/conversations",
    response_model=list[ConversationRead],
)
async def list_conversations(
    user_id: str = Depends(validate_user_id_match),
    limit: int = Query(default=10, le=50),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's conversations (FR-017).

    Returns conversations ordered by most recent first.
    """
    conversation_service = ConversationService(db)
    conversations = await conversation_service.list_conversations(user_id, limit)
    return conversations


@router.get(
    "/{user_id}/conversations/{conversation_id}/messages",
    response_model=list[MessageRead],
    responses={
        404: {"model": ErrorResponse, "description": "Conversation not found"},
    },
)
async def get_conversation_messages(
    conversation_id: int = Path(..., description="Conversation ID"),
    user_id: str = Depends(validate_user_id_match),
    limit: int = Query(default=50, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Get conversation messages (FR-017).

    Returns messages in chronological order.
    """
    conversation_service = ConversationService(db)

    # Verify conversation exists and is owned by user
    conversation = await conversation_service.get_conversation(user_id, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Conversation not found"},
        )

    messages = await conversation_service.get_messages(user_id, conversation_id, limit)
    return messages
