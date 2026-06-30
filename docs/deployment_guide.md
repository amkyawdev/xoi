# Deployment Guide

Guide for deploying Amkyaw AI Agent to various platforms.

## Frontend Deployment (Vercel)

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to frontend directory
cd frontend

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Option 2: GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your repository
5. Configure build settings:
   - Framework Preset: Other
   - Root Directory: ./frontend
   - Build Command: (leave empty)
   - Output Directory: ./

6. Click "Deploy"

### Environment Variables (Vercel)

Set these in Vercel dashboard → Settings → Environment Variables:

- `VITE_API_URL` - Your backend URL

---

## Backend Deployment (Render)

### Option 1: Render Dashboard

1. Create a [Render](https://render.com) account
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free tier works for testing

5. Add Environment Variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `OPENAI_API_KEY`
   - etc.

6. Click "Create Web Service"

### Option 2: Railway

1. Create a [Railway](https://railway.app) account
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. Add Environment Variables

---

## Database (Neon PostgreSQL)

### Setup

1. Create a [Neon](https://neon.tech) account
2. Create a new project
3. Copy the connection string

### Connection String Format

```
postgresql://username:password@ep-xxx-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
```

### Update Backend

Set `DATABASE_URL` in your backend environment with the Neon connection string.

---

## Docker Deployment (Optional)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run

```bash
docker build -t amkyaw-backend .
docker run -p 8000:8000 --env-file .env amkyaw-backend
```

---

## Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure CORS for production domains
- [ ] Set up proper database backups
- [ ] Enable rate limiting
- [ ] Add monitoring/logging
- [ ] Set up error tracking (e.g., Sentry)
