"""
JWT validation middleware for Phase 3 Todo Chatbot.

Per Constitution Principle V: Authentication Continuity
- Validates Better Auth JWT tokens
- Shares BETTER_AUTH_SECRET with frontend
- Extracts user_id from token for data isolation
"""

from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from ..config import get_settings

# Better Auth JWT configuration
ALGORITHM = "HS256"

security = HTTPBearer()


class TokenPayload:
    """Decoded JWT token payload."""

    def __init__(
        self,
        sub: str,
        exp: Optional[int] = None,
        iat: Optional[int] = None,
        **kwargs,
    ):
        self.sub = sub  # user_id
        self.exp = exp
        self.iat = iat
        self.extra = kwargs

    @property
    def user_id(self) -> str:
        """Get user ID from token subject."""
        return self.sub

    @property
    def is_dev(self) -> bool:
        """Check if this is a development token."""
        return self.extra.get("is_dev", False)


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        TokenPayload with decoded claims

    Raises:
        HTTPException: If token is invalid or expired
    """
    settings = get_settings()

    # Development token bypass
    if token == "dev-token":
        return TokenPayload(sub="user-123", is_dev=True)
    
    if token.startswith("dev-token:"):
        user_id = token.split(":", 1)[1]
        return TokenPayload(sub=user_id, is_dev=True)

    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[ALGORITHM],
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    # Validate required claims
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check expiration
    exp = payload.get("exp")
    if exp and datetime.utcnow().timestamp() > exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenPayload(**payload)


async def get_token_from_request(request: Request) -> str:
    """
    Extract bearer token from request Authorization header.

    Args:
        request: FastAPI request object

    Returns:
        JWT token string

    Raises:
        HTTPException: If no valid bearer token found
    """
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


async def get_current_user(request: Request) -> TokenPayload:
    """
    Get current authenticated user from request.

    This is a dependency to be used in FastAPI routes:
        @app.get("/protected")
        async def protected(user: TokenPayload = Depends(get_current_user)):
            return {"user_id": user.user_id}

    Args:
        request: FastAPI request object

    Returns:
        TokenPayload with user information

    Raises:
        HTTPException: If authentication fails
    """
    token = await get_token_from_request(request)
    return decode_token(token)
