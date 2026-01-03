# Convert Annotation Videos to Browser-Compatible Format

## Problem
The annotation videos in `data/visualizations/annotation_videos/` use the 'mp4v' codec (MPEG-4 Part 2), which modern browsers don't support. This causes errors like:
- "FFmpegDemuxer: no supported streams"
- Videos don't play in browsers

## Solution
Convert annotation videos to H.264 codec (browser-compatible) using the conversion script.

## Usage

### Option 1: Using FFmpeg (Recommended - Faster, Better Quality)

1. **Install FFmpeg** (if not already installed):
   ```bash
   # macOS
   brew install ffmpeg
   
   # Linux
   sudo apt-get install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

2. **Run the conversion script**:
   ```bash
   python convert_annotation_videos.py
   ```

   This will:
   - Convert all annotation videos to H.264 codec
   - Save them to `data/visualizations/annotation_videos_browser/`
   - Preserve frame numbers and all annotations
   - Make them browser-compatible

### Option 2: Using OpenCV Only (Slower, but no FFmpeg needed)

If FFmpeg is not available, the script will automatically fall back to OpenCV:
```bash
python convert_annotation_videos.py
```

Note: OpenCV conversion is slower but will work without FFmpeg.

## Output

Converted videos will be saved to:
```
data/visualizations/annotation_videos_browser/
```

These videos:
- ✅ Use H.264 codec (browser-compatible)
- ✅ Have frame numbers overlaid (same as original annotation videos)
- ✅ Match frame-for-frame with original annotation videos
- ✅ Will work in the segmentation validator UI

## After Conversion

The UI will automatically:
1. Try to load browser-compatible annotation videos first
2. Fall back to regular videos if annotation videos aren't available
3. Display frame numbers and annotations correctly

## Verification

After conversion, test in the UI:
1. Select a video
2. Click on atomic/composite signs
3. Verify that:
   - Videos play correctly
   - Frame numbers match annotations
   - Segments play from correct start to end frames

## Troubleshooting

### FFmpeg not found
- Install FFmpeg (see above)
- Or let the script use OpenCV fallback (slower)

### Conversion fails
- Check that input videos exist in `data/visualizations/annotation_videos/`
- Verify you have write permissions for output directory
- Check console for specific error messages

### Videos still don't play
- Clear browser cache
- Check browser console for errors
- Verify converted videos exist in `annotation_videos_browser/` directory
