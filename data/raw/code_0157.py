import psycopg2
from psycopg2 import sql

# Connection configuration
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

def migrate_tables(tables):
    try:
        src_conn = psycopg2.connect(**on_premise_config)
        dest_conn = psycopg2.connect(**cloud_config)
        
        with src_conn.cursor() as src_cur, dest_conn.cursor() as dest_cur:
            for table in tables:
                # Get schema
                src_cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table,))
                columns = src_cur.fetchall()
                col_defs = [f"{col[0]} {col[1]}" for col in columns]
                
                # Create table
                create_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
                    sql.Identifier(table), 
                    sql.SQL(", ").join(sql.SQL(cd) for cd in col_defs)
                )
                dest_cur.execute(create_query)
                
                # Copy data
                src_cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
                rows = src_cur.fetchall()
                
                insert_query = sql.SQL("INSERT INTO {} VALUES ({})").format(
                    sql.Identifier(table), 
                    sql.SQL(", ").join([sql.Placeholder()] * len(columns))
                )
                
                for row in rows:
                    dest_cur.execute(insert_query, row)
                
                dest_conn.commit()
                print(f"Migrated: {table}")

        src_conn.close()
        dest_conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    tables_to_migrate = ['table1', 'table2']
    migrate_tables(tables_to_migrate)