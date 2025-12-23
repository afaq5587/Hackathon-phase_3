# Claude Code Agents & Skills - Complete Setup

This directory contains a comprehensive development system with specialized agents and skills for full-stack development.

## 📁 Directory Structure

```
.claude/
├── agents/                      # Specialized development agents
│   ├── backend-developer.md     # Backend Python/FastAPI expert
│   ├── frontend-designer.md     # Frontend React/Next.js expert
│   └── backend-agent-creator.md # Agent creation tool
│
├── skills/                      # Development skills/commands
│   ├── backend.*.md             # Backend skills (6 skills)
│   ├── frontend.*.md            # Frontend skills (5 skills)
│   ├── README.md                # Backend skills guide
│   └── FRONTEND_README.md       # Frontend skills guide
│
├── commands/                    # Project management skills
│   └── sp.*.md                  # Spec-driven development commands
│
├── BACKEND_SETUP.md            # Backend setup documentation
├── FRONTEND_SETUP.md           # Frontend setup documentation
└── README.md                    # This file
```

---

## 🤖 Available Agents

### 1. Backend Developer Agent
**File**: `agents/backend-developer.md`

Expert in Python, FastAPI, SQLModel, and PostgreSQL development.

**Skills Used**:
- `/backend.model` - Database models
- `/backend.migration` - Schema migrations
- `/backend.service` - Business logic services
- `/backend.api` - REST API endpoints
- `/backend.mcp` - AI agent tools
- `/backend.test` - Backend testing

**Best For**: API development, database design, backend features

---

### 2. Frontend Designer Agent
**File**: `agents/frontend-designer.md`

Expert in React, Next.js, TypeScript, and Tailwind CSS.

**Skills Used**:
- `/frontend.component` - React components
- `/frontend.page` - Next.js pages
- `/frontend.hook` - Custom hooks
- `/frontend.api` - API clients
- `/frontend.test` - Frontend testing

**Best For**: UI/UX design, component development, frontend features

---

### 3. Backend Agent Creator
**File**: `agents/backend-agent-creator.md`

Creates new specialized backend agent configurations.

**Best For**: Creating custom agents for specific backend patterns

---

## 🛠️ Available Skills

### Backend Skills (6 Total)

| Skill | Purpose | Example |
|-------|---------|---------|
| `/backend.model` | Create database models | `Create Task model with fields` |
| `/backend.migration` | Database migrations | `Add priority field to tasks` |
| `/backend.service` | Business logic services | `Create TaskService with CRUD` |
| `/backend.api` | REST API endpoints | `POST /api/{user_id}/tasks` |
| `/backend.mcp` | MCP tools for AI | `add_task tool` |
| `/backend.test` | Backend testing | `Test TaskService methods` |

### Frontend Skills (5 Total)

| Skill | Purpose | Example |
|-------|---------|---------|
| `/frontend.component` | React components | `Create Button component` |
| `/frontend.page` | Next.js pages | `Create chat page at /chat` |
| `/frontend.hook` | Custom hooks | `Create useChat hook` |
| `/frontend.api` | API client functions | `Create getTasks function` |
| `/frontend.test` | Frontend testing | `Test Button component` |

---

## 🚀 Quick Start Guide

### Backend Development

```bash
# Complete CRUD feature implementation
/backend.model Create Task with title, description, completed
/backend.migration Create tasks table with indexes
/backend.service Create TaskService with CRUD operations
/backend.api POST /api/{user_id}/tasks
/backend.api GET /api/{user_id}/tasks
/backend.test Create tests for TaskService and API
```

### Frontend Development

```bash
# Complete chat interface
/frontend.component Create ChatInput, MessageBubble, MessageList
/frontend.hook Create useChat for state management
/frontend.page Create chat page at /chat
/frontend.test Create tests for chat components
```

### Full-Stack Feature

```bash
# Backend
/backend.model Create Task model
/backend.service Create TaskService
/backend.api Create task API endpoints
/backend.mcp Create add_task, list_tasks MCP tools

# Frontend
/frontend.component Create TaskList, TaskItem components
/frontend.hook Create useTasks hook
/frontend.page Create tasks page at /tasks
/frontend.api Create task API functions

# Tests
/backend.test Test TaskService and API
/frontend.test Test task components and hook
```

---

## 📖 Documentation

### Detailed Guides
- **Backend**: See `BACKEND_SETUP.md` for complete backend documentation
- **Frontend**: See `FRONTEND_SETUP.md` for complete frontend documentation

### Skill Documentation
- **Backend Skills**: See `skills/README.md`
- **Frontend Skills**: See `skills/FRONTEND_README.md`
- **Individual Skills**: Each `skills/*.md` file contains detailed instructions

---

## 🎯 Development Workflow

### Standard Feature Implementation

1. **Plan** - Define requirements and architecture
2. **Backend** - Implement data models, services, and APIs
3. **Frontend** - Create UI components and pages
4. **Integration** - Connect frontend to backend
5. **Testing** - Write comprehensive tests
6. **Polish** - Refine UX and performance

### Using Agents

```bash
# Launch backend agent for API development
# (Use Task tool with backend-developer agent)

# Launch frontend agent for UI development
# (Use Task tool with frontend-designer agent)
```

---

## 🏗️ Project Architecture

### Backend Stack
- Python 3.13+
- FastAPI
- SQLModel
- PostgreSQL (Neon)
- OpenAI Agents SDK
- MCP Protocol
- pytest

### Frontend Stack
- Next.js 16+ (App Router)
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- Better Auth
- React Testing Library
- Jest

---

## 🔐 Code Standards

### Backend Standards
- ✅ Type hints on all functions
- ✅ Async/await for I/O operations
- ✅ User data isolation (always filter by user_id)
- ✅ Comprehensive error handling
- ✅ SQLModel for database models
- ✅ Pydantic for validation
- ✅ pytest for testing

### Frontend Standards
- ✅ TypeScript strict mode
- ✅ Functional components with hooks
- ✅ Tailwind CSS for styling
- ✅ WCAG AA accessibility
- ✅ Mobile-first responsive design
- ✅ Component composition
- ✅ React Testing Library for tests

---

## ✅ Features

### Backend Features
- Database modeling and migrations
- RESTful API development
- Service layer architecture
- MCP tools for AI agents
- Authentication and authorization
- Comprehensive testing

### Frontend Features
- Component-based architecture
- Server and Client components
- Custom React hooks
- API integration
- Responsive design
- Accessibility (WCAG AA)
- Performance optimization

---

## 📊 Statistics

- **Total Agents**: 3
- **Total Skills**: 11 (6 backend + 5 frontend)
- **Documentation Files**: 5
- **Lines of Code**: ~10,000+ in documentation and examples

---

## 🆘 Getting Help

1. **Skill Documentation**: Check individual skill .md files
2. **Setup Guides**: See BACKEND_SETUP.md and FRONTEND_SETUP.md
3. **Examples**: Each skill includes real-world examples
4. **Project Specs**: Check `specs/` directory for requirements

---

## 🎓 Best Practices

### Development
1. Start with backend models and APIs
2. Build frontend components and hooks
3. Integrate frontend with backend
4. Write tests for all features
5. Optimize performance
6. Ensure accessibility

### Code Quality
1. Use TypeScript/type hints
2. Follow naming conventions
3. Write clear docstrings/comments
4. Handle errors gracefully
5. Test edge cases
6. Keep functions focused

### Security
1. Always validate user input
2. Enforce user data isolation
3. Use authentication on protected routes
4. Sanitize data for display
5. Use HTTPS in production
6. Never commit secrets

---

## 🚀 Next Steps

1. **Review Documentation**: Read BACKEND_SETUP.md and FRONTEND_SETUP.md
2. **Try Skills**: Use `/backend.model` or `/frontend.component` to test
3. **Build Features**: Follow the workflow to implement complete features
4. **Write Tests**: Ensure quality with comprehensive testing
5. **Deploy**: Use the deployment guides in the project root

---

**Complete Development System Ready! 🎉**

You have everything needed for full-stack development with:
- ✅ Backend and Frontend agents
- ✅ 11 specialized skills
- ✅ Comprehensive documentation
- ✅ Real-world examples
- ✅ Best practices and standards
- ✅ Testing frameworks

Happy coding! 🚀
