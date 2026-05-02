import subprocess
import boto3
import schedule
import time
from datetime import datetime

BUCKET_NAME = "my-backup-bucket"
DB_NAME = "production_db"

def run_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    
    try:
        # Create Backup using pg_dump (example for PostgreSQL)
        subprocess.run(["pg_dump", DB_NAME, "-f", backup_file], check=True)
        
        # Upload to Cloud Storage
        s3 = boto3.client('s3')
        s3.upload_file(backup_file, BUCKET_NAME, backup_file)
        
        # Monitoring/Alerting
        print(f"SUCCESS: Backup {backup_file} completed and uploaded.")
        os.remove(backup_file)
    except Exception as e:
        print(f"FAILURE: Backup failed. Error: {e}")

if __name__ == "__main__":
    schedule.every().day.at("02:00").do(run_backup)
    while True:
        schedule.run_pending()
        time.sleep(60)