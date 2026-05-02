"""
Auto-generated Python code
Scenario : Cloud Database Services
Prompt   : response_000.txt
Run      : 1
"""

import psycopg2
from psycopg2 import sql
import sys

# Connection details
on_premise_config = {
    'dbname': 'on_premise_dbname',
    'user': 'on_premise_user',
    'password': 'on_premise_password',
    'host': 'on_premise_host',
    'port': 'on_premise_port'
}

cloud_config = {
    'dbname': 'cloud_dbname',
    'user': 'cloud_user',
    'password': 'cloud_password',
    'host': 'cloud_host',
    'port': 'cloud_port'
}

def export_schema_and_data(src_conn, dest_conn, tables):
    with src_conn.cursor() as src_cur, dest_conn.cursor() as dest_cur:
        for table in tables:
            print(f"Processing table: {table}")

            # Copy schema
            src_cur.execute(sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s"), (table,))
            columns = src_cur.fetchall()
            
            col_defs = [f"{col[0]} {col[1]}" for col in columns]
            create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
                sql.Identifier(table), sql.SQL(", ").join(sql.SQL(col_def) for col_def in col_defs))
            
            dest_cur.execute(create_table_query)
            print(f"Schema applied for table {table}")

            # Copy data
            src_cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
            rows = src_cur.fetchall()
            for row in rows:
                insert_query = sql.SQL("INSERT INTO {} VALUES ({})").format(
                    sql.Identifier(table), sql.SQL(", ").join(sql.Placeholder() * len(row)))
                dest_cur.execute(insert_query, row)

            dest_conn.commit()
            print(f"Data copied for table {table}")

def perform_integrity_checks(src_conn, dest_conn, tables):
    with src_conn.cursor() as src_cur, dest_conn.cursor() as dest_cur:
        for table in tables:
            src_cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table)))
            src_rows = src_cur.fetchone()[0]
            
            dest_cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table)))
            dest_rows = dest_cur.fetchone()[0]
            
            if src_rows == dest_rows:
                print(f"Integrity check passed for table {table}: Row count matches")
            else:
                print(f"Integrity check failed for table {table}: Row counts do not match ({src_rows} vs {dest_rows})")

def main():
    try:
        # Connect to source and destination databases
        src_conn = psycopg2.connect(**on_premise_config)
        dest_conn = psycopg2.connect(**cloud_config)

        # Specify the tables to migrate
        tables_to_migrate = ['table1', 'table2']  # Update with actual table names

        export_schema_and_data(src_conn, dest_conn, tables_to_migrate)
        perform_integrity_checks(src_conn, dest_conn, tables_to_migrate)

        print("Migration completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if src_conn:
            src_conn.close()
        if dest_conn:
            dest_conn.close()

if __name__ == "__main__":
    main()