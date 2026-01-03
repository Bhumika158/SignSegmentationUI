# Fix "Not Found" Error on Static Site

## Problem
Accessing https://signsegmentationui-static.onrender.com gives "Not Found"

## Solution

### Step 1: Verify Render Static Site Settings

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your `sign-segmentation-ui` static site
3. Go to **Settings**
4. Check these settings:

**Critical Settings:**
- **Publish Directory**: Must be `.` (dot = root directory)
- **Build Command**: Can be empty or `echo "No build needed"`
- **Branch**: Should be `main` (or your default branch)

### Step 2: Commit and Push Files

```bash
cd /Users/bhumi/Projects/SignSegmentationUI_standalone

# Add all new files
git add config.js index.html DEPLOY_CONFIG.md RENDER_STATIC_SETUP.md .gitignore validation_api_tinydb.py

# Commit
git commit -m "Add config.js and index.html for static site deployment"

# Push to GitHub
git push origin main
```

### Step 3: Force Redeploy in Render

1. In Render dashboard → Static site
2. Click **Manual Deploy** → **Deploy latest commit**
3. Wait for deployment to complete

### Step 4: Test Direct File Access

Try accessing the HTML file directly:
- https://signsegmentationui-static.onrender.com/segmentation_validator.html

If this works, the `index.html` will redirect to it automatically.

## Common Issues

### Issue 1: Publish Directory is Wrong
- **Wrong**: Empty or `SignSegmentationUI/`
- **Correct**: `.` (dot)

### Issue 2: Files Not in Root
- Make sure `segmentation_validator.html` is in the **root** of your GitHub repo
- Check: https://github.com/Bhumika158/SignSegmentationUI

### Issue 3: Branch Mismatch
- Settings → Branch should match your GitHub default branch
- Usually `main` or `master`

## Verify File Structure

Your GitHub repo should have this structure:
```
SignSegmentationUI/
├── segmentation_validator.html  ← Main UI file
├── index.html                    ← Redirect file
├── config.js                     ← API configuration
├── requirements.txt
├── validation_api_tinydb.py
└── ... (other files)
```

## After Fixing

Once deployed correctly, you should be able to access:
- https://signsegmentationui-static.onrender.com (redirects to HTML)
- https://signsegmentationui-static.onrender.com/segmentation_validator.html (direct access)

Both should work and connect to your API at:
- https://signsegmentationui.onrender.com/api

