"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_001.txt
Run      : 3
"""

import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name):
        # Initialize the database connection
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.db_name = db_name

    def create_table(self, table_name, columns):
        # Create a table with specified columns
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {' , '.join([f'{column[0]} {column[1]}' for column in columns])}
            )
        """)
        self.conn.commit()  # Save changes to the database

    def insert_data(self, table_name, data):
        # Insert data into a specified table
        self.cursor.execute(f"""
            INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(data))})
        """, data)
        self.conn.commit()  # Save changes to the database

    def read_data(self, table_name, conditions=None):
        # Read data from a specified table
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += f" WHERE {' AND '.join([f'{key} = ?' for key in conditions.keys()])}"
        self.cursor.execute(query, list(conditions.values()) if conditions else [])
        return self.cursor.fetchall()

    def update_data(self, table_name, conditions, updates):
        # Update data in a specified table
        self.cursor.execute(f"""
            UPDATE {table_name} 
            SET {' , '.join([f'{key} = ?' for key in updates.keys()])} 
            WHERE {' AND '.join([f'{key} = ?' for key in conditions.keys()])}
        """, (*conditions.values(), *updates.values()))
        self.conn.commit()  # Save changes to the database

    def delete_data(self, table_name, conditions):
        # Delete data from a specified table
        self.cursor.execute(f"""
            DELETE FROM {table_name} 
            WHERE {' AND '.join([f'{key} = ?' for key in conditions.keys()])}
        """, list(conditions.values()))
        self.conn.commit()  # Save changes to the database

    def drop_table(self, table_name):
        # Drop a specified table
        self.cursor.execute(f"DROP TABLE {table_name}")
        self.conn.commit()  # Save changes to the database

    def close_connection(self):
        # Close the database connection
        self.conn.close()


# Usage example
if __name__ == "__main__":
    db_name = "example.db"
    if not os.path.exists(db_name):
        os.system(f"sqlite3 {db_name}")

    db_manager = DatabaseManager(db_name)
    db_manager.create_table("users", [
        ("id", "INTEGER PRIMARY KEY"),
        ("name", "TEXT"),
        ("email", "TEXT UNIQUE")
    ])

    try:
        db_manager.insert_data("users", (1, "John Doe", "john@example.com"))
        db_manager.insert_data("users", (2, "Jane Doe", "jane@example.com"))

        users = db_manager.read_data("users")
        print(users)

        db_manager.update_data("users", {"id": 1}, {"name": "John Smith"})

        users = db_manager.read_data("users")
        print(users)

        db_manager.delete_data("users", {"id": 2})

        users = db_manager.read_data("users")
        print(users)

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        db_manager.drop_table("users")
        db_manager.close_connection()