'use client';

import { useState, useCallback, useEffect } from 'react';
import { useChat, ChatMessage } from '@/lib/hooks/useChat';
import { ChatInput } from './ChatInput';
import { MessageList } from './MessageList';
import Link from 'next/link';
import { signOut, getStoredUser } from '@/lib/auth';

/**
 * Main chat container orchestrating chat flow.
 *
 * Per FR-066: Responsive breakpoints (320px-1920px)
 * Per FR-068: Typing indicator during API calls
 * Per FR-083: Error boundary for frontend chat errors
 */
export function ChatContainer() {
  const { messages, isLoading, error, sendMessage, clearError } = useChat();
  const [welcomeSent, setWelcomeSent] = useState(false);
  const [localMessages, setLocalMessages] = useState<ChatMessage[]>([]);

  // Sync local messages with hook messages
  useEffect(() => {
    if (messages.length > 0) {
      setLocalMessages(messages);
      setWelcomeSent(true);
    }
  }, [messages]);

  // Initial Welcome Flow
  useEffect(() => {
    if (messages.length === 0 && !isLoading && !welcomeSent) {
      const user = getStoredUser();
      const name = user?.name || 'User';
      
      const welcomeMsg: ChatMessage = {
        id: 'system-welcome',
        role: 'assistant',
        content: `Welcome to the Neural Interface, ${name}. Bio-link established. I am standing by to orchestrate your directives. How shall we proceed?`,
        createdAt: new Date(),
      };
      
      setLocalMessages([welcomeMsg]);
      setWelcomeSent(true);
    }
  }, [messages, isLoading, welcomeSent]);

  // Handle message sending with local state update
  const handleSendMessage = async (content: string) => {
    await sendMessage(content);
  };

  const displayMessages = localMessages.length > 0 ? localMessages : messages;

  return (
    <div className="chat-container neon-border glass-card">
      {/* Header (same as before) */}
      <header className="border-b border-white/5 bg-neon-dark/40 px-6 py-4 flex items-center justify-between backdrop-blur-md relative z-20">
        <div className="flex items-center gap-3">
          <Link href="/" className="group flex items-center gap-3">
            <div className="h-2 w-2 rounded-full bg-neon-cyan animate-pulse shadow-[0_0_10px_#00f3ff]" />
            <div>
              <h1 className="text-sm font-bold tracking-widest text-neon-cyan uppercase group-hover:text-white transition-colors">
                Neural Interface
              </h1>
              <p className="text-[10px] text-gray-500 font-mono uppercase tracking-tighter group-hover:text-neon-cyan/50 transition-colors">
                Active Session // Secure Link
              </p>
            </div>
          </Link>
        </div>
        <div className="flex items-center gap-4">
          <Link 
            href="/"
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-neon-cyan/20 text-[10px] font-mono text-neon-cyan hover:bg-neon-cyan/5 transition-all uppercase tracking-tighter"
          >
            Terminal Dashboard
          </Link>
          <div className="robotic-tag">v3.1.2</div>
          <button 
            onClick={() => signOut()}
            className="p-1.5 rounded-lg border border-neon-magenta/30 text-neon-magenta hover:bg-neon-magenta/10 transition-all group"
            aria-label="System Shutdown"
            title="System Shutdown (Log Out)"
          >
            <svg className="w-4 h-4 group-hover:rotate-90 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </header>
      
      {/* Error banner */}
      {error && (
        <div
          className="bg-red-500/10 border-b border-red-500/20 px-4 py-3"
          role="alert"
        >
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <p className="text-sm text-red-500 font-mono">[CRITICAL ERROR] {error}</p>
            <button
              onClick={clearError}
              className="text-red-500 hover:text-red-400"
              aria-label="Dismiss error"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Message list */}
      <MessageList messages={displayMessages} isTyping={isLoading} />

      {/* Input area */}
      <ChatInput
        onSend={handleSendMessage}
        disabled={isLoading}
        placeholder={
          isLoading
            ? 'Process in queue...'
            : 'Enter neural directive...'
        }
      />
    </div>
  );
}
