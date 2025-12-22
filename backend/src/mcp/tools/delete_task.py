"""
delete_task MCP tool implementation.

Per mcp-tools.md: Remove a task from the user's list.
FR-014: Task deletion via chat
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...services import TaskService


async def delete_task(
    db: AsyncSession,
    user_id: str,
    task_id: int,
) -> dict[str, Any]:
    """
    Remove a task from the user's list.

    Args:
        db: Database session
        user_id: Owner of the task
        task_id: ID of the task to delete

    Returns:
        {task_id, status, title} on success
        {error, task_id} on failure

    Per mcp-tools.md error cases:
    - Task not found: {"error": "Task not found", "task_id": ...}
    """
    task_service = TaskService(db)

    # Get task first to capture title for response
    task = await task_service.get_by_id(user_id, task_id)
    if not task:
        return {"error": "Task not found", "task_id": task_id}

    title = task.title

    # Delete the task
    deleted = await task_service.delete(user_id, task_id)
    if not deleted:
        return {"error": "Task not found", "task_id": task_id}

    return {
        "task_id": task_id,
        "status": "deleted",
        "title": title,
    }
