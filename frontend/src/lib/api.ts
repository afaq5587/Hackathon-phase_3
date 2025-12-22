/**
 * Backend API client for Phase 3 Todo Chatbot.
 *
 * Per CLAUDE.md:
 * - API calls through /lib/api.ts
 * - JWT token attached to all backend requests
 */

import { getToken, handleSessionExpiry } from './auth';

// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types per chat-api.yaml
export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ToolCall {
  tool: string;
  arguments: Record<string, unknown>;
  result?: Record<string, unknown>;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls?: ToolCall[];
}

export interface Conversation {
  id: number;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  conversation_id: number;
  user_id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

export interface ApiError {
  error: string;
  message: string;
}

/**
 * API client with JWT authentication.
 */
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make authenticated API request.
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = getToken();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    // Handle auth errors
    if (response.status === 401) {
      handleSessionExpiry();
      throw new Error('Session expired');
    }

    if (response.status === 403) {
      throw new Error('Access denied');
    }

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.message || 'API request failed');
    }

    return response.json();
  }

  /**
   * Send chat message and get AI response.
   * POST /api/{user_id}/chat
   */
  async chat(userId: string, request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>(`/api/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * List user's conversations.
   * GET /api/{user_id}/conversations
   */
  async listConversations(
    userId: string,
    limit: number = 10
  ): Promise<Conversation[]> {
    return this.request<Conversation[]>(
      `/api/${userId}/conversations?limit=${limit}`
    );
  }

  /**
   * Get conversation messages.
   * GET /api/{user_id}/conversations/{conversation_id}/messages
   */
  async getMessages(
    userId: string,
    conversationId: number,
    limit: number = 50
  ): Promise<Message[]> {
    return this.request<Message[]>(
      `/api/${userId}/conversations/${conversationId}/messages?limit=${limit}`
    );
  }

  /**
   * Get user's tasks.
   * GET /api/{user_id}/tasks
   */
  async getTasks(userId: string): Promise<any[]> {
    return this.request<any[]>(`/api/${userId}/tasks`);
  }

  /**
   * Create a new task.
   * POST /api/{user_id}/tasks
   */
  async createTask(userId: string, data: { title: string, description?: string }): Promise<any> {
    return this.request<any>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Update a task.
   * PUT /api/{user_id}/tasks/{task_id}
   */
  async updateTask(userId: string, taskId: number, data: any): Promise<any> {
    return this.request<any>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Delete a task.
   * DELETE /api/{user_id}/tasks/{task_id}
   */
  async deleteTask(userId: string, taskId: number): Promise<void> {
    await this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Toggle task completion.
   * PATCH /api/{user_id}/tasks/{task_id}/complete
   */
  async toggleTaskComplete(userId: string, taskId: number): Promise<any> {
    return this.request<any>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }

  /**
   * Health check.
   * GET /health
   */
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

// Export singleton instance
export const api = new ApiClient();

// Export class for custom instances
export { ApiClient };
