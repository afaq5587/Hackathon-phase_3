---
description: Create database migration for SQLModel schema changes with proper validation and rollback
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse migration requirements** from user input:
   - What schema changes are needed (new table, add column, modify column, drop column, add index, etc.)
   - Which models are affected
   - Data migration requirements (if any)
   - Backward compatibility considerations

2. **Analyze current schema state**:
   - Read all SQLModel models in `backend/src/models/`
   - Check existing migration files in `backend/migrations/`
   - Identify the latest migration number
   - Understand current database structure

3. **Design the migration**:
   - Determine migration type:
     - DDL (Data Definition): CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX
     - DML (Data Manipulation): UPDATE, INSERT, DELETE for data migration
   - Plan forward migration (upgrade) steps
   - Plan backward migration (downgrade) steps for rollback
   - Consider data safety and integrity constraints

4. **Create migration file**:
   - File naming: `backend/migrations/{sequence}_{description}.py`
   - Use sequential numbering (001, 002, 003, etc.)
   - Description should be clear and concise (e.g., `add_priority_to_tasks`)

5. **Implement migration structure**:
   ```python
   """
   Migration: {description}
   Created: {date}

   Changes:
   - {list of schema changes}
   """

   from sqlalchemy import text
   from sqlalchemy.ext.asyncio import AsyncSession

   async def upgrade(session: AsyncSession) -> None:
       """Apply forward migration."""
       # Implementation here
       pass

   async def downgrade(session: AsyncSession) -> None:
       """Rollback migration."""
       # Implementation here
       pass
   ```

6. **Write upgrade logic**:
   - Use raw SQL with `await session.execute(text(...))` for DDL
   - For complex data migrations, use SQLModel queries
   - Add proper error handling
   - Use transactions to ensure atomicity
   - Add validation checks before making changes
   - Include comments explaining each step

7. **Write downgrade logic**:
   - Reverse all changes made in upgrade
   - Preserve data where possible
   - Handle cases where downgrade may lose data
   - Add warnings for destructive operations

8. **Add safety checks**:
   - Check if migration already applied (idempotency)
   - Validate database state before migration
   - Add constraints after data population (not before)
   - Use IF EXISTS / IF NOT EXISTS where applicable
   - Add indexes after bulk inserts

9. **Update SQLModel models** (if needed):
   - Modify model classes in `backend/src/models/` to match new schema
   - Add/remove fields
   - Update Field() definitions with proper types and constraints
   - Update __tablename__ if table renamed
   - Add/update indexes and relationships

10. **Create migration runner** (if not exists):
    - Create `backend/migrations/__init__.py`
    - Implement `run_migrations()` function
    - Add migration tracking table
    - Support upgrade and downgrade operations

11. **Testing checklist**:
    - [ ] Migration runs successfully on clean database
    - [ ] Downgrade successfully reverses changes
    - [ ] Existing data preserved (if applicable)
    - [ ] All constraints and indexes created
    - [ ] No SQL syntax errors
    - [ ] Migration is idempotent (can run multiple times safely)
    - [ ] SQLModel models match new schema

12. **Documentation**:
    - Add migration description in docstring
    - Document any manual steps required
    - Note any data loss or breaking changes
    - Add rollback instructions

## Example Migrations

### Add column to existing table
```python
async def upgrade(session: AsyncSession) -> None:
    """Add priority column to tasks table."""
    await session.execute(text("""
        ALTER TABLE tasks
        ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium'
    """))
    await session.commit()

async def downgrade(session: AsyncSession) -> None:
    """Remove priority column from tasks table."""
    await session.execute(text("""
        ALTER TABLE tasks
        DROP COLUMN IF EXISTS priority
    """))
    await session.commit()
```

### Create new table
```python
async def upgrade(session: AsyncSession) -> None:
    """Create tags table."""
    await session.execute(text("""
        CREATE TABLE IF NOT EXISTS tags (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            color VARCHAR(7),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, name)
        )
    """))

    await session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_tags_user_id ON tags(user_id)
    """))
    await session.commit()

async def downgrade(session: AsyncSession) -> None:
    """Drop tags table."""
    await session.execute(text("DROP TABLE IF EXISTS tags CASCADE"))
    await session.commit()
```

### Add index
```python
async def upgrade(session: AsyncSession) -> None:
    """Add composite index for user tasks by status."""
    await session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_tasks_user_completed
        ON tasks(user_id, completed)
    """))
    await session.commit()

async def downgrade(session: AsyncSession) -> None:
    """Remove composite index."""
    await session.execute(text("""
        DROP INDEX IF EXISTS idx_tasks_user_completed
    """))
    await session.commit()
```

## Example Usage

```bash
# Add a new column
/backend.migration Add priority field to tasks (low, medium, high, urgent)

# Create a new table
/backend.migration Create tags table with name, color, and user_id

# Add an index
/backend.migration Add index on tasks(user_id, created_at) for performance
```

## Best Practices

- Always use IF EXISTS / IF NOT EXISTS for idempotency
- Test migrations on a copy of production data
- Keep migrations small and focused
- Never edit existing migrations after deployment
- Use transactions for atomic changes
- Add indexes after bulk data operations
- Consider performance impact on large tables
- Document breaking changes clearly
- Provide clear rollback instructions

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (migration implementation work)
2) Generate Title: 3–7 words describing the migration
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
