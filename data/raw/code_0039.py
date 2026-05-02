#!/usr/bin/env python3

import os
import json
import gzip
import shutil
from datetime import datetime

HOT_DIR = "hot_data"
COLD_DIR = "cold_storage"
INDEX_FILE = "cold_index.json"


class ColdStorageSystem:
    def __init__(self):
        os.makedirs(HOT_DIR, exist_ok=True)
        os.makedirs(COLD_DIR, exist_ok=True)
        self.index = self.load_index()

    def load_index(self):
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_index(self):
        with open(INDEX_FILE, "w") as f:
            json.dump(self.index, f, indent=2)

    def add_file(self, filename, content):
        path = os.path.join(HOT_DIR, filename)
        with open(path, "w") as f:
            f.write(content)

        self.index[filename] = {
            "status": "hot",
            "created_at": str(datetime.utcnow())
        }
        self.save_index()

    def archive_file(self, filename):
        hot_path = os.path.join(HOT_DIR, filename)
        if not os.path.exists(hot_path):
            return

        cold_path = os.path.join(COLD_DIR, filename + ".gz")

        with open(hot_path, "rb") as f_in:
            with gzip.open(cold_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(hot_path)

        self.index[filename]["status"] = "cold"
        self.index[filename]["archived_at"] = str(datetime.utcnow())
        self.save_index()

    def retrieve_file(self, filename):
        cold_path = os.path.join(COLD_DIR, filename + ".gz")

        if not os.path.exists(cold_path):
            hot_path = os.path.join(HOT_DIR, filename)
            if os.path.exists(hot_path):
                with open(hot_path, "r") as f:
                    return f.read()
            return None

        with gzip.open(cold_path, "rb") as f:
            return f.read().decode()

    def restore_file(self, filename):
        cold_path = os.path.join(COLD_DIR, filename + ".gz")
        hot_path = os.path.join(HOT_DIR, filename)

        if not os.path.exists(cold_path):
            return

        with gzip.open(cold_path, "rb") as f_in:
            with open(hot_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        self.index[filename]["status"] = "hot"
        self.index[filename]["restored_at"] = str(datetime.utcnow())
        self.save_index()

    def delete_file(self, filename):
        hot_path = os.path.join(HOT_DIR, filename)
        cold_path = os.path.join(COLD_DIR, filename + ".gz")

        if os.path.exists(hot_path):
            os.remove(hot_path)

        if os.path.exists(cold_path):
            os.remove(cold_path)

        if filename in self.index:
            del self.index[filename]
            self.save_index()

    def list_files(self):
        return self.index


def main():
    storage = ColdStorageSystem()

    while True:
        print("\n--- COLD STORAGE SYSTEM ---")
        print("1. Add File")
        print("2. Archive File")
        print("3. Retrieve File")
        print("4. Restore File")
        print("5. Delete File")
        print("6. List Files")
        print("7. Exit")

        choice = input("Select option: ")

        if choice == "1":
            name = input("Filename: ")
            content = input("Content: ")
            storage.add_file(name, content)
            print("Added to hot storage")

        elif choice == "2":
            name = input("Filename: ")
            storage.archive_file(name)
            print("Archived to cold storage")

        elif choice == "3":
            name = input("Filename: ")
            data = storage.retrieve_file(name)
            print(data if data else "Not found")

        elif choice == "4":
            name = input("Filename: ")
            storage.restore_file(name)
            print("Restored to hot storage")

        elif choice == "5":
            name = input("Filename: ")
            storage.delete_file(name)
            print("Deleted")

        elif choice == "6":
            print(json.dumps(storage.list_files(), indent=2))

        elif choice == "7":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()