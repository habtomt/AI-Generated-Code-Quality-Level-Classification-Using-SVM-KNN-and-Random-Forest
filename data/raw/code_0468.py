"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_001.txt
Run      : 3
"""

import os
import json
from datetime import datetime

class VersionControlSystem:
    def __init__(self, storage_dir):
        # Create the storage directory if it doesn't exist
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        self.storage_dir = storage_dir
        self.file_map = {}  # {file_name: [versions]}

    def save_version(self, file_name, content):
        # Create a new version of the file
        version = len(self.file_map.get(file_name, [])) + 1
        self.file_map[file_name] = self.file_map.get(file_name, []) + [(version, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
        
        # Save the version to the storage directory
        with open(os.path.join(self.storage_dir, f"{file_name}_{version}.txt"), "w") as f:
            f.write(content)

    def get_version_history(self, file_name):
        # Return the version history of the file
        return self.file_map.get(file_name, [])

    def restore_version(self, file_name, version):
        # Check if the version exists
        if version <= 0 or version > len(self.file_map[file_name]):
            raise ValueError("Invalid version")
        
        # Get the content of the version
        version_info = self.file_map[file_name][version - 1]
        content = version_info[1]
        
        # Save the content to the current file
        with open(os.path.join(self.storage_dir, file_name), "w") as f:
            f.write(content)

# Usage
if __name__ == "__main__":
    vcs = VersionControlSystem("vcs_storage")

    # Save a file
    vcs.save_version("example.txt", "This is the first version of the file.")

    # Save a new version of the file
    vcs.save_version("example.txt", "This is the second version of the file.")

    # Get the version history
    print(vcs.get_version_history("example.txt"))

    # Restore a previous version
    vcs.restore_version("example.txt", 1)