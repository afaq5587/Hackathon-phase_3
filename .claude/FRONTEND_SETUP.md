# Frontend Development Setup Complete ✅

This document describes the frontend development agent and skills system configured for Next.js/React/TypeScript development.

## Overview

A comprehensive frontend development system with:
- **1 Frontend Designer Agent** - Expert agent for UI/UX implementation
- **5 Frontend Skills** - Specialized tools for frontend tasks
- **Complete Documentation** - Usage guides and examples

---

## 🎨 Frontend Designer Agent

**Agent Name**: `frontend-designer`

**Location**: `.claude/agents/frontend-designer.md`

**Purpose**: Expert frontend designer and developer specializing in React, Next.js 16+, TypeScript, and Tailwind CSS. Creates beautiful, accessible, and performant user interfaces.

**Capabilities**:
- React component development
- Next.js page creation with App Router
- Custom React hooks
- API client integration
- Tailwind CSS styling
- Accessibility (WCAG AA)
- Performance optimization
- Frontend testing

---

## 🛠️ Frontend Skills

All skills are located in `.claude/skills/` and can be invoked directly:

### 1. `/frontend.component` - Component Creation
Create React/Next.js components with TypeScript, Tailwind styling, and accessibility.

**Example**:
```bash
/frontend.component Create Button with variants (primary, secondary, danger) and sizes (sm, md, lg)
```

**Creates**:
- Functional component with hooks
- TypeScript props interface
- Tailwind CSS styling
- Accessibility features (ARIA, keyboard nav)
- Loading and error states
- Responsive design

---

### 2. `/frontend.page` - Page Creation
Create Next.js pages with routing, layouts, data fetching, and SEO metadata.

**Example**:
```bash
/frontend.page Create chat page at /chat with authentication and ChatContainer
```

**Creates**:
- Next.js page file with App Router
- SEO metadata (title, description, OG)
- Data fetching (Server/Client components)
- Authentication checks
- Loading and error states
- Responsive layout

---

### 3. `/frontend.hook` - Custom Hook Creation
Create custom React hooks for reusable stateful logic and data fetching.

**Example**:
```bash
/frontend.hook Create useChat hook for managing messages and sending
```

**Creates**:
- Custom hook function
- TypeScript types for params and return
- State management with useState/useReducer
- Side effects with useEffect
- Error handling
- Cleanup functions
- Performance optimization

---

### 4. `/frontend.api` - API Client Functions
Create API client functions for backend communication with TypeScript types.

**Example**:
```bash
/frontend.api Create getTasks and createTask API functions
```

**Creates**:
- API function with proper HTTP method
- TypeScript request/response types
- Error handling
- Authentication headers
- Query parameters

---

### 5. `/frontend.test` - Frontend Testing
Create tests for components, hooks, and pages using React Testing Library.

**Example**:
```bash
/frontend.test Create tests for Button component and useTasks hook
```

**Creates**:
- Component render tests
- User interaction tests
- Hook behavior tests
- Accessibility tests
- Error state tests

---

## 📋 Complete Feature Implementation Workflow

To implement a complete frontend feature (e.g., Chat Interface):

```bash
# Step 1: Create UI components
/frontend.component Create Button with variants and loading state
/frontend.component Create Input with validation
/frontend.component Create Card for containers

# Step 2: Build feature components
/frontend.component Create ChatInput with auto-resize textarea and send button
/frontend.component Create MessageBubble with user/assistant styling
/frontend.component Create MessageList with auto-scroll
/frontend.component Create ChatContainer orchestrating the chat flow

# Step 3: Create custom hooks
/frontend.hook Create useChat for managing chat state and API calls
/frontend.hook Create useDebounce for search optimization

# Step 4: Add API integration
/frontend.api Create sendMessage API function
/frontend.api Create getMessages API function
/frontend.api Create getChatHistory API function

# Step 5: Create pages
/frontend.page Create chat page at /chat with authentication
/frontend.page Create home page at / with hero and features

# Step 6: Write tests
/frontend.test Create tests for ChatInput, MessageBubble, MessageList
/frontend.test Create tests for useChat hook
/frontend.test Create integration tests for chat page
```

---

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app/                     # Next.js 16+ App Router
│   │   ├── (auth)/             # Route groups for auth
│   │   │   ├── login/page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── chat/               # Chat feature
│   │   │   ├── page.tsx
│   │   │   ├── loading.tsx
│   │   │   └── error.tsx
│   │   ├── tasks/              # Tasks feature
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Home/landing page
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Card.tsx
│   │   ├── chat/               # Chat feature components
│   │   │   ├── ChatContainer.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── MessageList.tsx
│   │   │   └── TypingIndicator.tsx
│   │   └── layout/             # Layout components
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   │
│   ├── lib/                    # Utilities and helpers
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useChat.ts
│   │   │   ├── useTasks.ts
│   │   │   ├── useDebounce.ts
│   │   │   └── useAuth.ts
│   │   ├── api.ts              # API client functions
│   │   ├── auth.ts             # Authentication
│   │   └── utils.ts            # Utility functions
│   │
│   └── styles/
│       └── globals.css         # Global styles + Tailwind
│
├── tailwind.config.js          # Tailwind configuration
├── next.config.js              # Next.js configuration
├── tsconfig.json               # TypeScript configuration
└── jest.config.js              # Jest test configuration
```

---

## 🎨 Design Standards

### Visual Design Principles
1. **Hierarchy**: Clear visual hierarchy (size, weight, color)
2. **Spacing**: Consistent spacing (Tailwind scale: p-4, m-2, gap-3)
3. **Typography**: Readable fonts, proper line-height
4. **Color**: Limited palette, meaningful usage
5. **Contrast**: WCAG AA minimum (4.5:1 for text)

### Tailwind Color System
```typescript
// Primary actions
"bg-blue-600 text-white hover:bg-blue-700"

// Secondary actions
"bg-gray-200 text-gray-900 hover:bg-gray-300"

// Success states
"text-green-600 bg-green-50"

// Error states
"text-red-600 border-red-300"

// Warning states
"text-yellow-600 bg-yellow-50"
```

### Responsive Breakpoints
```typescript
// Mobile first approach
"px-4 sm:px-6 md:px-8 lg:px-12"

// Breakpoints:
// sm: 640px  (phones landscape, small tablets)
// md: 768px  (tablets)
// lg: 1024px (small laptops)
// xl: 1280px (desktops)
// 2xl: 1536px (large screens)
```

---

## ♿ Accessibility Standards (WCAG AA)

All components must meet these requirements:

### Keyboard Navigation
- ✅ All interactive elements accessible via keyboard
- ✅ Logical tab order (tabindex)
- ✅ Escape key closes modals/menus
- ✅ Arrow keys for navigation in lists

### ARIA Labels
```typescript
<button aria-label="Close dialog" aria-pressed={isOpen}>
<input aria-describedby="error-message" aria-invalid={hasError}>
<div role="alert" aria-live="polite">
```

### Focus Indicators
```typescript
"focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
```

### Color Contrast
- **Normal text**: 4.5:1 minimum
- **Large text** (18pt+): 3:1 minimum
- **UI components**: 3:1 minimum

### Semantic HTML
```typescript
<nav>, <main>, <article>, <section>, <aside>, <header>, <footer>
<button> for actions
<a> for navigation
<h1>-<h6> for headings
```

---

## ⚡ Performance Best Practices

### Code Splitting
```typescript
// Lazy load heavy components
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Spinner />,
  ssr: false
})
```

### Memoization
```typescript
// Memoize expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  const processed = useMemo(() => processData(data), [data])
  return <div>{processed}</div>
})

// Memoize callbacks
const handleClick = useCallback(() => {
  // Handler logic
}, [dependencies])
```

### Image Optimization
```typescript
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Description"
  width={800}
  height={600}
  priority // For above-the-fold images
/>
```

---

## 🧪 Testing Standards

### Component Tests
```typescript
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
})
```

### Hook Tests
```typescript
import { renderHook, act } from '@testing-library/react'

describe('useChat', () => {
  it('sends message successfully', async () => {
    const { result } = renderHook(() => useChat('user-123'))

    act(() => {
      result.current.setInput('Hello')
    })

    await act(async () => {
      await result.current.sendMessage()
    })

    expect(result.current.messages).toHaveLength(2) // user + assistant
  })
})
```

---

## 🚀 Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5+
- **UI Library**: React 18+
- **Styling**: Tailwind CSS 3+
- **Authentication**: Better Auth
- **API Client**: Fetch API with TypeScript
- **Testing**: Jest + React Testing Library
- **State Management**: React hooks + Context API
- **Forms**: Custom hooks or React Hook Form

---

## 📚 Quick Reference

### Create a Button Component
```bash
/frontend.component Create Button with variants (primary, secondary, danger), sizes (sm, md, lg), and loading state
```

### Create a Chat Page
```bash
/frontend.page Create chat page at /chat - protected, server component, uses ChatContainer
```

### Create a Data Hook
```bash
/frontend.hook Create useTasks hook to fetch tasks with loading, error, and refetch
```

### Create API Functions
```bash
/frontend.api Create getTasks(userId, status) and createTask(userId, data) functions
```

### Write Tests
```bash
/frontend.test Create tests for Button component - rendering, interactions, states
/frontend.test Create tests for useChat hook - sending, receiving, errors
```

---

## ✅ What's Been Set Up

- ✅ Frontend Designer Agent configuration
- ✅ 5 specialized frontend skills
- ✅ Complete documentation and examples
- ✅ Accessibility standards (WCAG AA)
- ✅ Performance optimization patterns
- ✅ Testing frameworks and patterns
- ✅ Design system guidelines
- ✅ Responsive design standards

---

## 🎓 Usage Tips

1. **Mobile First**: Always design for mobile, then enhance for desktop
2. **Accessibility**: Use semantic HTML and ARIA labels
3. **TypeScript**: Define proper types for all props and states
4. **Tailwind**: Use utility classes, avoid custom CSS
5. **Components**: Keep them small, focused, and reusable
6. **Hooks**: Extract reusable logic into custom hooks
7. **Testing**: Test user behavior, not implementation
8. **Performance**: Use React.memo, useMemo, useCallback wisely

---

**System Ready for Frontend Development! 🎨**

You now have a complete frontend development system with an agent and skills that follow modern React/Next.js best practices, accessibility standards, and beautiful design principles.
