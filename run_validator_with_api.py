#!/usr/bin/env python3
"""
Run the validation UI with API backend.
This starts both the API server and the static file server.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import signal
import os
import threading
import http.server
import socketserver

API_PORT = 8001
UI_PORT = 8000

def start_api_server(use_tinydb=True):
    """Start the FastAPI backend server in a separate thread."""
    print("Starting API server...")
    import uvicorn
    
    if use_tinydb:
        try:
            from validation_api_tinydb import app
            print("  Using TinyDB database")
        except ImportError:
            print("  ⚠️  TinyDB not available, falling back to JSON")
            from validation_api import app
    else:
        from validation_api import app
        print("  Using JSON database")
    
    def run_api():
        uvicorn.run(app, host="0.0.0.0", port=API_PORT, log_level="info")
    
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    return api_thread

def start_ui_server():
    """Start the static file server for the UI."""
    print("Starting UI server...")
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    # Serve from current directory (standalone repo)
    os.chdir(Path(__file__).parent)
    handler = MyHTTPRequestHandler
    
    ui_server = socketserver.TCPServer(("", UI_PORT), handler)
    ui_server.allow_reuse_address = True
    return ui_server

def main():
    import sys
    
    # Check if user wants to use MongoDB instead
    use_tinydb = True
    if len(sys.argv) > 1:
        if sys.argv[1] == "--mongodb":
            use_tinydb = False
            try:
                from validation_api_mongodb import app
            except ImportError:
                print("⚠️  MongoDB API not available. Using TinyDB instead.")
                use_tinydb = True
        elif sys.argv[1] == "--json":
            use_tinydb = False
    
    print("=" * 70)
    print("Sign Segmentation Validator - Starting Services")
    print("=" * 70)
    
    # Start API server
    api_thread = start_api_server(use_tinydb=use_tinydb)
    time.sleep(2)  # Give API time to start
    
    # Start UI server
    ui_server = start_ui_server()
    
    url = f"http://localhost:{UI_PORT}/segmentation_validator.html"
    db_type = "TinyDB" if use_tinydb else "JSON"
    db_file = "outputs/validation_database_tinydb.json" if use_tinydb else "outputs/validation_database.json"
    
    print(f"\n✓ API Server: http://localhost:{API_PORT}")
    print(f"✓ UI Server: {url}")
    print(f"✓ Database: {db_type} ({db_file})")
    print(f"\nOpening browser...")
    print("Press Ctrl+C to stop all servers\n")
    print("Usage: python run_validator_with_api.py [--tinydb|--mongodb|--json]")
    
    try:
        webbrowser.open(url)
        ui_server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        ui_server.shutdown()
        print("Servers stopped.")

if __name__ == "__main__":
    main()
