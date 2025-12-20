# 🎨 AI Image Personalization

Transform children's photos into beautiful cartoon illustrations using AI! This application uses advanced face detection and stylization to create personalized illustrations perfect for storybooks, gifts, and more.

## ✨ Features

- 📸 **Photo Upload**: Simple drag-and-drop or click-to-upload interface
- 🤖 **AI-Powered Stylization**: Uses Hugging Face's state-of-the-art models for face detection and cartoon stylization
- 🎨 **Beautiful UI**: Modern, responsive design built with React
- ⚡ **Fast Processing**: Results in 25-35 seconds
- 💾 **Easy Download**: One-click download of personalized illustrations

## 🚀 Live Demo

- **Frontend**: [Coming Soon - Deploy to Vercel]
- **Backend API**: [Coming Soon - Deploy to Railway/Render]

## 🛠️ Tech Stack

### Frontend
- React 19
- Vite
- Modern CSS with responsive design

### Backend
- Django 4.2+
- Django REST Framework
- Hugging Face Inference API
- OpenCV for image processing
- Gunicorn + WhiteNoise for production

## 📋 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

### Prerequisites
- Python 3.8+
- Node.js 16+
- Hugging Face API token (free at https://huggingface.co/settings/tokens)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rudresh45/ai-img-personalyztion.git
   cd ai-img-personalyztion
   ```

2. **Setup backend**
   ```bash
   setup_backend.bat
   ```

3. **Start backend** (in one terminal)
   ```bash
   start_backend.bat
   ```

4. **Start frontend** (in another terminal)
   ```bash
   start_frontend.bat
   ```

5. **Open browser**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api

## 🌐 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for comprehensive deployment instructions.

**Quick Deployment Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

### Recommended Platforms
- **Frontend**: Vercel (free tier)
- **Backend**: Railway or Render (free tier)

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Full deployment guide
- [TECHNICAL_NOTES.md](TECHNICAL_NOTES.md) - Technical implementation details
- [QUICK_FIX.md](QUICK_FIX.md) - Common issues and solutions

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────┐         ┌──────────────────┐
│   React     │ ──────> │   Django    │ ──────> │  Hugging Face    │
│  Frontend   │  HTTP   │   Backend   │   API   │  Inference API   │
│  (Vite)     │ <────── │   (REST)    │ <────── │  (AI Models)     │
└─────────────┘         └─────────────┘         └──────────────────┘
```

## 🔑 Environment Variables

### Backend (.env)
```bash
HUGGINGFACE_API_TOKEN=your_token_here
FRONTEND_URL=https://your-frontend.vercel.app  # Production only
DEBUG=False  # Production only
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api  # Local
# VITE_API_URL=https://your-backend.railway.app/api  # Production
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for providing free AI model inference
- OpenCV for image processing capabilities
- The open-source community for amazing tools and libraries

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ by Rudresh**