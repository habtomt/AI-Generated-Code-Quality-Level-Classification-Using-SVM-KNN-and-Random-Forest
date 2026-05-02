import uuid
import time
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

@dataclass
class Subscription:
    subscription_id: str
    user_id: str
    plan_name: str
    amount: float
    frequency_days: int
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    next_payment_date: datetime = field(default_factory=datetime.now)
    history: List[dict] = field(default_factory=list)

class SubscriptionManager:
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}

    def create_subscription(self, user_id: str, plan: str, amount: float, interval: int) -> str:
        sub_id = str(uuid.uuid4())[:8]
        new_sub = Subscription(
            subscription_id=sub_id,
            user_id=user_id,
            plan_name=plan,
            amount=amount,
            frequency_days=interval,
            next_payment_date=datetime.now() + timedelta(days=interval)
        )
        self.subscriptions[sub_id] = new_sub
        return sub_id

    def cancel_subscription(self, sub_id: str) -> bool:
        if sub_id in self.subscriptions:
            self.subscriptions[sub_id].status = SubscriptionStatus.CANCELLED
            return True
        return False

    def update_subscription(self, sub_id: str, new_status: SubscriptionStatus) -> None:
        if sub_id in self.subscriptions:
            self.subscriptions[sub_id].status = new_status

    def process_recurring_payments(self):
        now = datetime.now()
        for sub_id, sub in self.subscriptions.items():
            if sub.status == SubscriptionStatus.ACTIVE and now >= sub.next_payment_date:
                self._execute_payment(sub)

    def _execute_payment(self, sub: Subscription):
        # Mock payment processing logic
        transaction_id = str(uuid.uuid4())
        payment_record = {
            "transaction_id": transaction_id,
            "amount": sub.amount,
            "date": datetime.now().isoformat(),
            "status": "success"
        }
        sub.history.append(payment_record)
        sub.next_payment_date += timedelta(days=sub.frequency_days)
        print(f"Processed ${sub.amount} for {sub.plan_name} (Sub ID: {sub.subscription_id})")

    def get_user_subscriptions(self, user_id: str) -> List[Subscription]:
        return [sub for sub in self.subscriptions.values() if sub.user_id == user_id]

# Example Execution
if __name__ == "__main__":
    manager = SubscriptionManager()

    # 1. User signs up for Monthly Premium and Weekly Basic plans
    user_a = "user_123"
    premium_id = manager.create_subscription(user_a, "Monthly Premium", 29.99, 30)
    basic_id = manager.create_subscription(user_a, "Weekly Basic", 9.99, 7)

    # 2. Simulate time passing for the Weekly Basic (forcing payment date to now)
    manager.subscriptions[basic_id].next_payment_date = datetime.now() - timedelta(minutes=1)

    print(f"Active Subscriptions for {user_a}:")
    for s in manager.get_user_subscriptions(user_a):
        print(f"- {s.plan_name}: {s.status.value}")

    # 3. Process payments
    print("\nRunning billing cycle...")
    manager.process_recurring_payments()

    # 4. Cancel a subscription
    manager.cancel_subscription(premium_id)
    print(f"\nStatus of {premium_id} after cancellation: {manager.subscriptions[premium_id].status.value}")