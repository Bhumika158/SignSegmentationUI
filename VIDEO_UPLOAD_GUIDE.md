# Video Upload Guide for Render

Since GitHub Releases has a 10MB file size limit and some videos exceed this, we've set up video serving via the API. Here's how to upload videos to Render.

## Option 1: Render Disk Storage (Recommended)

### Step 1: Add Disk Service in Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your `sign-segmentation-api` service
3. Go to **Settings** → **Disk**
4. Click **Add Disk**
5. Set:
   - **Name**: `videos-storage`
   - **Mount Path**: `/tmp/videos`
   - **Size**: 1GB (or more if needed)

### Step 2: Upload Videos via SSH

1. In Render dashboard → Your API service → **Shell** tab
2. Or use SSH (if enabled):
   ```bash
   ssh <your-render-service>@ssh.render.com
   ```

3. Create videos directory:
   ```bash
   mkdir -p /tmp/videos
   ```

4. Upload videos using `scp` or `rsync`:
   ```bash
   # From your local machine
   cd /Users/bhumi/Projects/dhwani5.0
   
   # Upload all videos
   rsync -avz --progress videos/ <your-render-service>@ssh.render.com:/tmp/videos/
   
   # Or use scp for individual files
   scp videos/My_Name_Is.mp4 <your-render-service>@ssh.render.com:/tmp/videos/
   ```

### Step 3: Set Environment Variable

In Render dashboard → API service → **Environment**:
- Add: `VIDEO_BASE_PATH=/tmp/videos`

## Option 2: Upload via Render File Manager (If Available)

Some Render plans include a file manager:
1. Go to your service → **Files** tab
2. Navigate to `/tmp/videos`
3. Upload videos directly

## Option 3: Use Cloud Storage (S3/Google Cloud/Azure)

### For AWS S3:

1. Create S3 bucket
2. Upload videos to bucket
3. Make bucket public or use signed URLs
4. Update API to fetch from S3:

```python
# In validation_api_tinydb.py, add:
import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

@app.get("/api/videos/{video_id}")
def get_video(video_id: str):
    try:
        # Try local first
        video_path = find_video_file(video_id, "regular")
        if video_path:
            return FileResponse(str(video_path), media_type="video/mp4")
        
        # Fallback to S3
        s3_key = f"videos/{video_id}.mp4"
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=3600
        )
        return RedirectResponse(url=url)
    except Exception as e:
        raise HTTPException(404, f"Video not found: {video_id}")
```

## Option 4: Compress Videos (Temporary Solution)

If you want to use GitHub Releases, compress videos:

```bash
# Install ffmpeg if not installed
brew install ffmpeg  # macOS

# Compress a video (reduce quality to fit under 10MB)
cd /Users/bhumi/Projects/dhwani5.0/videos
for file in *.mp4; do
    ffmpeg -i "$file" -c:v libx264 -crf 28 -preset slow -c:a copy "compressed_${file}"
done
```

**Note**: This reduces video quality. Not recommended for production.

## Quick Start: Render Disk

The easiest solution is Render Disk:

1. **Add Disk** in Render dashboard (1GB should be enough for 327MB of videos)
2. **Set environment variable**: `VIDEO_BASE_PATH=/tmp/videos`
3. **Upload videos** via SSH/rsync
4. **Redeploy** the API service

The API will automatically serve videos from `/tmp/videos/` once uploaded.

## Verify Videos Are Accessible

After uploading, test:

```bash
# Test API endpoint
curl -I https://signsegmentationui.onrender.com/api/videos/My_Name_Is

# Should return 200 OK with Content-Type: video/mp4
```

## Current API Endpoints

- `GET /api/videos/{video_id}` - Regular video
- `GET /api/videos/{video_id}/landmark` - Landmark video (with overlaid landmarks)
- `GET /api/videos/{video_id}/annotation` - Annotation video (browser-compatible)

All endpoints automatically fall back to regular video if the specific type isn't found.

