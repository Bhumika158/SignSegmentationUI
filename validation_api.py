#!/usr/bin/env python3
"""
FastAPI backend for storing and retrieving sign segmentation validation results.
Uses JSON file storage (NoSQL-like) for simplicity and persistence.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
from pathlib import Path
import json
from datetime import datetime

app = FastAPI(title="Sign Segmentation Validator API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database file (JSON-based NoSQL storage)
import os
DB_PATH = os.getenv("DB_PATH", "data/validation_database.json")
DB_FILE = Path(DB_PATH)

# Ensure outputs directory exists
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

# Initialize database if it doesn't exist
def init_database():
    """Initialize database file if it doesn't exist."""
    if not DB_FILE.exists():
        with open(DB_FILE, 'w') as f:
            json.dump({"validations": {}}, f, indent=2)
        print(f"Initialized database: {DB_FILE}")

# Initialize on import
init_database()


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


def load_database() -> Dict:
    """Load validation database from JSON file."""
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"validations": {}}


def save_database(data: Dict):
    """Save validation database to JSON file."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.get("/")
def root():
    return {"message": "Sign Segmentation Validator API", "status": "running"}


@app.get("/api/validations")
def get_all_validations():
    """Get all validation results."""
    db = load_database()
    return {"validations": db.get("validations", {})}


@app.get("/api/validations/{video_id}")
def get_video_validations(video_id: str):
    """Get validation results for a specific video."""
    db = load_database()
    validations = db.get("validations", {})
    return {
        "video_id": video_id,
        "validations": validations.get(video_id, [])
    }


@app.post("/api/validations", response_model=ValidationResponse)
def save_validation(request: ValidationRequest):
    """Save a validation result for a video."""
    db = load_database()
    
    if "validations" not in db:
        db["validations"] = {}
    
    video_id = request.video_id
    validation = request.validation.dict()
    
    # Add validation to the list for this video
    if video_id not in db["validations"]:
        db["validations"][video_id] = []
    
    db["validations"][video_id].append(validation)
    
    # Save to database
    save_database(db)
    
    return ValidationResponse(
        success=True,
        message="Validation saved successfully",
        video_id=video_id,
        total_validations=len(db["validations"][video_id])
    )


@app.get("/api/status/{video_id}")
def get_video_status(video_id: str):
    """Get the latest validation status for a video."""
    db = load_database()
    validations = db.get("validations", {}).get(video_id, [])
    
    if not validations:
        return {
            "video_id": video_id,
            "status": "pending",
            "last_updated": None,
            "has_feedback": False
        }
    
    latest = validations[-1]
    return {
        "video_id": video_id,
        "status": latest["status"],
        "last_updated": latest["timestamp"],
        "has_feedback": bool(latest.get("feedback", "").strip())
    }


@app.get("/api/stats")
def get_validation_stats():
    """Get overall validation statistics."""
    db = load_database()
    validations = db.get("validations", {})
    
    total_videos = len(validations)
    pending = 0
    completed = 0
    needs_review = 0
    in_progress = 0
    
    for video_id, video_validations in validations.items():
        if not video_validations:
            pending += 1
        else:
            latest = video_validations[-1]
            status = latest["status"]
            if status == "correct":
                completed += 1
            elif status == "incorrect":
                needs_review += 1
            elif status == "needs_review":
                in_progress += 1
            else:
                pending += 1
    
    return {
        "total_videos": total_videos,
        "pending": pending,
        "completed": completed,
        "needs_review": needs_review,
        "in_progress": in_progress
    }


@app.delete("/api/validations/{video_id}")
def delete_video_validations(video_id: str):
    """Delete all validations for a video (admin function)."""
    db = load_database()
    
    if video_id in db.get("validations", {}):
        del db["validations"][video_id]
        save_database(db)
        return {"success": True, "message": f"Validations deleted for {video_id}"}
    else:
        raise HTTPException(status_code=404, detail="Video not found")


# Serve static files (HTML, etc.) - serve from current directory
try:
    app.mount("/", StaticFiles(directory=".", html=True), name="static")
except:
    pass  # If static files mounting fails, API still works


if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("Sign Segmentation Validator API Server")
    print("=" * 70)
    print(f"Database: {DB_FILE}")
    print(f"API will be available at: http://localhost:8001")
    print(f"Frontend should connect to: http://localhost:8001/api")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8001)
