"""
add_task MCP tool implementation.

Per mcp-tools.md: Create a new task for the user's todo list.
FR-011: Task creation via natural language
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...models import TaskCreate
from ...services import TaskService


async def add_task(
    db: AsyncSession,
    user_id: str,
    title: str,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        db: Database session
        user_id: Owner of the task
        title: Task title (1-200 chars)
        description: Optional task description

    Returns:
        {task_id, status, title} on success
        {error} on failure

    Per mcp-tools.md error cases:
    - Empty title: {"error": "Title cannot be empty"}
    - Title too long: {"error": "Title exceeds 200 characters"}
    """
    # Validate title
    if not title or not title.strip():
        return {"error": "Title cannot be empty"}

    title = title.strip()
    if len(title) > 200:
        return {"error": "Title exceeds 200 characters"}

    # Validate description length
    if description and len(description) > 1000:
        description = description[:1000]

    # Create task
    task_service = TaskService(db)
    task_data = TaskCreate(
        title=title,
        description=description,
    )

    task = await task_service.create(user_id, task_data)

    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title,
    }
