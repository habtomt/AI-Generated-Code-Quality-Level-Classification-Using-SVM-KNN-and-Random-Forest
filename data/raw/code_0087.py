#!/usr/bin/env python3

import uuid
import time
import hmac
import hashlib
import json
from dataclasses import dataclass
from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------
# International Payment System (Mock)
# -----------------------------

SECRET_KEY = b"global_payments_secret"


SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "TRY", "JPY", "AUD"}
RESTRICTED_COUNTRIES = {"NK", "IR", "SY"}  # mock compliance restrictions


EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.78,
    "TRY": 32.5,
    "JPY": 155.0,
    "AUD": 1.5
}


@dataclass
class InternationalPayment:
    user_id: str
    country: str
    amount: float
    currency: str
    target_currency: str


def generate_tx_id():
    return str(uuid.uuid4())


def sign(data: dict) -> str:
    msg = json.dumps(data, sort_keys=True).encode()
    return hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()


def convert_currency(amount, from_currency, to_currency):
    usd_amount = amount / EXCHANGE_RATES[from_currency]
    return usd_amount * EXCHANGE_RATES[to_currency]


def compliance_check(country: str) -> bool:
    return country not in RESTRICTED_COUNTRIES


def fraud_check(amount: float) -> bool:
    return amount < 10000  # mock rule


def process_gateway(payment: InternationalPayment):
    time.sleep(0.2)
    return {
        "approved": True,
        "provider_ref": str(uuid.uuid4())[:10]
    }


@app.route("/intl/pay", methods=["POST"])
def international_pay():
    data = request.get_json()

    payment = InternationalPayment(
        user_id=data["user_id"],
        country=data["country"],
        amount=float(data["amount"]),
        currency=data["currency"],
        target_currency=data.get("target_currency", "USD")
    )

    if payment.currency not in SUPPORTED_CURRENCIES:
        return jsonify({"status": "error", "message": "Unsupported currency"}), 400

    if not compliance_check(payment.country):
        return jsonify({"status": "rejected", "message": "Country not compliant"}), 403

    if not fraud_check(payment.amount):
        return jsonify({"status": "rejected", "message": "Fraud risk detected"}), 403

    converted = convert_currency(
        payment.amount,
        payment.currency,
        payment.target_currency
    )

    gateway = process_gateway(payment)

    transaction = {
        "transaction_id": generate_tx_id(),
        "user_id": payment.user_id,
        "country": payment.country,
        "original_amount": payment.amount,
        "original_currency": payment.currency,
        "converted_amount": converted,
        "target_currency": payment.target_currency,
        "approved": gateway["approved"],
        "provider_ref": gateway["provider_ref"],
        "timestamp": time.time()
    }

    transaction["signature"] = sign(transaction)

    return jsonify({"status": "success", "transaction": transaction})


@app.route("/intl/verify", methods=["POST"])
def verify():
    data = request.get_json()
    tx = data["transaction"]
    signature = data["signature"]

    expected = sign(tx)

    if hmac.compare_digest(signature, expected):
        return jsonify({"status": "valid"})
    return jsonify({"status": "invalid"}), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(port=5003, debug=True)