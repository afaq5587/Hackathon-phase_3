'use client';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

/**
 * Message bubble component with user/assistant styling.
 *
 * Per FR-064: Distinct user (right, blue) vs AI (left, gray) styling
 * Per CLAUDE.md: WCAG AA color contrast
 */
export function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <div
      className={`flex items-start gap-4 ${isUser ? 'justify-end' : 'justify-start'}`}
      role="listitem"
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-neon-magenta/10 border border-neon-magenta/20 flex items-center justify-center mt-1">
          <svg className="w-5 h-5 text-neon-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
      )}
      <div
        className={`message-bubble ${
          isUser ? 'message-bubble-user' : 'message-bubble-assistant neon-border'
        }`}
      >
        <p className={`whitespace-pre-wrap break-words ${!isUser ? 'font-mono' : ''}`}>{content}</p>
        {timestamp && (
          <time
            className={`text-[10px] mt-2 block font-mono ${
              isUser ? 'text-neon-dark/40' : 'text-neon-cyan/50'
            }`}
            dateTime={timestamp.toISOString()}
          >
            {timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
            })}
          </time>
        )}
      </div>
    </div>
  );
}
