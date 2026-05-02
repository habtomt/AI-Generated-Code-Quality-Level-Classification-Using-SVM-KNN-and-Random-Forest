#!/usr/bin/env python3

import os
import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

STORAGE_DIR = "cloud_storage"
METADATA_FILE = os.path.join(STORAGE_DIR, "metadata.json")

os.makedirs(STORAGE_DIR, exist_ok=True)

if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        json.dump({}, f)


def load_metadata():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)


def save_metadata(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class CloudStorageHandler(BaseHTTPRequestHandler):

    def _send_response(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()

        try:
            data = json.loads(body)
        except:
            self._send_response(400, {"error": "Invalid JSON"})
            return

        path = urlparse(self.path).path

        if path == "/upload":
            self.handle_upload(data)
        elif path == "/sync":
            self.handle_sync(data)
        else:
            self._send_response(404, {"error": "Unknown endpoint"})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/download":
            self.handle_download(params)
        elif path == "/metadata":
            self.handle_metadata(params)
        else:
            self._send_response(404, {"error": "Unknown endpoint"})

    def handle_upload(self, data):
        filename = data.get("filename")
        content = data.get("content_base64")
        metadata = data.get("metadata", {})

        if not filename or not content:
            self._send_response(400, {"error": "filename and content required"})
            return

        try:
            file_path = os.path.join(STORAGE_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(content))

            meta = load_metadata()
            meta[filename] = {
                "metadata": metadata,
                "size": os.path.getsize(file_path)
            }
            save_metadata(meta)

            self._send_response(200, {"message": "Upload successful", "filename": filename})
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    def handle_download(self, params):
        filename = params.get("filename", [None])[0]

        if not filename:
            self._send_response(400, {"error": "filename required"})
            return

        file_path = os.path.join(STORAGE_DIR, filename)

        if not os.path.exists(file_path):
            self._send_response(404, {"error": "File not found"})
            return

        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        self._send_response(200, {
            "filename": filename,
            "content_base64": encoded
        })

    def handle_metadata(self, params):
        filename = params.get("filename", [None])[0]

        meta = load_metadata()

        if filename:
            self._send_response(200, meta.get(filename, {}))
        else:
            self._send_response(200, meta)

    def handle_sync(self, data):
        # Dummy cross-platform sync simulation
        self._send_response(200, {
            "message": "Sync completed",
            "platforms": ["web", "mobile", "desktop"]
        })


def run(server_class=HTTPServer, handler_class=CloudStorageHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Cloud storage API running on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()