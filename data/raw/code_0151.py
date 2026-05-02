import functools

# Mock Database
users_db = {
    "alice": {"role": "admin", "id": 1},
    "bob": {"role": "editor", "id": 2},
    "charlie": {"role": "viewer", "id": 3}
}

# Current session mock
current_user = None

def login(username):
    global current_user
    if username in users_db:
        current_user = users_db[username]
        print(f"\n--- Logged in as: {username} (Role: {current_user['role']}) ---")
    else:
        print(f"\nUser {username} not found.")

def require_role(allowed_roles):
    """Decorator to enforce role-based access control (RBAC)."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_user is None:
                print(f"[Access Denied] No user logged in.")
                return None
            if current_user["role"] not in allowed_roles:
                print(f"[Access Denied] Role '{current_user['role']}' lacks permission for {func.__name__}.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_role(["admin", "editor", "viewer"])
def view_dashboard():
    print("[Action] Displaying public dashboard data...")

@require_role(["admin", "editor"])
def edit_content():
    print("[Action] Content updated successfully.")

@require_role(["admin"])
def delete_user(target_username):
    print(f"[Action] User '{target_username}' has been deleted from the system.")

def run_rbac_demo():
    # 1. Admin access
    login("alice")
    view_dashboard()
    edit_content()
    delete_user("bob")

    # 2. Editor access
    login("bob")
    view_dashboard()
    edit_content()
    delete_user("alice") # Should fail

    # 3. Viewer access
    login("charlie")
    view_dashboard()
    edit_content() # Should fail

if __name__ == "__main__":
    run_rbac_demo()