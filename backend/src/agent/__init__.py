"""
OpenAI Agents SDK agent for Phase 3 Todo Chatbot.

Uses the official openai-agents SDK: https://openai.github.io/openai-agents-python/
"""

from .todo_agent import (
    TodoAgent,
    TodoAgentRunner,
    TodoContext,
    SYSTEM_PROMPT,
    create_todo_agent,
)

__all__ = [
    "TodoAgent",
    "TodoAgentRunner",
    "TodoContext",
    "SYSTEM_PROMPT",
    "create_todo_agent",
]
