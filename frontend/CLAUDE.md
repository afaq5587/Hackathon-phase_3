# Frontend Development Guidelines

## Stack
- Next.js 15+ (App Router)
- TypeScript
- React 19
- Tailwind CSS
- Better Auth (client)

## Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout with auth
│   │   ├── page.tsx         # Landing page
│   │   ├── chat/
│   │   │   └── page.tsx     # Main chat interface
│   │   └── api/
│   │       └── auth/        # Better Auth routes
│   ├── components/
│   │   ├── chat/            # Chat-specific components
│   │   │   ├── ChatContainer.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── TypingIndicator.tsx
│   │   └── ui/              # Reusable UI components
│   ├── lib/
│   │   ├── api.ts           # Backend API client
│   │   ├── auth.ts          # Better Auth client
│   │   └── hooks/
│   │       └── useChat.ts   # Chat state management
│   └── styles/
│       └── globals.css      # Tailwind + custom styles
└── tests/
    └── components/          # Component tests
```

## Conventions
- Use server components by default
- Client components only when needed (interactivity)
- API calls through `/lib/api.ts`
- JWT token attached to all backend requests
- Responsive design: 320px - 1920px
- WCAG AA color contrast

## Patterns
```tsx
// API calls
import { api } from '@/lib/api';
const response = await api.chat(userId, message);

// Auth check
import { useAuth } from '@/lib/auth';
const { user, isLoading } = useAuth();
```

## Running
```bash
# Development
npm run dev

# Build
npm run build

# Tests
npm run test
```
