---
description: Create a new FastAPI REST endpoint with proper validation, error handling, and documentation
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse endpoint requirements** from user input:
   - HTTP method (GET, POST, PUT, DELETE, PATCH)
   - Endpoint path (e.g., `/api/{user_id}/tasks`)
   - Request body schema (if applicable)
   - Response schema
   - Authentication requirements
   - Query parameters and path parameters
   - Error cases to handle

2. **Verify project structure**:
   - Check that `backend/src/api/` exists
   - Check that required models exist in `backend/src/models/`
   - Check that required services exist in `backend/src/services/`
   - Verify database connection is configured in `backend/src/db.py`

3. **Create or update the API route file**:
   - File location: `backend/src/api/{resource}.py`
   - Import required dependencies:
     - `from fastapi import APIRouter, Depends, HTTPException, status`
     - `from sqlalchemy.ext.asyncio import AsyncSession`
     - Required models from `backend.src.models`
     - Required services from `backend.src.services`
     - Auth dependencies from `backend.src.api.deps`
   - Create APIRouter instance
   - Add route decorator with method, path, response_model, status_code

4. **Implement endpoint logic following FastAPI patterns**:
   - Use dependency injection for database session: `db: AsyncSession = Depends(get_db)`
   - Use dependency injection for authentication: `current_user: User = Depends(get_current_user)`
   - Validate user_id matches authenticated user (if applicable)
   - Use Pydantic models for request/response validation
   - Implement async/await for all database operations
   - Use proper HTTP status codes (200, 201, 204, 400, 401, 403, 404, 500)
   - Handle errors with HTTPException

5. **Add input validation**:
   - Use Pydantic Field validators
   - Check required fields are present
   - Validate data types and formats
   - Enforce business logic constraints
   - Return clear error messages with field-level details

6. **Add error handling**:
   - Catch database errors (IntegrityError, NoResultFound)
   - Handle business logic errors
   - Return appropriate HTTP status codes
   - Provide user-friendly error messages
   - Log errors for debugging

7. **Add docstring documentation**:
   - Describe endpoint purpose
   - Document parameters (path, query, body)
   - Document response structure
   - Document error cases
   - Include example requests/responses

8. **Register the router**:
   - Open `backend/src/api/__init__.py`
   - Import the new router
   - Include it in the main API router with prefix and tags

9. **Create corresponding Pydantic schemas** (if needed):
   - Request schema (e.g., `TaskCreate`, `TaskUpdate`)
   - Response schema (e.g., `TaskRead`)
   - Place in `backend/src/models/{resource}.py`
   - Use Field() for validation and documentation

10. **Validation checklist**:
    - [ ] Endpoint follows RESTful conventions
    - [ ] Uses proper HTTP methods and status codes
    - [ ] Implements authentication/authorization
    - [ ] Validates all inputs with Pydantic
    - [ ] Handles errors gracefully
    - [ ] Uses async/await for database operations
    - [ ] Has comprehensive docstrings
    - [ ] Follows project code style (type hints, formatting)
    - [ ] Is registered in the API router

11. **Testing recommendations**:
    - Suggest creating integration tests in `backend/tests/integration/`
    - Test successful requests with valid data
    - Test validation errors with invalid data
    - Test authentication/authorization
    - Test error cases (not found, server errors)

## Example Usage

```bash
# Create a new endpoint
/backend.api POST /api/{user_id}/tasks - Create a new task endpoint

# With detailed specification
/backend.api Create GET endpoint at /api/{user_id}/tasks/{task_id} that retrieves a single task by ID, validates user ownership, and returns 404 if not found
```

## Code Quality Standards

- Use Python type hints for all parameters and return types
- Follow async/await patterns consistently
- Use Pydantic models for all request/response data
- Implement proper error handling with HTTPException
- Add comprehensive docstrings
- Follow RESTful API conventions
- Ensure user data isolation (verify user_id)
- Use dependency injection for services and database

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (API implementation work)
2) Generate Title: 3–7 words describing the API endpoint created
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
