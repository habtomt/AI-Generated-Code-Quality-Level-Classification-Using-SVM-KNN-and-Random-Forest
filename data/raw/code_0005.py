import hashlib
from functools import wraps

# In-memory "database"
users_db = {}

# Roles and permissions
ROLES = {
    "admin": ["create", "read", "update", "delete"],
    "editor": ["read", "update"],
    "viewer": ["read"]
}

# Utility functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role):
    if role not in ROLES:
        raise ValueError("Invalid role")
    users_db[username] = {
        "password": hash_password(password),
        "role": role
    }

def authenticate(username, password):
    user = users_db.get(username)
    if not user:
        return None
    if user["password"] == hash_password(password):
        return {"username": username, "role": user["role"]}
    return None

# Authorization decorator
def requires_permission(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user is None:
                raise PermissionError("Authentication required")
            role = user["role"]
            if permission not in ROLES.get(role, []):
                raise PermissionError(f"Role '{role}' does not have '{permission}' permission")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

# Application actions
@requires_permission("create")
def create_resource(user, data):
    print(f"{user['username']} created resource: {data}")

@requires_permission("read")
def read_resource(user):
    print(f"{user['username']} is reading resources")

@requires_permission("update")
def update_resource(user, data):
    print(f"{user['username']} updated resource to: {data}")

@requires_permission("delete")
def delete_resource(user):
    print(f"{user['username']} deleted a resource")

# Demo
if __name__ == "__main__":
    register_user("alice", "password123", "admin")
    register_user("bob", "password123", "editor")
    register_user("charlie", "password123", "viewer")

    user_admin = authenticate("alice", "password123")
    user_editor = authenticate("bob", "password123")
    user_viewer = authenticate("charlie", "password123")

    create_resource(user_admin, "New Data")
    read_resource(user_editor)
    update_resource(user_editor, "Updated Data")

    try:
        delete_resource(user_viewer)
    except PermissionError as e:
        print(e)