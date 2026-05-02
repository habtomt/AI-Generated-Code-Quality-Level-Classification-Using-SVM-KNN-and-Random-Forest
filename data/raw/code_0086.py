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
# Mobile Payment Integration Layer (Mock SDK)
# -----------------------------

SECRET_KEY = b"mobile_secure_key_change_me"


@dataclass
class MobilePaymentRequest:
    user_id: str
    wallet_type: str  # e.g. apple_pay, google_pay, paypal_wallet
    amount: float
    currency: str
    token: str  # payment token from mobile SDK


def generate_tx_id():
    return str(uuid.uuid4())


def sign_payload(payload: dict) -> str:
    msg = json.dumps(payload, sort_keys=True).encode()
    return hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()


def verify_token(token: str) -> bool:
    return len(token) > 10


def mock_wallet_gateway(req: MobilePaymentRequest) -> dict:
    time.sleep(0.3)
    approved = hash(req.token + req.user_id) % 2 == 0
    return {
        "approved": approved,
        "wallet_ref": str(uuid.uuid4())[:10],
        "message": "Approved" if approved else "Declined"
    }


class MobilePaymentSDK:
    @staticmethod
    def create_payment(user_id, wallet_type, amount, currency, token):
        req = MobilePaymentRequest(
            user_id=user_id,
            wallet_type=wallet_type,
            amount=amount,
            currency=currency,
            token=token
        )

        if not verify_token(req.token):
            return {"status": "error", "message": "Invalid wallet token"}

        gateway = mock_wallet_gateway(req)

        tx = {
            "transaction_id": generate_tx_id(),
            "user_id": req.user_id,
            "wallet_type": req.wallet_type,
            "amount": req.amount,
            "currency": req.currency,
            "approved": gateway["approved"],
            "wallet_ref": gateway["wallet_ref"],
            "timestamp": time.time()
        }

        tx["signature"] = sign_payload(tx)

        if not gateway["approved"]:
            return {"status": "failed", "transaction": tx}

        return {"status": "success", "transaction": tx}


@app.route("/mobile/pay", methods=["POST"])
def mobile_pay():
    data = request.get_json()

    result = MobilePaymentSDK.create_payment(
        user_id=data["user_id"],
        wallet_type=data["wallet_type"],
        amount=float(data["amount"]),
        currency=data.get("currency", "USD"),
        token=data["token"]
    )

    return jsonify(result)


@app.route("/mobile/verify", methods=["POST"])
def verify_transaction():
    data = request.get_json()
    signature = data.get("signature")
    transaction = data.get("transaction")

    expected = sign_payload(transaction)

    if hmac.compare_digest(signature, expected):
        return jsonify({"status": "valid"})
    return jsonify({"status": "invalid"}), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(port=5002, debug=True)