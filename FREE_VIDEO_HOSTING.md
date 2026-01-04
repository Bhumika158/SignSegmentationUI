# Free Video Hosting Solutions

Since Render free tier doesn't support disks, here are free alternatives:

## Option 1: Cloudflare R2 (Recommended - Easiest Free Option)

**Free Tier**: 10GB storage, 1M requests/month

### Setup:

1. **Create Cloudflare Account**: https://dash.cloudflare.com/sign-up
2. **Enable R2**: Dashboard → R2 → Create bucket
3. **Upload Videos**: Use Cloudflare dashboard or CLI
4. **Get Public URL**: R2 provides public URLs

### Update API:

```python
# Add to validation_api_tinydb.py
import requests

R2_BUCKET_URL = os.getenv("R2_BUCKET_URL", "https://your-bucket.r2.cloudflarestorage.com")

@app.get("/api/videos/{video_id}")
def get_video(video_id: str):
    # Try local first, then R2
    video_path = find_video_file(video_id, "regular")
    if video_path:
        return FileResponse(str(video_path), media_type="video/mp4")
    
    # Fetch from R2
    r2_url = f"{R2_BUCKET_URL}/videos/{video_id}.mp4"
    response = requests.get(r2_url, stream=True)
    if response.status_code == 200:
        return StreamingResponse(response.iter_content(), media_type="video/mp4")
    raise HTTPException(404, f"Video not found: {video_id}")
```

## Option 2: AWS S3 (Free Tier)

**Free Tier**: 5GB storage, 20,000 GET requests/month (first 12 months)

### Setup:

1. **Create AWS Account**: https://aws.amazon.com/free/
2. **Create S3 Bucket**: Make it public
3. **Upload Videos**: Use AWS Console or CLI
4. **Get Public URLs**: `https://your-bucket.s3.amazonaws.com/videos/{video_id}.mp4`

### Update API:

Similar to R2, but use S3 URLs.

## Option 3: Compress Videos (Quick Fix)

Reduce video file sizes to fit under 10MB for GitHub Releases.

### Compress Script:

```bash
# Install ffmpeg if needed
brew install ffmpeg  # macOS

# Compress all videos
cd /Users/bhumi/Projects/dhwani5.0/videos
mkdir -p compressed

for file in *.mp4; do
    ffmpeg -i "$file" \
        -c:v libx264 \
        -crf 28 \
        -preset slow \
        -vf "scale=640:-1" \
        -c:a aac \
        -b:a 128k \
        "compressed/${file}"
    
    # Check size
    size=$(stat -f%z "compressed/${file}")
    if [ $size -lt 10485760 ]; then  # 10MB in bytes
        echo "✓ $file compressed to $(($size / 1024 / 1024))MB"
    else
        echo "✗ $file still too large: $(($size / 1024 / 1024))MB"
    fi
done
```

**Note**: This reduces quality. Not ideal for production.

## Option 4: Google Cloud Storage (Free Tier)

**Free Tier**: 5GB storage, 5GB egress/month

Similar setup to S3.

## Option 5: Use Different Free Hosting

- **Railway**: Free tier with persistent storage
- **Fly.io**: Free tier with volumes
- **Render** (paid): $7/month for disk storage

## Recommended: Cloudflare R2

**Why R2?**
- ✅ 10GB free (enough for your 327MB)
- ✅ 1M requests/month free
- ✅ Easy setup
- ✅ Public URLs work directly
- ✅ No egress fees

### Quick R2 Setup:

1. Sign up: https://dash.cloudflare.com
2. R2 → Create bucket → Name: `sign-segmentation-videos`
3. Upload videos via dashboard
4. Get public URL format: `https://pub-xxxxx.r2.dev/videos/{video_id}.mp4`
5. Update API to use R2 URLs

## Implementation

I can update the API to support R2/S3 if you choose that option. Just let me know which one you prefer!

