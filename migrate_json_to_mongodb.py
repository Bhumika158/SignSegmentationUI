#!/usr/bin/env python3
"""
Migrate validation data from JSON file to MongoDB.
Run this once to migrate existing validations.
"""

import json
from pathlib import Path
from pymongo import MongoClient
import os
from datetime import datetime

# Configuration
import os
JSON_DB_PATH = os.getenv("DB_PATH", "data/validation_database.json")
JSON_DB_FILE = Path(JSON_DB_PATH)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "sign_validation_db"
COLLECTION_NAME = "validations"


def migrate():
    """Migrate validations from JSON to MongoDB."""
    
    # Check if JSON file exists
    if not JSON_DB_FILE.exists():
        print(f"✗ JSON database file not found: {JSON_DB_FILE}")
        print("  Nothing to migrate.")
        return
    
    # Load JSON data
    print(f"Loading data from {JSON_DB_FILE}...")
    try:
        with open(JSON_DB_FILE, 'r') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"✗ Error reading JSON file: {e}")
        return
    
    validations = json_data.get("validations", {})
    if not validations:
        print("  No validations found in JSON file.")
        return
    
    print(f"  Found {len(validations)} videos with validations")
    
    # Connect to MongoDB
    print(f"\nConnecting to MongoDB at {MONGODB_URI}...")
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print("✓ Connected to MongoDB")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("  Make sure MongoDB is running.")
        return
    
    # Create indexes
    collection.create_index("video_id")
    collection.create_index([("video_id", 1), ("timestamp", -1)])
    
    # Migrate data
    print(f"\nMigrating validations to MongoDB...")
    migrated_count = 0
    skipped_count = 0
    
    for video_id, video_validations in validations.items():
        for validation in video_validations:
            # Add video_id to validation document
            validation["video_id"] = video_id
            
            # Check if already exists (by video_id, timestamp, status)
            existing = collection.find_one({
                "video_id": video_id,
                "timestamp": validation["timestamp"],
                "status": validation["status"]
            })
            
            if existing:
                skipped_count += 1
                continue
            
            # Insert into MongoDB
            collection.insert_one(validation)
            migrated_count += 1
    
    print(f"\n✓ Migration complete!")
    print(f"  Migrated: {migrated_count} validations")
    print(f"  Skipped (duplicates): {skipped_count} validations")
    
    # Verify
    total_in_mongodb = collection.count_documents({})
    print(f"  Total in MongoDB: {total_in_mongodb} validations")
    
    # Ask about backup
    backup_path = JSON_DB_FILE.with_suffix('.json.backup')
    if not backup_path.exists():
        import shutil
        shutil.copy(JSON_DB_FILE, backup_path)
        print(f"\n✓ Created backup: {backup_path}")
    
    print("\nNext steps:")
    print("  1. Use validation_api_mongodb.py instead of validation_api.py")
    print("  2. Test the API to verify data is accessible")
    print("  3. Keep JSON file as backup (already backed up)")


if __name__ == "__main__":
    print("=" * 70)
    print("JSON to MongoDB Migration Tool")
    print("=" * 70)
    migrate()
