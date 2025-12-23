"""
Vercel serverless entry point for Phase 3 Todo Chatbot Backend.
This file is specifically for Vercel deployment.
"""
# Import the FastAPI app
from src.main import app

# Vercel expects 'app' to be the ASGI application
# No need for Mangum - Vercel has native ASGI support
__all__ = ["app"]
