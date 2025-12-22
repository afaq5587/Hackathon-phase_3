# Phase 3: AI-Powered Todo Chatbot

An AI-powered todo management chatbot with a beautiful, responsive frontend. Users can create, view, complete, delete, and update tasks using natural language conversation.

## Features

- **Natural Language Task Management**: Create tasks by simply typing what you need to do
- **Smart Task Operations**: List, complete, delete, and update tasks via chat
- **Beautiful Chat Interface**: Modern, responsive UI with typing indicators
- **Conversation Persistence**: Chat history persists across sessions
- **WCAG AA Compliant**: Accessible color contrast and keyboard navigation

## Tech Stack

### Backend
- Python 3.13+
- FastAPI
- SQLModel (ORM)
- OpenAI Agents SDK
- Official MCP SDK
- Neon PostgreSQL

### Frontend
- Next.js 15+
- TypeScript
- React 19
- Tailwind CSS
- Better Auth (JWT)

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.13+
- Docker (optional)
- Neon PostgreSQL database

### 1. Clone and Setup

```bash
cd phase_3
cp .env.example .env
# Edit .env with your credentials
```

### 2. Configure Environment

Edit `.env` with your credentials:
```
DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars
OPENAI_API_KEY=sk-your-openai-api-key
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up --build
```

### 4. Or Run Locally

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

### 5. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
phase_3/
├── backend/
│   ├── src/
│   │   ├── api/          # FastAPI routes
│   │   ├── agent/        # OpenAI agent
│   │   ├── mcp/          # MCP tools
│   │   ├── models/       # SQLModel models
│   │   ├── services/     # Business logic
│   │   └── main.py       # Entry point
│   └── migrations/       # SQL migrations
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js pages
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities
│   │   └── styles/       # CSS
│   └── tailwind.config.js
├── specs/                # Feature specifications
└── docker-compose.yml    # Docker setup
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/{user_id}/chat | Send chat message |
| GET | /api/{user_id}/conversations | List conversations |
| GET | /api/{user_id}/conversations/{id}/messages | Get messages |
| GET | /health | Health check |

## MCP Tools

| Tool | Description |
|------|-------------|
| add_task | Create a new task |
| list_tasks | List tasks (all/pending/completed) |
| complete_task | Mark task as complete |
| delete_task | Remove a task |
| update_task | Update task title/description |

## Usage Examples

Try these natural language commands in the chat:

- "Add a task to buy groceries"
- "Show me all my tasks"
- "What's pending?"
- "Mark task 1 as complete"
- "Delete task 2"
- "Change task 3 to 'Buy fruits'"

## Development

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Linting
```bash
# Backend
cd backend
ruff check .

# Frontend
cd frontend
npm run lint
```

## License

MIT License - Hackathon Phase 3 Project
