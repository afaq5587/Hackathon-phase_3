# Backend Development Skills

This directory contains specialized skills for backend development tasks using the FastAPI + SQLModel + Python stack.

## Available Skills

### 1. `/backend.api` - API Endpoint Creation
Create FastAPI REST endpoints with proper validation, error handling, and documentation.

**When to use:**
- Creating new API endpoints
- Adding CRUD operations to existing resources
- Implementing custom API logic

**Example:**
```bash
/backend.api POST /api/{user_id}/tasks - Create a new task endpoint
```

---

### 2. `/backend.model` - Database Model Creation
Create SQLModel database models with proper fields, validation, and relationships.

**When to use:**
- Defining new database tables
- Adding fields to existing models
- Setting up relationships between models

**Example:**
```bash
/backend.model Create Task model with title, description, completed, user_id
```

---

### 3. `/backend.service` - Service Layer Creation
Create service classes with business logic, database operations, and proper error handling.

**When to use:**
- Implementing business logic
- Creating CRUD operations for models
- Adding domain-specific operations

**Example:**
```bash
/backend.service Create TaskService for task management with CRUD operations
```

---

### 4. `/backend.migration` - Database Migration
Create database migrations for SQLModel schema changes with proper validation and rollback.

**When to use:**
- Altering database schema (add/remove columns)
- Creating new tables
- Adding indexes for performance

**Example:**
```bash
/backend.migration Add priority field to tasks (low, medium, high, urgent)
```

---

### 5. `/backend.mcp` - MCP Tool Creation
Create MCP (Model Context Protocol) tools for AI agents to interact with backend services.

**When to use:**
- Creating new AI agent capabilities
- Exposing backend operations to AI
- Implementing conversational interfaces

**Example:**
```bash
/backend.mcp add_task - Creates a new task with title and optional description
```

---

### 6. `/backend.test` - Backend Testing
Create comprehensive tests including unit, integration, and API contract tests.

**When to use:**
- Testing new features
- Ensuring code quality
- Validating API contracts

**Example:**
```bash
/backend.test Create unit tests for TaskService with CRUD operations
```

---

## Skill Development Workflow

### Typical Feature Implementation Flow:

1. **Create the Model** (`/backend.model`)
   - Define the database schema
   - Set up fields, validation, and relationships

2. **Create Migration** (`/backend.migration`)
   - Generate migration for the new model
   - Run migration to create table

3. **Create Service Layer** (`/backend.service`)
   - Implement business logic
   - Add CRUD operations and domain methods

4. **Create API Endpoints** (`/backend.api`)
   - Expose operations via REST API
   - Add validation and error handling

5. **Create MCP Tools** (`/backend.mcp`) *(if needed)*
   - Enable AI agent interaction
   - Implement conversational interface

6. **Write Tests** (`/backend.test`)
   - Unit tests for services
   - Integration tests for APIs
   - Contract tests for MCP tools

---

## Project Stack

- **Language**: Python 3.13+
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **AI**: OpenAI Agents SDK
- **Protocol**: MCP (Model Context Protocol)
- **Testing**: pytest, httpx

---

## Code Standards

All skills follow these standards:

- **Type Hints**: Required on all functions and parameters
- **Async/Await**: Use for all database and I/O operations
- **User Isolation**: Always filter by `user_id`
- **Error Handling**: Graceful error handling with clear messages
- **Documentation**: Comprehensive docstrings
- **Validation**: Pydantic models for all inputs
- **Testing**: Test coverage for all features
- **Security**: Input validation, SQL injection prevention, authentication

---

## Quick Reference

### Common Patterns

**Create a complete feature (Task Management):**
```bash
# 1. Model
/backend.model Create Task with title, description, completed, user_id, timestamps

# 2. Migration
/backend.migration Create tasks table with indexes on user_id and (user_id, completed)

# 3. Service
/backend.service Create TaskService with create, get, list, update, delete, mark_completed

# 4. API
/backend.api POST /api/{user_id}/tasks - Create task
/backend.api GET /api/{user_id}/tasks - List tasks
/backend.api GET /api/{user_id}/tasks/{id} - Get task
/backend.api PUT /api/{user_id}/tasks/{id} - Update task
/backend.api DELETE /api/{user_id}/tasks/{id} - Delete task

# 5. MCP Tools (for AI chatbot)
/backend.mcp add_task - Create task via natural language
/backend.mcp list_tasks - List tasks with filtering
/backend.mcp complete_task - Mark task as complete

# 6. Tests
/backend.test Create unit tests for TaskService
/backend.test Create integration tests for task API endpoints
/backend.test Create contract tests for task MCP tools
```

---

## File Locations

```
backend/
├── src/
│   ├── models/          # SQLModel definitions
│   │   ├── task.py
│   │   └── __init__.py
│   ├── services/        # Business logic
│   │   ├── task_service.py
│   │   └── __init__.py
│   ├── api/             # FastAPI endpoints
│   │   ├── tasks.py
│   │   └── __init__.py
│   ├── mcp/             # MCP tools for AI
│   │   ├── tools/
│   │   │   ├── add_task.py
│   │   │   └── __init__.py
│   │   └── server.py
│   ├── db.py            # Database connection
│   ├── config.py        # Configuration
│   └── main.py          # FastAPI app
├── migrations/          # Database migrations
│   └── 001_create_tasks.py
└── tests/               # Test suite
    ├── unit/
    ├── integration/
    ├── contract/
    └── conftest.py
```

---

## Additional Resources

- **Project Guidelines**: `backend/CLAUDE.md`
- **API Contracts**: `specs/*/contracts/`
- **Data Models**: `specs/*/data-model.md`
- **Architecture**: `specs/*/plan.md`
- **Requirements**: `specs/*/spec.md`

---

## Support

For questions or issues with skills:
1. Check the skill's markdown file for detailed instructions
2. Review example implementations in the skill documentation
3. Consult project specifications in `specs/` directory
4. Follow existing code patterns in `backend/src/`
