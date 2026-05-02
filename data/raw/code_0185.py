import os
import tarfile
import shutil
from datetime import datetime

def archive_cold_data(source_dir, archive_dir, threshold_days=90):
    os.makedirs(archive_dir, exist_ok=True)
    current_time = datetime.now().timestamp()
    
    files_to_archive = []
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        last_access = os.path.getatime(file_path)
        
        if (current_time - last_access) > (threshold_days * 86400):
            files_to_archive.append(file_path)

    if files_to_archive:
        archive_name = f"cold_storage_{datetime.now().strftime('%Y%m%d')}.tar.gz"
        with tarfile.open(os.path.join(archive_dir, archive_name), "w:gz") as tar:
            for file in files_to_archive:
                tar.add(file, arcname=os.path.basename(file))
                os.remove(file)

if __name__ == "__main__":
    archive_cold_data("./active_data", "./glacier_storage")