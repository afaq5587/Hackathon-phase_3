---
description: Create React/Next.js components with TypeScript, proper props, styling, and accessibility
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse component requirements** from user input:
   - Component name and purpose
   - Component type (presentational, container, layout, form)
   - Props and their types
   - State requirements
   - Events and callbacks
   - Styling approach (Tailwind classes, CSS modules)
   - Accessibility requirements

2. **Verify project structure**:
   - Check `frontend/src/components/` exists
   - Review existing component patterns
   - Check Tailwind configuration in `frontend/tailwind.config.js`
   - Verify TypeScript is configured

3. **Determine component location**:
   - **UI Components**: `frontend/src/components/ui/{ComponentName}.tsx` - Reusable UI elements (Button, Input, Card)
   - **Feature Components**: `frontend/src/components/{feature}/{ComponentName}.tsx` - Feature-specific (chat, tasks)
   - **Layout Components**: `frontend/src/components/layout/{ComponentName}.tsx` - Layout elements (Header, Sidebar)
   - **Form Components**: `frontend/src/components/forms/{ComponentName}.tsx` - Form inputs and validation

4. **Create component file structure**:
   ```typescript
   /**
    * {ComponentName} Component
    *
    * {Brief description of component purpose}
    *
    * @example
    * <{ComponentName} prop1="value" prop2={value} />
    */

   import React from 'react'

   interface {ComponentName}Props {
     // Props interface
   }

   export function {ComponentName}({ props }: {ComponentName}Props) {
     // Component implementation
   }
   ```

5. **Define TypeScript props interface**:
   - Define all props with proper types
   - Mark optional props with `?`
   - Use union types for variants (`'primary' | 'secondary'`)
   - Add JSDoc comments for complex props
   - Extend HTML element props when needed

   ```typescript
   interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
     variant?: 'primary' | 'secondary' | 'danger'
     size?: 'sm' | 'md' | 'lg'
     loading?: boolean
     icon?: React.ReactNode
     children: React.ReactNode
   }
   ```

6. **Implement component logic**:
   - Use functional components with hooks
   - Add state management with `useState` if needed
   - Add side effects with `useEffect` if needed
   - Implement event handlers
   - Add loading and error states
   - Handle edge cases (empty data, errors)

7. **Add styling with Tailwind CSS**:
   - Use Tailwind utility classes
   - Implement responsive design (sm:, md:, lg: breakpoints)
   - Add hover, focus, and active states
   - Use conditional classes with `clsx` or `cn` utility
   - Ensure WCAG AA color contrast

   ```typescript
   import { cn } from '@/lib/utils'

   const buttonStyles = cn(
     'px-4 py-2 rounded-lg font-medium transition-colors',
     variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
     variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
     loading && 'opacity-50 cursor-not-allowed'
   )
   ```

8. **Add accessibility features**:
   - Use semantic HTML elements
   - Add ARIA labels and roles
   - Ensure keyboard navigation works
   - Add focus indicators
   - Provide alt text for images
   - Add screen reader announcements

   ```typescript
   <button
     type="button"
     aria-label="Close dialog"
     aria-disabled={loading}
     className={styles}
   >
     {children}
   </button>
   ```

9. **Add loading and error states**:
   - Show loading spinners or skeletons
   - Display error messages gracefully
   - Provide retry mechanisms
   - Show empty states with helpful messages

10. **Handle events and callbacks**:
    - Define event handler props
    - Use proper TypeScript event types
    - Prevent default behavior when needed
    - Handle async operations

    ```typescript
    interface FormProps {
      onSubmit: (data: FormData) => void | Promise<void>
      onChange?: (field: string, value: string) => void
    }
    ```

11. **Add component documentation**:
    - JSDoc comment at top of component
    - Document all props in interface
    - Provide usage examples
    - Note any important behaviors or constraints

12. **Export component**:
    - Use named export for component
    - Export types if needed by consumers
    - Create barrel export in index.ts if applicable

13. **Testing checklist**:
    - [ ] Component renders without errors
    - [ ] All props work correctly
    - [ ] Responsive design works on all breakpoints
    - [ ] Accessibility features implemented
    - [ ] Loading and error states display correctly
    - [ ] Events fire correctly
    - [ ] TypeScript types are correct
    - [ ] Styling matches design requirements

## Example Component Implementations

### Simple UI Component (Button)
```typescript
/**
 * Button Component
 *
 * Reusable button with variants, sizes, and loading state.
 *
 * @example
 * <Button variant="primary" size="md" onClick={handleClick}>
 *   Click Me
 * </Button>
 */

import React from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ReactNode
  children: React.ReactNode
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center font-medium transition-colors rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2'

  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
  }

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }

  return (
    <button
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        (loading || disabled) && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={loading || disabled}
      aria-busy={loading}
      {...props}
    >
      {loading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {icon && <span className="mr-2">{icon}</span>}
      {children}
    </button>
  )
}
```

### Feature Component (ChatInput)
```typescript
/**
 * ChatInput Component
 *
 * Text input for chat messages with send button and keyboard shortcuts.
 *
 * @example
 * <ChatInput
 *   onSend={handleSend}
 *   disabled={loading}
 *   placeholder="Type a message..."
 * />
 */

import React, { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/Button'

interface ChatInputProps {
  onSend: (message: string) => void | Promise<void>
  disabled?: boolean
  placeholder?: string
  maxLength?: number
}

export function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Type a message...',
  maxLength = 1000
}: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [isSending, setIsSending] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [message])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const trimmedMessage = message.trim()
    if (!trimmedMessage || disabled || isSending) return

    setIsSending(true)
    try {
      await onSend(trimmedMessage)
      setMessage('') // Clear input on success
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setIsSending(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter, new line on Shift+Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const isDisabled = disabled || isSending

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 items-end">
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isDisabled}
          maxLength={maxLength}
          rows={1}
          className="w-full px-4 py-3 pr-12 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-label="Chat message input"
        />
        <span className="absolute bottom-2 right-2 text-xs text-gray-400">
          {message.length}/{maxLength}
        </span>
      </div>

      <Button
        type="submit"
        disabled={isDisabled || !message.trim()}
        loading={isSending}
        aria-label="Send message"
      >
        Send
      </Button>
    </form>
  )
}
```

### List Component (MessageList)
```typescript
/**
 * MessageList Component
 *
 * Displays a scrollable list of chat messages with auto-scroll.
 *
 * @example
 * <MessageList messages={messages} loading={loading} />
 */

import React, { useEffect, useRef } from 'react'
import { MessageBubble } from './MessageBubble'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

interface MessageListProps {
  messages: Message[]
  loading?: boolean
  emptyMessage?: string
}

export function MessageList({
  messages,
  loading = false,
  emptyMessage = 'No messages yet. Start a conversation!'
}: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  if (!loading && messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <p>{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-4 p-4 overflow-y-auto h-full">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          role={message.role}
          content={message.content}
          timestamp={message.created_at}
        />
      ))}

      {loading && (
        <div className="flex items-center gap-2 text-gray-500">
          <div className="animate-pulse">●</div>
          <div className="animate-pulse animation-delay-200">●</div>
          <div className="animate-pulse animation-delay-400">●</div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
```

## Example Usage

```bash
# Create a UI component
/frontend.component Create Button component with variants (primary, secondary, danger) and sizes (sm, md, lg)

# Create a feature component
/frontend.component Create ChatInput with auto-resize textarea, send on Enter, and character count

# Create a layout component
/frontend.component Create Header with logo, navigation, and user menu
```

## Best Practices

- Use functional components with hooks
- Define proper TypeScript interfaces for props
- Use Tailwind CSS for styling
- Ensure responsive design (mobile-first)
- Add accessibility features (ARIA, keyboard nav)
- Handle loading and error states
- Use semantic HTML elements
- Add proper focus indicators
- Implement keyboard shortcuts where appropriate
- Keep components focused and single-purpose
- Extract reusable logic into custom hooks
- Use React.memo for performance optimization when needed

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (component implementation)
2) Generate Title: 3–7 words describing the component
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
