# security_alert_notifier.py

import time
import threading

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


class SecurityEvent:
    def __init__(self, username: str, issue: str):
        self.username = username
        self.issue = issue


class SecurityMonitor:
    def __init__(self):
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(callback)

    def detect_issue(self, event: SecurityEvent):
        for callback in self.listeners:
            callback(event)


class AlertService:
    def send_alert(self, event: SecurityEvent):
        title = "URGENT: Security Alert"
        message = (
            f"User: {event.username}\n"
            f"Issue: {event.issue}\n"
            "Please change your password immediately."
        )

        if HAS_PLYER:
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
        else:
            print(f"\n[SECURITY ALERT]\n{title}\n{message}\n")


class AppSimulator:
    def __init__(self):
        self.monitor = SecurityMonitor()
        self.alert_service = AlertService()
        self.monitor.subscribe(self.alert_service.send_alert)

    def run(self):
        simulated_events = [
            SecurityEvent("ezgi", "Login from unknown device detected"),
            SecurityEvent("ezgi", "Multiple failed login attempts detected"),
            SecurityEvent("ezgi", "Suspicious password reset request"),
        ]

        for event in simulated_events:
            time.sleep(3)
            self.monitor.detect_issue(event)


if __name__ == "__main__":
    app = AppSimulator()

    t = threading.Thread(target=app.run)
    t.start()
    t.join()