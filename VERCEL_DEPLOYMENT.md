# Vercel Deployment Configuration

This guide explains how to configure environment variables in Vercel for both frontend and backend deployments.

## Deployed URLs
- **Frontend**: https://taskmanager-pi-liard.vercel.app/
- **Backend**: https://todoagent-navy.vercel.app/

## Backend Environment Variables (todoagent-navy)

Set these environment variables in your Vercel backend project dashboard:

### Required Variables

1. **DATABASE_URL**
   ```
   postgresql://neondb_owner:npg_5sjSbVMm7hCk@ep-shiny-butterfly-ah5omg0i-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

2. **BETTER_AUTH_SECRET**
   ```
   VyjAovwOyAF0L7xduZb8ihHG66r5yGfI
   ```

3. **GEMINI_API_KEY**
   ```
   AIzaSyCZn-NuPdYY3iqMfG587jSLK1zj1DxG7M8
   ```

4. **CORS_ORIGINS** (Critical for frontend-backend connection)
   ```
   https://taskmanager-pi-liard.vercel.app,http://localhost:3000
   ```

### Steps to Set Backend Environment Variables:

1. Go to https://vercel.com/dashboard
2. Select your backend project: `todoagent-navy`
3. Go to **Settings** → **Environment Variables**
4. Add each variable above with its value
5. Make sure to select all environments (Production, Preview, Development)
6. Click **Save**
7. **Redeploy** your backend for changes to take effect

---

## Frontend Environment Variables (taskmanager-pi-liard)

Set these environment variables in your Vercel frontend project dashboard:

### Required Variables

1. **DATABASE_URL** (for Better Auth database)
   ```
   postgresql://neondb_owner:npg_n93BcYgNxOor@ep-winter-night-ahrtfj3x-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

2. **BETTER_AUTH_SECRET** (must match backend)
   ```
   VyjAovwOyAF0L7xduZb8ihHG66r5yGfI
   ```

3. **NEXT_PUBLIC_API_URL** (Critical for frontend-backend connection)
   ```
   https://todoagent-navy.vercel.app
   ```

4. **NEXT_PUBLIC_APP_URL**
   ```
   https://taskmanager-pi-liard.vercel.app
   ```

5. **GEMINI_API_KEY** (if needed by frontend)
   ```
   AIzaSyCZn-NuPdYY3iqMfG587jSLK1zj1DxG7M8
   ```

### Steps to Set Frontend Environment Variables:

1. Go to https://vercel.com/dashboard
2. Select your frontend project: `taskmanager-pi-liard`
3. Go to **Settings** → **Environment Variables**
4. Add each variable above with its value
5. Make sure to select all environments (Production, Preview, Development)
6. Click **Save**
7. **Redeploy** your frontend for changes to take effect

---

## Important Notes

### CORS Configuration
- The backend **MUST** have `CORS_ORIGINS` set to include your frontend URL
- Without this, the frontend will get CORS errors when calling the backend API

### Environment Variable Prefixes
- **NEXT_PUBLIC_*** variables are exposed to the browser
- Variables without this prefix are server-side only
- Never put secrets in NEXT_PUBLIC_* variables unless they're meant for the browser

### Better Auth Secret
- Must be the **same value** in both frontend and backend
- This is critical for JWT token validation

### Redeployment Required
- After adding/changing environment variables, you **must redeploy**
- Go to **Deployments** tab → Click ⋯ on latest deployment → **Redeploy**
- Or push a new commit to trigger automatic deployment

---

## Verification Steps

### 1. Test Backend Health
```bash
curl https://todoagent-navy.vercel.app/health
```
Should return:
```json
{"status":"healthy","version":"1.0.0","environment":"serverless"}
```

### 2. Test Frontend Loading
Visit https://taskmanager-pi-liard.vercel.app/ and verify:
- Page loads without errors
- No CORS errors in browser console (F12)
- Auth forms are visible

### 3. Test Frontend-Backend Connection
1. Open browser console (F12) on https://taskmanager-pi-liard.vercel.app/
2. Try signing up with a test account
3. Check **Network** tab for API calls to `https://todoagent-navy.vercel.app`
4. Should see successful requests (status 200) with no CORS errors

---

## Troubleshooting

### CORS Errors
If you see: `Access to fetch at 'https://todoagent-navy.vercel.app/...' has been blocked by CORS policy`

**Solution:**
1. Verify `CORS_ORIGINS` is set in backend with frontend URL
2. Redeploy backend
3. Clear browser cache

### Environment Variables Not Working
**Solution:**
1. Go to Vercel dashboard
2. Check **Deployments** tab
3. Click on latest deployment → **View Source**
4. Verify environment variables are showing up
5. If not, redeploy

### Backend Connection Refused
**Solution:**
1. Verify `NEXT_PUBLIC_API_URL=https://todoagent-navy.vercel.app` in frontend
2. Test backend health endpoint
3. Redeploy frontend

---

## Local Development

For local development, update your local `.env` files:

### Backend (.env)
```env
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

Then restart both servers:
```bash
# Backend
cd backend
uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```
