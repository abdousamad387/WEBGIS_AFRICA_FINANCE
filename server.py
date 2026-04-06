#!/usr/bin/env python3
"""Local development server for Africa Finance WebGIS (port 9999)."""
import http.server
import os
import sys
import webbrowser

PORT = 9999
DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIR)

handler = http.server.SimpleHTTPRequestHandler
handler.extensions_map.update({".js": "application/javascript", ".json": "application/json"})

print(f"  Africa Finance WebGIS")
print(f"  http://localhost:{PORT}")
print(f"  Ctrl+C pour arreter\n")

try:
    webbrowser.open(f"http://localhost:{PORT}")
    with http.server.HTTPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n  Serveur arrete.")
    sys.exit(0)
