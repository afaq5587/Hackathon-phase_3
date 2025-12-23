---
description: Create frontend tests for components, hooks, and pages using React Testing Library and Jest
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse testing requirements** from user input:
   - What to test (component, hook, page, utility)
   - Test scenarios (rendering, interactions, edge cases)
   - Mocking requirements

2. **Verify test structure**:
   - Check `frontend/tests/` or `frontend/__tests__/` exists
   - Review existing test patterns
   - Verify Jest and React Testing Library are configured

3. **Create test file**:
   - Location: Same directory as component with `.test.tsx` suffix
   - Or: `frontend/tests/{component}.test.tsx`

4. **Write tests using React Testing Library**:
   ```typescript
   import { render, screen, fireEvent, waitFor } from '@testing-library/react'
   import { Component } from './Component'

   describe('Component', () => {
     it('renders correctly', () => {
       render(<Component />)
       expect(screen.getByText('Hello')).toBeInTheDocument()
     })

     it('handles click event', async () => {
       const handleClick = jest.fn()
       render(<Component onClick={handleClick} />)

       fireEvent.click(screen.getByRole('button'))

       await waitFor(() => {
         expect(handleClick).toHaveBeenCalledTimes(1)
       })
     })
   })
   ```

## Example Test Implementations

```typescript
// Component test
describe('Button', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const onClick = jest.fn()
    render(<Button onClick={onClick}>Click</Button>)
    fireEvent.click(screen.getByText('Click'))
    expect(onClick).toHaveBeenCalled()
  })

  it('shows loading state', () => {
    render(<Button loading>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})

// Hook test
import { renderHook, act } from '@testing-library/react'
import { useTasks } from './useTasks'

describe('useTasks', () => {
  it('fetches tasks on mount', async () => {
    const { result } = renderHook(() => useTasks())

    expect(result.current.loading).toBe(true)

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
      expect(result.current.tasks.length).toBeGreaterThan(0)
    })
  })
})
```

## Example Usage

```bash
/frontend.test Create tests for Button component
/frontend.test Create tests for useTasks hook
```
