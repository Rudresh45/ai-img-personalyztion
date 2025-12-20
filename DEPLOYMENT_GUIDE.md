# Deployment Guide - AI Photo Personalization

This guide covers deploying the frontend to Vercel and backend to a hosting platform.

## Prerequisites

- GitHub account
- Vercel account (free)
- Backend hosting account (Railway, Render, or similar)
- Hugging Face API token

## Backend Deployment

### Option 1: Railway (Recommended)

1. **Create Railway Account**: Visit [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Django

3. **Configure Environment Variables**:
   Go to your project → Variables tab and add:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   FRONTEND_URL=https://your-app.vercel.app
   DEBUG=False
   ```

4. **Get Backend URL**: Copy your Railway app URL (e.g., `https://your-app.railway.app`)

### Option 2: Render

1. **Create Render Account**: Visit [render.com](https://render.com)

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend/server && python manage.py migrate && gunicorn server.wsgi:application`

3. **Add Environment Variables**:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   FRONTEND_URL=https://your-app.vercel.app
   DEBUG=False
   PYTHON_VERSION=3.11
   ```

4. **Get Backend URL**: Copy your Render app URL

## Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. **Push to GitHub**: Ensure your code is pushed to GitHub

2. **Import to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `frontend` directory as the root

3. **Configure Build Settings**:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

### Step 2: Set Environment Variables

In Vercel dashboard → Settings → Environment Variables, add:

```
VITE_API_URL=https://your-backend-url.com/api
```

**Important**: Replace `your-backend-url.com` with your actual backend URL from Railway/Render.

### Step 3: Redeploy

After adding environment variables:
- Go to Deployments tab
- Click "..." on latest deployment → Redeploy

## Update Backend CORS

After deploying frontend, update your backend `.env` file (or environment variables on hosting platform):

```bash
FRONTEND_URL=https://your-app.vercel.app
```

Then redeploy the backend.

## Testing the Deployment

1. **Open Frontend**: Visit your Vercel URL
2. **Open Browser DevTools**: Press F12
3. **Upload a Photo**: Try uploading a test image
4. **Check Network Tab**: 
   - Look for request to `/api/upload/`
   - Should return `201 Created`
   - No CORS errors in Console

### Common Issues

**CORS Error**: 
- Verify `FRONTEND_URL` is set correctly in backend
- Ensure it matches your Vercel URL exactly (including https://)
- Redeploy backend after changing environment variables

**"Cannot connect to server"**:
- Check backend is running (visit backend URL in browser)
- Verify `VITE_API_URL` in Vercel matches backend URL
- Check backend logs for errors

**Upload fails silently**:
- Check browser Console for errors
- Verify backend has `HUGGINGFACE_API_TOKEN` set
- Check backend logs

## Local Development

For local development, create `.env` files:

**Backend** (`backend/.env`):
```bash
HUGGINGFACE_API_TOKEN=your_token_here
DEBUG=True
```

**Frontend** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000/api
```

Then run:
```bash
# Terminal 1 - Backend
cd backend
env\Scripts\activate  # Windows
python server\manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Environment Variables Reference

### Backend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `HUGGINGFACE_API_TOKEN` | Yes | API token for AI processing | `hf_xxx...` |
| `FRONTEND_URL` | Production only | Vercel frontend URL for CORS | `https://app.vercel.app` |
| `BACKEND_DOMAIN` | Production only | Backend domain (no https://) | `app.railway.app` |
| `DEBUG` | No | Debug mode (False in production) | `False` |

### Frontend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `VITE_API_URL` | Yes | Backend API URL | `https://backend.railway.app/api` |

## Security Notes

- Never commit `.env` files to Git
- Always use `DEBUG=False` in production
- Keep API tokens secure
- Use HTTPS in production (Vercel/Railway provide this automatically)
