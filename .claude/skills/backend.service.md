---
description: Create a service layer class with business logic, database operations, and proper error handling
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse service requirements** from user input:
   - Service name and purpose
   - Domain entity it operates on
   - Business operations needed (CRUD, custom logic)
   - Data validation rules
   - Error handling requirements
   - Dependencies on other services

2. **Verify project structure**:
   - Check `backend/src/services/` exists
   - Check that models exist in `backend/src/models/`
   - Verify database connection in `backend/src/db.py`
   - Check for existing related services

3. **Create service file**:
   - File location: `backend/src/services/{entity}_service.py`
   - Follow naming convention: `{Entity}Service` class
   - Example: `TaskService`, `UserService`, `ConversationService`

4. **Implement service class structure**:
   ```python
   """
   {Entity}Service: Business logic for {entity} operations.

   Handles:
   - {list of operations}
   """

   from typing import List, Optional
   from sqlalchemy import select
   from sqlalchemy.ext.asyncio import AsyncSession
   from sqlmodel import col

   from ..models.{entity} import {Entity}, {Entity}Create, {Entity}Update


   class {Entity}Service:
       """Service for {entity} business logic and data operations."""

       @staticmethod
       async def create(
           db: AsyncSession,
           data: {Entity}Create,
           user_id: str
       ) -> {Entity}:
           """Create a new {entity}."""
           pass

       @staticmethod
       async def get_by_id(
           db: AsyncSession,
           entity_id: int,
           user_id: str
       ) -> Optional[{Entity}]:
           """Get {entity} by ID with user ownership validation."""
           pass

       @staticmethod
       async def list_all(
           db: AsyncSession,
           user_id: str,
           skip: int = 0,
           limit: int = 100
       ) -> List[{Entity}]:
           """List all {entities} for a user with pagination."""
           pass

       @staticmethod
       async def update(
           db: AsyncSession,
           entity_id: int,
           data: {Entity}Update,
           user_id: str
       ) -> Optional[{Entity}]:
           """Update {entity} with validation."""
           pass

       @staticmethod
       async def delete(
           db: AsyncSession,
           entity_id: int,
           user_id: str
       ) -> bool:
           """Delete {entity} with user ownership validation."""
           pass
   ```

5. **Implement CRUD operations**:

   **CREATE:**
   - Validate input data using Pydantic schema
   - Create model instance with user_id
   - Add to database session
   - Commit and refresh to get generated ID
   - Return created entity

   **READ:**
   - Use SQLAlchemy select statements
   - Filter by user_id for data isolation
   - Handle not found cases (return None or raise)
   - Use eager loading for relationships if needed

   **UPDATE:**
   - Fetch existing entity with ownership validation
   - Update only provided fields (partial updates)
   - Update `updated_at` timestamp
   - Commit and refresh
   - Return updated entity

   **DELETE:**
   - Validate ownership before deletion
   - Delete entity from database
   - Return success boolean
   - Handle foreign key constraints

6. **Add business logic methods**:
   - Implement domain-specific operations beyond CRUD
   - Examples:
     - `mark_as_completed()` for tasks
     - `send_notification()` for messages
     - `calculate_statistics()` for analytics
   - Keep business rules in service layer, not in API endpoints

7. **Add data validation**:
   - Validate business rules (e.g., title length, due dates)
   - Check uniqueness constraints
   - Validate relationships (foreign keys exist)
   - Return clear validation errors

8. **Implement error handling**:
   - Catch IntegrityError for constraint violations
   - Handle NoResultFound for missing entities
   - Raise custom exceptions for business rule violations
   - Add meaningful error messages

9. **Add user isolation**:
   - **CRITICAL**: Always filter by user_id
   - Validate user_id matches authenticated user
   - Prevent cross-user data access
   - Add user_id to all WHERE clauses

10. **Add type hints and documentation**:
    - Type hint all parameters and return values
    - Add comprehensive docstrings to each method
    - Document parameters, return values, and exceptions
    - Include usage examples in docstrings

11. **Register service** in `backend/src/services/__init__.py`:
    ```python
    from .{entity}_service import {Entity}Service

    __all__ = ["{Entity}Service", ...]
    ```

12. **Testing checklist**:
    - [ ] All CRUD operations work correctly
    - [ ] User isolation enforced (no cross-user access)
    - [ ] Input validation works
    - [ ] Error cases handled gracefully
    - [ ] Type hints on all methods
    - [ ] Comprehensive docstrings
    - [ ] Async/await used consistently
    - [ ] Service registered in __init__.py

## Example Service Implementation

```python
"""
TaskService: Business logic for task management operations.

Handles:
- Task creation with validation
- Task retrieval with user isolation
- Task updates and completion
- Task deletion with ownership checks
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from ..models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    """Service for task business logic and data operations."""

    @staticmethod
    async def create(
        db: AsyncSession,
        task_data: TaskCreate,
        user_id: str
    ) -> Task:
        """
        Create a new task for a user.

        Args:
            db: Database session
            task_data: Task creation data
            user_id: Owner user ID

        Returns:
            Created task with generated ID

        Raises:
            ValueError: If task data is invalid
        """
        task = Task(
            **task_data.model_dump(),
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        task_id: int,
        user_id: str
    ) -> Optional[Task]:
        """
        Get task by ID with user ownership validation.

        Args:
            db: Database session
            task_id: Task ID
            user_id: User ID for ownership check

        Returns:
            Task if found and owned by user, None otherwise
        """
        stmt = select(Task).where(
            col(Task.id) == task_id,
            col(Task.user_id) == user_id
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_by_user(
        db: AsyncSession,
        user_id: str,
        completed: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """
        List tasks for a user with optional filtering.

        Args:
            db: Database session
            user_id: User ID
            completed: Filter by completion status (None = all)
            skip: Number of records to skip (pagination)
            limit: Maximum records to return

        Returns:
            List of tasks matching criteria
        """
        stmt = select(Task).where(col(Task.user_id) == user_id)

        if completed is not None:
            stmt = stmt.where(col(Task.completed) == completed)

        stmt = stmt.offset(skip).limit(limit).order_by(Task.created_at.desc())

        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        task_id: int,
        task_data: TaskUpdate,
        user_id: str
    ) -> Optional[Task]:
        """
        Update task with ownership validation.

        Args:
            db: Database session
            task_id: Task ID
            task_data: Update data (partial)
            user_id: User ID for ownership check

        Returns:
            Updated task if found and owned, None otherwise
        """
        task = await TaskService.get_by_id(db, task_id, user_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete(
        db: AsyncSession,
        task_id: int,
        user_id: str
    ) -> bool:
        """
        Delete task with ownership validation.

        Args:
            db: Database session
            task_id: Task ID
            user_id: User ID for ownership check

        Returns:
            True if deleted, False if not found or not owned
        """
        task = await TaskService.get_by_id(db, task_id, user_id)
        if not task:
            return False

        await db.delete(task)
        await db.commit()
        return True

    @staticmethod
    async def mark_completed(
        db: AsyncSession,
        task_id: int,
        user_id: str,
        completed: bool = True
    ) -> Optional[Task]:
        """
        Mark task as completed or incomplete.

        Args:
            db: Database session
            task_id: Task ID
            user_id: User ID for ownership check
            completed: Completion status

        Returns:
            Updated task if found and owned, None otherwise
        """
        return await TaskService.update(
            db,
            task_id,
            TaskUpdate(completed=completed),
            user_id
        )
```

## Example Usage

```bash
# Create a new service
/backend.service Create TaskService for task management with CRUD operations

# With detailed requirements
/backend.service Create ConversationService with methods to create conversations, add messages, and retrieve conversation history
```

## Best Practices

- Use static methods for stateless operations
- Keep business logic in services, not in API routes
- Always validate user ownership for data isolation
- Use type hints for better IDE support and type checking
- Write comprehensive docstrings
- Handle errors at the service layer
- Return None for not found, don't raise exceptions (let API layer decide)
- Use Pydantic schemas for input validation
- Keep methods focused and single-purpose
- Use async/await consistently

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (service implementation work)
2) Generate Title: 3–7 words describing the service created
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
