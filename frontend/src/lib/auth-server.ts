import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

import { Pool } from "pg";

const pool = new Pool({
    connectionString: process.env.DATABASE_URL
});

console.log("Initializing Better Auth with PostgreSQL (Neon)...");

export const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET as string || "development-secret-123-at-least-32-chars",
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    database: pool,
    emailAndPassword: {
        enabled: true
    },
    plugins: [
        nextCookies()
    ]
});

console.log("Better Auth Initialized.");
