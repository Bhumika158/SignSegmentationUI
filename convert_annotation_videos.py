#!/usr/bin/env python3
"""
Convert annotation videos from 'mp4v' codec to browser-compatible H.264 codec.
This allows annotation videos to play in browsers.
"""

import cv2
import subprocess
import sys
from pathlib import Path
from tqdm import tqdm

def convert_video_to_h264(input_path: str, output_path: str, fps: float = None):
    """
    Convert video to H.264 codec using ffmpeg (preferred) or OpenCV fallback.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    if not input_path.exists():
        print(f"  ⚠️  Input file not found: {input_path}")
        return False
    
    # Try ffmpeg first (better quality, faster)
    try:
        # Get FPS from input video if not provided
        if fps is None:
            cap = cv2.VideoCapture(str(input_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
        
        # Use ffmpeg to convert to H.264
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-c:v', 'libx264',  # H.264 codec
            '-preset', 'medium',  # Balance between speed and compression
            '-crf', '23',  # Good quality
            '-c:a', 'aac',  # Audio codec
            '-movflags', '+faststart',  # Web optimization
            '-y',  # Overwrite output
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"  ✓ Converted: {output_path.name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  FFmpeg conversion failed: {e.stderr}")
        print(f"  Trying OpenCV fallback...")
        
    except FileNotFoundError:
        print(f"  ⚠️  FFmpeg not found, trying OpenCV fallback...")
    
    # Fallback: Use OpenCV (slower, but works without ffmpeg)
    try:
        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            print(f"  ⚠️  Cannot open video: {input_path}")
            return False
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if fps is None:
            fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Use H.264 codec (avc1) - browser compatible
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for _ in tqdm(range(frame_count), desc=f"  Converting {input_path.name}"):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        cap.release()
        out.release()
        
        print(f"  ✓ Converted: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"  ✗ OpenCV conversion failed: {e}")
        return False


def main():
    # Try multiple paths - local first, then parent directory
    annotation_dir = None
    output_dir = None
    for base_path in [Path('data/visualizations'), Path('../data/visualizations')]:
        if (base_path / 'annotation_videos').exists():
            annotation_dir = base_path / 'annotation_videos'
            output_dir = base_path / 'annotation_videos_browser'
            break
    
    if not annotation_dir:
        annotation_dir = Path('data/visualizations/annotation_videos')
        output_dir = Path('data/visualizations/annotation_videos_browser')
    
    if not annotation_dir.exists():
        print(f"Error: Annotation videos directory not found: {annotation_dir}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    annotation_videos = list(annotation_dir.glob('*_annotation_guide.mp4'))
    
    if not annotation_videos:
        print("No annotation videos found.")
        sys.exit(0)
    
    print("=" * 80)
    print("Converting Annotation Videos to Browser-Compatible Format")
    print("=" * 80)
    print(f"Input: {annotation_dir}")
    print(f"Output: {output_dir}")
    print(f"Found {len(annotation_videos)} videos to convert\n")
    
    converted = 0
    failed = 0
    
    for video_path in tqdm(annotation_videos, desc="Converting videos"):
        output_path = output_dir / video_path.name
        
        # Skip if already converted
        if output_path.exists():
            print(f"  ⊙ Skipping (already exists): {video_path.name}")
            converted += 1
            continue
        
        if convert_video_to_h264(str(video_path), str(output_path)):
            converted += 1
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Conversion complete!")
    print(f"  ✓ Converted: {converted}")
    if failed > 0:
        print(f"  ✗ Failed: {failed}")
    print(f"Output directory: {output_dir}")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Update segmentation_validator.html to use converted videos")
    print("2. The converted videos use H.264 codec and will work in browsers")


if __name__ == '__main__':
    main()
