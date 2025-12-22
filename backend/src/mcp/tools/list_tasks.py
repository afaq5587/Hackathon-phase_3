"""
list_tasks MCP tool implementation.

Per mcp-tools.md: Retrieve tasks from the user's todo list.
FR-012: Task listing with filters
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...services import TaskService


async def list_tasks(
    db: AsyncSession,
    user_id: str,
    status: str = "all",
) -> list[dict[str, Any]]:
    """
    Retrieve tasks from the user's todo list.

    Args:
        db: Database session
        user_id: Owner of the tasks
        status: Filter - "all", "pending", or "completed"

    Returns:
        List of tasks with {id, title, description, completed, created_at}

    Per mcp-tools.md edge cases:
    - No tasks: Empty array []
    - Invalid status: Default to "all"
    """
    # Validate status
    if status not in ("all", "pending", "completed"):
        status = "all"

    task_service = TaskService(db)
    tasks = await task_service.list_tasks(user_id, status=status)

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat() + "Z",
        }
        for task in tasks
    ]
