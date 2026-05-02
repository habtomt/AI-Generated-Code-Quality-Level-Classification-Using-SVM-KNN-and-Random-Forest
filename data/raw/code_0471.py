"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_004.txt
Run      : 3
"""

# Import necessary libraries
import os
import fcntl
import threading
from datetime import datetime
import logging
import time

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define file class to handle file operations
class FileStorage:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.lock = threading.Lock()

    def create_directory(self, dir_path):
        try:
            os.mkdir(dir_path)
            logging.info(f"Directory created: {dir_path}")
        except FileExistsError:
            logging.warning(f"Directory already exists: {dir_path}")
        except OSError as e:
            logging.error(f"Error creating directory: {e}")

    def upload_file(self, file_path, file_data):
        try:
            with open(file_path, 'wb') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(file_data)
                fcntl.flock(f, fcntl.LOCK_UN)
            logging.info(f"File uploaded: {file_path}")
        except Exception as e:
            logging.error(f"Error uploading file: {e}")

    def download_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                file_data = f.read()
                fcntl.flock(f, fcntl.LOCK_UN)
            logging.info(f"File downloaded: {file_path}")
            return file_data
        except Exception as e:
            logging.error(f"Error downloading file: {e}")

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            logging.info(f"File deleted: {file_path}")
        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}")
        except OSError as e:
            logging.error(f"Error deleting file: {e}")

    def get_file_size(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            logging.info(f"File size: {file_size} bytes")
            return file_size
        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}")
        except OSError as e:
            logging.error(f"Error getting file size: {e}")

# Define storage class to handle storage operations
class Storage:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.file_storage = FileStorage(storage_path)

    def create_directory(self, dir_path):
        self.file_storage.create_directory(os.path.join(self.storage_path, dir_path))

    def upload_file(self, file_path, file_data):
        self.file_storage.upload_file(os.path.join(self.storage_path, file_path), file_data)

    def download_file(self, file_path):
        return self.file_storage.download_file(os.path.join(self.storage_path, file_path))

    def delete_file(self, file_path):
        self.file_storage.delete_file(os.path.join(self.storage_path, file_path))

    def get_file_size(self, file_path):
        return self.file_storage.get_file_size(os.path.join(self.storage_path, file_path))

# Define a function to simulate file operations
def simulate_file_operations(storage):
    file_path = "example.txt"
    file_data = b"Hello, World!"

    # Upload file
    start_time = time.time()
    storage.upload_file(file_path, file_data)
    end_time = time.time()
    logging.info(f"Upload time: {end_time - start_time} seconds")

    # Download file
    start_time = time.time()
    file_data = storage.download_file(file_path)
    end_time = time.time()
    logging.info(f"Download time: {end_time - start_time} seconds")

    # Get file size
    start_time = time.time()
    file_size = storage.get_file_size(file_path)
    end_time = time.time()
    logging.info(f"Get file size time: {end_time - start_time} seconds")

# Define main function
def main():
    storage_path = "/tmp/storage"
    storage = Storage(storage_path)

    # Create directory
    storage.create_directory("example")

    # Simulate file operations
    simulate_file_operations(storage)

if __name__ == "__main__":
    main()