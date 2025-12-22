"""
update_task MCP tool implementation.

Per mcp-tools.md: Update a task's title or description.
FR-015: Task update via chat
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...models import TaskUpdate
from ...services import TaskService


async def update_task(
    db: AsyncSession,
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update a task's title or description.

    Args:
        db: Database session
        user_id: Owner of the task
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        {task_id, status, title} on success
        {error, task_id?} on failure

    Per mcp-tools.md error cases:
    - Task not found: {"error": "Task not found", "task_id": ...}
    - No fields to update: {"error": "No updates provided"}
    - Empty title: {"error": "Title cannot be empty"}
    """
    # Check if any updates provided
    if title is None and description is None:
        return {"error": "No updates provided"}

    # Validate title if provided
    if title is not None:
        title = title.strip()
        if not title:
            return {"error": "Title cannot be empty"}
        if len(title) > 200:
            return {"error": "Title exceeds 200 characters"}

    # Validate description length
    if description is not None and len(description) > 1000:
        description = description[:1000]

    task_service = TaskService(db)

    # Check task exists
    task = await task_service.get_by_id(user_id, task_id)
    if not task:
        return {"error": "Task not found", "task_id": task_id}

    # Build update data
    update_data = TaskUpdate()
    if title is not None:
        update_data.title = title
    if description is not None:
        update_data.description = description

    # Update the task
    updated_task = await task_service.update(user_id, task_id, update_data)

    return {
        "task_id": task_id,
        "status": "updated",
        "title": updated_task.title,
    }
