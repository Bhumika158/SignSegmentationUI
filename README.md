# Sign Segmentation Validation UI

A web-based tool for validating sign language video segmentation with per-segment validation capabilities.

## Features

- ✅ Per-segment validation (atomic and composite components)
- ✅ Real-time progress tracking
- ✅ Database persistence (TinyDB/JSON/MongoDB)
- ✅ Video playback with frame-accurate segmentation
- ✅ Comment/feedback for each segment
- ✅ Overall validation confirmation

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with TinyDB (recommended)
python run_validator_tinydb.py
```

This starts:
- API server on port 8001
- UI server on port 8000
- Opens browser automatically

### Deploy to Render.com

1. **Deploy Backend API:**
   - Go to [render.com](https://render.com)
   - New → Web Service
   - Connect this GitHub repository
   - Settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn validation_api_tinydb:app --host 0.0.0.0 --port $PORT`
   - Copy your API URL

2. **Deploy Frontend:**
   - New → Static Site
   - Connect this GitHub repository
   - **Publish Directory**: `.` (root)
   - Copy your frontend URL

3. **Connect Frontend to Backend:**
   - Create `config.js`:
   ```javascript
   const API_CONFIG = {
       BASE_URL: 'https://your-api-url.onrender.com/api'
   };
   ```
   - Commit and push

## Project Structure

```
.
├── segmentation_validator.html    # Main UI
├── validation_api_tinydb.py      # API backend (TinyDB)
├── validation_api.py              # API backend (JSON)
├── validation_api_mongodb.py     # API backend (MongoDB)
├── run_validator_tinydb.py       # Combined server script
├── requirements.txt               # Python dependencies
├── Procfile                      # Heroku/Railway config
├── render.yaml                    # Render.com config
└── README_DEPLOYMENT.md          # Detailed deployment guide
```

## Data Requirements

The application expects:
- `data/manual_annotations_hierarchical.json` - Annotation data
- `videos/` - Video files
- `data/visualizations/` - Visualization files (optional)

## Database

- **TinyDB** (default): File-based, works locally and on most platforms
- **MongoDB**: Recommended for production (use MongoDB Atlas)

## Documentation

- `README_DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT.md` - Deployment options and configurations
- `VALIDATION_API_README.md` - API documentation

## License

[Your License Here]
