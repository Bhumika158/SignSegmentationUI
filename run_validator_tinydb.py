#!/usr/bin/env python3
"""
Run the validation UI with TinyDB API backend.
This starts both the TinyDB API server and the static file server.
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

def start_api_server():
    """Start the TinyDB FastAPI backend server in a separate thread."""
    print("Starting TinyDB API server...")
    import uvicorn
    
    try:
        from validation_api_tinydb import app
    except ImportError:
        print("⚠️  TinyDB not installed. Install with: pip install tinydb")
        print("   Falling back to JSON storage...")
        from validation_api import app
    
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
        
        def log_message(self, format, *args):
            """Override to show requests in console"""
            print(f"[UI Server] {args[0]}")
    
    # Serve from current directory (standalone repo)
    os.chdir(Path(__file__).parent)
    handler = MyHTTPRequestHandler
    
    ui_server = socketserver.TCPServer(("", UI_PORT), handler)
    ui_server.allow_reuse_address = True
    return ui_server

def main():
    print("=" * 70)
    print("Sign Segmentation Validator - Starting Services (TinyDB)")
    print("=" * 70)
    
    # Start API server
    api_thread = start_api_server()
    time.sleep(2)  # Give API time to start
    
    # Start UI server
    ui_server = start_ui_server()
    
    url = f"http://localhost:{UI_PORT}/segmentation_validator.html"
    print(f"\n✓ API Server: http://localhost:{API_PORT}")
    print(f"✓ UI Server: {url}")
    print(f"✓ Database: TinyDB (data/validation_database_tinydb.json)")
    print(f"\nOpening browser...")
    print("Press Ctrl+C to stop all servers\n")
    
    try:
        webbrowser.open(url)
        ui_server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        ui_server.shutdown()
        print("Servers stopped.")

if __name__ == "__main__":
    main()
