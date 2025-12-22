'use client';

import { useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';

export interface Message {
  id: string | number;
  role: 'user' | 'assistant';
  content: string;
  createdAt?: Date;
}

interface MessageListProps {
  messages: Message[];
  isTyping?: boolean;
}

/**
 * Message list component displaying conversation.
 *
 * Per FR-078: Display historical messages on page load
 * Auto-scrolls to bottom on new messages.
 */
export function MessageList({ messages, isTyping = false }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change or typing starts
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  if (messages.length === 0 && !isTyping) {
    return (
      <div className="chat-messages flex items-center justify-center bg-neon-dark/20">
        <div className="text-center space-y-4">
          <div className="inline-block p-4 rounded-full bg-neon-cyan/5 border border-neon-cyan/20 animate-float">
            <svg className="w-12 h-12 text-neon-cyan/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold tracking-widest text-white uppercase italic">
            Interface Ready
          </h2>
          <p className="text-sm text-gray-500 font-mono max-w-xs mx-auto">
            Input directive to begin task orchestration...
          </p>
          <div className="flex flex-wrap justify-center gap-2 pt-4">
            <button className="robotic-tag hover:border-neon-cyan cursor-pointer transition-colors">"List objectives"</button>
            <button className="robotic-tag hover:border-neon-cyan cursor-pointer transition-colors">"Add task: Optimize core"</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-messages" role="list" aria-label="Chat messages">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          role={message.role}
          content={message.content}
          timestamp={message.createdAt}
        />
      ))}
      {isTyping && <TypingIndicator />}
      <div ref={bottomRef} aria-hidden="true" />
    </div>
  );
}
