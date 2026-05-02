#!/usr/bin/env python3

import os
import hashlib
import json
import random
import shutil
from datetime import datetime

NODES = ["node_a", "node_b", "node_c"]
REPLICATION_FACTOR = 2
METADATA_FILE = "metadata.json"


class DistributedFileSystem:
    def __init__(self):
        self.nodes = NODES
        self.replication = REPLICATION_FACTOR
        self.metadata = {}
        self.load_metadata()
        self.init_nodes()

    def init_nodes(self):
        for node in self.nodes:
            os.makedirs(node, exist_ok=True)

    def load_metadata(self):
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def save_metadata(self):
        with open(METADATA_FILE, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def hash_file(self, content):
        return hashlib.sha256(content.encode()).hexdigest()

    def choose_nodes(self, file_hash):
        random.seed(file_hash)
        return random.sample(self.nodes, self.replication)

    def write_file(self, filename, content):
        file_hash = self.hash_file(content)
        target_nodes = self.choose_nodes(file_hash)

        for node in target_nodes:
            path = os.path.join(node, filename)
            with open(path, "w") as f:
                f.write(content)

        self.metadata[filename] = {
            "hash": file_hash,
            "nodes": target_nodes,
            "timestamp": str(datetime.utcnow())
        }

        self.save_metadata()

    def read_file(self, filename):
        if filename not in self.metadata:
            return None

        for node in self.metadata[filename]["nodes"]:
            path = os.path.join(node, filename)
            if os.path.exists(path):
                with open(path, "r") as f:
                    return f.read()

        return None

    def delete_file(self, filename):
        if filename not in self.metadata:
            return

        for node in self.metadata[filename]["nodes"]:
            path = os.path.join(node, filename)
            if os.path.exists(path):
                os.remove(path)

        del self.metadata[filename]
        self.save_metadata()

    def list_files(self):
        return list(self.metadata.keys())

    def simulate_node_failure(self, node):
        node_path = os.path.join(".", node)
        if os.path.exists(node_path):
            shutil.rmtree(node_path)


def main():
    dfs = DistributedFileSystem()

    while True:
        print("\n--- DISTRIBUTED FILE SYSTEM ---")
        print("1. Write File")
        print("2. Read File")
        print("3. Delete File")
        print("4. List Files")
        print("5. Simulate Node Failure")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            name = input("Filename: ")
            content = input("Content: ")
            dfs.write_file(name, content)
            print("Stored with replication")

        elif choice == "2":
            name = input("Filename: ")
            data = dfs.read_file(name)
            print(data if data else "File not found")

        elif choice == "3":
            name = input("Filename: ")
            dfs.delete_file(name)
            print("Deleted")

        elif choice == "4":
            print(dfs.list_files())

        elif choice == "5":
            node = input(f"Node {NODES}: ")
            dfs.simulate_node_failure(node)
            print(f"{node} removed")

        elif choice == "6":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()