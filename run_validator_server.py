#!/usr/bin/env python3
"""
Simple HTTP server to run the Sign Segmentation Validator UI.
This allows the HTML file to load JSON and video files without CORS issues.

Note: For persistent validation storage, use run_validator_with_api.py instead,
which includes the API backend for NoSQL database storage.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow loading resources
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    # Serve from current directory (standalone repo)
    os.chdir(Path(__file__).parent)
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/segmentation_validator.html"
        print("=" * 70)
        print("Sign Segmentation Validator Server")
        print("=" * 70)
        print(f"\nServer running at: {url}")
        print(f"\nPress Ctrl+C to stop the server")
        print("\nOpening browser...")
        
        # Open browser automatically
        try:
            webbrowser.open(url)
        except:
            print(f"Could not open browser automatically. Please visit: {url}")
        
        print("\n" + "=" * 70)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    main()
