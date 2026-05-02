"""
Auto-generated Python code
Scenario : Cloud Database Services
Prompt   : response_000.txt
Run      : 3
"""

# Import necessary libraries
import sqlite3
import mysql.connector
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table

# Define database connection parameters
# On-premise SQLite database
sqlite_db = 'YOUR_ON_PREMISE_DB_NAME.db'
sqlite_conn_str = f'sqlite:///{sqlite_db}'

# Cloud-based PostgreSQL database
pg_host = 'YOUR_CLOUD_PG_HOST'
pg_port = 5432
pg_username = 'YOUR_CLOUD_PG_USERNAME'
pg_password = 'YOUR_CLOUD_PG_PASSWORD'
pg_db = 'YOUR_CLOUD_PG_DB_NAME'

# Define a function to transfer schema from SQLite to PostgreSQL
def transfer_schema():
    # Establish connections to SQLite and PostgreSQL databases
    sqlite_engine = create_engine(sqlite_conn_str)
    pg_engine = create_engine(f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # Get metadata from SQLite database
    meta = MetaData()
    meta.reflect(bind=sqlite_engine)

    # Iterate over tables in SQLite database
    for table_name in meta.tables:
        # Create table in PostgreSQL database
        table = meta.tables[table_name]
        table.create(bind=pg_engine)

# Define a function to upload data from SQLite to PostgreSQL
def upload_data():
    # Establish connections to SQLite and PostgreSQL databases
    sqlite_engine = create_engine(sqlite_conn_str)
    pg_engine = create_engine(f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # Get data from SQLite database
    for table_name in sqlite_engine.table_names():
        df = pd.read_sql_table(table_name, sqlite_engine)
        # Upload data to PostgreSQL database
        df.to_sql(table_name, pg_engine, if_exists='replace', index=False)

# Define a function to perform integrity checks
def integrity_check():
    # Establish connections to PostgreSQL database
    pg_engine = create_engine(f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # Get metadata from PostgreSQL database
    meta = MetaData()
    meta.reflect(bind=pg_engine)

    # Iterate over tables in PostgreSQL database
    for table_name in meta.tables:
        # Perform integrity checks
        try:
            # Check for duplicates
            query = f"SELECT * FROM {table_name} GROUP BY {', '.join(meta.tables[table_name].c.keys())} HAVING COUNT(*) > 1"
            result = pg_engine.execute(query)
            if result.rowcount > 0:
                print(f"Integrity check failed: duplicates found in table {table_name}")
        except Exception as e:
            print(f"Error performing integrity check: {e}")

# Main function
def main():
    try:
        # Transfer schema from SQLite to PostgreSQL
        transfer_schema()
        print("Schema transferred successfully")

        # Upload data from SQLite to PostgreSQL
        upload_data()
        print("Data uploaded successfully")

        # Perform integrity checks
        integrity_check()
        print("Integrity checks completed successfully")
    except Exception as e:
        print(f"Error: {e}")

# Run the main function
if __name__ == '__main__':
    main()