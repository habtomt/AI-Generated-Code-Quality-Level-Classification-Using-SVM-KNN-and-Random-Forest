import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta

class AccessManagementSystem:
    def __init__(self, db_path="ams_data.json"):
        self.db_path = db_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {
            "users": {},
            "roles": {
                "admin": ["read", "write", "delete", "delegate"],
                "editor": ["read", "write"],
                "viewer": ["read"]
            },
            "files": {}
        }

    def _save_data(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, role="viewer"):
        if username in self.data["users"]:
            return False
        self.data["users"][username] = {
            "password": self._hash_password(password),
            "role": role,
            "delegated_permissions": []
        }
        self._save_data()
        return True

    def authenticate(self, username, password):
        user = self.data["users"].get(username)
        if user and user["password"] == self._hash_password(password):
            return True
        return False

    def authorize(self, username, action, resource_id=None):
        user = self.data["users"].get(username)
        if not user:
            return False

        # Check Role-Based Access Control (RBAC)
        role_permissions = self.data["roles"].get(user["role"], [])
        if action in role_permissions:
            return True

        # Check Delegated Permissions
        for delegation in user["delegated_permissions"]:
            if delegation["resource"] == resource_id and action in delegation["actions"]:
                if datetime.fromisoformat(delegation["expiry"]) > datetime.now():
                    return True
        return False

    def delegate_access(self, owner, target_user, resource_id, actions, duration_min=60):
        if not self.authorize(owner, "delegate"):
            return False
        
        if target_user not in self.data["users"]:
            return False

        expiry = (datetime.now() + timedelta(minutes=duration_min)).isoformat()
        delegation = {
            "resource": resource_id,
            "actions": actions,
            "expiry": expiry,
            "granted_by": owner
        }
        
        self.data["users"][target_user]["delegated_permissions"].append(delegation)
        self._save_data()
        return True

    def access_file(self, username, file_id, action):
        if self.authorize(username, action, resource_id=file_id):
            return f"Access GRANTED: User '{username}' performed '{action}' on '{file_id}'"
        return f"Access DENIED: User '{username}' lacks '{action}' permission"

if __name__ == "__main__":
    ams = AccessManagementSystem()

    # Setup environment
    ams.create_user("alice", "admin123", role="admin")
    ams.create_user("bob", "bob456", role="viewer")

    # 1. Standard RBAC Authentication & Authorization
    if ams.authenticate("alice", "admin123"):
        print(ams.access_file("alice", "financial_report.pdf", "write"))

    # 2. Bob tries to write (Denied by role)
    print(ams.access_file("bob", "financial_report.pdf", "write"))

    # 3. Alice delegates specific 'write' rights to Bob for 10 minutes
    print("\nDelegating rights...")
    ams.delegate_access("alice", "bob", "financial_report.pdf", ["write"], duration_min=10)

    # 4. Bob tries to write again (Granted by delegation)
    print(ams.access_file("bob", "financial_report.pdf", "write"))