"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_001.txt
Run      : 2
"""

# Import necessary libraries
import sqlite3
from sqlite3 import Error

# Connect to SQLite database
def create_connection():
    try:
        conn = sqlite3.connect('database.db')  # Create or connect to the database
        return conn
    except Error as e:
        print(e)

# Create table
def create_table(conn):
    """
    Create a new table with columns id, name, age, and email.
    """
    sql_create_table = """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            email TEXT UNIQUE
                        );"""
    try:
        cur = conn.cursor()
        cur.execute(sql_create_table)
    except Error as e:
        print(e)

# Insert data
def insert_data(conn, name, age, email):
    """
    Insert a new user into the users table.
    :param conn: Connection to the SQLite database.
    :param name: Name of the user.
    :param age: Age of the user.
    :param email: Email of the user.
    """
    sql_insert_data = """INSERT INTO users(name, age, email)
                        VALUES(?,?,?)"""
    try:
        cur = conn.cursor()
        cur.execute(sql_insert_data, (name, age, email))
        conn.commit()
    except Error as e:
        print(e)

# Get all data
def get_all_data(conn):
    """
    Get all users from the users table.
    :param conn: Connection to the SQLite database.
    :return: List of tuples containing user data.
    """
    sql_get_all_data = """SELECT * FROM users"""
    try:
        cur = conn.cursor()
        cur.execute(sql_get_all_data)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)
    finally:
        cur.close()

# Get data by id
def get_data_by_id(conn, id):
    """
    Get user by id from the users table.
    :param conn: Connection to the SQLite database.
    :param id: Id of the user.
    :return: Tuple containing user data.
    """
    sql_get_data_by_id = """SELECT * FROM users WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql_get_data_by_id, (id,))
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)
    finally:
        cur.close()

# Update data
def update_data(conn, id, name, age, email):
    """
    Update user data in the users table.
    :param conn: Connection to the SQLite database.
    :param id: Id of the user.
    :param name: Name of the user.
    :param age: Age of the user.
    :param email: Email of the user.
    """
    sql_update_data = """UPDATE users SET name = ?, age = ?, email = ?
                        WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql_update_data, (name, age, email, id))
        conn.commit()
    except Error as e:
        print(e)

# Delete data
def delete_data(conn, id):
    """
    Delete user by id from the users table.
    :param conn: Connection to the SQLite database.
    :param id: Id of the user.
    """
    sql_delete_data = """DELETE FROM users WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql_delete_data, (id,))
        conn.commit()
    except Error as e:
        print(e)

# Main function
def main():
    # Create a database connection
    conn = create_connection()
    
    # Create table
    create_table(conn)
    
    # Insert data
    insert_data(conn, 'John Doe', 30, 'john@example.com')
    insert_data(conn, 'Jane Doe', 25, 'jane@example.com')
    
    # Print all data
    print("All Data:")
    print(get_all_data(conn))
    
    # Get data by id
    print("\nData by id:")
    print(get_data_by_id(conn, 1))
    
    # Update data
    update_data(conn, 1, 'John Smith', 31, 'john.smith@example.com')
    
    # Print updated data
    print("\nUpdated Data:")
    print(get_data_by_id(conn, 1))
    
    # Delete data
    delete_data(conn, 2)
    
    # Print remaining data
    print("\nRemaining Data:")
    print(get_all_data(conn))
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()