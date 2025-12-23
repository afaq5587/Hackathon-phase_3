---
description: Create custom React hooks for reusable stateful logic, data fetching, and side effects
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse hook requirements** from user input:
   - Hook name and purpose
   - State management needs
   - Side effects (API calls, subscriptions, timers)
   - Dependencies and parameters
   - Return values
   - Error handling requirements

2. **Verify project structure**:
   - Check `frontend/src/lib/hooks/` exists
   - Review existing hook patterns
   - Check for related utilities

3. **Determine hook type and location**:
   - **Data Fetching Hooks**: `frontend/src/lib/hooks/use{Entity}.ts` - API data fetching
   - **State Management Hooks**: `frontend/src/lib/hooks/use{Feature}.ts` - Complex state logic
   - **Side Effect Hooks**: `frontend/src/lib/hooks/use{Effect}.ts` - Side effects management
   - **Utility Hooks**: `frontend/src/lib/hooks/use{Utility}.ts` - Helper functions

4. **Create hook file structure**:
   ```typescript
   /**
    * use{HookName} Hook
    *
    * {Brief description of what the hook does}
    *
    * @example
    * const { data, loading, error } = use{HookName}(params)
    */

   import { useState, useEffect } from 'react'

   export function use{HookName}(params) {
     // Hook implementation
   }
   ```

5. **Define TypeScript types**:
   - Define parameter types
   - Define return type as object or tuple
   - Create interfaces for complex data structures
   - Use generics when appropriate

   ```typescript
   interface Use{HookName}Params {
     param1: string
     param2?: number
   }

   interface Use{HookName}Return {
     data: DataType | null
     loading: boolean
     error: Error | null
     refetch: () => void
   }

   export function use{HookName}(
     params: Use{HookName}Params
   ): Use{HookName}Return {
     // Implementation
   }
   ```

6. **Implement state management**:
   - Use `useState` for component state
   - Use `useReducer` for complex state logic
   - Initialize with proper default values
   - Consider state updates carefully

7. **Add side effects with useEffect**:
   - Fetch data on mount or dependency change
   - Set up subscriptions or listeners
   - Clean up resources in return function
   - Handle async operations properly

   ```typescript
   useEffect(() => {
     let cancelled = false

     async function fetchData() {
       try {
         const result = await api.getData()
         if (!cancelled) {
           setData(result)
         }
       } catch (error) {
         if (!cancelled) {
           setError(error)
         }
       }
     }

     fetchData()

     return () => {
       cancelled = true // Cleanup
     }
   }, [dependency])
   ```

8. **Add error handling**:
   - Catch and store errors in state
   - Provide error recovery mechanisms
   - Log errors for debugging
   - Return clear error messages

9. **Implement loading states**:
   - Track loading state during async operations
   - Set loading to true at start
   - Set loading to false when complete
   - Handle multiple concurrent requests

10. **Add utility functions**:
    - Provide refetch/retry functions
    - Add mutation functions (create, update, delete)
    - Implement debouncing/throttling if needed
    - Add helper methods for common operations

11. **Optimize performance**:
    - Use `useCallback` for memoized callbacks
    - Use `useMemo` for expensive computations
    - Avoid unnecessary re-renders
    - Consider debouncing for rapid updates

12. **Add documentation**:
    - JSDoc comment with description
    - Document parameters and return values
    - Provide usage examples
    - Note any important behaviors

13. **Testing checklist**:
    - [ ] Hook follows naming convention (use prefix)
    - [ ] TypeScript types are complete
    - [ ] Loading states work correctly
    - [ ] Error handling works
    - [ ] Cleanup functions prevent memory leaks
    - [ ] Dependencies array is correct
    - [ ] Hook can be reused across components
    - [ ] Performance is optimized

## Example Hook Implementations

### Data Fetching Hook
```typescript
/**
 * useTasks Hook
 *
 * Fetches and manages tasks for the authenticated user.
 * Provides loading, error states, and refetch functionality.
 *
 * @example
 * const { tasks, loading, error, refetch } = useTasks({ status: 'pending' })
 */

import { useState, useEffect, useCallback } from 'react'

interface Task {
  id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string
}

interface UseTasksParams {
  status?: 'all' | 'pending' | 'completed'
  autoFetch?: boolean
}

interface UseTasksReturn {
  tasks: Task[]
  loading: boolean
  error: Error | null
  refetch: () => Promise<void>
}

export function useTasks({
  status = 'all',
  autoFetch = true
}: UseTasksParams = {}): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(autoFetch)
  const [error, setError] = useState<Error | null>(null)

  const fetchTasks = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`/api/tasks?status=${status}`)

      if (!res.ok) {
        throw new Error(`Failed to fetch tasks: ${res.statusText}`)
      }

      const data = await res.json()
      setTasks(data)
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'))
      console.error('Failed to fetch tasks:', err)
    } finally {
      setLoading(false)
    }
  }, [status])

  useEffect(() => {
    if (autoFetch) {
      fetchTasks()
    }
  }, [autoFetch, fetchTasks])

  return {
    tasks,
    loading,
    error,
    refetch: fetchTasks
  }
}
```

### State Management Hook with Actions
```typescript
/**
 * useChat Hook
 *
 * Manages chat state including messages, input, and sending.
 * Handles real-time message updates and API communication.
 *
 * @example
 * const { messages, input, setInput, sendMessage, loading } = useChat(userId)
 */

import { useState, useCallback } from 'react'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

interface UseChatReturn {
  messages: Message[]
  input: string
  setInput: (input: string) => void
  sendMessage: () => Promise<void>
  loading: boolean
  error: Error | null
}

export function useChat(userId: string): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const sendMessage = useCallback(async () => {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('') // Clear input immediately
    setLoading(true)
    setError(null)

    // Optimistic update - add user message immediately
    const tempUserMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString()
    }
    setMessages(prev => [...prev, tempUserMessage])

    try {
      const res = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      })

      if (!res.ok) {
        throw new Error('Failed to send message')
      }

      const data = await res.json()

      // Add assistant response
      const assistantMessage: Message = {
        id: data.id,
        role: 'assistant',
        content: data.response,
        created_at: data.created_at
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'))
      // Remove optimistic update on error
      setMessages(prev => prev.filter(m => m.id !== tempUserMessage.id))
      setInput(userMessage) // Restore input
    } finally {
      setLoading(false)
    }
  }, [input, loading, userId])

  return {
    messages,
    input,
    setInput,
    sendMessage,
    loading,
    error
  }
}
```

### Side Effect Hook (Debounce)
```typescript
/**
 * useDebounce Hook
 *
 * Debounces a value, delaying updates until after a specified delay.
 * Useful for search inputs and API calls.
 *
 * @example
 * const debouncedSearch = useDebounce(searchTerm, 500)
 */

import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    // Set up timeout to update debounced value
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    // Clean up timeout if value changes before delay
    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}

// Usage example:
// const [searchTerm, setSearchTerm] = useState('')
// const debouncedSearchTerm = useDebounce(searchTerm, 500)
//
// useEffect(() => {
//   if (debouncedSearchTerm) {
//     searchAPI(debouncedSearchTerm)
//   }
// }, [debouncedSearchTerm])
```

### Utility Hook (Local Storage)
```typescript
/**
 * useLocalStorage Hook
 *
 * Syncs state with localStorage, providing persistent state.
 * Automatically serializes/deserializes JSON values.
 *
 * @example
 * const [theme, setTheme] = useLocalStorage('theme', 'light')
 */

import { useState, useEffect } from 'react'

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((val: T) => T)) => void] {
  // Get from localStorage or use initial value
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue
    }

    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(`Error loading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  // Update localStorage when value changes
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function (same API as useState)
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)

      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      }
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }

  return [storedValue, setValue]
}
```

### Form Hook
```typescript
/**
 * useForm Hook
 *
 * Manages form state, validation, and submission.
 * Provides utilities for handling form inputs and errors.
 *
 * @example
 * const { values, errors, handleChange, handleSubmit } = useForm({
 *   initialValues: { email: '', password: '' },
 *   onSubmit: async (values) => { ... }
 * })
 */

import { useState, useCallback, FormEvent } from 'react'

interface UseFormOptions<T> {
  initialValues: T
  onSubmit: (values: T) => void | Promise<void>
  validate?: (values: T) => Partial<Record<keyof T, string>>
}

interface UseFormReturn<T> {
  values: T
  errors: Partial<Record<keyof T, string>>
  touched: Partial<Record<keyof T, boolean>>
  handleChange: (field: keyof T, value: any) => void
  handleBlur: (field: keyof T) => void
  handleSubmit: (e: FormEvent) => Promise<void>
  setFieldValue: (field: keyof T, value: any) => void
  setFieldError: (field: keyof T, error: string) => void
  resetForm: () => void
  isSubmitting: boolean
}

export function useForm<T extends Record<string, any>>({
  initialValues,
  onSubmit,
  validate
}: UseFormOptions<T>): UseFormReturn<T> {
  const [values, setValues] = useState<T>(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({})
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = useCallback((field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }))
    }
  }, [errors])

  const handleBlur = useCallback((field: keyof T) => {
    setTouched(prev => ({ ...prev, [field]: true }))

    // Validate single field on blur
    if (validate) {
      const fieldErrors = validate(values)
      if (fieldErrors[field]) {
        setErrors(prev => ({ ...prev, [field]: fieldErrors[field] }))
      }
    }
  }, [validate, values])

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Validate all fields
    if (validate) {
      const validationErrors = validate(values)
      if (Object.keys(validationErrors).length > 0) {
        setErrors(validationErrors)
        setIsSubmitting(false)
        return
      }
    }

    try {
      await onSubmit(values)
    } catch (error) {
      console.error('Form submission error:', error)
    } finally {
      setIsSubmitting(false)
    }
  }, [values, validate, onSubmit])

  const setFieldValue = useCallback((field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }))
  }, [])

  const setFieldError = useCallback((field: keyof T, error: string) => {
    setErrors(prev => ({ ...prev, [field]: error }))
  }, [])

  const resetForm = useCallback(() => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
    setIsSubmitting(false)
  }, [initialValues])

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    handleSubmit,
    setFieldValue,
    setFieldError,
    resetForm,
    isSubmitting
  }
}
```

## Example Usage

```bash
# Create a data fetching hook
/frontend.hook Create useTasks hook to fetch and manage task list with loading and error states

# Create a state management hook
/frontend.hook Create useChat hook for managing chat messages and sending

# Create a utility hook
/frontend.hook Create useDebounce hook to debounce value updates
```

## Best Practices

- **Naming**: Always prefix with `use` (e.g., `useTasks`)
- **Single Responsibility**: Each hook should do one thing well
- **Cleanup**: Always clean up side effects in useEffect return
- **Dependencies**: Include all dependencies in useEffect arrays
- **Memoization**: Use useCallback and useMemo to prevent unnecessary re-renders
- **TypeScript**: Provide complete type definitions
- **Error Handling**: Always handle errors gracefully
- **Loading States**: Track async operation states
- **Reusability**: Make hooks generic and reusable
- **Documentation**: Add clear JSDoc comments
- **Testing**: Test hooks with @testing-library/react-hooks
- **Performance**: Avoid creating new objects/functions on every render

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (hook implementation)
2) Generate Title: 3–7 words describing the hook
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
