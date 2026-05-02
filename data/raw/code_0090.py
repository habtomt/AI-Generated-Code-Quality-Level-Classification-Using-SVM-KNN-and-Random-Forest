# app_update_notification.py

import time
import threading

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


class UpdateNotifier:
    def __init__(self, current_version: str):
        self.current_version = current_version

    def check_for_update(self):
        # Simulated latest version from server
        latest_version = "2.0.0"

        if latest_version != self.current_version:
            self.send_notification(latest_version)

    def send_notification(self, latest_version: str):
        title = "App Update Available"
        message = (
            f"A new version ({latest_version}) is available.\n"
            "Includes performance improvements, bug fixes, and stability upgrades."
        )

        if HAS_PLYER:
            notification.notify(
                title=title,
                message=message,
                timeout=6
            )
        else:
            print(f"[NOTIFICATION] {title}\n{message}")


def run_update_checker():
    notifier = UpdateNotifier(current_version="1.0.0")

    while True:
        notifier.check_for_update()
        time.sleep(10)


if __name__ == "__main__":
    thread = threading.Thread(target=run_update_checker)
    thread.start()
    thread.join()