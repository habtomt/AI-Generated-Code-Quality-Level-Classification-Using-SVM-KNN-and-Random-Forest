import time
import random
from plyer import notification

# Mock database of users and message snippets
SENDERS = ["Alice", "Bob", "Charlie", "David", "Eve", "Support Team"]
MESSAGES = [
    "Hey! Are we still meeting at 5?",
    "Check out this new Python script I wrote.",
    "The project deadline has been moved to Friday.",
    "Don't forget to bring the documents.",
    "Your password was successfully changed.",
    "Can you review the pull request?"
]

def receive_message_mock():
    """Simulates receiving a new message."""
    sender = random.choice(SENDERS)
    content = random.choice(MESSAGES)
    # Create a short snippet
    snippet = (content[:47] + "..") if len(content) > 50 else content
    return sender, snippet

def trigger_notification(sender, snippet):
    """Triggers a system notification."""
    notification.notify(
        title=f"New Message from {sender}",
        message=snippet,
        app_name="MessengerApp",
        timeout=10,
    )
    print(f"[LOG] Notification sent: {sender} - {snippet}")

def run_app():
    print("--- Message Listener Started ---")
    print("Press Ctrl+C to stop the app.")
    
    try:
        while True:
            # Simulate waiting for a message (random interval)
            time.sleep(random.randint(5, 15))
            
            sender, snippet = receive_message_mock()
            trigger_notification(sender, snippet)
            
    except KeyboardInterrupt:
        print("\n--- App Stopped ---")

if __name__ == "__main__":
    # Dependency: pip install plyer
    run_app()