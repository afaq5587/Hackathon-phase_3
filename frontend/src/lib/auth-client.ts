'use client';

import { createAuthClient } from "better-auth/react"

// Lazy initialization to prevent SSR issues
let _authClient: ReturnType<typeof createAuthClient> | null = null;

function getAuthClient() {
    if (typeof window === 'undefined') {
        // Return a mock during SSR
        return {
            signIn: (() => Promise.resolve()) as any,
            signUp: (() => Promise.resolve()) as any,
            signOut: (() => Promise.resolve()) as any,
            useSession: (() => ({ data: null, isPending: true, error: null })) as any,
        };
    }

    if (!_authClient) {
        _authClient = createAuthClient({
            baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"
        });
    }

    return _authClient;
}

export const authClient = getAuthClient();
export const { signIn, signUp, useSession } = authClient;

