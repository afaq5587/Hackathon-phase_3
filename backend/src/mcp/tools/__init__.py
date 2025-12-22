"""
MCP tools for Phase 3 Todo Chatbot.

Per Constitution Principle III: MCP-Native Tools
All task operations exposed via these tools.
"""

from .add_task import add_task
from .complete_task import complete_task
from .delete_task import delete_task
from .list_tasks import list_tasks
from .update_task import update_task

__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
]


# Tool name to function mapping
TOOL_FUNCTIONS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}
