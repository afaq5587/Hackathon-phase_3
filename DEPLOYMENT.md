# Deployment Guide - Phase 3 Todo Chatbot

## 🚀 Deployed URLs

- **Frontend**: https://taskmanager-pi-liard.vercel.app/
- **Backend**: https://todoagent-navy.vercel.app/

---

## 🔧 Vercel Environment Variables Setup

### Frontend Environment Variables
**Project**: taskmanager-pi-liard

Go to: Vercel Dashboard → taskmanager-pi-liard → Settings → Environment Variables

Add these variables for **all environments** (Production, Preview, Development):

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=https://todoagent-navy.vercel.app

# Frontend URL (for Better Auth)
NEXT_PUBLIC_APP_URL=https://taskmanager-pi-liard.vercel.app

# Better Auth Secret (must match backend)
BETTER_AUTH_SECRET=VyjAovwOyAF0L7xduZb8ihHG66r5yGfI

# Database URL (Neon PostgreSQL)
DATABASE_URL=postgresql://neondb_owner:npg_n93BcYgNxOor@ep-winter-night-ahrtfj3x-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Backend Environment Variables
**Project**: todoagent-navy

Go to: Vercel Dashboard → todoagent-navy → Settings → Environment Variables

Add these variables for **all environments** (Production, Preview, Development):

```bash
# Database URL (Neon PostgreSQL)
DATABASE_URL=postgresql://neondb_owner:npg_n93BcYgNxOor@ep-winter-night-ahrtfj3x-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require

# Better Auth Secret (must match frontend)
BETTER_AUTH_SECRET=VyjAovwOyAF0L7xduZb8ihHG66r5yGfI

# Gemini API Key
GEMINI_API_KEY=AIzaSyCZn-NuPdYY3iqMfG587jSLK1zj1DxG7M8

# CORS Origins (your frontend URL)
CORS_ORIGINS=https://taskmanager-pi-liard.vercel.app,http://localhost:3000

# Debug mode (false for production)
DEBUG=false
```

---

## 📋 After Setting Environment Variables

1. **Redeploy Both Projects**:
   - Go to Deployments tab in each project
   - Click "..." on latest deployment → "Redeploy"
   - OR push a new commit to trigger automatic deployment

2. **Test Backend Health**:
   ```
   https://todoagent-navy.vercel.app/health
   ```
   Should return:
   ```json
   {
     "status": "healthy",
     "version": "1.0.0",
     "environment": "serverless"
   }
   ```

3. **Test Frontend**:
   ```
   https://taskmanager-pi-liard.vercel.app/
   ```
   - Should load without errors
   - Try signing up/logging in
   - Try creating tasks via chat

---

## 🔍 Troubleshooting

### Backend Returns 500 Error
- Check Function Logs in Vercel Dashboard
- Verify all environment variables are set correctly
- Ensure DATABASE_URL is correct and database is accessible

### Frontend Can't Connect to Backend
- Check browser console for CORS errors
- Verify `NEXT_PUBLIC_API_URL` is set in frontend
- Verify `CORS_ORIGINS` includes frontend URL in backend

### Database Connection Issues
- Ensure DATABASE_URL has `?sslmode=require` at the end
- Check Neon dashboard to verify database is running
- Verify connection string credentials are correct

---

## 🔄 Local Development

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on: http://localhost:3000

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```
Runs on: http://localhost:8000

Make sure to use the local URLs in your `.env` file for local development.
