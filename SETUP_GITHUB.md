# Setup GitHub Repository

## Step 1: Initialize and Push to GitHub

Run these commands in the `SignSegmentationUI_standalone` directory:

```bash
cd /Users/bhumi/Projects/SignSegmentationUI_standalone

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sign Segmentation Validation UI"

# Set main branch
git branch -M main

# Add remote repository
git remote add origin https://github.com/Bhumika158/SignSegmentationUI.git

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy to Render.com

### Deploy Backend API:

1. Go to [render.com](https://render.com) → Sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub account and select `Bhumika158/SignSegmentationUI`
4. Configure:
   - **Name**: `sign-segmentation-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn validation_api_tinydb:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Wait for deployment (2-3 minutes)
7. **Copy your API URL** (e.g., `https://sign-segmentation-api.onrender.com`)

### Deploy Frontend:

1. In Render, click "New" → "Static Site"
2. Connect GitHub and select `Bhumika158/SignSegmentationUI`
3. Configure:
   - **Name**: `sign-segmentation-ui`
   - **Build Command**: (leave empty)
   - **Publish Directory**: `.` (root)
4. Click "Create Static Site"
5. **Copy your frontend URL**

### Connect Frontend to Backend:

1. In your local repo, create `config.js`:
```javascript
const API_CONFIG = {
    BASE_URL: 'https://sign-segmentation-api.onrender.com/api'
};
```

2. **IMPORTANT**: Add `config.js` to `.gitignore` (already done) - don't commit it!

3. For Render Static Site, you can:
   - Use environment variables in Render dashboard
   - Or create `config.js` directly in Render's file editor
   - Or use a build script to generate it

## Alternative: Use Environment Variables

Instead of `config.js`, you can set the API URL via environment variable and update the HTML to read it.

## Next Steps

After deployment:
1. Test the API: `curl https://your-api-url.onrender.com/`
2. Visit your frontend URL
3. The UI should automatically connect to the API

## Notes

- Database files are stored in `/tmp` on Render (ephemeral)
- For production, use MongoDB Atlas (free tier available)
- Videos and annotation files need to be hosted separately or included in the repo

