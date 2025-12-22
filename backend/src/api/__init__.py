"""
FastAPI API routers for Phase 3 Todo Chatbot.

Per CLAUDE.md: All routes under /api/
"""

from fastapi import APIRouter

# Main API router
api_router = APIRouter(prefix="/api")


def include_routers():
    """
    Include all API routers.

    Called after all router modules are loaded to avoid circular imports.
    """
    from .chat import router as chat_router
    from .tasks import router as tasks_router

    api_router.include_router(chat_router, tags=["Chat"])
    api_router.include_router(tasks_router, tags=["Tasks"])


__all__ = ["api_router", "include_routers"]
