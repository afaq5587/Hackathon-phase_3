"""
Task Service for Phase 3 Todo Chatbot.

Provides CRUD operations for tasks with user isolation.
Per Constitution Principle V: All queries include user_id filter.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """Service for task CRUD operations with user isolation."""

    def __init__(self, db: AsyncSession):
        """Initialize with database session."""
        self.db = db

    async def create(self, user_id: str, task_data: TaskCreate) -> Task:
        """
        Create a new task for user.

        Args:
            user_id: Owner of the task
            task_data: Task creation data

        Returns:
            Created task with ID
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_by_id(self, user_id: str, task_id: int) -> Optional[Task]:
        """
        Get task by ID with user isolation.

        Args:
            user_id: Owner to filter by
            task_id: Task ID to find

        Returns:
            Task if found and owned by user, None otherwise
        """
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_tasks(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Task]:
        """
        List user's tasks with optional status filter.

        Per data-model.md query patterns:
        - All tasks: WHERE user_id = :user_id
        - Pending: WHERE user_id = :user_id AND completed = false
        - Completed: WHERE user_id = :user_id AND completed = true

        Args:
            user_id: Owner to filter by
            status: Optional filter - "all", "pending", or "completed"
            limit: Maximum tasks to return
            offset: Number of tasks to skip

        Returns:
            List of tasks matching criteria
        """
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        # "all" or None returns all tasks

        query = query.order_by(Task.created_at.desc()).limit(limit).offset(offset)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(
        self, user_id: str, task_id: int, task_data: TaskUpdate
    ) -> Optional[Task]:
        """
        Update task with user isolation.

        Args:
            user_id: Owner to filter by
            task_id: Task ID to update
            task_data: Fields to update

        Returns:
            Updated task if found, None otherwise
        """
        task = await self.get_by_id(user_id, task_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def complete(self, user_id: str, task_id: int) -> Optional[Task]:
        """
        Mark task as complete.

        Args:
            user_id: Owner to filter by
            task_id: Task ID to complete

        Returns:
            Updated task if found, None otherwise
        """
        return await self.update(
            user_id, task_id, TaskUpdate(completed=True)
        )

    async def delete(self, user_id: str, task_id: int) -> bool:
        """
        Delete task with user isolation.

        Args:
            user_id: Owner to filter by
            task_id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        task = await self.get_by_id(user_id, task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True
