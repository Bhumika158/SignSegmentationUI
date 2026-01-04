# Quick Video Setup Guide

## Problem
GitHub Releases has a 10MB file size limit, and some videos exceed this (e.g., Waterfall.mp4 is 15MB).

## Solution: Serve Videos via API ✅

I've added video serving endpoints to your API. Videos will be served from the backend instead of GitHub.

## What Changed

1. **API Endpoints Added**:
   - `GET /api/videos/{video_id}` - Regular video
   - `GET /api/videos/{video_id}/annotation` - Annotation video
   - `GET /api/videos/{video_id}/landmark` - Landmark video

2. **HTML Updated**: Now uses API endpoints for videos on deployed sites

3. **Environment Variable**: `VIDEO_BASE_PATH=/tmp/videos` (set in render.yaml)

## Next Steps

### Option 1: Render Disk (Easiest)

1. **Add Disk in Render**:
   - Go to: https://dashboard.render.com
   - Click your `sign-segmentation-api` service
   - Settings → **Disk** → **Add Disk**
   - Name: `videos-storage`
   - Mount Path: `/tmp/videos`
   - Size: **1GB** (enough for 327MB of videos)

2. **Upload Videos via SSH**:
   ```bash
   # From your local machine
   cd /Users/bhumi/Projects/dhwani5.0
   
   # Get SSH info from Render dashboard → Your service → Shell tab
   # Then upload:
   rsync -avz --progress videos/ <render-service>@ssh.render.com:/tmp/videos/
   ```

3. **Redeploy**: Render will auto-redeploy after you push the code changes

### Option 2: Manual Upload via Render Shell

1. In Render dashboard → Your API service → **Shell** tab
2. Run:
   ```bash
   mkdir -p /tmp/videos
   ```
3. Use the file upload feature (if available) or upload via SSH

### Option 3: Cloud Storage (S3/Google Cloud)

See `VIDEO_UPLOAD_GUIDE.md` for detailed instructions.

## Commit and Deploy

```bash
cd /Users/bhumi/Projects/SignSegmentationUI_standalone

# Files are already staged
git commit -m "Add video serving via API endpoints

- Add /api/videos/{video_id} endpoints to serve videos
- Update HTML to use API endpoints for videos on deployed sites
- Add VIDEO_BASE_PATH environment variable
- Support for regular, landmark, and annotation videos"

git push origin main
```

## After Deployment

1. **Wait 1-2 minutes** for Render to redeploy
2. **Add Render Disk** (if using Option 1)
3. **Upload videos** to `/tmp/videos/`
4. **Test**: Visit https://signsegmentationui-static.onrender.com and try playing a video

## Verify It Works

```bash
# Test API endpoint (after uploading videos)
curl -I https://signsegmentationui.onrender.com/api/videos/My_Name_Is

# Should return: HTTP/1.1 200 OK
# Content-Type: video/mp4
```

## Current Status

- ✅ API endpoints added
- ✅ HTML updated to use API
- ✅ Environment variable configured
- ⚠️ Videos need to be uploaded to Render Disk

Once videos are uploaded, everything will work!

