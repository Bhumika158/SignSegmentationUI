#!/usr/bin/env python3
"""
FastAPI backend for storing and retrieving sign segmentation validation results.
Uses TinyDB (lightweight NoSQL database) - simpler alternative to MongoDB.
No server required, just a Python library.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

# TinyDB imports
try:
    from tinydb import TinyDB, Query
    TINYDB_AVAILABLE = True
except ImportError:
    TINYDB_AVAILABLE = False
    print("Warning: tinydb not installed. Install with: pip install tinydb")

app = FastAPI(title="Sign Segmentation Validator API - TinyDB")

# Enable CORS for frontend
import os
# Default allowed origins (add your static site URL)
default_origins = [
    "https://signsegmentationui-static.onrender.com",
    "http://localhost:8000",
    "http://localhost:8001"
]
CORS_ORIGINS = os.getenv("CORS_ORIGINS", ",".join(default_origins)).split(",") if os.getenv("CORS_ORIGINS") else default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Set CORS_ORIGINS env var in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TinyDB database file
# For deployment, use absolute path or environment variable
import os
# Default to local data directory, or /tmp for cloud platforms
if os.getenv("RENDER") or os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("DYNO") or os.getenv("PORT"):
    # Running on cloud platform - use /tmp or persistent storage
    DB_PATH = os.getenv("DB_PATH", "/tmp/validation_database_tinydb.json")
else:
    # Local development
    DB_PATH = os.getenv("DB_PATH", "data/validation_database_tinydb.json")
DB_FILE = Path(DB_PATH)
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

db = None
Validation = Query()


def get_database():
    """Get or initialize the database."""
    global db
    if db is None:
        if not TINYDB_AVAILABLE:
            raise RuntimeError("TinyDB not installed. Install with: pip install tinydb")
        try:
            db = TinyDB(str(DB_FILE))
            print(f"✓ TinyDB initialized: {DB_FILE}")
            print(f"✓ Database file exists: {DB_FILE.exists()}")
            # Test the database
            test_count = len(db.all())
            print(f"✓ Database test: {test_count} existing records")
        except Exception as e:
            print(f"✗ Error initializing TinyDB: {e}")
            raise
    return db


# Initialize on startup
@app.on_event("startup")
async def startup_event():
    if TINYDB_AVAILABLE:
        try:
            get_database()  # Initialize database
        except Exception as e:
            print(f"\n✗ Failed to initialize TinyDB: {e}\n")
            print("   Make sure the outputs/ directory exists and is writable\n")
    else:
        print("\n⚠️  TinyDB not available. Install with: pip install tinydb\n")
        print("   API endpoints will return 503 Service Unavailable\n")


class ValidationEntry(BaseModel):
    timestamp: str
    status: str  # "correct", "incorrect", "needs_review"
    feedback: str
    validator: str = "community_member"


class ValidationRequest(BaseModel):
    video_id: str
    validation: ValidationEntry


class ValidationResponse(BaseModel):
    success: bool
    message: str
    video_id: str
    total_validations: int


@app.get("/")
def root():
    try:
        db = get_database()
        tinydb_status = "connected"
    except Exception as e:
        tinydb_status = f"error: {str(e)}"
    return {
        "message": "Sign Segmentation Validator API - TinyDB",
        "status": "running",
        "tinydb": tinydb_status
    }


@app.get("/api/validations")
def get_all_validations():
    """Get all validation results grouped by video_id."""
    try:
        db = get_database()
        all_docs = db.all()
        
        # Group by video_id
        validations_dict = {}
        for doc in all_docs:
            video_id = doc.get("video_id")
            if video_id not in validations_dict:
                validations_dict[video_id] = []
            
            # Remove video_id from response (it's in the key)
            validation = {k: v for k, v in doc.items() if k != "video_id"}
            validations_dict[video_id].append(validation)
        
        return {"validations": validations_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/validations/{video_id}")
def get_video_validations(video_id: str):
    """Get validation results for a specific video."""
    try:
        db = get_database()
        results = db.search(Validation.video_id == video_id)
        validations = []
        
        for doc in results:
            # Remove video_id from response
            validation = {k: v for k, v in doc.items() if k != "video_id"}
            validations.append(validation)
        
        # Sort by timestamp
        validations.sort(key=lambda x: x.get("timestamp", ""))
        
        return {
            "video_id": video_id,
            "validations": validations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/validations", response_model=ValidationResponse)
def save_validation(request: ValidationRequest):
    """Save a validation result for a video."""
    try:
        db = get_database()
        video_id = request.video_id
        validation = request.validation.dict()
        validation["video_id"] = video_id
        
        # Insert validation
        db.insert(validation)
        
        # Count total validations for this video
        total = len(db.search(Validation.video_id == video_id))
        
        return ValidationResponse(
            success=True,
            message="Validation saved successfully",
            video_id=video_id,
            total_validations=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/status/{video_id}")
def get_video_status(video_id: str):
    """Get the latest validation status for a video."""
    try:
        db = get_database()
        results = db.search(Validation.video_id == video_id)
        
        if not results:
            return {
                "video_id": video_id,
                "status": "pending",
                "last_updated": None,
                "has_feedback": False
            }
        
        # Get latest by timestamp
        latest = max(results, key=lambda x: x.get("timestamp", ""))
        
        return {
            "video_id": video_id,
            "status": latest["status"],
            "last_updated": latest["timestamp"],
            "has_feedback": bool(latest.get("feedback", "").strip())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/stats")
def get_validation_stats():
    """Get overall validation statistics."""
    try:
        db = get_database()
        all_docs = db.all()
        video_ids = set(doc.get("video_id") for doc in all_docs if doc.get("video_id"))
        total_videos = len(video_ids)
        
        # Get latest status for each video
        status_counts = {"pending": 0, "correct": 0, "incorrect": 0, "needs_review": 0, "in_progress": 0}
        videos_with_status = set()
        
        for video_id in video_ids:
            results = db.search(Validation.video_id == video_id)
            if results:
                latest = max(results, key=lambda x: x.get("timestamp", ""))
                status = latest.get("status", "pending")
                videos_with_status.add(video_id)
                
                if status == "correct":
                    status_counts["correct"] += 1
                elif status == "incorrect":
                    status_counts["incorrect"] += 1
                elif status == "needs_review":
                    status_counts["needs_review"] += 1
        
        status_counts["pending"] = total_videos - len(videos_with_status)
        
        return {
            "total_videos": total_videos,
            **status_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/api/validations/{video_id}")
def delete_video_validations(video_id: str):
    """Delete all validations for a video (admin function)."""
    try:
        db = get_database()
        removed = db.remove(Validation.video_id == video_id)
        return {
            "success": True,
            "message": f"Deleted validations for {video_id}",
            "count": len(removed)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Serve static files (HTML, etc.) - serve from project root
try:
    app.mount("/", StaticFiles(directory="..", html=True), name="static")
except:
    pass


if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("Sign Segmentation Validator API Server - TinyDB")
    print("=" * 70)
    print(f"Database: {DB_FILE}")
    print(f"API will be available at: http://localhost:8001")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8001)
