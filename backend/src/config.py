"""
Environment configuration for Phase 3 Todo Chatbot Backend.

Loads and validates required environment variables per .env.example:
- DATABASE_URL: Neon PostgreSQL connection string
- BETTER_AUTH_SECRET: JWT validation secret (shared with frontend)
- OPENAI_API_KEY: OpenAI API key for Agents SDK
"""

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    database_url: str
    better_auth_secret: str
    gemini_api_key: str

    # Optional settings with defaults
    debug: bool = False
    cors_origins: list[str] = None

    def __post_init__(self):
        # Validate required settings
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        # In Phase 3, we require BETTER_AUTH_SECRET for JWT validation
        if not self.better_auth_secret:
            raise ValueError("BETTER_AUTH_SECRET environment variable is required")


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Uses lru_cache to ensure settings are only loaded once.
    """
    cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo.db"),
        better_auth_secret=os.getenv("BETTER_AUTH_SECRET", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        cors_origins=cors_origins,
    )
