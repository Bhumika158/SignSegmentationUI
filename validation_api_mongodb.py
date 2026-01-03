#!/usr/bin/env python3
"""
FastAPI backend for storing and retrieving sign segmentation validation results.
Uses MongoDB (NoSQL database) for scalable, persistent storage.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import os

# MongoDB imports
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("Warning: pymongo not installed. Install with: pip install pymongo")

app = FastAPI(title="Sign Segmentation Validator API - MongoDB")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "sign_validation_db"
COLLECTION_NAME = "validations"

client = None
db = None
collection = None


def connect_mongodb():
    """Connect to MongoDB and initialize database/collection."""
    global client, db, collection
    
    if not MONGODB_AVAILABLE:
        raise RuntimeError("MongoDB driver (pymongo) not installed. Install with: pip install pymongo")
    
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Create indexes for better query performance
        collection.create_index("video_id")
        collection.create_index([("video_id", 1), ("timestamp", -1)])
        
        print(f"✓ Connected to MongoDB: {DB_NAME}.{COLLECTION_NAME}")
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ MongoDB connection failed: {e}")
        print(f"  Make sure MongoDB is running on {MONGODB_URI}")
        print(f"  Or set MONGODB_URI environment variable")
        return False
    except Exception as e:
        print(f"✗ MongoDB error: {e}")
        return False


# Try to connect on startup
@app.on_event("startup")
async def startup_event():
    if not connect_mongodb():
        print("\n⚠️  MongoDB not available. API will not work properly.")
        print("   Install MongoDB: https://www.mongodb.com/try/download/community")
        print("   Or use validation_api.py with JSON storage instead.\n")


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
    mongodb_status = "connected" if (client and db) else "disconnected"
    return {
        "message": "Sign Segmentation Validator API - MongoDB",
        "status": "running",
        "mongodb": mongodb_status
    }


@app.get("/api/validations")
def get_all_validations():
    """Get all validation results grouped by video_id."""
    if not collection:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        # Group by video_id
        pipeline = [
            {"$group": {
                "_id": "$video_id",
                "validations": {"$push": "$$ROOT"}
            }},
            {"$project": {
                "_id": 0,
                "video_id": "$_id",
                "validations": {
                    "$map": {
                        "input": "$validations",
                        "as": "v",
                        "in": {
                            "timestamp": "$$v.timestamp",
                            "status": "$$v.status",
                            "feedback": "$$v.feedback",
                            "validator": "$$v.validator"
                        }
                    }
                }
            }}
        ]
        
        results = list(collection.aggregate(pipeline))
        validations_dict = {item["video_id"]: item["validations"] for item in results}
        
        return {"validations": validations_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/validations/{video_id}")
def get_video_validations(video_id: str):
    """Get validation results for a specific video."""
    if not collection:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        # Find all validations for this video, sorted by timestamp
        cursor = collection.find(
            {"video_id": video_id},
            {"_id": 0, "video_id": 0}  # Exclude MongoDB _id and video_id from results
        ).sort("timestamp", 1)
        
        validations = list(cursor)
        
        return {
            "video_id": video_id,
            "validations": validations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/validations", response_model=ValidationResponse)
def save_validation(request: ValidationRequest):
    """Save a validation result for a video."""
    if not collection:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        video_id = request.video_id
        validation = request.validation.dict()
        validation["video_id"] = video_id  # Store video_id in document
        
        # Insert validation document
        result = collection.insert_one(validation)
        
        # Count total validations for this video
        total = collection.count_documents({"video_id": video_id})
        
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
    if not collection:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        # Find latest validation for this video
        latest = collection.find_one(
            {"video_id": video_id},
            sort=[("timestamp", -1)],
            projection={"_id": 0, "video_id": 0}
        )
        
        if not latest:
            return {
                "video_id": video_id,
                "status": "pending",
                "last_updated": None,
                "has_feedback": False
            }
        
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
    if not collection:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        # Get distinct video IDs
        video_ids = collection.distinct("video_id")
        total_videos = len(video_ids)
        
        # Get latest status for each video
        pipeline = [
            {"$sort": {"video_id": 1, "timestamp": -1}},
            {"$group": {
                "_id": "$video_id",
                "latest_status": {"$first": "$status"}
            }}
        ]
        
        status_counts = {"pending": 0, "correct": 0, "incorrect": 0, "needs_review": 0, "in_progress": 0}
        
        for item in collection.aggregate(pipeline):
            status = item["latest_status"]
            if status == "correct":
                status_counts["correct"] += 1
            elif status == "incorrect":
                status_counts["incorrect"] += 1
            elif status == "needs_review":
                status_counts["needs_review"] += 1
            else:
                status_counts["pending"] += 1
        
        # Count videos with no validations
        videos_with_validations = len(set(item["_id"] for item in collection.aggregate(pipeline)))
        status_counts["pending"] = total_videos - videos_with_validations
        
        return {
            "total_videos": total_videos,
            **status_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/api/validations/{video_id}")
def delete_video_validations(video_id: str):
    """Delete all validations for a video (admin function)."""
    if not collection:
        raise HTTPException(status_code=503, detail="MongoDB not connected")
    
    try:
        result = collection.delete_many({"video_id": video_id})
        return {
            "success": True,
            "message": f"Deleted {result.deleted_count} validations for {video_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Serve static files (HTML, etc.) - serve from current directory
try:
    app.mount("/", StaticFiles(directory=".", html=True), name="static")
except:
    pass  # If static files mounting fails, API still works


if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("Sign Segmentation Validator API Server - MongoDB")
    print("=" * 70)
    print(f"MongoDB URI: {MONGODB_URI}")
    print(f"Database: {DB_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"API will be available at: http://localhost:8001")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8001)
