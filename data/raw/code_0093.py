# promo_notification.py

import time
import threading

try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False


class Promotion:
    def __init__(self, title: str, discount: str, valid_minutes: int):
        self.title = title
        self.discount = discount
        self.valid_minutes = valid_minutes


class PromotionService:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def push_promotion(self, promo: Promotion):
        for callback in self.subscribers:
            callback(promo)


class NotificationService:
    def notify(self, promo: Promotion):
        title = f"🔥 Limited Time Offer: {promo.title}"
        message = (
            f"Discount: {promo.discount}\n"
            f"Valid for: {promo.valid_minutes} minutes only!\n"
            "Act now before the offer expires!"
        )

        if HAS_PLYER:
            notification.notify(
                title=title,
                message=message,
                timeout=8
            )
        else:
            print(f"\n[PROMO NOTIFICATION]\n{title}\n{message}\n")


class PromoApp:
    def __init__(self):
        self.service = PromotionService()
        self.notifier = NotificationService()
        self.service.subscribe(self.notifier.notify)

    def run(self):
        promos = [
            Promotion("Summer Sale", "50% OFF", 30),
            Promotion("Flash Deal", "Buy 1 Get 1 Free", 15),
            Promotion("Weekend Special", "30% OFF", 45),
        ]

        for promo in promos:
            time.sleep(2)
            self.service.push_promotion(promo)


if __name__ == "__main__":
    app = PromoApp()

    thread = threading.Thread(target=app.run)
    thread.start()
    thread.join()