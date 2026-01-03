# Deployment Configuration Guide

## Current Deployment URLs

- **API Backend**: https://signsegmentationui.onrender.com
- **Static Frontend**: https://signsegmentationui-static.onrender.com

## Configuration File

The `config.js` file has been created with the correct API URL:

```javascript
const API_CONFIG = {
    BASE_URL: 'https://signsegmentationui.onrender.com/api'
};
```

## How to Deploy config.js

### Option 1: Commit to GitHub (Recommended)

Since `config.js` is now allowed in the repository:

```bash
cd /Users/bhumi/Projects/SignSegmentationUI_standalone

# Add config.js
git add config.js

# Commit
git commit -m "Add API configuration for Render deployment"

# Push to GitHub
git push origin main
```

Render will automatically redeploy the static site with the new config.js file.

### Option 2: Add via Render Dashboard

1. Go to your Render dashboard
2. Select the `sign-segmentation-ui` static site
3. Click on "Settings" → "Environment"
4. Or use the file editor to create `config.js` directly

### Option 3: Use Build Script

Create a build script that generates `config.js` during deployment.

## Verify Configuration

After deploying `config.js`:

1. Visit: https://signsegmentationui-static.onrender.com
2. Open browser console (F12)
3. You should see: `Using API URL from config.js: https://signsegmentationui.onrender.com/api`
4. The API status indicator (top-right) should show green "✓ API Connected"

## Testing

Test the API connection:
```bash
# Test API root
curl https://signsegmentationui.onrender.com/

# Test validations endpoint
curl https://signsegmentationui.onrender.com/api/validations
```

## Troubleshooting

### If API not connecting:

1. **Check CORS**: Make sure API allows requests from `https://signsegmentationui-static.onrender.com`
   - Update `CORS_ORIGINS` environment variable in Render API service
   - Or update `validation_api_tinydb.py` to include your static URL

2. **Check config.js**: Verify it's accessible at:
   - https://signsegmentationui-static.onrender.com/config.js

3. **Check browser console**: Look for errors in F12 console

### Update CORS in API:

In Render dashboard → API service → Environment:
- Add: `CORS_ORIGINS` = `https://signsegmentationui-static.onrender.com`

Or update the code to include your static URL in allowed origins.

