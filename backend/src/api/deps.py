"""
FastAPI dependency injection for Phase 3 Todo Chatbot.

Per Constitution Principle V: User Isolation
- All queries MUST include user_id filter
- Path parameter user_id must match JWT user
"""

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from .auth import TokenPayload, get_current_user


async def get_authenticated_user(
    user: TokenPayload = Depends(get_current_user),
) -> TokenPayload:
    """
    Get authenticated user from JWT token.

    Basic dependency - just validates token and returns payload.
    """
    return user


async def validate_user_id_match(
    user_id: str = Path(..., description="User ID from path"),
    current_user: TokenPayload = Depends(get_current_user),
) -> str:
    """
    Validate that path user_id matches authenticated user.

    Per Constitution Principle V: Authentication Continuity
    - JWT validation required on all /api/{user_id}/ endpoints
    - User_id path parameter must match JWT user

    Args:
        user_id: User ID from URL path
        current_user: Authenticated user from JWT

    Returns:
        Validated user_id

    Raises:
        HTTPException 403: If user_id doesn't match JWT user
    """
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this resource",
        )
    return user_id


async def get_db_session(
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    """
    Get database session dependency.

    Wrapper around get_db for consistent naming.
    """
    return db


class AuthenticatedRequest:
    """
    Combined dependency for authenticated requests.

    Provides both validated user_id and database session.

    Usage:
        @app.get("/api/{user_id}/resource")
        async def endpoint(
            auth: AuthenticatedRequest = Depends(get_authenticated_request),
        ):
            user_id = auth.user_id
            async with auth.db as session:
                ...
    """

    def __init__(self, user_id: str, db: AsyncSession, user: TokenPayload):
        self.user_id = user_id
        self.db = db
        self.user = user


async def get_authenticated_request(
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
    user: TokenPayload = Depends(get_current_user),
) -> AuthenticatedRequest:
    """
    Get combined authenticated request dependencies.

    Validates:
    1. JWT token is valid
    2. Path user_id matches JWT user
    3. Database session is available

    Returns:
        AuthenticatedRequest with user_id, db session, and user payload
    """
    return AuthenticatedRequest(user_id=user_id, db=db, user=user)
