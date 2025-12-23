"""
Vercel serverless entry point for Phase 3 Todo Chatbot Backend.
This file is specifically for Vercel deployment.
"""
from src.main import app, handler

# Export for Vercel
__all__ = ["app", "handler"]
