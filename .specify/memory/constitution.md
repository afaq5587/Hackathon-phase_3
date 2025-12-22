<!--
  Sync Impact Report
  ===================
  Version change: 1.0.0 (initial)
  Modified principles: N/A (new constitution)
  Added sections:
    - Core Principles (6 principles)
    - Technology Stack Requirements
    - API & MCP Protocol Standards
    - Security & Authentication
    - Governance
  Removed sections: N/A
  Templates status:
    - plan-template.md: ✅ Compatible
    - spec-template.md: ✅ Compatible
    - tasks-template.md: ✅ Compatible
    - phr-template.prompt.md: ✅ Compatible
  Follow-up TODOs: None
-->

# Phase 3: AI-Powered Todo Chatbot Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All implementation MUST follow the Spec-Driven Development workflow: Specify → Plan → Tasks → Implement. No code generation without an approved spec. Agents MUST NOT write code manually; the spec MUST be refined until Claude Code generates correct output. Every implementation change MUST reference a task ID and trace back to the specification.

**Rationale**: The hackathon mandates spec-driven development with Claude Code and Spec-Kit Plus. Manual coding is prohibited.

### II. Stateless Architecture First

The chat endpoint and MCP server MUST be stateless. All conversation state, message history, and task data MUST persist to the Neon PostgreSQL database. Server restarts MUST NOT lose conversation context. Any request MUST be processable by any server instance.

**Rationale**: Phase 3 explicitly requires "Stateless chat endpoint that persists conversation state to database" for scalability, resilience, and horizontal scaling readiness.

### III. MCP-Native Tool Design

All task operations MUST be exposed as MCP tools using the Official MCP SDK. Tool interfaces MUST follow the documented schema: add_task, list_tasks, complete_task, delete_task, update_task. Each tool MUST accept user_id as a required parameter. Tool responses MUST include task_id, status, and title fields.

**Rationale**: Phase 3 architecture mandates MCP server with standardized tools for AI agent interaction.

### IV. Agent-First Conversation Flow

The OpenAI Agents SDK MUST orchestrate all chat interactions. The agent MUST: (1) Receive user message, (2) Fetch conversation history from database, (3) Build message array for agent, (4) Store user message, (5) Run agent with MCP tools, (6) Store assistant response, (7) Return response to client. The agent MUST confirm actions with friendly responses and handle errors gracefully.

**Rationale**: The conversation flow is explicitly defined in Phase 3 requirements for stateless request cycle processing.

### V. Authentication Continuity

All endpoints MUST require valid JWT tokens from Better Auth (Phase 2). Requests without tokens MUST receive 401 Unauthorized. Each user MUST only see/modify their own tasks and conversations. Token verification MUST use the shared BETTER_AUTH_SECRET between frontend and backend.

**Rationale**: Phase 3 builds on Phase 2's authentication infrastructure. User isolation is mandatory.

### VI. Monorepo Structure Compliance

The project MUST maintain the monorepo structure: /frontend (ChatKit UI), /backend (FastAPI + Agents SDK + MCP), /specs (specification files). Each directory MUST have its own CLAUDE.md for context. Root CLAUDE.md MUST reference AGENTS.md for cross-agent instructions.

**Rationale**: Hackathon mandates monorepo organization for Claude Code to navigate and edit both frontend and backend in a single context.

## Technology Stack Requirements

The following stack is mandatory for Phase 3 and MUST NOT be substituted:

| Component | Technology | Constraint |
|-----------|------------|------------|
| Frontend | OpenAI ChatKit | Required for chat UI |
| Backend | Python FastAPI | Required for API server |
| AI Framework | OpenAI Agents SDK | Required for agent logic |
| MCP Server | Official MCP SDK (Python) | Required for tool exposure |
| ORM | SQLModel | Required for database models |
| Database | Neon Serverless PostgreSQL | Required for persistence |
| Authentication | Better Auth (JWT) | Inherited from Phase 2 |

**Additional Requirements**:
- Database models MUST include: Task, Conversation, Message
- All models MUST include user_id for data isolation
- Conversation and Message models MUST support chat history reconstruction

## API & MCP Protocol Standards

### Chat API Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/{user_id}/chat | Send message & get AI response |

**Request Schema**:
- conversation_id (integer, optional): Existing conversation ID
- message (string, required): User's natural language message

**Response Schema**:
- conversation_id (integer): The conversation ID
- response (string): AI assistant's response
- tool_calls (array): List of MCP tools invoked

### MCP Tools Specification

All MCP tools MUST conform to the following interfaces:

1. **add_task**: Create a new task
   - Parameters: user_id (required), title (required), description (optional)
   - Returns: task_id, status, title

2. **list_tasks**: Retrieve tasks from the list
   - Parameters: user_id (required), status (optional: "all", "pending", "completed")
   - Returns: Array of task objects

3. **complete_task**: Mark a task as complete
   - Parameters: user_id (required), task_id (required)
   - Returns: task_id, status, title

4. **delete_task**: Remove a task from the list
   - Parameters: user_id (required), task_id (required)
   - Returns: task_id, status, title

5. **update_task**: Modify task title or description
   - Parameters: user_id (required), task_id (required), title (optional), description (optional)
   - Returns: task_id, status, title

## Security & Authentication

### Mandatory Security Controls

1. **JWT Validation**: All /api/{user_id}/chat endpoints MUST validate JWT tokens
2. **User Isolation**: Queries MUST filter by authenticated user_id
3. **Path-Parameter Match**: user_id in URL MUST match token's user_id
4. **No Hardcoded Secrets**: Use .env files for BETTER_AUTH_SECRET, OPENAI_API_KEY, DATABASE_URL
5. **Error Responses**: Security errors MUST return appropriate HTTP status codes (401, 403) without leaking internal details

### Environment Variables

Required environment variables for Phase 3:
- DATABASE_URL: Neon PostgreSQL connection string
- BETTER_AUTH_SECRET: Shared JWT signing secret
- OPENAI_API_KEY: OpenAI API key for Agents SDK
- NEXT_PUBLIC_OPENAI_DOMAIN_KEY: ChatKit domain key (production)

## Governance

### Amendment Process

1. Any principle change MUST be documented with rationale
2. Changes MUST be reviewed against hackathon requirements
3. Version MUST be incremented according to semantic versioning:
   - MAJOR: Backward incompatible principle removals/redefinitions
   - MINOR: New principle/section added or materially expanded
   - PATCH: Clarifications, wording, typo fixes

### Compliance Verification

1. All PRs MUST verify compliance with this constitution
2. Code reviews MUST check task ID references
3. MCP tool implementations MUST match the specification
4. Statelessness MUST be verified (no in-memory state across requests)

### Constitutional Hierarchy

Constitution > Specify > Plan > Tasks

If conflicts arise between spec files, this hierarchy determines precedence.

**Version**: 1.0.0 | **Ratified**: 2025-12-20 | **Last Amended**: 2025-12-20
