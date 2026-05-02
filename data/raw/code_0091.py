# upcoming_event_notifier.py

import time
import threading

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


class Event:
    def __init__(self, title: str, event_time: str, details: str):
        self.title = title
        self.event_time = event_time
        self.details = details


class SubscriptionService:
    def __init__(self):
        self.subscribed_events = []

    def subscribe(self, event: Event):
        self.subscribed_events.append(event)


class NotificationService:
    def notify(self, event: Event):
        title = f"Upcoming Event: {event.title}"
        message = f"Time: {event.event_time}\nDetails: {event.details}"

        if HAS_PLYER:
            notification.notify(
                title=title,
                message=message,
                timeout=8
            )
        else:
            print(f"\n[NOTIFICATION]\n{title}\n{message}\n")


class EventReminderEngine:
    def __init__(self, subscription_service: SubscriptionService, notifier: NotificationService):
        self.subscription_service = subscription_service
        self.notifier = notifier

    def start(self):
        while True:
            for event in self.subscription_service.subscribed_events:
                self.notifier.notify(event)
                time.sleep(2)
            time.sleep(10)


def seed_events(service: SubscriptionService):
    service.subscribe(Event("AI Conference", "2026-04-24 10:00", "Deep learning and ML trends."))
    service.subscribe(Event("Team Meeting", "2026-04-24 14:30", "Sprint planning and updates."))
    service.subscribe(Event("Webinar", "2026-04-25 18:00", "Cloud architecture best practices."))


if __name__ == "__main__":
    subscription_service = SubscriptionService()
    seed_events(subscription_service)

    notifier = NotificationService()
    engine = EventReminderEngine(subscription_service, notifier)

    thread = threading.Thread(target=engine.start)
    thread.daemon = True
    thread.start()

    while True:
        time.sleep(1)