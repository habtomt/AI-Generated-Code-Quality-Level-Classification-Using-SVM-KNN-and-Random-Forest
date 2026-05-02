import os
import json
import zlib
import hashlib
import shutil
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class IntegratedStorageSystem:
    """
    A comprehensive file management system featuring:
    1. Version Control (Tracking & Restoration)
    2. Access Management (RBAC & Delegation)
    3. Security (Encryption at rest & Integrity)
    4. Storage Efficiency (Compression & Deduplication)
    """
    def __init__(self, vault_dir=".system_vault", master_password="default-secret"):
        self.vault_dir = vault_dir
        self.objects_dir = os.path.join(vault_dir, "objects")
        self.config_path = os.path.join(vault_dir, "config.json")
        self.salt_path = os.path.join(vault_dir, "vault.salt")
        
        self._setup_directories()
        self.salt = self._get_or_create_salt()
        self.key = self._derive_key(master_password, self.salt)
        self.cipher = Fernet(self.key)
        self.db = self._load_db()

    def _setup_directories(self):
        os.makedirs(self.objects_dir, exist_ok=True)

    def _get_or_create_salt(self):
        if os.path.exists(self.salt_path):
            with open(self.salt_path, "rb") as f: return f.read()
        salt = os.urandom(16)
        with open(self.salt_path, "wb") as f: f.write(salt)
        return salt

    def _derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def _load_db(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f: return json.load(f)
        return {
            "users": {"admin": {"pwd": self._hash_pwd("admin123"), "role": "admin", "delegations": []}},
            "files": {}, # file_name: [versions]
            "roles": {"admin": ["read", "write", "delete", "delegate"], "user": ["read", "write"]}
        }

    def _save_db(self):
        with open(self.config_path, "w") as f:
            json.dump(self.db, f, indent=4)

    def _hash_pwd(self, pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    def _get_file_hash(self, path):
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192): hasher.update(chunk)
        return hasher.hexdigest()

    # --- ACCESS MANAGEMENT ---
    def authorize(self, username, action, resource=None):
        user = self.db["users"].get(username)
        if not user: return False
        
        if action in self.db["roles"].get(user["role"], []):
            return True
            
        for d in user["delegations"]:
            if d["resource"] == resource and action in d["actions"]:
                if datetime.fromisoformat(d["expiry"]) > datetime.now():
                    return True
        return False

    def delegate(self, owner, target, resource, actions, mins=30):
        if not self.authorize(owner, "delegate") or target not in self.db["users"]:
            return False
        expiry = (datetime.now() + timedelta(minutes=mins)).isoformat()
        self.db["users"][target]["delegations"].append({
            "resource": resource, "actions": actions, "expiry": expiry
        })
        self._save_db()
        return True

    # --- VERSION CONTROL & SECURITY ---
    def save_file(self, username, local_path, cloud_name, msg=""):
        if not self.authorize(username, "write"):
            return "Unauthorized"

        content_hash = self._get_file_hash(local_path)
        obj_path = os.path.join(self.objects_dir, content_hash)

        if not os.path.exists(obj_path):
            with open(local_path, "rb") as f:
                compressed = zlib.compress(f.read())
                encrypted = self.cipher.encrypt(compressed)
            with open(obj_path, "wb") as f:
                f.write(encrypted)

        version_entry = {
            "vid": content_hash[:8],
            "hash": content_hash,
            "msg": msg,
            "author": username,
            "ts": datetime.now().isoformat()
        }

        if cloud_name not in self.db["files"]:
            self.db["files"][cloud_name] = []
        
        # Deduplication check
        if not self.db["files"][cloud_name] or self.db["files"][cloud_name][-1]["hash"] != content_hash:
            self.db["files"][cloud_name].append(version_entry)
            self._save_db()
            return f"Committed version {version_entry['vid']}"
        return "No changes detected."

    def restore_file(self, username, cloud_name, vid, dest_path):
        if not self.authorize(username, "read", resource=cloud_name):
            return "Unauthorized"

        history = self.db["files"].get(cloud_name, [])
        version = next((v for v in history if v["vid"] == vid), None)
        if not version: return "Version not found"

        obj_path = os.path.join(self.objects_dir, version["hash"])
        with open(obj_path, "rb") as f:
            decrypted = self.cipher.decrypt(f.read())
            decompressed = zlib.decompress(decrypted)
        
        with open(dest_path, "wb") as f:
            f.write(decompressed)
        return f"Restored to {dest_path}"

if __name__ == "__main__":
    system = IntegratedStorageSystem()
    
    # 1. Setup sample local file
    doc_path = "local_doc.txt"
    with open(doc_path, "w") as f: f.write("Project Specification v1.0")

    # 2. Save Version 1 (Admin)
    print("Admin saving file...")
    print(system.save_file("admin", doc_path, "specs.txt", "Initial Draft"))

    # 3. Create a restricted user and try to access
    system.db["users"]["junior"] = {"pwd": system._hash_pwd("p123"), "role": "user", "delegations": []}
    print("\nJunior user access (write to admin file):")
    print(system.save_file("junior", doc_path, "specs.txt", "Unauthorized attempt"))

    # 4. Delegate specific rights
    print("\nAdmin delegating read rights to Junior...")
    system.delegate("admin", "junior", "specs.txt", ["read"])

    # 5. Restore version as Junior
    history = system.db["files"]["specs.txt"]
    if history:
        print("\nJunior restoring file via delegation:")
        print(system.restore_file("junior", "specs.txt", history[0]["vid"], "restored_doc.txt"))
    
    # 6. View History
    print("\nFile History:")
    print(json.dumps(system.db["files"]["specs.txt"], indent=2))