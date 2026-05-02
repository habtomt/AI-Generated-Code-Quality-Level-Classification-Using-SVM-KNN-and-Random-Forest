import time
from plyer import notification

def check_for_updates():
    """
    Simulates a version check against a remote server.
    In a real app, this would fetch data from an API.
    """
    latest_version = "v2.1.0"
    update_details = (
        "• Faster load times\n"
        "• Fixed UI crashing on startup\n"
        "• Improved battery optimization"
    )
    return latest_version, update_details

def send_update_notification(version, details):
    """Triggers the system notification for the new version."""
    notification.notify(
        title=f"Update Available: {version}",
        message=f"Improvements and bug fixes are ready for you!\n{details}",
        app_name="AppUpdater",
        app_icon=None,  # Path to .ico or .png file
        timeout=15
    )

def main():
    print("Checking for updates...")
    # Simulate network latency
    time.sleep(2)
    
    version, details = check_for_updates()
    send_update_notification(version, details)
    
    print(f"Notification sent for version {version}.")

if __name__ == "__main__":
    # Dependency: pip install plyer
    main()