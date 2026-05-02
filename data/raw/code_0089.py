# notification_app.py

import time
import threading
from dataclasses import dataclass
from typing import List, Callable

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


@dataclass
class Message:
    sender: str
    content: str


class MessageService:
    def __init__(self):
        self.listeners: List[Callable[[Message], None]] = []

    def subscribe(self, listener: Callable[[Message], None]):
        self.listeners.append(listener)

    def receive_message(self, message: Message):
        for listener in self.listeners:
            listener(message)


class NotificationManager:
    def __init__(self):
        pass

    def notify(self, message: Message):
        title = f"New message from {message.sender}"
        body = message.content[:50] + ("..." if len(message.content) > 50 else "")

        if HAS_PLYER:
            notification.notify(
                title=title,
                message=body,
                timeout=5
            )
        else:
            print(f"[NOTIFICATION] {title} - {body}")


class ChatAppSimulator:
    def __init__(self):
        self.service = MessageService()
        self.notifier = NotificationManager()
        self.service.subscribe(self.notifier.notify)

    def start_receiving(self):
        messages = [
            Message("Alice", "Hey! Are we still meeting today at 6 PM?"),
            Message("Bob", "Don't forget to review the PR I sent earlier."),
            Message("Charlie", "Lunch tomorrow? I found a great place nearby."),
            Message("Diana", "The deployment was successful 🚀"),
        ]

        for msg in messages:
            time.sleep(2)
            self.service.receive_message(msg)


if __name__ == "__main__":
    app = ChatAppSimulator()

    receiver_thread = threading.Thread(target=app.start_receiving)
    receiver_thread.start()

    receiver_thread.join()