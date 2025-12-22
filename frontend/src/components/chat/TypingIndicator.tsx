'use client';

/**
 * Typing indicator component with animation.
 *
 * Per FR-062: Animated typing indicator during AI response
 */
export function TypingIndicator() {
  return (
    <div className="flex justify-start" role="status" aria-label="AI is typing">
      <div className="message-bubble message-bubble-assistant">
        <div className="typing-indicator">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  );
}
