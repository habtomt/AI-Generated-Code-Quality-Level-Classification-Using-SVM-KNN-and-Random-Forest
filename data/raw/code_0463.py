"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_001.txt
Run      : 2
"""

import os
import pickle
import hashlib

class VersionControlSystem:
    def __init__(self, storage_dir='storage'):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_file(self, filename, content):
        """Save a new version of the file."""
        with open(os.path.join(self.storage_dir, f'{filename}.data'), 'wb') as f:
            pickle.dump(content, f)
        with open(os.path.join(self.storage_dir, f'{filename}.hash'), 'w') as f:
            f.write(hashlib.sha256(content.encode()).hexdigest())

    def get_file(self, filename):
        """Get the content of the latest version of the file."""
        try:
            with open(os.path.join(self.storage_dir, f'{filename}.data'), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def get_version(self, filename, version):
        """Get the content of a specific version of the file."""
        try:
            with open(os.path.join(self.storage_dir, f'{filename}.data.{version}'), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def list_versions(self, filename):
        """List all versions of the file."""
        versions = []
        for f in os.listdir(self.storage_dir):
            if f.startswith(f'{filename}.data.') and f.endswith('.data'):
                versions.append(int(f.split('.')[-1].split('.')[0]))
        return sorted(versions, reverse=True)

    def view_version_history(self, filename):
        """View the version history of the file."""
        versions = self.list_versions(filename)
        print(f'Version History for {filename}:')
        for version in versions:
            content = self.get_version(filename, version)
            if content:
                print(f'Version {version}: {content[:20]}...')


def main():
    vcs = VersionControlSystem()
    while True:
        print('\nOptions:')
        print('1. Save file')
        print('2. Get latest file')
        print('3. Get version')
        print('4. List versions')
        print('5. View version history')
        print('6. Quit')
        choice = input('Choose an option: ')
        if choice == '1':
            filename = input('Enter filename: ')
            content = input('Enter file content: ')
            vcs.save_file(filename, content)
        elif choice == '2':
            filename = input('Enter filename: ')
            print('Latest version:')
            print(vcs.get_file(filename))
        elif choice == '3':
            filename = input('Enter filename: ')
            version = int(input('Enter version: '))
            print(f'Version {version}:')
            print(vcs.get_version(filename, version))
        elif choice == '4':
            filename = input('Enter filename: ')
            print('Versions:')
            print(vcs.list_versions(filename))
        elif choice == '5':
            filename = input('Enter filename: ')
            vcs.view_version_history(filename)
        elif choice == '6':
            break
        else:
            print('Invalid option. Please choose again.')


if __name__ == '__main__':
    main()