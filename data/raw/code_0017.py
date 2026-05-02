#!/usr/bin/env python3

import os
import time
import zipfile
import boto3
import schedule
from datetime import datetime

BACKUP_DIR = "./data"
TEMP_BACKUP_FILE = "/tmp/backup.zip"
LOG_FILE = "backup_log.txt"

BUCKET_NAME = os.environ.get("AWS_BUCKET", "my-backup-bucket")
REGION = os.environ.get("AWS_REGION", "us-east-1")


def log(message):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line, end="")


def create_backup():
    log("Starting backup job")

    try:
        with zipfile.ZipFile(TEMP_BACKUP_FILE, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(BACKUP_DIR):
                for file in files:
                    path = os.path.join(root, file)
                    arcname = os.path.relpath(path, BACKUP_DIR)
                    zipf.write(path, arcname)

        log("Backup archive created")

        s3 = boto3.client("s3", region_name=REGION)

        key = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"

        s3.upload_file(TEMP_BACKUP_FILE, BUCKET_NAME, key)

        log(f"Backup uploaded to s3://{BUCKET_NAME}/{key}")

        with open("last_success.txt", "w") as f:
            f.write(datetime.utcnow().isoformat())

        log("Backup job completed successfully")

    except Exception as e:
        log(f"Backup failed: {str(e)}")


def monitor_backups():
    log("Running backup monitor")

    try:
        if not os.path.exists("last_success.txt"):
            log("No successful backup found")
            return

        with open("last_success.txt", "r") as f:
            last = f.read().strip()

        last_time = datetime.fromisoformat(last)
        delta = datetime.utcnow() - last_time

        if delta.total_seconds() > 3600 * 24:
            log("WARNING: Last backup older than 24 hours")
        else:
            log("Backup status healthy")

    except Exception as e:
        log(f"Monitor error: {str(e)}")


def setup_scheduler():
    schedule.every(1).hours.do(create_backup)
    schedule.every(30).minutes.do(monitor_backups)

    log("Scheduler started")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    setup_scheduler()