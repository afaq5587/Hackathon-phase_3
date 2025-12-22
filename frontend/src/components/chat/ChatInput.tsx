'use client';

import { useState, useCallback, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

/**
 * Chat input component with text field and send button.
 *
 * Per FR-065: Enter key submission handler
 * Per FR-071: Aria labels and keyboard navigation
 */
export function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Type a message...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = useCallback(() => {
    const trimmed = message.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      setMessage('');
    }
  }, [message, disabled, onSend]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  return (
    <div className="chat-input-area">
      <div className="flex gap-4 items-center max-w-4xl mx-auto p-2 bg-white/5 rounded-2xl border border-white/5 focus-within:border-neon-cyan/30 transition-all duration-300">
        <div className="flex-1 relative">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-neon-cyan/50 animate-pulse">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </div>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="w-full pl-12 pr-4 py-3 bg-transparent text-white placeholder-gray-600 focus:outline-none resize-none font-mono text-sm leading-6"
            aria-label="Chat message input"
            aria-describedby="chat-input-hint"
          />
        </div>
        <button
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          className="group relative flex items-center justify-center p-3 rounded-xl bg-neon-cyan text-neon-dark disabled:bg-gray-800 disabled:text-gray-600 transition-all duration-300 overflow-hidden"
          aria-label="Send message"
        >
          <div className="absolute inset-0 bg-white translate-y-full group-hover:translate-y-0 transition-transform duration-300 opacity-20" />
          <svg
            className="w-6 h-6 transform group-hover:rotate-12 transition-transform"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M14 5l7 7m0 0l-7 7m7-7H3"
            />
          </svg>
        </button>
      </div>
      <div className="flex justify-center mt-2">
        <span id="chat-input-hint" className="text-[10px] uppercase font-mono text-gray-600 tracking-tighter">
          [ENTER] Transmit Directive // [SHIFT+ENTER] Line Break
        </span>
      </div>
    </div>
  );
}
