'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { ChatContainer } from '@/components/chat/ChatContainer';

/**
 * Chat page integrating ChatContainer.
 *
 * Per CLAUDE.md: Main chat interface
 * Redirects to home if not authenticated.
 */
export default function ChatPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const { user, isLoading } = useAuth();

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isLoading && !user) {
      router.push('/');
    }
  }, [mounted, isLoading, user, router]);

  // Avoid hydration mismatch and handle initial load
  if (!mounted || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-transparent">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-neon-cyan shadow-[0_0_15px_#00f3ff]"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return <ChatContainer />;
}
