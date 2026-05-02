import os
import json
import zlib
import hashlib
import shutil
from datetime import datetime

class MiniVCS:
    """
    A lightweight version control system using content-addressable storage
    and zlib compression for storage efficiency.
    """
    def __init__(self, root_dir=".vcs_store"):
        self.root_dir = root_dir
        self.objects_dir = os.path.join(root_dir, "objects")
        self.registry_file = os.path.join(root_dir, "registry.json")
        self._init_repo()

    def _init_repo(self):
        os.makedirs(self.objects_dir, exist_ok=True)
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, 'w') as f:
                json.dump({}, f)

    def _get_file_hash(self, file_path):
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def commit(self, file_path, message):
        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found"}

        content_hash = self._get_file_hash(file_path)
        file_name = os.path.basename(file_path)
        
        # Compression and Storage
        object_path = os.path.join(self.objects_dir, content_hash)
        if not os.path.exists(object_path):
            with open(file_path, 'rb') as f_in:
                compressed_data = zlib.compress(f_in.read())
            with open(object_path, 'wb') as f_out:
                f_out.write(compressed_data)

        # Update History
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)

        if file_name not in registry:
            registry[file_name] = []

        # Check for redundant commits
        if registry[file_name] and registry[file_name][-1]['hash'] == content_hash:
            return {"status": "ignored", "message": "No changes detected"}

        entry = {
            "version_id": content_hash[:8],
            "hash": content_hash,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        }
        registry[file_name].append(entry)

        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=4)

        return {"status": "success", "version": entry['version_id']}

    def get_history(self, file_name):
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)
        return registry.get(file_name, [])

    def restore(self, file_name, version_id, output_path=None):
        with open(self.registry_file, 'r') as f:
            registry = json.load(f)

        history = registry.get(file_name, [])
        version = next((v for v in history if v['version_id'] == version_id), None)
        
        if not version:
            return False

        object_path = os.path.join(self.objects_dir, version['hash'])
        out_path = output_path or file_name

        with open(object_path, 'rb') as f_in:
            decompressed_data = zlib.decompress(f_in.read())
        
        with open(out_path, 'wb') as f_out:
            f_out.write(decompressed_data)
        
        return True

if __name__ == "__main__":
    vcs = MiniVCS()
    filename = "document.txt"

    # Version 1
    with open(filename, "w") as f:
        f.write("First version of the content.")
    vcs.commit(filename, "Initial draft")

    # Version 2
    with open(filename, "w") as f:
        f.write("Second version with more details.")
    vcs.commit(filename, "Added details")

    # Display History
    print(f"History for {filename}:")
    history = vcs.get_history(filename)
    for entry in history:
        print(f"[{entry['version_id']}] {entry['timestamp']}: {entry['message']}")

    # Restore
    if history:
        original_v = history[0]['version_id']
        vcs.restore(filename, original_v, "restored_doc.txt")
        print(f"\nRestored version {original_v} to 'restored_doc.txt'")