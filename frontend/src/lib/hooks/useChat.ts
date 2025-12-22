'use client';

import { useState, useCallback, useEffect } from 'react';
import { api, ChatResponse, Message as ApiMessage } from '../api';
import { getStoredUser } from '../auth';

export interface ChatMessage {
  id: string | number;
  role: 'user' | 'assistant';
  content: string;
  createdAt?: Date;
}

interface UseChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: number | null;
}

interface UseChatReturn extends UseChatState {
  sendMessage: (content: string) => Promise<void>;
  clearError: () => void;
  loadHistory: () => Promise<void>;
}

/**
 * Chat state management hook.
 *
 * Per FR-044, FR-069: State management with optimistic UI updates
 * Per FR-076, FR-077: Conversation persistence across sessions
 */
export function useChat(): UseChatReturn {
  const [state, setState] = useState<UseChatState>({
    messages: [],
    isLoading: false,
    error: null,
    conversationId: null,
  });

  // Get user ID for API calls
  const getUserId = useCallback(() => {
    const user = getStoredUser();
    return user?.id || 'anonymous';
  }, []);

  // Load conversation history on mount
  const loadHistory = useCallback(async () => {
    const userId = getUserId();

    try {
      // Get most recent conversation
      const conversations = await api.listConversations(userId, 1);

      if (conversations.length > 0) {
        const conversation = conversations[0];
        const apiMessages = await api.getMessages(userId, conversation.id);

        // Convert API messages to chat messages
        const messages: ChatMessage[] = apiMessages.map((msg: ApiMessage) => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
          createdAt: new Date(msg.created_at),
        }));

        setState((prev) => ({
          ...prev,
          messages,
          conversationId: conversation.id,
        }));
      }
    } catch (err) {
      // Silently fail - user might not have any conversations yet
      console.error('Failed to load history:', err);
    }
  }, [getUserId]);

  // Load history on mount
  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  // Send a message
  const sendMessage = useCallback(
    async (content: string) => {
      const userId = getUserId();
      const tempId = `temp-${Date.now()}`;

      // Optimistic update: add user message immediately
      const userMessage: ChatMessage = {
        id: tempId,
        role: 'user',
        content,
        createdAt: new Date(),
      };

      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, userMessage],
        isLoading: true,
        error: null,
      }));

      try {
        // Call API
        const response: ChatResponse = await api.chat(userId, {
          conversation_id: state.conversationId || undefined,
          message: content,
        });

        // Add assistant response
        const assistantMessage: ChatMessage = {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          content: response.response,
          createdAt: new Date(),
        };

        setState((prev) => ({
          ...prev,
          messages: [...prev.messages, assistantMessage],
          conversationId: response.conversation_id,
          isLoading: false,
        }));
      } catch (err) {
        // Handle error
        const errorMessage = err instanceof Error ? err.message : 'Failed to send message';

        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
      }
    },
    [getUserId, state.conversationId]
  );

  // Clear error
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    sendMessage,
    clearError,
    loadHistory,
  };
}
