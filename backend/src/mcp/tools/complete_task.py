"""
complete_task MCP tool implementation.

Per mcp-tools.md: Mark a task as complete.
FR-013: Task completion via chat
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...services import TaskService


async def complete_task(
    db: AsyncSession,
    user_id: str,
    task_id: int,
) -> dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        db: Database session
        user_id: Owner of the task
        task_id: ID of the task to complete

    Returns:
        {task_id, status, title} on success
        {error, task_id} on failure

    Per mcp-tools.md:
    - Already completed: Return success (idempotent)
    - Task not found: {"error": "Task not found", "task_id": ...}
    """
    task_service = TaskService(db)

    # Get task first to capture title for response
    task = await task_service.get_by_id(user_id, task_id)
    if not task:
        return {"error": "Task not found", "task_id": task_id}

    # Mark as complete (idempotent - succeeds even if already complete)
    await task_service.complete(user_id, task_id)

    return {
        "task_id": task_id,
        "status": "completed",
        "title": task.title,
    }
