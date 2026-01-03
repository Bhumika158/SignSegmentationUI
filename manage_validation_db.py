#!/usr/bin/env python3
"""
Utility script to manage the validation database.
View, clear, or delete specific entries from the TinyDB database.
"""

import json
import sys
from pathlib import Path
from tinydb import TinyDB, Query

import os
# Use environment variable or default path
DB_PATH = os.getenv("DB_PATH", "data/validation_database_tinydb.json")
DB_FILE = Path(DB_PATH)

def show_all_validations():
    """Show all validations in the database."""
    if not DB_FILE.exists():
        print("Database file does not exist.")
        return
    
    db = TinyDB(str(DB_FILE))
    all_docs = db.all()
    
    if not all_docs:
        print("Database is empty.")
        return
    
    print(f"\n{'='*70}")
    print(f"Validation Database: {len(all_docs)} total entries")
    print(f"{'='*70}\n")
    
    # Group by video_id
    by_video = {}
    for doc in all_docs:
        video_id = doc.get('video_id', 'Unknown')
        if video_id not in by_video:
            by_video[video_id] = []
        by_video[video_id].append(doc)
    
    for video_id, validations in sorted(by_video.items()):
        print(f"📹 {video_id}: {len(validations)} validation(s)")
        for i, val in enumerate(validations, 1):
            status = val.get('status', 'unknown')
            timestamp = val.get('timestamp', 'unknown')
            feedback = val.get('feedback', '')[:50]  # First 50 chars
            print(f"   {i}. [{status}] {timestamp}")
            if feedback:
                print(f"      Feedback: {feedback}...")
        print()

def clear_all_validations():
    """Clear all validations from the database."""
    if not DB_FILE.exists():
        print("Database file does not exist.")
        return
    
    db = TinyDB(str(DB_FILE))
    count = len(db.all())
    
    if count == 0:
        print("Database is already empty.")
        return
    
    confirm = input(f"⚠️  Are you sure you want to delete ALL {count} validation(s)? (yes/no): ")
    if confirm.lower() == 'yes':
        db.truncate()
        print(f"✓ Deleted all {count} validation(s).")
    else:
        print("Cancelled.")

def delete_video_validations(video_id):
    """Delete all validations for a specific video."""
    if not DB_FILE.exists():
        print("Database file does not exist.")
        return
    
    db = TinyDB(str(DB_FILE))
    Validation = Query()
    
    results = db.search(Validation.video_id == video_id)
    count = len(results)
    
    if count == 0:
        print(f"No validations found for video: {video_id}")
        return
    
    confirm = input(f"⚠️  Delete {count} validation(s) for '{video_id}'? (yes/no): ")
    if confirm.lower() == 'yes':
        removed = db.remove(Validation.video_id == video_id)
        print(f"✓ Deleted {len(removed)} validation(s) for '{video_id}'.")
    else:
        print("Cancelled.")

def show_database_stats():
    """Show database statistics."""
    if not DB_FILE.exists():
        print("Database file does not exist.")
        return
    
    db = TinyDB(str(DB_FILE))
    all_docs = db.all()
    
    if not all_docs:
        print("Database is empty.")
        return
    
    # Count by status
    status_counts = {}
    video_ids = set()
    
    for doc in all_docs:
        status = doc.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        video_ids.add(doc.get('video_id', 'Unknown'))
    
    print(f"\n{'='*70}")
    print("Database Statistics")
    print(f"{'='*70}")
    print(f"Total validations: {len(all_docs)}")
    print(f"Videos with validations: {len(video_ids)}")
    print(f"\nBy status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    print(f"{'='*70}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_validation_db.py show          - Show all validations")
        print("  python manage_validation_db.py stats         - Show database statistics")
        print("  python manage_validation_db.py clear        - Clear all validations")
        print("  python manage_validation_db.py delete VIDEO  - Delete validations for a video")
        print(f"\nDatabase location: {DB_FILE}")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'show':
        show_all_validations()
    elif command == 'stats':
        show_database_stats()
    elif command == 'clear':
        clear_all_validations()
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Please specify a video_id to delete")
            print("Usage: python manage_validation_db.py delete VIDEO_ID")
            sys.exit(1)
        video_id = sys.argv[2]
        delete_video_validations(video_id)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
