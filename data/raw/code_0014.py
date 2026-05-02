#!/usr/bin/env python3

import os
import time
import json
import shutil
import hashlib
from datetime import datetime
from threading import Thread, Event


# ---------------------------
# CONFIGURATION
# ---------------------------

BACKUP_INTERVAL_SECONDS = 5
BACKUP_ROOT = "distributed_backup_storage"
DATABASE_SIMULATION_FILE = "cloud_database.json"
MAX_VERSIONS = 5


# ---------------------------
# UTILITIES
# ---------------------------

def ensure_dirs():
    os.makedirs(BACKUP_ROOT, exist_ok=True)


def compute_hash(file_path):
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def load_database():
    if not os.path.exists(DATABASE_SIMULATION_FILE):
        data = {"users": [], "transactions": [], "meta": {"created": str(datetime.now())}}
        with open(DATABASE_SIMULATION_FILE, "w") as f:
            json.dump(data, f, indent=2)
    with open(DATABASE_SIMULATION_FILE, "r") as f:
        return json.load(f)


def save_database(data):
    with open(DATABASE_SIMULATION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------
# BACKUP ENGINE
# ---------------------------

class BackupManager:
    def __init__(self):
        self.stop_event = Event()
        ensure_dirs()

    def create_backup(self):
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        version_dir = os.path.join(BACKUP_ROOT, f"backup_{timestamp}")
        os.makedirs(version_dir, exist_ok=True)

        backup_file = os.path.join(version_dir, "database.json")

        shutil.copy2(DATABASE_SIMULATION_FILE, backup_file)

        checksum = compute_hash(backup_file)

        meta = {
            "timestamp": timestamp,
            "checksum": checksum
        }

        with open(os.path.join(version_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)

        print(f"[BACKUP CREATED] {version_dir}")
        self.cleanup_old_backups()

    def cleanup_old_backups(self):
        backups = sorted(os.listdir(BACKUP_ROOT))
        if len(backups) > MAX_VERSIONS:
            to_delete = backups[:-MAX_VERSIONS]
            for b in to_delete:
                shutil.rmtree(os.path.join(BACKUP_ROOT, b))
                print(f"[CLEANUP] Removed old backup {b}")

    def restore_latest(self):
        backups = sorted(os.listdir(BACKUP_ROOT))
        if not backups:
            print("[RESTORE] No backups found")
            return

        latest = backups[-1]
        backup_file = os.path.join(BACKUP_ROOT, latest, "database.json")

        shutil.copy2(backup_file, DATABASE_SIMULATION_FILE)
        print(f"[RESTORE] Restored from {latest}")

    def schedule_backups(self):
        while not self.stop_event.is_set():
            self.create_backup()
            time.sleep(BACKUP_INTERVAL_SECONDS)

    def start(self):
        t = Thread(target=self.schedule_backups, daemon=True)
        t.start()
        return t

    def stop(self):
        self.stop_event.set()


# ---------------------------
# SIMULATION WORKLOAD
# ---------------------------

def simulate_database_changes():
    data = load_database()

    data["users"].append({"id": len(data["users"]) + 1, "name": f"user_{time.time()}"})
    data["transactions"].append({"id": len(data["transactions"]) + 1, "amount": round(time.time() % 100, 2)})

    save_database(data)
    print("[DB UPDATED]")


# ---------------------------
# MAIN
# ---------------------------

def main():
    manager = BackupManager()
    thread = manager.start()

    try:
        for _ in range(20):
            simulate_database_changes()
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        manager.stop()
        thread.join(timeout=2)
        manager.restore_latest()
        print("[SYSTEM SHUTDOWN]")


if __name__ == "__main__":
    main()