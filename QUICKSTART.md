# 🚀 Quick Start Guide

## Prerequisites
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Replicate API account (free at https://replicate.com)

## Setup (5 minutes)

### 1. Get Replicate API Token
1. Go to https://replicate.com/account/api-tokens
2. Create a free account if needed
3. Copy your API token

### 2. Configure Backend
```bash
# Navigate to backend directory
cd backend

# Copy environment template
copy .env.example .env

# Edit .env and add your token:
# REPLICATE_API_TOKEN=your_token_here
```

### 3. Run Setup Script
```bash
# From project root
setup_backend.bat
```

This will:
- Activate virtual environment
- Install Python dependencies
- Run database migrations

### 4. Start Backend
```bash
start_backend.bat
```

Backend runs on: http://localhost:8000

### 5. Start Frontend (in new terminal)
```bash
start_frontend.bat
```

Frontend runs on: http://localhost:5173

## Usage

1. Open http://localhost:5173 in your browser
2. Upload a child's photo (clear face, good lighting)
3. Click "Personalize Photo"
4. Wait 25-35 seconds for AI processing
5. Download your personalized illustration!

## Troubleshooting

### "Module not found: django"
- Make sure virtual environment is activated
- Run: `pip install -r backend/requirements.txt`

### "CORS error" in browser
- Check backend is running on port 8000
- Check frontend is running on port 5173

### "Replicate API error"
- Verify API token in `backend/.env`
- Check you have credits on Replicate (free tier available)

### "No face detected"
- Use a photo with clear, visible face
- Ensure good lighting
- Try a different photo

## What's Next?

- Read [README.md](README.md) for full documentation
- Check [TECHNICAL_NOTES.md](TECHNICAL_NOTES.md) for implementation details
- Review [walkthrough.md](C:/Users/This/.gemini/antigravity/brain/7362fe2d-1f46-4ade-8d90-52e8e79853a6/walkthrough.md) for architecture

## Need Help?

Check the comprehensive documentation in:
- `README.md` - Full project overview
- `TECHNICAL_NOTES.md` - Technical details and limitations
- Architecture diagram - Visual system overview

---

**Enjoy creating personalized illustrations! ✨**
