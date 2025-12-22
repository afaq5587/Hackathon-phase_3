"""
Task API endpoints for Phase 3 Todo Chatbot.

REST API for task CRUD operations:
- GET /api/{user_id}/tasks - List user's tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{task_id} - Get specific task
- PUT /api/{user_id}/tasks/{task_id} - Update task
- PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion
- DELETE /api/{user_id}/tasks/{task_id} - Delete task
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models.task import TaskCreate, TaskRead, TaskUpdate
from ..services.task_service import TaskService
from .deps import validate_user_id_match

router = APIRouter()


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str
    message: str


@router.get(
    "/{user_id}/tasks",
    response_model=list[TaskRead],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
async def list_tasks(
    user_id: str = Depends(validate_user_id_match),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    limit: int = Query(default=50, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's tasks with optional status filter.

    Query parameters:
    - status: Filter by "pending", "completed", or "all" (default: all)
    - limit: Maximum number of tasks to return (default: 50, max: 100)

    Returns tasks ordered by creation date (newest first).
    """
    task_service = TaskService(db)
    tasks = await task_service.list_tasks(
        user_id=user_id,
        status=status_filter,
        limit=limit,
    )
    return tasks


@router.post(
    "/{user_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new task for the user.

    Request body:
    - title: Task title (required, 1-200 chars)
    - description: Task description (optional, max 1000 chars)
    """
    # Validate non-empty title
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "validation_error", "message": "Task title cannot be empty"},
        )

    task_service = TaskService(db)
    task = await task_service.create(user_id, task_data)
    return task


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskRead,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
async def get_task(
    task_id: int = Path(..., description="Task ID"),
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific task by ID.

    Returns 404 if task doesn't exist or doesn't belong to the user.
    """
    task_service = TaskService(db)
    task = await task_service.get_by_id(user_id, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Task not found"},
        )

    return task


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskRead,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
async def update_task(
    task_data: TaskUpdate,
    task_id: int = Path(..., description="Task ID"),
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a task's title, description, or completion status.

    All fields are optional. Only provided fields will be updated.
    """
    task_service = TaskService(db)
    task = await task_service.update(user_id, task_id, task_data)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Task not found"},
        )

    return task


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskRead,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
async def toggle_task_complete(
    task_id: int = Path(..., description="Task ID"),
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
):
    """
    Toggle task completion status.

    If task is incomplete, marks it as complete.
    If task is complete, marks it as incomplete.
    """
    task_service = TaskService(db)

    # Get current task
    task = await task_service.get_by_id(user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Task not found"},
        )

    # Toggle completion status
    updated_task = await task_service.update(
        user_id,
        task_id,
        TaskUpdate(completed=not task.completed),
    )

    return updated_task


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
async def delete_task(
    task_id: int = Path(..., description="Task ID"),
    user_id: str = Depends(validate_user_id_match),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a task.

    Returns 404 if task doesn't exist or doesn't belong to the user.
    """
    task_service = TaskService(db)
    deleted = await task_service.delete(user_id, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Task not found"},
        )
