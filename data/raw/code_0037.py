#!/usr/bin/env python3

import sqlite3
import os

DB_NAME = os.environ.get("DB_NAME", "app_database.db")


class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)")
        self.conn.commit()

    def create_user(self, name, email, age):
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        return self.cursor.fetchall()

    def update_user(self, user_id, name=None, email=None, age=None):
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if email:
            fields.append("email = ?")
            values.append(email)
        if age is not None:
            fields.append("age = ?")
            values.append(age)

        values.append(user_id)

        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


def main():
    db = DatabaseManager()

    while True:
        print("\n--- DATABASE MENU ---")
        print("1. Create User")
        print("2. Get User")
        print("3. List Users")
        print("4. Update User")
        print("5. Delete User")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            age = int(input("Age: "))
            user_id = db.create_user(name, email, age)
            print(f"User created with ID: {user_id}")

        elif choice == "2":
            user_id = int(input("User ID: "))
            user = db.get_user(user_id)
            print(dict(user) if user else "Not found")

        elif choice == "3":
            users = db.get_all_users()
            for u in users:
                print(dict(u))

        elif choice == "4":
            user_id = int(input("User ID: "))
            name = input("New Name (blank skip): ") or None
            email = input("New Email (blank skip): ") or None
            age_input = input("New Age (blank skip): ")
            age = int(age_input) if age_input else None
            db.update_user(user_id, name, email, age)
            print("Updated")

        elif choice == "5":
            user_id = int(input("User ID: "))
            db.delete_user(user_id)
            print("Deleted")

        elif choice == "6":
            db.close()
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()