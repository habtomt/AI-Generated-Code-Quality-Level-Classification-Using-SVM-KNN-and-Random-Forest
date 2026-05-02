"""
Auto-generated Python code
Scenario : File Storage & Management
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
import os
import hashlib
import getpass
from typing import Dict, List

# Define a class to represent a user
class User:
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = self._hash_password(password)
        self.role = role
        self.permissions = self._get_role_permissions(role)

    def _hash_password(self, password: str) -> str:
        # Hash the password for secure storage
        return hashlib.sha256(password.encode()).hexdigest()

    def _get_role_permissions(self, role: str) -> Dict[str, List[str]]:
        # Define permissions for each role
        permissions = {
            'admin': ['read', 'write', 'delete'],
            'user': ['read', 'write']
        }
        return permissions.get(role, [])

# Define a class to represent an access manager
class AccessManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username: str, password: str, role: str):
        # Create a new user and add them to the access manager
        user = User(username, password, role)
        self.users[username] = user

    def authenticate_user(self, username: str, password: str) -> bool:
        # Attempt to authenticate a user
        if username in self.users:
            user = self.users[username]
            return user.password == self._hash_password(password)
        return False

    def authorize_user(self, username: str, action: str, resource: str) -> bool:
        # Determine if a user has permission to perform an action on a resource
        if username in self.users:
            user = self.users[username]
            return action in user.permissions and resource in self._get_allowed_resources(user.role)
        return False

    def _get_allowed_resources(self, role: str) -> List[str]:
        # Define allowed resources for each role
        resources = {
            'admin': ['files', 'directories'],
            'user': ['files']
        }
        return resources.get(role, [])

# Define a function to run the program
def main():
    # Create an access manager
    access_manager = AccessManager()

    # Define some users
    users = {
        'admin': {'username': 'admin', 'password': 'password', 'role': 'admin'},
        'user': {'username': 'user', 'password': 'password', 'role': 'user'}
    }

    # Add users to the access manager
    for username, user in users.items():
        access_manager.add_user(user['username'], user['password'], user['role'])

    # Authenticate a user
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    if access_manager.authenticate_user(username, password):
        print("Authentication successful!")
    else:
        print("Authentication failed!")

    # Authorize a user
    action = input("Enter the action you want to perform (read, write, delete): ")
    resource = input("Enter the resource you want to access (files, directories): ")
    if access_manager.authorize_user(username, action, resource):
        print("Authorization successful!")
    else:
        print("Authorization failed!")

if __name__ == "__main__":
    main()