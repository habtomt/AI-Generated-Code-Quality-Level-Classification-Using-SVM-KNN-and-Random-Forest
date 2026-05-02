import boto3
import mysql.connector

# AWS Config
rds = boto3.client('rds', region_name='us-west-2')
DB_ID = "mydbinstance"

def setup_secure_db():
    # 1. Create RDS Instance
    rds.create_db_instance(
        DBInstanceIdentifier=DB_ID,
        DBInstanceClass='db.m5.large',
        Engine='mysql',
        MasterUsername='admin',
        MasterUserPassword='SecurePassword123!',
        StorageEncrypted=True,
        KmsKeyId='arn:aws:kms:us-west-2:123456789012:key/your-key',
        AllocatedStorage=20
    )
    print("Instance creation initiated.")

    # 2. Setup Security Rules (Once available)
    # Using mysql-connector for DB-level security
    conn = mysql.connector.connect(host='your-db-endpoint', user='admin', password='...')
    cursor = conn.cursor()
    
    # Enforce SSL and Roles
    cursor.execute("CREATE ROLE 'readonly';")
    cursor.execute("GRANT SELECT ON mydatabase.* TO 'readonly';")
    cursor.execute("FLUSH PRIVILEGES;")
    
    conn.close()

if __name__ == "__main__":
    setup_secure_db()