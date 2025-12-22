"""
MCP Server setup for Phase 3 Todo Chatbot.

Per Constitution Principle III: MCP-Native Tools
- All task operations are MCP tools
- Single unified interface for agent
"""

from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent

# Create MCP server instance
mcp_server = Server("todo-chatbot-mcp")


def get_tools() -> list[Tool]:
    """
    Get list of available MCP tools.

    Returns all tools as MCP Tool objects for registration.
    """
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's unique identifier",
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title (1-200 characters)",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                        "maxLength": 1000,
                    },
                },
                "required": ["user_id", "title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="Retrieve tasks from the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's unique identifier",
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by task status",
                        "enum": ["all", "pending", "completed"],
                        "default": "all",
                    },
                },
                "required": ["user_id"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's unique identifier",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="delete_task",
            description="Remove a task from the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's unique identifier",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="update_task",
            description="Update a task's title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's unique identifier",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)",
                        "maxLength": 1000,
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]


# Register tools list handler
@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return get_tools()
