"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_001.txt
Run      : 1
"""

import mysql.connector
from pymongo import MongoClient

# Relational Database (MySQL) Setup
def setup_mysql_db():
    # Establish a connection to the MySQL server
    try:
        # Replace 'YOUR_HOST', 'YOUR_USER', 'YOUR_PASSWORD' with your actual MySQL credentials
        db = mysql.connector.connect(
            host='YOUR_HOST',
            user='YOUR_USER',
            password='YOUR_PASSWORD'
        )
        cursor = db.cursor()
        
        # Create a database
        cursor.execute("CREATE DATABASE IF NOT EXISTS my_database")
        cursor.execute("USE my_database")
        
        # Create a table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                email VARCHAR(100)
            )
        """)
        
        # Add an index for performance optimization
        cursor.execute("ALTER TABLE my_table ADD INDEX (name)")
        
        db.commit()
        db.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

# Non-Relational Database (MongoDB) Setup
def setup_mongodb():
    # Establish a connection to the MongoDB server
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['myDatabase']
        collection = db['myCollection']
        
        # Create an index for performance optimization
        collection.create_index('name')
        
        client.close()
    except Exception as e:
        print("An error occurred: {}".format(e))

# CRUD Operations for Relational Database (MySQL)
def mysql_crud_operations():
    try:
        db = mysql.connector.connect(
            host='YOUR_HOST',
            user='YOUR_USER',
            password='YOUR_PASSWORD',
            database='my_database'
        )
        cursor = db.cursor()
        
        # Create
        cursor.execute("INSERT INTO my_table (name, age, email) VALUES ('John Doe', 30, 'john.doe@mail.com')")
        db.commit()
        
        # Read
        cursor.execute("SELECT * FROM my_table WHERE name = 'John Doe'")
        result = cursor.fetchall()
        for row in result:
            print(row)
        
        # Update
        cursor.execute("UPDATE my_table SET age = 31 WHERE name = 'John Doe'")
        db.commit()
        
        # Delete
        cursor.execute("DELETE FROM my_table WHERE name = 'John Doe'")
        db.commit()
        
        db.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

# CRUD Operations for Non-Relational Database (MongoDB)
def mongodb_crud_operations():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['myDatabase']
        collection = db['myCollection']
        
        # Create
        collection.insert_one({ 'name': "John Doe", 'age': 30, 'email': "john.doe@mail.com" })
        
        # Read
        result = collection.find({ 'name': "John Doe" })
        for document in result:
            print(document)
        
        # Update
        collection.update_one({ 'name': "John Doe" }, { '$set': { 'age': 31 } })
        
        # Delete
        collection.delete_one({ 'name': "John Doe" })
        
        client.close()
    except Exception as e:
        print("An error occurred: {}".format(e))

if __name__ == "__main__":
    setup_mysql_db()
    setup_mongodb()
    mysql_crud_operations()
    mongodb_crud_operations()