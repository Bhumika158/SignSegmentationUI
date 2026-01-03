# Quick Deployment Guide

## 🚀 Fastest Way: Render.com (Free Tier)

### Step 1: Deploy Backend API

1. Go to [render.com](https://render.com) → Sign up (free)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `sign-segmentation-api`
   - **Root Directory**: `SignSegmentationUI`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn validation_api_tinydb:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Wait for deployment (2-3 minutes)
7. Copy your API URL (e.g., `https://sign-segmentation-api.onrender.com`)

### Step 2: Deploy Frontend

1. In Render, click "New" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `sign-segmentation-ui`
   - **Build Command**: (leave empty)
   - **Publish Directory**: `SignSegmentationUI`
4. Click "Create Static Site"
5. Copy your frontend URL

### Step 3: Connect Frontend to Backend

1. In your GitHub repo, create `SignSegmentationUI/config.js`:
```javascript
const API_CONFIG = {
    BASE_URL: 'https://sign-segmentation-api.onrender.com/api'
};
```

2. Commit and push:
```bash
git add SignSegmentationUI/config.js
git commit -m "Add API configuration"
git push
```

3. Render will auto-redeploy the frontend

### Step 4: Test

Visit your frontend URL - it should connect to the API automatically!

## 🔄 Alternative: Railway.app

1. Go to [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub"
3. Add two services:
   - **Backend**: Select `SignSegmentationUI/validation_api_tinydb.py`
   - **Frontend**: Static site pointing to `SignSegmentationUI/`
4. Railway auto-detects and deploys!

## 📝 Important Notes

- **Database**: TinyDB files are ephemeral on most platforms. For production, use MongoDB Atlas (free tier available)
- **CORS**: Update `CORS_ORIGINS` environment variable with your frontend URL
- **Port**: Most platforms set `PORT` automatically - use `$PORT` in start command

## 🐛 Troubleshooting

**API not connecting?**
- Check `config.js` has correct API URL
- Verify CORS settings in API
- Check API logs in Render/Railway dashboard

**Database not persisting?**
- Use MongoDB Atlas instead of TinyDB
- Or configure external file storage

## 🔒 Security

Before going to production:
1. Set `CORS_ORIGINS` to your frontend URL only
2. Add rate limiting
3. Use MongoDB with authentication
4. Enable HTTPS (usually automatic)

