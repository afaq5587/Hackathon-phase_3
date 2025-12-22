"""
Todo Agent using OpenAI Agents SDK.

Per Constitution Principle IV: Agent-First Conversation
- OpenAI Agents SDK manages conversation state and tool execution
- Agent decides when to call MCP tools
- Built-in agent loop handles tool calling automatically
- Friendly, helpful response generation

SDK: https://openai.github.io/openai-agents-python/
"""

import json
from dataclasses import dataclass
from typing import Any, Optional

from agents import Agent, Runner, RunContextWrapper, function_tool, set_default_openai_api
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..models import TaskCreate, TaskUpdate
from ..services.task_service import TaskService

settings = get_settings()

# Use Chat Completions API instead of Responses API (required for non-OpenAI models)
set_default_openai_api("chat_completions")

# Reference: https://ai.google.dev/gemini-api/docs/openai
# Gemini provides OpenAI-compatible API endpoint
external_client = AsyncOpenAI(
    api_key=settings.gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Create model using OpenAI Chat Completions compatible interface
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",  # Most stable on v1beta endpoint
    openai_client=external_client
)
# System prompt for the todo agent
SYSTEM_PROMPT = """You are a friendly and helpful AI assistant that helps users manage their todo list.
You can help users:
- Create new tasks ("Add a task to...", "I need to remember...", "Create...")
- View their tasks ("Show me...", "What's pending?", "List...")
- Mark tasks as complete ("Mark as complete", "Done with...", "Finished...")
- Delete tasks ("Delete...", "Remove...", "Cancel...")
- Update tasks ("Change...", "Update...", "Rename...")

When responding:
1. Be friendly and conversational
2. Confirm actions with the task details
3. Offer helpful follow-up suggestions when appropriate
4. If you're unsure what the user wants, ask for clarification

Task response guidelines:
- After adding: "I've added '{title}' to your task list!"
- After listing: Show tasks in a numbered list with status
- After completing: "Nice work! '{title}' is marked as complete."
- After deleting: "'{title}' has been removed from your list."
- After updating: "I've updated '{title}' for you."

If the user's request is unclear, respond with:
"I'm not sure what you'd like me to do with your tasks. You can ask me to:
- Add a new task
- Show your tasks
- Mark a task as complete
- Delete a task
- Update a task title"
"""


@dataclass
class TodoContext:
    """Context passed to tools containing user info and database session."""
    user_id: str
    db: AsyncSession
    tool_calls: list[dict[str, Any]]


# Define tools using @function_tool decorator
# The SDK automatically extracts schema from type annotations and docstrings

@function_tool
async def add_task(
    ctx: RunContextWrapper[TodoContext],
    title: str,
    description: Optional[str] = None,
) -> str:
    """Create a new task for the user's todo list.

    Args:
        title: The task title (1-200 characters)
        description: Optional task description
    """
    context = ctx.context

    # Validate title
    if not title or not title.strip():
        return json.dumps({"error": "Title cannot be empty"})

    title = title.strip()
    if len(title) > 200:
        return json.dumps({"error": "Title exceeds 200 characters"})

    # Create task
    task_service = TaskService(context.db)
    task_data = TaskCreate(
        title=title,
        description=description[:1000] if description else None,
    )
    task = await task_service.create(context.user_id, task_data)

    result = {
        "task_id": task.id,
        "status": "created",
        "title": task.title,
    }

    # Record tool call
    context.tool_calls.append({
        "tool": "add_task",
        "arguments": {"title": title, "description": description},
        "result": result,
    })

    return json.dumps(result)


@function_tool
async def list_tasks(
    ctx: RunContextWrapper[TodoContext],
    status: str = "all",
) -> str:
    """Retrieve tasks from the user's todo list.

    Args:
        status: Filter by task status - "all", "pending", or "completed"
    """
    context = ctx.context

    # Validate status
    if status not in ("all", "pending", "completed"):
        status = "all"

    task_service = TaskService(context.db)
    tasks = await task_service.list_tasks(context.user_id, status=status)

    result = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat() + "Z",
        }
        for task in tasks
    ]

    # Record tool call
    context.tool_calls.append({
        "tool": "list_tasks",
        "arguments": {"status": status},
        "result": result,
    })

    return json.dumps(result)


@function_tool
async def complete_task(
    ctx: RunContextWrapper[TodoContext],
    task_id: int,
) -> str:
    """Mark a task as complete.

    Args:
        task_id: The ID of the task to complete
    """
    context = ctx.context
    task_service = TaskService(context.db)

    # Get task first to capture title for response
    task = await task_service.get_by_id(context.user_id, task_id)
    if not task:
        result = {"error": "Task not found", "task_id": task_id}
    else:
        await task_service.complete(context.user_id, task_id)
        result = {
            "task_id": task_id,
            "status": "completed",
            "title": task.title,
        }

    # Record tool call
    context.tool_calls.append({
        "tool": "complete_task",
        "arguments": {"task_id": task_id},
        "result": result,
    })

    return json.dumps(result)


@function_tool
async def delete_task(
    ctx: RunContextWrapper[TodoContext],
    task_id: int,
) -> str:
    """Remove a task from the user's todo list.

    Args:
        task_id: The ID of the task to delete
    """
    context = ctx.context
    task_service = TaskService(context.db)

    # Get task first to capture title for response
    task = await task_service.get_by_id(context.user_id, task_id)
    if not task:
        result = {"error": "Task not found", "task_id": task_id}
    else:
        title = task.title
        deleted = await task_service.delete(context.user_id, task_id)
        if deleted:
            result = {
                "task_id": task_id,
                "status": "deleted",
                "title": title,
            }
        else:
            result = {"error": "Task not found", "task_id": task_id}

    # Record tool call
    context.tool_calls.append({
        "tool": "delete_task",
        "arguments": {"task_id": task_id},
        "result": result,
    })

    return json.dumps(result)


@function_tool
async def update_task(
    ctx: RunContextWrapper[TodoContext],
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Update a task's title or description.

    Args:
        task_id: The ID of the task to update
        title: New task title (optional)
        description: New task description (optional)
    """
    context = ctx.context

    # Check if any updates provided
    if title is None and description is None:
        result = {"error": "No updates provided"}
        context.tool_calls.append({
            "tool": "update_task",
            "arguments": {"task_id": task_id},
            "result": result,
        })
        return json.dumps(result)

    # Validate title if provided
    if title is not None:
        title = title.strip()
        if not title:
            return json.dumps({"error": "Title cannot be empty"})
        if len(title) > 200:
            return json.dumps({"error": "Title exceeds 200 characters"})

    task_service = TaskService(context.db)

    # Check task exists
    task = await task_service.get_by_id(context.user_id, task_id)
    if not task:
        result = {"error": "Task not found", "task_id": task_id}
    else:
        # Build update data
        update_data = TaskUpdate()
        if title is not None:
            update_data.title = title
        if description is not None:
            update_data.description = description[:1000] if description else None

        # Update the task
        updated_task = await task_service.update(context.user_id, task_id, update_data)
        result = {
            "task_id": task_id,
            "status": "updated",
            "title": updated_task.title,
        }

    # Record tool call
    context.tool_calls.append({
        "tool": "update_task",
        "arguments": {"task_id": task_id, "title": title, "description": description},
        "result": result,
    })

    return json.dumps(result)


def create_todo_agent() -> Agent[TodoContext]:
    """
    Create the todo agent with all tools registered.

    Returns:
        Configured Agent instance
    """
    return Agent[TodoContext](
        name="TodoAssistant",
        instructions=SYSTEM_PROMPT,
        model=model,
        tools=[
            add_task,
            list_tasks,
            complete_task,
            delete_task,
            update_task,
        ],
    )


class TodoAgentRunner:
    """
    Wrapper to run the todo agent with proper context.

    Handles conversation flow using the OpenAI Agents SDK Runner.
    """

    def __init__(self, db: AsyncSession, user_id: str):
        """
        Initialize the agent runner.

        Args:
            db: Database session for tool execution
            user_id: Current user's ID for data isolation
        """
        self.db = db
        self.user_id = user_id
        self.agent = create_todo_agent()

    async def run(
        self,
        message: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[str, list[dict[str, Any]]]:
        """
        Process user message and generate response.

        Args:
            message: User's message
            conversation_history: Previous messages in conversation

        Returns:
            Tuple of (response_text, tool_calls)
        """
        # Create context with tool_calls tracker
        context = TodoContext(
            user_id=self.user_id,
            db=self.db,
            tool_calls=[],
        )

        # Build input with conversation history
        if conversation_history:
            input_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in conversation_history
            ]
            input_messages.append({"role": "user", "content": message})
        else:
            input_messages = message

        # Run the agent - SDK handles the tool calling loop automatically
        result = await Runner.run(
            self.agent,
            input_messages,
            context=context,
        )

        response_text = result.final_output or "I'm not sure how to help with that."

        return response_text, context.tool_calls

# Backwards compatibility alias

TodoAgent = TodoAgentRunner
