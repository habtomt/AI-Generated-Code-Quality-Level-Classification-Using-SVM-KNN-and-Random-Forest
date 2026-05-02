"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_001.txt
Run      : 1
"""

from flask import Flask, request, jsonify
import schedule
import time

app = Flask(__name__)

# Sample data stores
users = {
    1: {"name": "Alice", "subscriptions": []},
    2: {"name": "Bob", "subscriptions": []}
}

subscriptions = [
    {"id": 1, "name": "Monthly Plan", "price": 10.0, "billing_cycle": "monthly"},
    {"id": 2, "name": "Yearly Plan", "price": 100.0, "billing_cycle": "yearly"}
]

def process_payments():
    # This function should be integrated with a payment gateway to process payments.
    # For simplicity, it just prints a message.
    print("Processing payments...")

# Define a function to automate payments
def automate_payments():
    for user in users.values():
        for subscription in user["subscriptions"]:
            if subscription["billing_cycle"] == "monthly":
                # Process monthly payment
                print(f"Processing monthly payment for {user['name']}...")
            elif subscription["billing_cycle"] == "yearly":
                # Process yearly payment
                print(f"Processing yearly payment for {user['name']}...")

# Run automate_payments() every day at 8:00 AM
schedule.every().day.at("08:00").do(automate_payments)

def send_webhook(subscription_id):
    # This function should be integrated with a webhook library to send a webhook.
    # For simplicity, it just prints a message.
    print(f"Sending webhook for subscription {subscription_id}...")

def cancel_subscription(user_id, subscription_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    subscription = next((sub for sub in user['subscriptions'] if sub["id"] == subscription_id), None)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404
    
    user['subscriptions'].remove(subscription)
    send_webhook(subscription_id)
    return jsonify({"message": "Subscription canceled"}), 200


@app.route('/users/<int:user_id>/subscriptions', methods=['GET'])
def get_user_subscriptions(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user["subscriptions"])


@app.route('/users/<int:user_id>/subscriptions', methods=['POST'])
def add_subscription(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    subscription_id = request.json.get('subscription_id')
    subscription = next((sub for sub in subscriptions if sub["id"] == subscription_id), None)
    
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404
    
    user['subscriptions'].append(subscription)
    schedule.every().day.at("08:00").do(send_webhook, subscription_id)
    return jsonify({"message": "Subscription added", "subscription": subscription}), 201


@app.route('/users/<int:user_id>/subscriptions/<int:subscription_id>', methods=['DELETE'])
def cancel_subscription_route(user_id, subscription_id):
    return cancel_subscription(user_id, subscription_id)


if __name__ == '__main__':
    app.run(debug=True)
    
    while True:
        schedule.run_pending()
        time.sleep(1)