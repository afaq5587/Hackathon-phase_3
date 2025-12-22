import { useSession as useBetterAuthSession } from './auth-client';
import { useState, useEffect } from 'react';

/**
 * Better Auth client for Phase 3 Todo Chatbot.
 *
 * Per Constitution Principle V: Authentication Continuity
 * - Shares BETTER_AUTH_SECRET with backend
 * - Manages JWT tokens for API requests
 */

// Auth state type
export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

// Token storage keys (migration/fallback)
const TOKEN_KEY = 'auth_token';

/**
 * Get stored auth token.
 * For BetterAuth, we might need to extract it or use the session.
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  // BetterAuth uses cookies by default, but we can store a session token if needed.
  // For now, let's look for the cookie-based session or the token key.
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Set auth token.
 */
export function setToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Clear auth token.
 */
export function clearToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem('auth_user');
}

/**
 * Get stored user (sync version for compatibility).
 */
export function getStoredUser(): User | null {
  if (typeof window === 'undefined') return null;
  const userJson = localStorage.getItem('auth_user');
  if (!userJson) return null;
  try {
    return JSON.parse(userJson);
  } catch {
    return null;
  }
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(): boolean {
  // We'll rely on useAuth for real reactive state, 
  // but for legacy checks, we check the token/session presence.
  return !!getToken();
}

/**
 * Sign out user.
 */
export async function signOut(): Promise<void> {
  const { authClient } = await import('./auth-client');
  await authClient.signOut();
  clearToken();
  if (typeof window !== 'undefined') {
    window.location.href = '/';
  }
}

/**
 * Handle session expiry.
 */
export function handleSessionExpiry(): void {
  clearToken();
  if (typeof window !== 'undefined') {
    sessionStorage.setItem('auth_message', 'Your session has expired. Please sign in again.');
    window.location.href = '/';
  }
}

/**
 * Get auth message.
 */
export function getAuthMessage(): string | null {
  if (typeof window === 'undefined') return null;
  const message = sessionStorage.getItem('auth_message');
  if (message) {
    sessionStorage.removeItem('auth_message');
  }
  return message;
}

/**
 * React hook for auth state.
 */
export function useAuth(): AuthState {
  const { data: session, isPending, error } = useBetterAuthSession();

  // Sync session to local storage for backend compatibility (temporary)
  useEffect(() => {
    if (session) {
      localStorage.setItem('auth_user', JSON.stringify(session.user));
      // BetterAuth handles its own token in cookies, 
      // but the backend expects an Authorization header with dev-token:id for now.
      // Let's keep it compatible until we migrate backend.
      localStorage.setItem(TOKEN_KEY, `dev-token:${session.user.id}`);
    }
  }, [session]);

  return {
    user: session?.user as User | null,
    isLoading: isPending,
    error: error ? error.message : null,
  };
}

/**
 * Auth context provider props.
 */
export interface AuthContextValue extends AuthState {
  signOut: () => void;
}
