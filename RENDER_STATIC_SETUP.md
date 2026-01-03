# Render Static Site Configuration

## Current Issue: "Not Found" Error

If you're getting "Not Found" when accessing the static URL, check these settings in Render:

## Render Static Site Settings

1. Go to your Render dashboard
2. Select the `sign-segmentation-ui` static site
3. Click "Settings"
4. Verify these settings:

### Required Settings:

- **Name**: `sign-segmentation-ui`
- **Build Command**: (leave empty or `echo "No build needed"`)
- **Publish Directory**: `.` (dot = root directory)
- **Branch**: `main` (or your default branch)

### Important:

- The `segmentation_validator.html` file must be in the **root** of your repository
- The Publish Directory should be `.` (current directory), NOT `SignSegmentationUI/`
- Make sure the file is committed and pushed to GitHub

## Verify Files in Repository

Check that these files are in the root:
- `segmentation_validator.html` ✅
- `config.js` ✅
- `index.html` ✅ (redirects to segmentation_validator.html)

## Direct URL Access

Try accessing the HTML file directly:
- https://signsegmentationui-static.onrender.com/segmentation_validator.html

If this works but the root URL doesn't, the `index.html` redirect will fix it.

## Troubleshooting Steps

1. **Check Render Logs**:
   - Go to Render dashboard → Static site → Logs
   - Look for any build/deployment errors

2. **Verify File Structure**:
   ```bash
   cd /Users/bhumi/Projects/SignSegmentationUI_standalone
   ls -la *.html
   ```

3. **Check GitHub**:
   - Verify `segmentation_validator.html` is in the root of your GitHub repo
   - URL: https://github.com/Bhumika158/SignSegmentationUI

4. **Redeploy**:
   - In Render dashboard → Static site → Manual Deploy
   - Or push a new commit to trigger auto-deploy

## Expected File Structure

```
SignSegmentationUI/ (GitHub repo root)
├── segmentation_validator.html  ← Must be here
├── config.js
├── index.html
├── requirements.txt
├── validation_api_tinydb.py
└── ... (other files)
```

## Quick Fix

If the file structure is correct but still getting "Not Found":

1. **Force Redeploy**:
   - Render dashboard → Static site → Manual Deploy → Deploy latest commit

2. **Check Publish Directory**:
   - Settings → Publish Directory should be `.` (not empty, not a subdirectory)

3. **Verify Branch**:
   - Settings → Branch should match your GitHub branch (usually `main`)

