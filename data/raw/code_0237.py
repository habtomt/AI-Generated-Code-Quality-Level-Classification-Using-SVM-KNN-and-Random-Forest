import time
from datetime import datetime, timedelta
from plyer import notification

# Mock database of user-subscribed events
SUBSCRIBED_EVENTS = [
    {
        "title": "Python Developer Workshop",
        "time": (datetime.now() + timedelta(minutes=30)).strftime("%H:%M"),
        "details": "Live coding session on asynchronous programming.",
        "notified": False
    },
    {
        "title": "Project Sync Meeting",
        "time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M"),
        "details": "Weekly roadmap review with the engineering team.",
        "notified": False
    }
]

def notify_event(event):
    """Triggers a system notification for a specific event."""
    notification.notify(
        title=f"Upcoming Event: {event['title']}",
        message=f"Starts at {event['time']}\n{event['details']}",
        app_name="EventNotifier",
        timeout=20
    )
    event["notified"] = True
    print(f"[LOG] Notification triggered for: {event['title']}")

def monitor_schedule():
    print("--- Event Monitor Active ---")
    print("Checking for upcoming subscribed events...")
    
    try:
        while True:
            for event in SUBSCRIBED_EVENTS:
                if not event["notified"]:
                    # In a real scenario, this would check if current time 
                    # is within a specific threshold of event['time']
                    notify_event(event)
            
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n--- Monitor Stopped ---")

if __name__ == "__main__":
    # Dependency: pip install plyer
    monitor_schedule()