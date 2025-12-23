"""
FastAPI application entry point for Phase 3 Todo Chatbot.

Per CLAUDE.md:
- All routes under /api/
- Return JSON responses
- Handle errors with HTTPException
"""

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import api_router, include_routers
from .config import get_settings

# Check if running in serverless environment
IS_SERVERLESS = os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI app instance
    """
    settings = get_settings()

    app = FastAPI(
        title="Phase 3 Todo Chatbot API",
        description="AI-Powered Todo Chatbot API for natural language task management",
        version="1.0.0",
    )

    # Configure CORS per constitution
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    include_routers()
    app.include_router(api_router)

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle uncaught exceptions with JSON response."""
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": "An unexpected error occurred",
            },
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for monitoring."""
        return {
            "status": "healthy",
            "version": "1.0.0",
            "environment": "serverless" if IS_SERVERLESS else "local"
        }

    # Startup event for non-serverless environments
    if not IS_SERVERLESS:
        @app.on_event("startup")
        async def startup():
            from .db import init_db
            await init_db()

        @app.on_event("shutdown")
        async def shutdown():
            from .db import close_db
            await close_db()

    return app


# Create app instance
app = create_app()
