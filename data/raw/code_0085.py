#!/usr/bin/env python3

import uuid
import time
import threading
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------
# Mock Subscription System
# -----------------------------

@dataclass
class Subscription:
    id: str
    user_id: str
    amount: float
    currency: str
    interval_seconds: int
    active: bool
    next_run: float


subscriptions = {}
lock = threading.Lock()


def generate_id():
    return str(uuid.uuid4())


def process_payment(subscription: Subscription):
    print(f"[PAYMENT] User {subscription.user_id} charged {subscription.amount} {subscription.currency} (sub {subscription.id})")


def scheduler_loop():
    while True:
        now = time.time()
        with lock:
            for sub in list(subscriptions.values()):
                if sub.active and now >= sub.next_run:
                    process_payment(sub)
                    sub.next_run = now + sub.interval_seconds
        time.sleep(1)


@app.route("/subscribe", methods=["POST"])
def create_subscription():
    data = request.get_json()

    sub = Subscription(
        id=generate_id(),
        user_id=data["user_id"],
        amount=float(data["amount"]),
        currency=data.get("currency", "USD"),
        interval_seconds=int(data["interval_seconds"]),
        active=True,
        next_run=time.time() + int(data["interval_seconds"])
    )

    with lock:
        subscriptions[sub.id] = sub

    return jsonify({"status": "created", "subscription": asdict(sub)})


@app.route("/subscriptions/<user_id>", methods=["GET"])
def list_subscriptions(user_id):
    with lock:
        result = [asdict(s) for s in subscriptions.values() if s.user_id == user_id]
    return jsonify(result)


@app.route("/cancel/<sub_id>", methods=["POST"])
def cancel_subscription(sub_id):
    with lock:
        if sub_id not in subscriptions:
            return jsonify({"status": "error", "message": "Not found"}), 404
        subscriptions[sub_id].active = False

    return jsonify({"status": "cancelled", "subscription_id": sub_id})


@app.route("/pause/<sub_id>", methods=["POST"])
def pause_subscription(sub_id):
    with lock:
        if sub_id not in subscriptions:
            return jsonify({"status": "error", "message": "Not found"}), 404
        subscriptions[sub_id].active = False

    return jsonify({"status": "paused", "subscription_id": sub_id})


@app.route("/resume/<sub_id>", methods=["POST"])
def resume_subscription(sub_id):
    with lock:
        if sub_id not in subscriptions:
            return jsonify({"status": "error", "message": "Not found"}), 404
        sub = subscriptions[sub_id]
        sub.active = True
        sub.next_run = time.time() + sub.interval_seconds

    return jsonify({"status": "resumed", "subscription_id": sub_id})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
    app.run(port=5001, debug=True)