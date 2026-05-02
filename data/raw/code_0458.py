"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_001.txt
Run      : 1
"""

import os
import shutil
import hashlib
from datetime import datetime

class VersionControlSystem:
    def __init__(self, repo_path):
        # Initialize the repository path and versions directory
        self.repo_path = repo_path
        self.versions_path = os.path.join(self.repo_path, '.versions')
        if not os.path.exists(self.versions_path):
            os.makedirs(self.versions_path)

    def _hash_file(self, file_path):
        # Generate a hash of a file's contents
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def _save_version(self, file_path):
        # Save a version of the file
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_hash = self._hash_file(file_path)
        version_file_name = f'{timestamp}_{file_hash}.bak'
        shutil.copy2(file_path, os.path.join(self.versions_path, version_file_name))
        print(f'Version saved: {version_file_name}')

    def track_file(self, file_path):
        # Add a file to version control
        try:
            if os.path.exists(file_path):
                self._save_version(file_path)
            else:
                print(f"File {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_versions(self, file_name):
        # List all versions of a file
        try:
            files = os.listdir(self.versions_path)
            versions = [f for f in files if f.endswith('.bak')]
            for version in versions:
                print(version)
        except Exception as e:
            print(f"An error occurred: {e}")

    def restore_version(self, file_name, version_name):
        # Restore a file to a specific version
        try:
            version_path = os.path.join(self.versions_path, version_name)
            if os.path.exists(version_path):
                shutil.copy2(version_path, os.path.join(self.repo_path, file_name))
                print(f'File {file_name} restored to version {version_name}.')
            else:
                print(f'Version {version_name} does not exist.')
        except Exception as e:
            print(f"An error occurred: {e}")

# Usage example
if __name__ == '__main__':
    # Initialize the VCS with a directory to manage
    vcs = VersionControlSystem('your_repository_directory')

    # Track and save a new version of a file
    vcs.track_file('example.txt')

    # List all saved versions of a file
    vcs.list_versions('example.txt')

    # Restore a specific version
    # Use a valid version name as seen in the list_versions output
    # vcs.restore_version('example.txt', '20230316103012_<hash>.bak')