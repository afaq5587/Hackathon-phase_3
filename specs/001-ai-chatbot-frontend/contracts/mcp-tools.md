# MCP Tools Specification

**Feature**: 001-ai-chatbot-frontend
**Date**: 2025-12-20
**Protocol**: Model Context Protocol (MCP)

## Overview

This document defines the MCP tool interfaces for the AI-powered todo chatbot. All tools follow Constitution Principle III and the schema defined in the Phase 3 requirements.

## Tool Registry

| Tool | Purpose | FR Reference |
|------|---------|--------------|
| add_task | Create a new task | FR-011 |
| list_tasks | Retrieve tasks | FR-012 |
| complete_task | Mark task complete | FR-013 |
| delete_task | Remove a task | FR-014 |
| update_task | Modify task details | FR-015 |

---

## 1. add_task

**Purpose**: Create a new task for a user.

### Schema

```json
{
  "name": "add_task",
  "description": "Create a new task for the user's todo list",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "The user's unique identifier"
      },
      "title": {
        "type": "string",
        "description": "The task title (1-200 characters)",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "type": "string",
        "description": "Optional task description",
        "maxLength": 1000
      }
    },
    "required": ["user_id", "title"]
  }
}
```

### Input Example

```json
{
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

### Output Schema

```json
{
  "type": "object",
  "properties": {
    "task_id": { "type": "integer" },
    "status": { "type": "string", "enum": ["created"] },
    "title": { "type": "string" }
  },
  "required": ["task_id", "status", "title"]
}
```

### Output Example

```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

### Error Cases

| Condition | Error Response |
|-----------|----------------|
| Empty title | `{"error": "Title cannot be empty"}` |
| Title too long | `{"error": "Title exceeds 200 characters"}` |
| Invalid user_id | `{"error": "User not found"}` |

---

## 2. list_tasks

**Purpose**: Retrieve tasks from the user's todo list with optional filtering.

### Schema

```json
{
  "name": "list_tasks",
  "description": "Retrieve tasks from the user's todo list",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "The user's unique identifier"
      },
      "status": {
        "type": "string",
        "description": "Filter by task status",
        "enum": ["all", "pending", "completed"],
        "default": "all"
      }
    },
    "required": ["user_id"]
  }
}
```

### Input Examples

```json
// All tasks
{ "user_id": "user123", "status": "all" }

// Pending only
{ "user_id": "user123", "status": "pending" }

// Completed only
{ "user_id": "user123", "status": "completed" }
```

### Output Schema

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": { "type": "integer" },
      "title": { "type": "string" },
      "description": { "type": "string", "nullable": true },
      "completed": { "type": "boolean" },
      "created_at": { "type": "string", "format": "date-time" }
    }
  }
}
```

### Output Example

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-20T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": null,
    "completed": true,
    "created_at": "2025-12-20T09:15:00Z"
  }
]
```

### Edge Cases

| Condition | Response |
|-----------|----------|
| No tasks | Empty array `[]` |
| Invalid status | Default to "all" |

---

## 3. complete_task

**Purpose**: Mark a task as complete.

### Schema

```json
{
  "name": "complete_task",
  "description": "Mark a task as complete",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "The user's unique identifier"
      },
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to complete"
      }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### Input Example

```json
{
  "user_id": "user123",
  "task_id": 3
}
```

### Output Schema

```json
{
  "type": "object",
  "properties": {
    "task_id": { "type": "integer" },
    "status": { "type": "string", "enum": ["completed"] },
    "title": { "type": "string" }
  },
  "required": ["task_id", "status", "title"]
}
```

### Output Example

```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

### Error Cases

| Condition | Error Response |
|-----------|----------------|
| Task not found | `{"error": "Task not found", "task_id": 3}` |
| Task belongs to different user | `{"error": "Task not found", "task_id": 3}` |
| Already completed | Return success (idempotent) |

---

## 4. delete_task

**Purpose**: Remove a task from the user's list.

### Schema

```json
{
  "name": "delete_task",
  "description": "Remove a task from the user's todo list",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "The user's unique identifier"
      },
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to delete"
      }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### Input Example

```json
{
  "user_id": "user123",
  "task_id": 2
}
```

### Output Schema

```json
{
  "type": "object",
  "properties": {
    "task_id": { "type": "integer" },
    "status": { "type": "string", "enum": ["deleted"] },
    "title": { "type": "string" }
  },
  "required": ["task_id", "status", "title"]
}
```

### Output Example

```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

### Error Cases

| Condition | Error Response |
|-----------|----------------|
| Task not found | `{"error": "Task not found", "task_id": 2}` |
| Task belongs to different user | `{"error": "Task not found", "task_id": 2}` |

---

## 5. update_task

**Purpose**: Modify a task's title or description.

### Schema

```json
{
  "name": "update_task",
  "description": "Update a task's title or description",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "The user's unique identifier"
      },
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to update"
      },
      "title": {
        "type": "string",
        "description": "New task title (optional)",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "type": "string",
        "description": "New task description (optional)",
        "maxLength": 1000
      }
    },
    "required": ["user_id", "task_id"]
  }
}
```

### Input Examples

```json
// Update title only
{
  "user_id": "user123",
  "task_id": 1,
  "title": "Buy groceries and fruits"
}

// Update description only
{
  "user_id": "user123",
  "task_id": 5,
  "description": "Prepare agenda items"
}

// Update both
{
  "user_id": "user123",
  "task_id": 1,
  "title": "Shopping",
  "description": "Get items from the store"
}
```

### Output Schema

```json
{
  "type": "object",
  "properties": {
    "task_id": { "type": "integer" },
    "status": { "type": "string", "enum": ["updated"] },
    "title": { "type": "string" }
  },
  "required": ["task_id", "status", "title"]
}
```

### Output Example

```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

### Error Cases

| Condition | Error Response |
|-----------|----------------|
| Task not found | `{"error": "Task not found", "task_id": 1}` |
| No fields to update | `{"error": "No updates provided"}` |
| Empty title | `{"error": "Title cannot be empty"}` |

---

## Agent Integration

### System Prompt Guidelines

The OpenAI Agents SDK agent should use these tools based on user intent:

| User Intent | Tool to Invoke |
|-------------|----------------|
| "Add a task...", "I need to remember...", "Create..." | add_task |
| "Show me...", "What's pending?", "List..." | list_tasks |
| "Mark as complete", "Done with...", "Finished..." | complete_task |
| "Delete...", "Remove...", "Cancel..." | delete_task |
| "Change...", "Update...", "Rename..." | update_task |

### Response Generation

After tool execution, the agent should:
1. Acknowledge the action with a friendly message
2. Include relevant details (task title, count, etc.)
3. Offer follow-up suggestions when appropriate

Example agent responses:
- add_task: "I've added '{title}' to your task list!"
- list_tasks: "Here are your {count} tasks: ..."
- complete_task: "Nice work! '{title}' is marked as complete."
- delete_task: "'{title}' has been removed from your list."
- update_task: "I've updated '{title}' for you."

---

## Security Notes

1. **User Isolation**: All tools receive user_id but MUST verify against authenticated user
2. **Input Validation**: Validate all string lengths before database operations
3. **Error Messages**: Never expose internal errors; use generic "Task not found" for unauthorized access
4. **Logging**: Log tool invocations for audit trail (without sensitive data)
