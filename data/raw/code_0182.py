import pysftp
import os
import hashlib

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def backup_to_remote(local_path, remote_path, hostname, username, password):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    
    local_checksum = calculate_checksum(local_path)
    
    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        sftp.put(local_path, remote_path)
        
        with sftp.open(remote_path + ".sha256", "w") as f:
            f.write(local_checksum)

if __name__ == "__main__":
    backup_to_remote("data.db", "/backups/data_v1.db", "example.com", "user", "pass")