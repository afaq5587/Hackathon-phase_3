# Backend Development Guidelines

## Stack
- Python 3.13+
- FastAPI
- SQLModel (ORM)
- OpenAI Agents SDK (openai-agents) - https://openai.github.io/openai-agents-python/
- Official MCP SDK (Python)
- Neon PostgreSQL

## Project Structure
```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── services/        # Business logic services
│   ├── api/             # FastAPI routes and middleware
│   ├── mcp/             # MCP server and tools
│   │   └── tools/       # Individual MCP tool implementations
│   ├── agent/           # OpenAI Agents SDK agent definition
│   ├── db.py            # Database connection
│   ├── config.py        # Environment configuration
│   └── main.py          # FastAPI app entry point
├── tests/
│   ├── contract/        # API contract tests
│   ├── integration/     # Integration tests
│   └── unit/            # Unit tests
└── migrations/          # Database migrations
```

## Conventions
- Use async/await for all database operations
- All models include user_id for data isolation
- JWT validation required on all /api/{user_id}/ endpoints
- MCP tools must follow schema in specs/001-ai-chatbot-frontend/contracts/mcp-tools.md
- Stateless design: no in-memory state between requests

## Running
```bash
# Development
uvicorn src.main:app --reload --port 8000

# Tests
pytest tests/
```

## API Patterns
- All routes under `/api/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- User isolation enforced via JWT + path parameter match
