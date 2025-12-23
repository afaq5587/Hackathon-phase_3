# Backend Development Setup Complete ✅

This document describes the backend development agent and skills system that has been configured for this project.

## Overview

A comprehensive backend development system has been created with:
- **1 Backend Developer Agent** - Expert agent that uses skills to implement features
- **6 Backend Skills** - Specialized tools for common backend tasks
- **Complete Documentation** - Usage guides and examples

---

## 🤖 Backend Developer Agent

**Agent Name**: `backend-developer`

**Location**: `.claude/agents/backend-developer.md`

**Purpose**: Expert backend developer specializing in Python/FastAPI/SQLModel development. Handles complete backend feature implementation following project standards.

**Capabilities**:
- Database model creation and migration
- Service layer implementation with business logic
- REST API endpoint development
- MCP tool creation for AI agents
- Comprehensive testing (unit, integration, contract)
- Security and performance optimization

**How to Use**:
```bash
# The main Claude assistant can invoke this agent when needed
# Or you can use the Task tool to launch it explicitly
```

---

## 🛠️ Backend Skills

All skills are located in `.claude/skills/` and can be invoked directly:

### 1. `/backend.model` - Database Model Creation
Create SQLModel database models with proper fields, validation, and relationships.

**Example**:
```bash
/backend.model Create Task model with title, description, completed, priority, due_date, user_id
```

**Creates**:
- Model class with table definition
- Pydantic schemas (Create, Update, Read)
- Field validation and constraints
- Indexes and relationships

---

### 2. `/backend.migration` - Database Migration
Create database migrations for schema changes with proper validation and rollback.

**Example**:
```bash
/backend.migration Add priority and due_date columns to tasks table
```

**Creates**:
- Migration script with upgrade/downgrade
- SQL statements for schema changes
- Index creation commands
- Data migration logic (if needed)

---

### 3. `/backend.service` - Service Layer Creation
Create service classes with business logic, database operations, and error handling.

**Example**:
```bash
/backend.service Create TaskService with CRUD operations and mark_completed method
```

**Creates**:
- Service class with static methods
- CRUD operations (create, read, update, delete)
- Business logic methods
- User isolation enforcement
- Error handling

---

### 4. `/backend.api` - API Endpoint Creation
Create FastAPI REST endpoints with proper validation, authentication, and documentation.

**Example**:
```bash
/backend.api POST /api/{user_id}/tasks - Create task endpoint
```

**Creates**:
- Route handler with proper HTTP method
- Request/response validation
- Authentication and authorization
- Error handling with proper status codes
- API documentation

---

### 5. `/backend.mcp` - MCP Tool Creation
Create MCP (Model Context Protocol) tools for AI agents to interact with backend services.

**Example**:
```bash
/backend.mcp add_task - Create MCP tool for AI to add tasks
```

**Creates**:
- MCP tool function with standardized interface
- Input parameter validation
- Service layer integration
- Standardized response format
- User-friendly messages for AI

---

### 6. `/backend.test` - Backend Testing
Create comprehensive tests including unit, integration, and contract tests.

**Example**:
```bash
/backend.test Create unit tests for TaskService and integration tests for task API
```

**Creates**:
- Unit tests for service methods
- Integration tests for API endpoints
- Contract tests for MCP tools
- Test fixtures and configuration
- pytest configuration

---

## 📋 Complete Feature Implementation Workflow

To implement a complete backend feature (e.g., Task Management with AI chatbot):

```bash
# Step 1: Create the database model
/backend.model Create Task with title, description, completed, priority, due_date, user_id

# Step 2: Create database migration
/backend.migration Create tasks table with indexes on user_id, (user_id, completed), (user_id, priority)

# Step 3: Create service layer
/backend.service Create TaskService with create, get_by_id, list_by_user, update, delete, mark_completed

# Step 4: Create REST API endpoints
/backend.api POST /api/{user_id}/tasks - Create task
/backend.api GET /api/{user_id}/tasks - List tasks with filtering
/backend.api GET /api/{user_id}/tasks/{id} - Get task by ID
/backend.api PUT /api/{user_id}/tasks/{id} - Update task
/backend.api DELETE /api/{user_id}/tasks/{id} - Delete task
/backend.api PATCH /api/{user_id}/tasks/{id}/complete - Mark task complete

# Step 5: Create MCP tools for AI chatbot (if needed)
/backend.mcp add_task - Create task via natural language
/backend.mcp list_tasks - List tasks with status filter
/backend.mcp complete_task - Mark task as complete
/backend.mcp update_task - Update task details
/backend.mcp delete_task - Delete task

# Step 6: Create comprehensive tests
/backend.test Create unit tests for TaskService
/backend.test Create integration tests for task API endpoints
/backend.test Create contract tests for task MCP tools
```

---

## 🏗️ Project Structure

```
backend/
├── src/
│   ├── models/              # SQLModel database models
│   │   ├── task.py          # Task model with schemas
│   │   ├── conversation.py  # Conversation model
│   │   ├── message.py       # Message model
│   │   └── __init__.py      # Model exports
│   │
│   ├── services/            # Business logic services
│   │   ├── task_service.py      # Task CRUD + business logic
│   │   ├── conversation_service.py
│   │   ├── chat_service.py      # Chat orchestration
│   │   └── __init__.py
│   │
│   ├── api/                 # FastAPI endpoints
│   │   ├── tasks.py         # Task REST endpoints
│   │   ├── chat.py          # Chat endpoints
│   │   ├── auth.py          # Authentication middleware
│   │   ├── deps.py          # Dependency injection
│   │   └── __init__.py
│   │
│   ├── mcp/                 # MCP tools for AI
│   │   ├── tools/           # Individual MCP tools
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── update_task.py
│   │   │   ├── delete_task.py
│   │   │   └── __init__.py
│   │   └── server.py        # MCP server setup
│   │
│   ├── agent/               # AI agent configuration
│   │   ├── todo_agent.py    # Todo chatbot agent
│   │   └── __init__.py
│   │
│   ├── db.py                # Database connection
│   ├── config.py            # Environment configuration
│   └── main.py              # FastAPI application
│
├── migrations/              # Database migrations
│   ├── 001_create_tasks.py
│   ├── 002_create_conversations.py
│   └── __init__.py
│
└── tests/                   # Test suite
    ├── unit/                # Unit tests
    │   ├── test_task_service.py
    │   └── test_conversation_service.py
    ├── integration/         # Integration tests
    │   ├── test_task_api.py
    │   └── test_chat_api.py
    ├── contract/            # Contract tests
    │   └── test_mcp_tools.py
    └── conftest.py          # Shared fixtures
```

---

## 🔐 Security Standards

All backend code must follow these security principles:

### User Isolation
```python
# ✅ ALWAYS filter by user_id
tasks = await db.execute(
    select(Task).where(
        Task.user_id == user_id,
        Task.completed == False
    )
)

# ❌ NEVER query without user_id
tasks = await db.execute(
    select(Task).where(Task.completed == False)
)
```

### Authentication
- All API endpoints require JWT validation
- User ID in JWT must match user_id in path parameter
- Use dependency injection for authentication

### Input Validation
- Use Pydantic models for all inputs
- Set max_length on string fields
- Use field validators for complex validation
- Sanitize user inputs

### SQL Injection Prevention
- Use SQLModel parameterized queries (automatic)
- Never concatenate user input into SQL strings
- Use Field() definitions for constraints

---

## 📊 Testing Standards

### Test Coverage Goals
- **80%+ overall coverage**
- **100% for critical paths** (authentication, data isolation)
- **All error cases covered**

### Test Types
1. **Unit Tests**: Test services in isolation
2. **Integration Tests**: Test API endpoints end-to-end
3. **Contract Tests**: Verify MCP tool interfaces
4. **E2E Tests**: Test complete user workflows

### Test Structure
```python
# AAA Pattern: Arrange, Act, Assert
async def test_create_task_success():
    # Arrange
    task_data = TaskCreate(title="Test Task")

    # Act
    task = await TaskService.create(db, task_data, user_id)

    # Assert
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.user_id == user_id
```

---

## 🚀 Technology Stack

- **Language**: Python 3.13+
- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.22+
- **Database**: PostgreSQL (Neon Serverless)
- **Validation**: Pydantic 2.0+
- **AI Integration**: OpenAI Agents SDK, MCP SDK
- **Testing**: pytest, pytest-asyncio, httpx
- **Development**: uvicorn, ruff, black

---

## 📚 Additional Resources

### Project Documentation
- **Backend Guidelines**: `backend/CLAUDE.md`
- **API Contracts**: `specs/001-ai-chatbot-frontend/contracts/`
- **Data Models**: `specs/001-ai-chatbot-frontend/data-model.md`
- **Architecture Plan**: `specs/001-ai-chatbot-frontend/plan.md`
- **Requirements**: `specs/001-ai-chatbot-frontend/spec.md`
- **Tasks**: `specs/001-ai-chatbot-frontend/tasks.md`

### Skills Documentation
- **Skills README**: `.claude/skills/README.md`
- **Individual Skills**: `.claude/skills/backend.*.md`

### Agent Documentation
- **Backend Developer**: `.claude/agents/backend-developer.md`
- **Agent Creator**: `.claude/agents/backend-agent-creator.md`

---

## 🎯 Quick Reference

### Common Commands

```bash
# Create a complete CRUD API
/backend.model Create {Entity} model
/backend.migration Create {entity} table
/backend.service Create {Entity}Service
/backend.api POST /api/{user_id}/{resource}
/backend.api GET /api/{user_id}/{resource}
/backend.test Create tests for {Entity}

# Add AI chatbot capability
/backend.mcp add_{entity} - Create via natural language
/backend.mcp list_{entities} - List with filtering
/backend.test Create contract tests for {entity} MCP tools

# Add field to existing model
/backend.migration Add {field} to {table}
/backend.model Update {Entity} with new field
/backend.service Update {Entity}Service methods
/backend.test Update tests for new field
```

---

## ✅ What's Been Set Up

- ✅ Backend Developer Agent configuration
- ✅ 6 specialized backend skills
- ✅ Complete documentation and examples
- ✅ Security standards and best practices
- ✅ Testing frameworks and patterns
- ✅ Development workflow and patterns
- ✅ Project structure guidelines

---

## 🎓 Usage Tips

1. **Use skills proactively**: Don't write code manually when a skill exists
2. **Follow the workflow**: Model → Migration → Service → API → MCP → Tests
3. **Test everything**: Write tests as you build features
4. **Enforce security**: Always filter by user_id
5. **Document code**: Add docstrings and type hints
6. **Follow patterns**: Check existing code for consistency
7. **Ask for clarification**: When requirements are unclear

---

## 🆘 Getting Help

If you need assistance:
1. Check the skill's markdown file for detailed instructions
2. Review examples in the skill documentation
3. Consult project specifications in `specs/` directory
4. Follow existing code patterns in `backend/src/`
5. Use the backend-developer agent for complex features

---

**System Ready for Backend Development! 🚀**

You now have a complete backend development system with agents and skills that follow project standards and best practices.
