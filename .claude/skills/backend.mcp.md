---
description: Create MCP (Model Context Protocol) tool for AI agent to interact with backend services
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse MCP tool requirements** from user input:
   - Tool name (e.g., `add_task`, `list_tasks`, `complete_task`)
   - Tool purpose and description
   - Input parameters (name, type, description, required/optional)
   - Output schema
   - Which service/database operations to call
   - Error cases to handle

2. **Verify project structure**:
   - Check `backend/src/mcp/tools/` exists
   - Check `backend/src/mcp/server.py` exists
   - Verify required services exist in `backend/src/services/`
   - Check MCP contract specifications in `specs/*/contracts/mcp-tools.md`

3. **Review MCP tool specification** (if exists):
   - Read `specs/*/contracts/mcp-tools.md` for tool schema
   - Check input parameter specifications
   - Verify output format requirements
   - Note any special validation rules

4. **Create MCP tool file**:
   - File location: `backend/src/mcp/tools/{tool_name}.py`
   - Use snake_case for filename
   - Each file exports one tool function

5. **Implement MCP tool structure**:
   ```python
   """
   MCP Tool: {tool_name}

   Description: {what this tool does}

   Per mcp-tools.md contract.
   """

   from typing import Any, Dict

   from sqlalchemy.ext.asyncio import AsyncSession

   from ...services.{service}_service import {Service}Service
   from ...models.{model} import {Model}Create, {Model}Update


   async def {tool_name}(
       db: AsyncSession,
       user_id: str,
       **kwargs: Any
   ) -> Dict[str, Any]:
       """
       {Tool description}

       Args:
           db: Database session
           user_id: User ID for data isolation
           **kwargs: Tool-specific parameters from AI agent

       Returns:
           Dict with 'success', 'message', and optional 'data'

       Example input:
           {
               "parameter1": "value1",
               "parameter2": "value2"
           }

       Example output:
           {
               "success": true,
               "message": "Operation completed successfully",
               "data": {...}
           }
       """
       pass
   ```

6. **Implement tool logic**:
   - Extract and validate parameters from kwargs
   - Call appropriate service methods
   - Handle database session properly
   - Return standardized response format
   - Include user-friendly success/error messages

7. **Define input schema** (for AI agent):
   - Document all parameters with types
   - Mark required vs optional parameters
   - Provide parameter descriptions
   - Include examples in docstring
   - Validate parameters before processing

8. **Define output schema**:
   - Always return Dict[str, Any]
   - Standard fields:
     - `success` (bool): Operation success status
     - `message` (str): Human-readable message
     - `data` (optional): Result data if applicable
     - `error` (optional): Error details if failed

9. **Add error handling**:
   - Catch service layer exceptions
   - Catch database errors
   - Catch validation errors
   - Return structured error responses
   - Log errors for debugging
   - Provide helpful error messages for the AI agent

10. **Add user isolation**:
    - **CRITICAL**: Always pass user_id to service calls
    - Validate user ownership
    - Prevent cross-user data access
    - Return only user's own data

11. **Register tool** in `backend/src/mcp/tools/__init__.py`:
    ```python
    from .{tool_name} import {tool_name}

    TOOLS = {
        "{tool_name}": {tool_name},
        # ... other tools
    }

    __all__ = ["TOOLS", "{tool_name}"]
    ```

12. **Update MCP server** in `backend/src/mcp/server.py`:
    - Import tool from tools module
    - Register tool with MCP server
    - Add tool to available tools list
    - Provide tool metadata (name, description, schema)

13. **Testing checklist**:
    - [ ] Tool follows MCP contract specification
    - [ ] Input parameters validated properly
    - [ ] Returns standardized response format
    - [ ] Error cases handled gracefully
    - [ ] User isolation enforced
    - [ ] Registered in tools __init__.py
    - [ ] Added to MCP server
    - [ ] Docstring complete with examples

## Example MCP Tool Implementations

### Simple CRUD Tool (Add Task)
```python
"""
MCP Tool: add_task

Creates a new task for the user.
Per mcp-tools.md contract.
"""

from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from ...services.task_service import TaskService
from ...models.task import TaskCreate


async def add_task(
    db: AsyncSession,
    user_id: str,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        db: Database session
        user_id: User ID from authentication
        title (str): Task title (required)
        description (str): Task description (optional)

    Returns:
        {
            "success": true,
            "message": "Task created successfully",
            "data": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": false,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    """
    try:
        # Extract and validate parameters
        title = kwargs.get("title")
        if not title or not isinstance(title, str):
            return {
                "success": False,
                "message": "Title is required and must be a string",
                "error": "invalid_input"
            }

        description = kwargs.get("description")

        # Create task via service
        task_data = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None
        )
        task = await TaskService.create(db, task_data, user_id)

        return {
            "success": True,
            "message": f"Task '{task.title}' created successfully!",
            "data": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to create task",
            "error": str(e)
        }
```

### Query Tool (List Tasks)
```python
"""
MCP Tool: list_tasks

Retrieves tasks for the user with optional filtering.
Per mcp-tools.md contract.
"""

from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ...services.task_service import TaskService


async def list_tasks(
    db: AsyncSession,
    user_id: str,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    List tasks for the authenticated user.

    Args:
        db: Database session
        user_id: User ID from authentication
        status (str): Filter by status - "pending", "completed", or "all" (optional, default: "all")
        limit (int): Maximum tasks to return (optional, default: 100)

    Returns:
        {
            "success": true,
            "message": "Found 5 tasks",
            "data": {
                "tasks": [...],
                "count": 5
            }
        }
    """
    try:
        # Extract parameters with defaults
        status = kwargs.get("status", "all")
        limit = kwargs.get("limit", 100)

        # Determine filter
        completed_filter: Optional[bool] = None
        if status == "pending":
            completed_filter = False
        elif status == "completed":
            completed_filter = True

        # Fetch tasks
        tasks = await TaskService.list_by_user(
            db,
            user_id,
            completed=completed_filter,
            limit=limit
        )

        # Format response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]

        status_text = {
            "pending": "pending",
            "completed": "completed",
            "all": "total"
        }.get(status, "total")

        return {
            "success": True,
            "message": f"Found {len(tasks)} {status_text} task(s)",
            "data": {
                "tasks": task_list,
                "count": len(tasks)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to retrieve tasks",
            "error": str(e)
        }
```

### Update Tool (Complete Task)
```python
"""
MCP Tool: complete_task

Marks a task as completed.
Per mcp-tools.md contract.
"""

from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from ...services.task_service import TaskService


async def complete_task(
    db: AsyncSession,
    user_id: str,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        db: Database session
        user_id: User ID from authentication
        task_id (int): ID of task to complete (required)

    Returns:
        {
            "success": true,
            "message": "Task 'Buy groceries' marked as completed!",
            "data": {...}
        }
    """
    try:
        # Extract and validate task_id
        task_id = kwargs.get("task_id")
        if not task_id:
            return {
                "success": False,
                "message": "Task ID is required",
                "error": "missing_task_id"
            }

        try:
            task_id = int(task_id)
        except (ValueError, TypeError):
            return {
                "success": False,
                "message": "Task ID must be a valid number",
                "error": "invalid_task_id"
            }

        # Complete the task
        task = await TaskService.mark_completed(db, task_id, user_id, completed=True)

        if not task:
            return {
                "success": False,
                "message": f"Task {task_id} not found. Want me to show your current tasks?",
                "error": "task_not_found"
            }

        return {
            "success": True,
            "message": f"Task '{task.title}' marked as completed!",
            "data": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to complete task",
            "error": str(e)
        }
```

## Example Usage

```bash
# Create a new MCP tool
/backend.mcp add_task - Creates a new task with title and optional description

# With detailed specification
/backend.mcp Create list_tasks tool that returns all tasks with optional status filter (pending, completed, all)

# Update operation
/backend.mcp Create complete_task tool to mark task as complete by ID
```

## MCP Tool Response Standards

Always return this format:
```python
{
    "success": bool,        # True if operation succeeded
    "message": str,         # Human-readable message for AI agent
    "data": dict | None,    # Result data (on success)
    "error": str | None     # Error code or details (on failure)
}
```

## Best Practices

- Follow MCP contract specifications exactly
- Always validate user_id to prevent cross-user access
- Return user-friendly messages for AI agent to convey
- Handle all error cases gracefully
- Use type hints for better validation
- Keep tools focused (one operation per tool)
- Document parameters clearly in docstrings
- Test with various input combinations
- Consider edge cases (empty lists, not found, etc.)
- Provide helpful error messages with actionable suggestions

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (MCP tool implementation)
2) Generate Title: 3–7 words describing the MCP tool
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
