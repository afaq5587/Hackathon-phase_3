---
description: Create comprehensive tests for backend code including unit, integration, and API contract tests
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse testing requirements** from user input:
   - What to test (service, API endpoint, MCP tool, model)
   - Test type (unit, integration, contract, e2e)
   - Test scenarios (happy path, edge cases, errors)
   - Coverage requirements

2. **Verify project structure**:
   - Check `backend/tests/` directory exists
   - Verify pytest is installed (`backend/requirements.txt`)
   - Check for pytest configuration (`pytest.ini` or `pyproject.toml`)
   - Review existing test patterns

3. **Determine test type and location**:
   - **Unit tests**: `backend/tests/unit/test_{module}.py` - Test individual functions/classes in isolation
   - **Integration tests**: `backend/tests/integration/test_{feature}.py` - Test multiple components together
   - **Contract tests**: `backend/tests/contract/test_{api}.py` - Test API contracts and schemas
   - **E2E tests**: `backend/tests/e2e/test_{workflow}.py` - Test complete user workflows

4. **Create test file structure**:
   ```python
   """
   Tests for {module/feature}

   Test Coverage:
   - {list test scenarios}
   """

   import pytest
   from httpx import AsyncClient
   from sqlalchemy.ext.asyncio import AsyncSession

   # Import what we're testing
   from src.{module} import {Component}


   @pytest.fixture
   async def sample_data():
       """Fixture providing test data."""
       return {...}


   class Test{Component}:
       """Test suite for {Component}."""

       async def test_{scenario}_success(self, ...):
           """Test {scenario} succeeds with valid input."""
           pass

       async def test_{scenario}_failure(self, ...):
           """Test {scenario} fails with invalid input."""
           pass
   ```

5. **Create test fixtures**:
   - Create `backend/tests/conftest.py` for shared fixtures
   - Database fixtures (test database, session)
   - Authentication fixtures (mock users, tokens)
   - Data fixtures (sample tasks, conversations)
   - Client fixtures (test HTTP client)

6. **Write unit tests for services**:
   ```python
   """Unit tests for TaskService"""

   import pytest
   from sqlalchemy.ext.asyncio import AsyncSession

   from src.services.task_service import TaskService
   from src.models.task import TaskCreate, TaskUpdate


   @pytest.mark.asyncio
   class TestTaskService:
       """Test TaskService methods."""

       async def test_create_task_success(
           self,
           db_session: AsyncSession,
           test_user_id: str
       ):
           """Test creating a task successfully."""
           # Arrange
           task_data = TaskCreate(
               title="Test Task",
               description="Test Description"
           )

           # Act
           task = await TaskService.create(db_session, task_data, test_user_id)

           # Assert
           assert task.id is not None
           assert task.title == "Test Task"
           assert task.user_id == test_user_id
           assert task.completed is False

       async def test_get_task_not_found(
           self,
           db_session: AsyncSession,
           test_user_id: str
       ):
           """Test getting non-existent task returns None."""
           # Act
           task = await TaskService.get_by_id(db_session, 99999, test_user_id)

           # Assert
           assert task is None

       async def test_user_isolation(
           self,
           db_session: AsyncSession,
           test_user_id: str,
           other_user_id: str
       ):
           """Test users can't access other users' tasks."""
           # Arrange - create task for user1
           task_data = TaskCreate(title="User 1 Task")
           task = await TaskService.create(db_session, task_data, test_user_id)

           # Act - try to get as user2
           result = await TaskService.get_by_id(db_session, task.id, other_user_id)

           # Assert
           assert result is None  # User 2 can't see User 1's task
   ```

7. **Write integration tests for API endpoints**:
   ```python
   """Integration tests for task API endpoints"""

   import pytest
   from httpx import AsyncClient
   from fastapi import status


   @pytest.mark.asyncio
   class TestTaskAPI:
       """Test task API endpoints."""

       async def test_create_task_api(
           self,
           client: AsyncClient,
           auth_headers: dict,
           test_user_id: str
       ):
           """Test POST /api/{user_id}/tasks endpoint."""
           # Arrange
           payload = {
               "title": "Buy groceries",
               "description": "Milk, eggs, bread"
           }

           # Act
           response = await client.post(
               f"/api/{test_user_id}/tasks",
               json=payload,
               headers=auth_headers
           )

           # Assert
           assert response.status_code == status.HTTP_201_CREATED
           data = response.json()
           assert data["title"] == "Buy groceries"
           assert data["completed"] is False
           assert "id" in data

       async def test_create_task_missing_title(
           self,
           client: AsyncClient,
           auth_headers: dict,
           test_user_id: str
       ):
           """Test validation error for missing title."""
           # Act
           response = await client.post(
               f"/api/{test_user_id}/tasks",
               json={"description": "No title"},
               headers=auth_headers
           )

           # Assert
           assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

       async def test_unauthorized_access(
           self,
           client: AsyncClient,
           test_user_id: str
       ):
           """Test endpoint requires authentication."""
           # Act - no auth headers
           response = await client.get(f"/api/{test_user_id}/tasks")

           # Assert
           assert response.status_code == status.HTTP_401_UNAUTHORIZED
   ```

8. **Write contract tests for MCP tools**:
   ```python
   """Contract tests for MCP tools"""

   import pytest
   from sqlalchemy.ext.asyncio import AsyncSession

   from src.mcp.tools.add_task import add_task
   from src.mcp.tools.list_tasks import list_tasks


   @pytest.mark.asyncio
   class TestMCPTools:
       """Test MCP tool contracts."""

       async def test_add_task_contract(
           self,
           db_session: AsyncSession,
           test_user_id: str
       ):
           """Test add_task returns correct schema."""
           # Act
           result = await add_task(
               db_session,
               test_user_id,
               title="Test Task",
               description="Test"
           )

           # Assert - verify contract fields
           assert "success" in result
           assert "message" in result
           assert result["success"] is True
           assert "data" in result
           assert "id" in result["data"]
           assert result["data"]["title"] == "Test Task"

       async def test_add_task_error_contract(
           self,
           db_session: AsyncSession,
           test_user_id: str
       ):
           """Test add_task error response schema."""
           # Act - missing required field
           result = await add_task(db_session, test_user_id)

           # Assert - verify error contract
           assert "success" in result
           assert "message" in result
           assert "error" in result
           assert result["success"] is False
           assert isinstance(result["message"], str)
   ```

9. **Add test fixtures in conftest.py**:
   ```python
   """Shared test fixtures"""

   import pytest
   import pytest_asyncio
   from httpx import AsyncClient
   from sqlalchemy.ext.asyncio import (
       AsyncSession,
       create_async_engine,
       async_sessionmaker
   )
   from sqlmodel import SQLModel

   from src.main import app
   from src.db import get_db


   @pytest.fixture(scope="session")
   def test_database_url():
       """Test database URL (SQLite in memory)."""
       return "sqlite+aiosqlite:///:memory:"


   @pytest_asyncio.fixture(scope="function")
   async def db_session(test_database_url):
       """Create test database session."""
       engine = create_async_engine(test_database_url)

       # Create all tables
       async with engine.begin() as conn:
           await conn.run_sync(SQLModel.metadata.create_all)

       # Create session
       async_session = async_sessionmaker(
           engine,
           class_=AsyncSession,
           expire_on_commit=False
       )

       async with async_session() as session:
           yield session

       # Cleanup
       await engine.dispose()


   @pytest.fixture
   def test_user_id():
       """Test user ID."""
       return "test-user-123"


   @pytest.fixture
   def other_user_id():
       """Another test user ID for isolation tests."""
       return "other-user-456"


   @pytest.fixture
   def auth_headers(test_user_id):
       """Mock authentication headers."""
       return {
           "Authorization": f"Bearer mock-jwt-token-{test_user_id}"
       }


   @pytest_asyncio.fixture
   async def client(db_session):
       """Test HTTP client."""
       # Override database dependency
       async def override_get_db():
           yield db_session

       app.dependency_overrides[get_db] = override_get_db

       async with AsyncClient(app=app, base_url="http://test") as ac:
           yield ac

       app.dependency_overrides.clear()
   ```

10. **Add pytest configuration**:
    Create `backend/pytest.ini`:
    ```ini
    [pytest]
    testpaths = tests
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    asyncio_mode = auto
    addopts =
        -v
        --tb=short
        --strict-markers
        --disable-warnings
    markers =
        asyncio: mark test as async
        unit: unit tests
        integration: integration tests
        contract: contract tests
        slow: slow running tests
    ```

11. **Testing checklist**:
    - [ ] Tests follow AAA pattern (Arrange, Act, Assert)
    - [ ] Each test is independent and isolated
    - [ ] Test names describe what they test
    - [ ] Happy path scenarios covered
    - [ ] Error cases covered
    - [ ] Edge cases covered
    - [ ] User isolation tested
    - [ ] All assertions are meaningful
    - [ ] Tests are fast and don't depend on external services
    - [ ] Fixtures reused appropriately

12. **Run tests**:
    ```bash
    # Run all tests
    pytest backend/tests/

    # Run specific test file
    pytest backend/tests/unit/test_task_service.py

    # Run with coverage
    pytest --cov=src --cov-report=html backend/tests/

    # Run only unit tests
    pytest -m unit backend/tests/

    # Run with verbose output
    pytest -v backend/tests/
    ```

## Example Usage

```bash
# Create tests for a service
/backend.test Create unit tests for TaskService with CRUD operations and user isolation

# Create API integration tests
/backend.test Create integration tests for chat API endpoint

# Create MCP contract tests
/backend.test Create contract tests for all MCP tools (add_task, list_tasks, complete_task)
```

## Test Categories

### Unit Tests
- Test individual functions/methods in isolation
- Mock external dependencies
- Fast execution
- High code coverage

### Integration Tests
- Test multiple components together
- Use real database (test DB)
- Test API endpoints end-to-end
- Verify component interactions

### Contract Tests
- Verify API contracts (request/response schemas)
- Validate MCP tool interfaces
- Ensure backwards compatibility
- Test error response formats

### E2E Tests
- Test complete user workflows
- Simulate real user interactions
- Test across multiple systems
- Slower but high confidence

## Best Practices

- Write tests before or alongside code (TDD)
- Keep tests simple and focused
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Test edge cases and error scenarios
- Ensure tests are deterministic (no flaky tests)
- Use fixtures for reusable test data
- Mock external services and APIs
- Test user data isolation
- Aim for high coverage but focus on critical paths
- Run tests frequently during development
- Keep tests fast (< 1 second per test ideally)

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (test implementation work)
2) Generate Title: 3–7 words describing the tests created
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
