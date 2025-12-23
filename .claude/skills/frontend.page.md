---
description: Create Next.js pages with proper routing, layouts, data fetching, and SEO metadata
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Parse page requirements** from user input:
   - Page name and route
   - Page type (static, dynamic, server/client component)
   - Data fetching requirements
   - Layout requirements
   - SEO metadata (title, description)
   - Authentication requirements
   - Loading and error states

2. **Verify project structure**:
   - Check `frontend/src/app/` exists (Next.js 13+ App Router)
   - Review existing page patterns
   - Check layout files
   - Verify authentication setup

3. **Determine page location and type**:
   - **Static Page**: `frontend/src/app/{route}/page.tsx` - No dynamic segments
   - **Dynamic Page**: `frontend/src/app/{route}/[id]/page.tsx` - With parameters
   - **Nested Routes**: `frontend/src/app/{parent}/{child}/page.tsx` - Nested paths
   - **Route Groups**: `frontend/src/app/(group)/{route}/page.tsx` - Organized routes

4. **Create page file structure**:
   ```typescript
   /**
    * {PageName} Page
    *
    * Route: /{route-path}
    * {Brief description}
    */

   import { Metadata } from 'next'

   export const metadata: Metadata = {
     title: 'Page Title',
     description: 'Page description'
   }

   export default function {PageName}Page() {
     return (
       // Page content
     )
   }
   ```

5. **Add SEO metadata**:
   ```typescript
   import { Metadata } from 'next'

   export const metadata: Metadata = {
     title: 'Page Title | App Name',
     description: 'Comprehensive page description for SEO',
     keywords: ['keyword1', 'keyword2'],
     openGraph: {
       title: 'Page Title',
       description: 'Description for social sharing',
       type: 'website',
     }
   }
   ```

6. **Implement data fetching** (if needed):

   **Server Component (default, recommended):**
   ```typescript
   async function getData() {
     const res = await fetch('https://api.example.com/data', {
       cache: 'no-store' // or 'force-cache' for static
     })
     if (!res.ok) throw new Error('Failed to fetch')
     return res.json()
   }

   export default async function Page() {
     const data = await getData()
     return <div>{/* Use data */}</div>
   }
   ```

   **Client Component (when needed):**
   ```typescript
   'use client'

   import { useState, useEffect } from 'react'

   export default function Page() {
     const [data, setData] = useState(null)
     const [loading, setLoading] = useState(true)

     useEffect(() => {
       fetch('/api/data')
         .then(res => res.json())
         .then(setData)
         .finally(() => setLoading(false))
     }, [])

     if (loading) return <div>Loading...</div>
     return <div>{/* Use data */}</div>
   }
   ```

7. **Add authentication checks** (if required):
   ```typescript
   import { redirect } from 'next/navigation'
   import { auth } from '@/lib/auth-server'

   export default async function ProtectedPage() {
     const session = await auth()

     if (!session) {
       redirect('/login')
     }

     return <div>Protected content for {session.user.email}</div>
   }
   ```

8. **Implement loading states**:
   - Create `loading.tsx` for page-level loading UI
   - Use Suspense boundaries for specific sections
   - Show skeleton loaders during data fetch

   ```typescript
   // app/dashboard/loading.tsx
   export default function Loading() {
     return (
       <div className="animate-pulse">
         <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
         <div className="h-64 bg-gray-200 rounded" />
       </div>
     )
   }
   ```

9. **Add error handling**:
   - Create `error.tsx` for error boundaries
   - Handle API errors gracefully
   - Provide retry mechanisms

   ```typescript
   // app/dashboard/error.tsx
   'use client'

   export default function Error({
     error,
     reset
   }: {
     error: Error & { digest?: string }
     reset: () => void
   }) {
     return (
       <div className="flex flex-col items-center justify-center min-h-screen">
         <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
         <p className="text-gray-600 mb-4">{error.message}</p>
         <button onClick={reset} className="px-4 py-2 bg-blue-600 text-white rounded">
           Try again
         </button>
       </div>
     )
   }
   ```

10. **Handle dynamic routes**:
    ```typescript
    // app/tasks/[id]/page.tsx
    interface PageProps {
      params: { id: string }
      searchParams: { [key: string]: string | string[] | undefined }
    }

    export default async function TaskPage({ params }: PageProps) {
      const task = await getTask(params.id)

      if (!task) {
        notFound() // Shows 404 page
      }

      return <div>{task.title}</div>
    }

    // Generate static params for SSG
    export async function generateStaticParams() {
      const tasks = await getTasks()
      return tasks.map((task) => ({ id: task.id.toString() }))
    }
    ```

11. **Add page layout structure**:
    ```typescript
    export default function Page() {
      return (
        <div className="min-h-screen bg-gray-50">
          {/* Header/Navigation */}
          <header className="bg-white shadow">
            {/* Header content */}
          </header>

          {/* Main Content */}
          <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            {/* Page content */}
          </main>

          {/* Footer (optional) */}
          <footer className="bg-white border-t">
            {/* Footer content */}
          </footer>
        </div>
      )
    }
    ```

12. **Implement responsive design**:
    - Mobile-first approach
    - Responsive breakpoints (sm, md, lg, xl)
    - Test on different screen sizes
    - Consider mobile navigation patterns

13. **Testing checklist**:
    - [ ] Page renders at correct route
    - [ ] Metadata displays correctly
    - [ ] Data fetching works
    - [ ] Authentication checks work
    - [ ] Loading states display
    - [ ] Error handling works
    - [ ] Responsive on all breakpoints
    - [ ] Navigation works correctly
    - [ ] SEO metadata is complete

## Example Page Implementations

### Static Landing Page
```typescript
/**
 * Home Page
 *
 * Route: /
 * Landing page with hero section and features
 */

import { Metadata } from 'next'
import { Button } from '@/components/ui/Button'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'AI Todo Chatbot | Manage Tasks Naturally',
  description: 'Manage your tasks through natural conversation with our AI-powered todo chatbot.',
  openGraph: {
    title: 'AI Todo Chatbot',
    description: 'Manage your tasks through natural conversation',
    type: 'website',
  }
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            Manage Tasks with
            <span className="text-blue-600"> Natural Language</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Just tell our AI what you need to do. No forms, no clicks—just conversation.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/signup">
              <Button variant="primary" size="lg">
                Get Started Free
              </Button>
            </Link>
            <Link href="/demo">
              <Button variant="secondary" size="lg">
                Try Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            title="Natural Language"
            description="Add tasks by simply typing what you need to do"
            icon="💬"
          />
          <FeatureCard
            title="Smart AI"
            description="Our AI understands context and helps you stay organized"
            icon="🤖"
          />
          <FeatureCard
            title="Always Synced"
            description="Access your tasks from anywhere, anytime"
            icon="☁️"
          />
        </div>
      </section>
    </div>
  )
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
```

### Protected Dashboard Page
```typescript
/**
 * Chat Page
 *
 * Route: /chat
 * Protected page for AI chat interface
 */

import { Metadata } from 'next'
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth-server'
import { ChatContainer } from '@/components/chat/ChatContainer'

export const metadata: Metadata = {
  title: 'Chat | AI Todo Assistant',
  description: 'Chat with your AI todo assistant'
}

export default async function ChatPage() {
  const session = await auth()

  if (!session) {
    redirect('/login?redirect=/chat')
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white border-b px-4 py-3">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold">AI Todo Assistant</h1>
          <div className="text-sm text-gray-600">
            {session.user.email}
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <main className="flex-1 overflow-hidden">
        <ChatContainer userId={session.user.id} />
      </main>
    </div>
  )
}
```

### Dynamic Page with Data Fetching
```typescript
/**
 * Task Detail Page
 *
 * Route: /tasks/[id]
 * Shows individual task details
 */

import { Metadata } from 'next'
import { notFound, redirect } from 'next/navigation'
import { auth } from '@/lib/auth-server'

interface PageProps {
  params: { id: string }
}

async function getTask(taskId: string, userId: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/tasks/${taskId}`,
    { cache: 'no-store' }
  )

  if (!res.ok) {
    if (res.status === 404) return null
    throw new Error('Failed to fetch task')
  }

  return res.json()
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const session = await auth()
  if (!session) return { title: 'Task' }

  const task = await getTask(params.id, session.user.id)

  return {
    title: task ? `${task.title} | Tasks` : 'Task Not Found',
    description: task?.description || 'Task details'
  }
}

export default async function TaskPage({ params }: PageProps) {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  const task = await getTask(params.id, session.user.id)

  if (!task) {
    notFound()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-start justify-between mb-4">
          <h1 className="text-3xl font-bold">{task.title}</h1>
          <span
            className={`px-3 py-1 rounded-full text-sm ${
              task.completed
                ? 'bg-green-100 text-green-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}
          >
            {task.completed ? 'Completed' : 'Pending'}
          </span>
        </div>

        {task.description && (
          <p className="text-gray-700 mb-6">{task.description}</p>
        )}

        <div className="text-sm text-gray-500">
          <p>Created: {new Date(task.created_at).toLocaleDateString()}</p>
          {task.updated_at !== task.created_at && (
            <p>Updated: {new Date(task.updated_at).toLocaleDateString()}</p>
          )}
        </div>
      </div>
    </div>
  )
}
```

### Client Component Page with State
```typescript
/**
 * Tasks Page
 *
 * Route: /tasks
 * Client-side task list with filtering
 */

'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/hooks/useAuth'
import { Button } from '@/components/ui/Button'

interface Task {
  id: number
  title: string
  completed: boolean
}

export default function TasksPage() {
  const { user } = useAuth()
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')

  useEffect(() => {
    if (!user) return

    fetch(`/api/${user.id}/tasks`)
      .then(res => res.json())
      .then(data => setTasks(data))
      .catch(error => console.error('Failed to fetch tasks:', error))
      .finally(() => setLoading(false))
  }, [user])

  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed
    if (filter === 'completed') return task.completed
    return true
  })

  if (loading) {
    return <div className="p-8">Loading tasks...</div>
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Your Tasks</h1>
        <div className="flex gap-2">
          <Button
            variant={filter === 'all' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setFilter('all')}
          >
            All
          </Button>
          <Button
            variant={filter === 'pending' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setFilter('pending')}
          >
            Pending
          </Button>
          <Button
            variant={filter === 'completed' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setFilter('completed')}
          >
            Completed
          </Button>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No {filter !== 'all' ? filter : ''} tasks found
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTasks.map(task => (
            <div
              key={task.id}
              className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <h3 className="font-medium">{task.title}</h3>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

## Example Usage

```bash
# Create a static landing page
/frontend.page Create home page at / with hero section and features

# Create a protected dashboard
/frontend.page Create chat page at /chat - protected, shows ChatContainer

# Create a dynamic detail page
/frontend.page Create task detail page at /tasks/[id] with data fetching
```

## Best Practices

- Use Server Components by default (better performance)
- Add proper metadata for SEO
- Implement loading states with loading.tsx
- Add error boundaries with error.tsx
- Protect routes with authentication checks
- Use dynamic imports for code splitting
- Implement proper TypeScript types
- Add responsive design (mobile-first)
- Use semantic HTML for accessibility
- Handle loading and error states gracefully
- Optimize images with next/image
- Use Link component for navigation

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage: **misc** (page implementation)
2) Generate Title: 3–7 words describing the page
3) Route: `history/prompts/<feature-name>/` (feature stages)
4) Create PHR with full PROMPT_TEXT and concise RESPONSE_TEXT
5) Validate: No unresolved placeholders, correct path, report ID + path + stage + title
