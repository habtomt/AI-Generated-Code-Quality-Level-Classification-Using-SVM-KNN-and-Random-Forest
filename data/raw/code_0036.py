#!/usr/bin/env python3

import os
import time
import json
import zipfile
import hashlib
import urllib.request
from datetime import datetime

SOURCE_DIR = os.environ.get("BACKUP_SOURCE_DIR", "./data")
BACKUP_URL = os.environ.get("BACKUP_URL", "http://localhost:8000/upload")
INTERVAL_SECONDS = int(os.environ.get("BACKUP_INTERVAL_SECONDS", "3600"))
TEMP_DIR = os.environ.get("BACKUP_TEMP_DIR", "./backups_temp")
METADATA_FILE = os.path.join(TEMP_DIR, "backup_metadata.json")


def ensure_dirs():
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)


def create_zip_backup():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(TEMP_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(SOURCE_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, SOURCE_DIR)
                zipf.write(full_path, arcname)

    return zip_path, zip_name, timestamp


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def upload_backup(file_path, file_name, checksum):
    with open(file_path, "rb") as f:
        data = f.read()

    req = urllib.request.Request(
        BACKUP_URL,
        data=data,
        method="PUT",
        headers={
            "Content-Type": "application/zip",
            "X-Backup-Filename": file_name,
            "X-Checksum-SHA256": checksum,
        },
    )

    with urllib.request.urlopen(req) as response:
        return response.status, response.read().decode("utf-8")


def save_metadata(record):
    metadata = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

    metadata.append(record)

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)


def run_backup():
    zip_path, zip_name, timestamp = create_zip_backup()
    checksum = calculate_sha256(zip_path)

    status, response = upload_backup(zip_path, zip_name, checksum)

    record = {
        "timestamp": timestamp,
        "file": zip_name,
        "checksum": checksum,
        "status": status,
        "response": response,
    }

    save_metadata(record)

    print(f"[{timestamp}] Backup uploaded: {zip_name} | Status: {status}")


def main():
    ensure_dirs()

    while True:
        try:
            run_backup()
        except Exception as e:
            print(f"[ERROR] Backup failed: {e}")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()