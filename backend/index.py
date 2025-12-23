"""
Vercel serverless entry point for Phase 3 Todo Chatbot Backend.
This file is specifically for Vercel deployment.
"""
from mangum import Mangum
from src.main import app

# Create Mangum handler for Vercel
handler = Mangum(app, lifespan="off")

# Export for Vercel
__all__ = ["handler"]
