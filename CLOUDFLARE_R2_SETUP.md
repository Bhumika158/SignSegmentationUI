# Cloudflare R2 Setup Guide (Free - Recommended)

Cloudflare R2 is the easiest free option: **10GB storage, 1M requests/month** - perfect for your 327MB of videos!

## Step 1: Create Cloudflare Account

1. Go to: https://dash.cloudflare.com/sign-up
2. Sign up (free)
3. Verify email

## Step 2: Create R2 Bucket

1. In Cloudflare dashboard, click **R2** in sidebar
2. Click **Create bucket**
3. Name: `sign-segmentation-videos`
4. Location: Choose closest to you
5. Click **Create bucket**

## Step 3: Upload Videos

### Option A: Via Cloudflare Dashboard

1. Click your bucket name
2. Click **Upload**
3. Create folder: `videos/`
4. Upload all videos from `/Users/bhumi/Projects/dhwani5.0/videos/`

### Option B: Via R2 API (Faster for many files)

```bash
# Install Cloudflare Wrangler CLI
npm install -g wrangler

# Login
wrangler login

# Upload videos
cd /Users/bhumi/Projects/dhwani5.0
wrangler r2 object put sign-segmentation-videos/videos/My_Name_Is.mp4 --file=videos/My_Name_Is.mp4

# Or upload all at once (create script)
for file in videos/*.mp4; do
    filename=$(basename "$file")
    wrangler r2 object put "sign-segmentation-videos/videos/$filename" --file="$file"
done
```

## Step 4: Make Bucket Public

1. In R2 dashboard → Your bucket → **Settings**
2. Under **Public Access**, click **Allow Access**
3. Copy the **Public URL** (looks like: `https://pub-xxxxx.r2.dev`)

## Step 5: Configure Render

1. Go to Render dashboard → Your API service → **Environment**
2. Add environment variable:
   - **Key**: `CLOUD_STORAGE_URL`
   - **Value**: Your R2 public URL (e.g., `https://pub-xxxxx.r2.dev`)

3. **Redeploy** the service

## Step 6: Test

After redeploying, test:

```bash
# Test API endpoint
curl -I https://signsegmentationui.onrender.com/api/videos/My_Name_Is

# Should redirect to R2 URL
```

## Video URL Format

Your videos will be accessible at:
- `https://pub-xxxxx.r2.dev/videos/{video_id}.mp4`

The API automatically redirects to these URLs when `CLOUD_STORAGE_URL` is set.

## Cost

**Free tier includes:**
- 10GB storage (you need ~327MB ✅)
- 1M requests/month (plenty for validation UI ✅)
- No egress fees (unlike S3)

## Troubleshooting

### Videos not loading?
1. Check bucket is public (Settings → Public Access)
2. Check `CLOUD_STORAGE_URL` environment variable is set correctly
3. Check video paths in R2 match: `videos/{video_id}.mp4`
4. Check Render logs for errors

### Upload taking too long?
Use the Wrangler CLI method (Option B) - much faster for many files.

