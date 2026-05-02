#!/usr/bin/env python3

import uuid
import time
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------
# Mock Refund Management System
# -----------------------------

@dataclass
class PaymentRecord:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    status: str  # "paid", "refunded", "partial_refund"


@dataclass
class RefundRequest:
    request_id: str
    transaction_id: str
    user_id: str
    amount: float
    reason: str
    status: str  # "pending", "approved", "rejected", "processed"


payments = {}
refund_requests = {}


def generate_id():
    return str(uuid.uuid4())


def get_payment(tx_id):
    return payments.get(tx_id)


def update_payment_record(payment: PaymentRecord, refund_amount: float):
    if refund_amount >= payment.amount:
        payment.status = "refunded"
    else:
        payment.status = "partial_refund"


def mock_refund_gateway(refund: RefundRequest):
    time.sleep(0.3)
    return {
        "approved": True,
        "gateway_ref": str(uuid.uuid4())[:10]
    }


@app.route("/payment/create", methods=["POST"])
def create_payment():
    data = request.get_json()

    tx = PaymentRecord(
        transaction_id=generate_id(),
        user_id=data["user_id"],
        amount=float(data["amount"]),
        currency=data.get("currency", "USD"),
        status="paid"
    )

    payments[tx.transaction_id] = tx

    return jsonify({"status": "created", "payment": asdict(tx)})


@app.route("/refund/request", methods=["POST"])
def request_refund():
    data = request.get_json()

    payment = get_payment(data["transaction_id"])
    if not payment:
        return jsonify({"status": "error", "message": "Payment not found"}), 404

    refund = RefundRequest(
        request_id=generate_id(),
        transaction_id=payment.transaction_id,
        user_id=payment.user_id,
        amount=float(data["amount"]),
        reason=data.get("reason", ""),
        status="pending"
    )

    refund_requests[refund.request_id] = refund

    gateway = mock_refund_gateway(refund)

    if not gateway["approved"]:
        refund.status = "rejected"
        return jsonify({"status": "failed", "refund": asdict(refund)}), 400

    refund.status = "processed"
    update_payment_record(payment, refund.amount)

    return jsonify({
        "status": "success",
        "refund": asdict(refund),
        "payment": asdict(payment),
        "gateway_ref": gateway["gateway_ref"]
    })


@app.route("/refund/status/<request_id>", methods=["GET"])
def refund_status(request_id):
    refund = refund_requests.get(request_id)
    if not refund:
        return jsonify({"status": "error", "message": "Not found"}), 404
    return jsonify(asdict(refund))


@app.route("/payment/<tx_id>", methods=["GET"])
def payment_status(tx_id):
    payment = payments.get(tx_id)
    if not payment:
        return jsonify({"status": "error", "message": "Not found"}), 404
    return jsonify(asdict(payment))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(port=5004, debug=True)