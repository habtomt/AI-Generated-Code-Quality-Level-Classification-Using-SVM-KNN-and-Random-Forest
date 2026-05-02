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
# Mock Secure Payment System
# -----------------------------

SECRET_KEY = b"super_secret_key_change_me"


@dataclass
class PaymentRequest:
    card_number: str
    expiry_month: int
    expiry_year: int
    cvv: str
    amount: float
    currency: str


def luhn_check(card_number: str) -> bool:
    digits = [int(d) for d in card_number if d.isdigit()]
    checksum = 0
    parity = len(digits) % 2

    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


def verify_card_data(req: PaymentRequest) -> bool:
    if not luhn_check(req.card_number):
        return False
    if not (1 <= req.expiry_month <= 12):
        return False
    if len(req.cvv) not in (3, 4):
        return False
    if req.amount <= 0:
        return False
    return True


def generate_transaction_id() -> str:
    return str(uuid.uuid4())


def sign_transaction(data: dict) -> str:
    message = json.dumps(data, sort_keys=True).encode()
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()


def mock_bank_authorization(req: PaymentRequest) -> dict:
    time.sleep(0.5)
    approved = int(req.card_number[-1]) % 2 == 0
    return {
        "approved": approved,
        "auth_code": str(uuid.uuid4())[:8].upper(),
        "message": "Approved" if approved else "Declined by bank"
    }


@app.route("/pay", methods=["POST"])
def process_payment():
    data = request.get_json()

    try:
        req = PaymentRequest(
            card_number=data["card_number"],
            expiry_month=int(data["expiry_month"]),
            expiry_year=int(data["expiry_year"]),
            cvv=data["cvv"],
            amount=float(data["amount"]),
            currency=data.get("currency", "USD")
        )
    except Exception:
        return jsonify({"status": "error", "message": "Invalid request format"}), 400

    if not verify_card_data(req):
        return jsonify({"status": "failed", "message": "Card validation failed"}), 400

    auth_result = mock_bank_authorization(req)

    transaction = {
        "transaction_id": generate_transaction_id(),
        "amount": req.amount,
        "currency": req.currency,
        "approved": auth_result["approved"],
        "auth_code": auth_result["auth_code"],
        "timestamp": time.time()
    }

    transaction["signature"] = sign_transaction(transaction)

    if not auth_result["approved"]:
        return jsonify({
            "status": "declined",
            "transaction": transaction,
            "message": auth_result["message"]
        }), 402

    return jsonify({
        "status": "success",
        "transaction": transaction,
        "message": "Payment processed successfully"
    })


@app.route("/verify", methods=["POST"])
def verify_transaction():
    data = request.get_json()
    signature = data.get("signature")
    transaction = data.get("transaction")

    expected_signature = sign_transaction(transaction)

    if hmac.compare_digest(signature, expected_signature):
        return jsonify({"status": "valid", "message": "Transaction verified"})
    else:
        return jsonify({"status": "invalid", "message": "Signature mismatch"}), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)