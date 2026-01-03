# Deployment Guide

## Deployment Options

Since GitHub Pages only serves static files, you have several options for deploying this full-stack application:

### Option 1: Render (Recommended - Free Tier Available)

**Deploy Backend API:**
1. Go to [render.com](https://render.com) and sign up
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Build Command**: `pip install -r SignSegmentationUI/requirements.txt`
   - **Start Command**: `cd SignSegmentationUI && uvicorn validation_api_tinydb:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. Add environment variable: `PORT` (auto-set by Render)

**Deploy Frontend (Static):**
1. Create a new "Static Site" on Render
2. Connect GitHub repository
3. Settings:
   - **Build Command**: (leave empty or `echo "No build needed"`)
   - **Publish Directory**: `SignSegmentationUI`
4. Update `segmentation_validator.html` API_BASE_URL to point to your Render API URL

### Option 2: Railway (Easy Deployment)

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub
3. Add service:
   - **Backend**: Web Service** - Points to `SignSegmentationUI/validation_api_tinydb.py`
   - **Frontend**: Static Site** - Points to `SignSegmentationUI/` folder
4. Railway auto-detects Python and serves static files

### Option 3: Fly.io (Global Edge Deployment)

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run: `fly launch` in project root
3. Create `fly.toml` (see below)
4. Deploy: `fly deploy`

### Option 4: Heroku (Classic Option)

1. Install Heroku CLI
2. Create `Procfile` (see below)
3. Deploy: `git push heroku main`

## Quick Deploy Scripts

### For Render/Railway

The API will automatically detect the port from environment variables.

### For Fly.io

Create `fly.toml`:
```toml
app = "sign-segmentation-validator"
primary_region = "iad"

[build]

[http_service]
  internal_port = 8001
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  protocol = "tcp"
  internal_port = 8001
```

### For Heroku

Create `Procfile`:
```
web: cd SignSegmentationUI && uvicorn validation_api_tinydb:app --host 0.0.0.0 --port $PORT
```

## Environment Variables

Set these in your hosting platform:

- `PORT` - Usually auto-set by platform
- `MONGODB_URI` - (Optional) If using MongoDB instead of TinyDB
- `CORS_ORIGINS` - (Optional) Comma-separated list of allowed origins

## Frontend Configuration

After deploying the backend, update `segmentation_validator.html`:

```javascript
// Change from:
const API_BASE_URL = 'http://localhost:8001/api';

// To your deployed API URL:
const API_BASE_URL = 'https://your-api-url.onrender.com/api';
// OR
const API_BASE_URL = 'https://your-api-url.railway.app/api';
```

## Database Considerations

### TinyDB (Default)
- File-based, works on most platforms
- Data stored in `outputs/validation_database_tinydb.json`
- **Note**: On ephemeral file systems (like Heroku), data will be lost on restart
- **Solution**: Use MongoDB or external storage

### MongoDB (Recommended for Production)
1. Use MongoDB Atlas (free tier available)
2. Set `MONGODB_URI` environment variable
3. Use `validation_api_mongodb.py` instead

## Step-by-Step: Render Deployment

### Backend API:
```bash
# 1. Push code to GitHub
git add .
git commit -m "Prepare for deployment"
git push

# 2. On Render.com:
# - New Web Service
# - Connect GitHub repo
# - Root Directory: SignSegmentationUI
# - Build: pip install -r requirements.txt
# - Start: uvicorn validation_api_tinydb:app --host 0.0.0.0 --port $PORT
# - Environment: Python 3
```

### Frontend:
```bash
# 1. Update API URL in segmentation_validator.html
# 2. On Render.com:
# - New Static Site
# - Connect GitHub repo
# - Build Command: (empty)
# - Publish Directory: SignSegmentationUI
```

## Testing Deployment

After deployment, test:
```bash
# Test API
curl https://your-api-url.onrender.com/

# Test validations endpoint
curl https://your-api-url.onrender.com/api/validations
```

## Troubleshooting

### CORS Issues
- Update `allow_origins` in API files to include your frontend URL
- Or set `CORS_ORIGINS` environment variable

### Database Not Persisting
- Use MongoDB Atlas for persistent storage
- Or configure external file storage (S3, etc.)

### Port Issues
- Most platforms set `PORT` automatically
- Use `uvicorn ... --port $PORT` in start command

## Security Notes

1. **CORS**: Restrict origins in production
2. **API Keys**: Don't commit secrets
3. **Rate Limiting**: Add rate limiting for production
4. **HTTPS**: Most platforms provide HTTPS automatically

