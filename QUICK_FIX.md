# Quick Fix for Upload Issue

## The Problem
Your Vercel-deployed frontend can't upload photos because:
1. Backend CORS only allows `localhost:5173`
2. Frontend doesn't know your backend URL

## Quick Solution

### If Backend is NOT Deployed Yet:
You need to deploy the backend first. The frontend on Vercel cannot connect to `localhost`.

**Deploy backend to Railway** (5 minutes):
1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   - `HUGGINGFACE_API_TOKEN` = your token
   - `FRONTEND_URL` = your Vercel URL (e.g., `https://your-app.vercel.app`)
   - `DEBUG` = `False`
5. Copy your Railway URL (e.g., `https://your-app.railway.app`)

### If Backend IS Already Deployed:

**Step 1: Update Backend Environment Variables**

Add to your backend hosting platform (Railway/Render/etc.):
```
FRONTEND_URL=https://your-vercel-app.vercel.app
```

**Step 2: Update Vercel Environment Variables**

1. Go to Vercel dashboard → Your project → Settings → Environment Variables
2. Add:
   ```
   VITE_API_URL=https://your-backend-url.com/api
   ```
3. Redeploy: Deployments tab → Click "..." → Redeploy

**Step 3: Test**
1. Open your Vercel app
2. Press F12 (DevTools) → Console tab
3. Upload a photo
4. Should work now! ✅

## Files Changed

I've already updated your code:
- ✅ `backend/server/server/settings.py` - Added environment-based CORS
- ✅ `frontend/src/components/UploadForm.jsx` - Better error messages
- ✅ `backend/.env.example` - Added new variables
- ✅ `DEPLOYMENT_GUIDE.md` - Full deployment instructions

## Next Steps

1. **If backend not deployed**: Deploy to Railway first
2. **Set environment variables** on both platforms
3. **Redeploy frontend** on Vercel
4. **Test upload** - should work!

Need detailed instructions? See [DEPLOYMENT_GUIDE.md](file:///c:/Users/This/Desktop/ai-img-personalyztion/DEPLOYMENT_GUIDE.md)
