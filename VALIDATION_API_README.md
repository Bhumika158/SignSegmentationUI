# Validation API - NoSQL Database Backend

## Overview

The validation system now uses a NoSQL database (JSON-based) to persist validation results across system restarts. This ensures that validation status is maintained even when the server is restarted.

## Architecture

- **Backend API**: FastAPI server (port 8001) - stores validations in JSON file
- **Frontend UI**: HTML/JavaScript - connects to API for saving/loading
- **Database**: JSON file (`outputs/validation_database.json`) - NoSQL-like storage

## Quick Start

### Option 1: Run with API (Recommended)

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Run the combined server (API + UI)
python run_validator_with_api.py
```

This starts:
- API server on port 8001
- UI server on port 8000
- Opens browser automatically

### Option 2: Run API and UI Separately

**Terminal 1 - API Server:**
```bash
python validation_api.py
```

**Terminal 2 - UI Server:**
```bash
python run_validator_server.py
```

## API Endpoints

### Get All Validations
```
GET http://localhost:8001/api/validations
```
Returns all validation results for all videos.

### Get Video Validations
```
GET http://localhost:8001/api/validations/{video_id}
```
Returns validation history for a specific video.

### Save Validation
```
POST http://localhost:8001/api/validations
Content-Type: application/json

{
  "video_id": "My_Name_Is",
  "validation": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "status": "correct",
    "feedback": "Segmentation looks accurate",
    "validator": "community_member"
  }
}
```

### Get Video Status
```
GET http://localhost:8001/api/status/{video_id}
```
Returns latest validation status for a video.

### Get Statistics
```
GET http://localhost:8001/api/stats
```
Returns overall validation statistics (pending, completed, etc.).

## Database Structure

The database is stored in `outputs/validation_database.json`:

```json
{
  "validations": {
    "My_Name_Is": [
      {
        "timestamp": "2024-01-15T10:30:00.000Z",
        "status": "correct",
        "feedback": "Segmentation looks accurate",
        "validator": "community_member"
      }
    ],
    "21_Twenty_One": [
      {
        "timestamp": "2024-01-15T11:00:00.000Z",
        "status": "needs_review",
        "feedback": "Frame alignment issue",
        "validator": "community_member"
      }
    ]
  }
}
```

## Features

### ✅ Persistent Storage
- Validations saved to JSON file (NoSQL-like)
- Survives server restarts
- Can be backed up easily

### ✅ Multi-User Support
- Each validation includes timestamp and validator
- Multiple validations per video (history)
- Latest status is used for progress table

### ✅ Automatic Fallback
- If API is unavailable, falls back to localStorage
- Ensures system works even if API is down
- Seamless user experience

### ✅ Real-time Updates
- Progress table updates immediately after saving
- Status reflects latest validation
- No page refresh needed

## Migration from localStorage

If you have existing validations in localStorage:
1. The system will automatically use them if API is unavailable
2. When you save new validations, they go to the API
3. Old localStorage data remains as backup

## Backup and Restore

### Backup Database
```bash
cp outputs/validation_database.json outputs/validation_database_backup.json
```

### Restore Database
```bash
cp outputs/validation_database_backup.json outputs/validation_database.json
```

## Production Deployment

For production use:

1. **Change CORS settings** in `validation_api.py`:
   ```python
   allow_origins=["https://your-domain.com"]  # Instead of "*"
   ```

2. **Use proper database** (optional):
   - MongoDB
   - PostgreSQL with JSONB
   - Any NoSQL database

3. **Add authentication** (if needed):
   - API keys
   - User authentication
   - Role-based access

## Troubleshooting

### API not connecting
- Check if API server is running: `python validation_api.py`
- Verify port 8001 is not in use
- Check browser console for CORS errors

### Validations not saving
- Check API server logs
- Verify `outputs/` directory is writable
- Check browser console for errors

### Database file not found
- API will create it automatically
- Ensure `outputs/` directory exists
- Check file permissions
