#!/usr/bin/env python3

import os
import json
import hashlib
import getpass

DATA_DIR = "access_system"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
FILES_DIR = os.path.join(DATA_DIR, "files")

DEFAULT_ROLES = {
    "admin": ["read", "write", "delete", "grant"],
    "editor": ["read", "write"],
    "viewer": ["read"]
}


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(FILES_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)


def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class AccessSystem:
    def __init__(self):
        ensure_storage()
        self.users = load_users()
        self.current_user = None

    def register(self):
        username = input("Username: ")
        if username in self.users:
            print("User exists")
            return

        password = getpass.getpass("Password: ")
        role = input("Role (admin/editor/viewer): ")

        if role not in DEFAULT_ROLES:
            print("Invalid role")
            return

        self.users[username] = {
            "password": hash_password(password),
            "role": role
        }
        save_users(self.users)
        print("User created")

    def login(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        user = self.users.get(username)
        if not user:
            print("User not found")
            return

        if user["password"] != hash_password(password):
            print("Wrong password")
            return

        self.current_user = username
        print(f"Logged in as {username}")

    def logout(self):
        self.current_user = None
        print("Logged out")

    def require_login(self):
        if not self.current_user:
            print("Login required")
            return False
        return True

    def get_role(self):
        return self.users[self.current_user]["role"]

    def has_permission(self, perm):
        role = self.get_role()
        return perm in DEFAULT_ROLES.get(role, [])

    def create_file(self):
        if not self.require_login():
            return
        if not self.has_permission("write"):
            print("Permission denied")
            return

        filename = input("Filename: ")
        content = input("Content: ")

        path = os.path.join(FILES_DIR, filename)
        with open(path, "w") as f:
            f.write(content)

        print("File created")

    def read_file(self):
        if not self.require_login():
            return
        if not self.has_permission("read"):
            print("Permission denied")
            return

        filename = input("Filename: ")
        path = os.path.join(FILES_DIR, filename)

        if not os.path.exists(path):
            print("File not found")
            return

        with open(path, "r") as f:
            print(f.read())

    def delete_file(self):
        if not self.require_login():
            return
        if not self.has_permission("delete"):
            print("Permission denied")
            return

        filename = input("Filename: ")
        path = os.path.join(FILES_DIR, filename)

        if os.path.exists(path):
            os.remove(path)
            print("Deleted")
        else:
            print("File not found")

    def grant_role(self):
        if not self.require_login():
            return
        if not self.has_permission("grant"):
            print("Permission denied")
            return

        target = input("Target user: ")
        role = input("New role: ")

        if role not in DEFAULT_ROLES:
            print("Invalid role")
            return

        if target not in self.users:
            print("User not found")
            return

        self.users[target]["role"] = role
        save_users(self.users)
        print("Role updated")

    def status(self):
        if not self.current_user:
            print("Not logged in")
        else:
            print(f"User: {self.current_user}, Role: {self.get_role()}")


def main():
    system = AccessSystem()

    commands = {
        "register": system.register,
        "login": system.login,
        "logout": system.logout,
        "create": system.create_file,
        "read": system.read_file,
        "delete": system.delete_file,
        "grant": system.grant_role,
        "status": system.status
    }

    print("Access Management System Ready")

    while True:
        cmd = input("\nCommand (register, login, logout, create, read, delete, grant, status, exit): ").strip()

        if cmd == "exit":
            break

        action = commands.get(cmd)
        if action:
            action()
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()