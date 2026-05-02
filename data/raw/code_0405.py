"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_003.txt
Run      : 2
"""

import os
import sqlite3
from datetime import datetime

# Create a database for data storage
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Create a table for infrequently accessed data
    c.execute('''
        CREATE TABLE IF NOT EXISTS infrequent_data
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         data TEXT, 
         created_at TEXT)
    ''')
    
    conn.commit()
    conn.close()

# Add data to the database
def add_data(db_name, data):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        # Get current timestamp
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert data into the table
        c.execute("INSERT INTO infrequent_data (data, created_at) VALUES (?, ?)", (data, created_at))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error adding data: {e}")

# Retrieve data from the database
def get_data(db_name, id=None):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        if id:
            c.execute("SELECT data FROM infrequent_data WHERE id=?", (id,))
        else:
            c.execute("SELECT data FROM infrequent_data")
        
        data = c.fetchall()
        
        conn.close()
        
        return data
    except sqlite3.Error as e:
        print(f"Error retrieving data: {e}")

# Delete data from the database
def delete_data(db_name, id):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        c.execute("DELETE FROM infrequent_data WHERE id=?", (id,))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error deleting data: {e}")

# Usage example
if __name__ == "__main__":
    db_name = 'infrequent_data.db'
    
    # Create database if it doesn't exist
    create_database(db_name)
    
    # Add some data
    add_data(db_name, 'This is some infrequently accessed data.')
    
    # Retrieve data
    retrieved_data = get_data(db_name)
    print("Retrieved Data:")
    for row in retrieved_data:
        print(row[0])
    
    # Delete data by ID
    delete_data(db_name, 1)