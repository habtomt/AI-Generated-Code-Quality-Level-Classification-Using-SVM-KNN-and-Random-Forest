import boto3
from datetime import datetime

rds_client = boto3.client('rds')

def create_backup(db_identifier):
    snapshot_id = f"{db_identifier}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create Snapshot
    response = rds_client.create_db_snapshot(
        DBInstanceIdentifier=db_identifier,
        DBSnapshotIdentifier=snapshot_id
    )
    print(f"Snapshot creation started: {snapshot_id}")
    return snapshot_id

def export_to_s3(snapshot_id, bucket_name, role_arn):
    rds_client.start_export_task(
        ExportTaskIdentifier=f"export-{snapshot_id}",
        SourceArn=f"arn:aws:rds:region:account:snapshot:{snapshot_id}",
        S3BucketName=bucket_name,
        IamRoleArn=role_arn
    )
    print("Export task initiated.")

if __name__ == "__main__":
    DB_ID = 'your-db-id'
    S3_BUCKET = 'my-backup-bucket'
    ROLE = 'arn:aws:iam::account:role/RDSExportRole'
    
    sid = create_backup(DB_ID)
    export_to_s3(sid, S3_BUCKET, ROLE)