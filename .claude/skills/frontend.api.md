---
description: Create API client functions for backend communication with proper error handling and TypeScript types
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse API requirements** from user input:
   - API endpoint URL and method
   - Request parameters and body
   - Response type
   - Authentication requirements
   - Error handling needs

2. **Verify project structure**:
   - Check `frontend/src/lib/api.ts` exists (main API client)
   - Review API base configuration
   - Check authentication setup

3. **Add API function to lib/api.ts**:
   ```typescript
   export async function {functionName}(
     params: ParamsType
   ): Promise<ResponseType> {
     const res = await apiClient.method('/endpoint', data)
     return res.data
   }
   ```

4. **Define TypeScript types**:
   - Request parameter types
   - Response data types
   - Error types

5. **Implement error handling**:
   - Handle network errors
   - Handle API errors (4xx, 5xx)
   - Provide clear error messages

## Example API Functions

```typescript
// GET request
export async function getTasks(
  userId: string,
  status?: 'all' | 'pending' | 'completed'
): Promise<Task[]> {
  const params = status !== 'all' ? { status } : {}
  const res = await fetch(
    `${API_URL}/api/${userId}/tasks?${new URLSearchParams(params)}`
  )
  if (!res.ok) throw new Error('Failed to fetch tasks')
  return res.json()
}

// POST request
export async function createTask(
  userId: string,
  data: TaskCreate
): Promise<Task> {
  const res = await fetch(`${API_URL}/api/${userId}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  if (!res.ok) throw new Error('Failed to create task')
  return res.json()
}

// PATCH request
export async function updateTask(
  userId: string,
  taskId: number,
  data: TaskUpdate
): Promise<Task> {
  const res = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  if (!res.ok) throw new Error('Failed to update task')
  return res.json()
}
```

## Example Usage

```bash
/frontend.api Create getTasks function for fetching tasks with optional status filter
/frontend.api Create createTask function for POST /api/{user_id}/tasks
```
