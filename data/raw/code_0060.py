#!/usr/bin/env python3

import os
import json
import hashlib
from collections import OrderedDict

STORAGE_ROOT = "scalable_storage"
META_FILE = os.path.join(STORAGE_ROOT, "index.json")
SHARD_COUNT = 8
CACHE_SIZE = 5


def ensure_storage():
    os.makedirs(STORAGE_ROOT, exist_ok=True)
    for i in range(SHARD_COUNT):
        os.makedirs(os.path.join(STORAGE_ROOT, f"shard_{i}"), exist_ok=True)

    if not os.path.exists(META_FILE):
        with open(META_FILE, "w") as f:
            json.dump({}, f)


def load_index():
    with open(META_FILE, "r") as f:
        return json.load(f)


def save_index(index):
    with open(META_FILE, "w") as f:
        json.dump(index, f, indent=2)


def hash_key(key):
    return int(hashlib.sha256(key.encode()).hexdigest(), 16)


def get_shard(key):
    return f"shard_{hash_key(key) % SHARD_COUNT}"


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class StorageSystem:
    def __init__(self):
        ensure_storage()
        self.index = load_index()
        self.cache = LRUCache(CACHE_SIZE)

    def put(self, filename, content):
        shard = get_shard(filename)
        path = os.path.join(STORAGE_ROOT, shard, filename)

        with open(path, "wb") as f:
            f.write(content.encode())

        self.index[filename] = {
            "shard": shard,
            "size": len(content)
        }

        self.cache.put(filename, content)
        save_index(self.index)

        print(f"Stored in {shard}")

    def get(self, filename):
        cached = self.cache.get(filename)
        if cached:
            print("Cache hit")
            return cached

        meta = self.index.get(filename)
        if not meta:
            print("Not found")
            return None

        path = os.path.join(STORAGE_ROOT, meta["shard"], filename)

        if not os.path.exists(path):
            print("Missing file")
            return None

        with open(path, "rb") as f:
            data = f.read().decode()

        self.cache.put(filename, data)
        print("Cache miss")
        return data

    def delete(self, filename):
        meta = self.index.get(filename)
        if not meta:
            print("Not found")
            return

        path = os.path.join(STORAGE_ROOT, meta["shard"], filename)

        if os.path.exists(path):
            os.remove(path)

        del self.index[filename]
        save_index(self.index)

        print("Deleted")

    def list_files(self):
        for k, v in self.index.items():
            print(f"{k} -> {v['shard']} ({v['size']} bytes)")


def main():
    store = StorageSystem()

    print("Scalable Storage System")

    while True:
        cmd = input("\nCommand (put/get/delete/list/exit): ").split()

        if not cmd:
            continue

        action = cmd[0]

        if action == "exit":
            break

        elif action == "put":
            filename = input("Filename: ")
            content = input("Content: ")
            store.put(filename, content)

        elif action == "get":
            filename = input("Filename: ")
            data = store.get(filename)
            if data:
                print("DATA:", data)

        elif action == "delete":
            filename = input("Filename: ")
            store.delete(filename)

        elif action == "list":
            store.list_files()

        else:
            print("Invalid command")


if __name__ == "__main__":
    main()