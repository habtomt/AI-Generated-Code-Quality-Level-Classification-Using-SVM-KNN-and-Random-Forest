import abc
import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

# --- Constants & Security ---
SECRET_KEY = b"your-high-entropy-secret-key-here"

class TransactionStatus(Enum):
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    FAILED = "FAILED"
    DECLINED = "DECLINED"

@dataclass
class PaymentResult:
    transaction_id: str
    status: TransactionStatus
    message: str
    timestamp: float

# --- Core Interfaces ---
class PaymentGateway(abc.ABC):
    @abc.abstractmethod
    def authorize(self, card_details: dict, amount: float) -> PaymentResult:
        pass

    @abc.abstractmethod
    def capture(self, transaction_id: str) -> PaymentResult:
        pass

# --- Implementation ---
class SecurePaymentProcessor(PaymentGateway):
    def __init__(self):
        self._transaction_ledger: Dict[str, dict] = {}

    def _generate_transaction_id(self) -> str:
        return secrets.token_hex(16)

    def _validate_card(self, card_details: dict) -> bool:
        # Basic industry standard check (Luhn Algorithm simulation)
        required = ["number", "expiry", "cvv", "holder"]
        return all(k in card_details for k in required) and len(card_details["cvv"]) >= 3

    def _sign_payload(self, data: str) -> str:
        return hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()

    def authorize(self, card_details: dict, amount: float) -> PaymentResult:
        if not self._validate_card(card_details):
            return PaymentResult(
                transaction_id="N/A",
                status=TransactionStatus.FAILED,
                message="Invalid card format or missing details",
                timestamp=time.time()
            )

        # In a real scenario, this communicates with an acquiring bank
        tx_id = self._generate_transaction_id()
        self._transaction_ledger[tx_id] = {
            "amount": amount,
            "status": TransactionStatus.AUTHORIZED,
            "signature": self._sign_payload(f"{tx_id}{amount}")
        }

        return PaymentResult(
            transaction_id=tx_id,
            status=TransactionStatus.AUTHORIZED,
            message="Authorization successful",
            timestamp=time.time()
        )

    def capture(self, transaction_id: str) -> PaymentResult:
        tx = self._transaction_ledger.get(transaction_id)
        
        if not tx:
            return PaymentResult(transaction_id, TransactionStatus.FAILED, "Transaction not found", time.time())
        
        if tx["status"] != TransactionStatus.AUTHORIZED:
            return PaymentResult(transaction_id, TransactionStatus.FAILED, "Invalid state transition", time.time())

        # Update status to Captured
        tx["status"] = TransactionStatus.CAPTURED
        return PaymentResult(
            transaction_id=transaction_id,
            status=TransactionStatus.CAPTURED,
            message="Funds captured successfully",
            timestamp=time.time()
        )

# --- Execution ---
if __name__ == "__main__":
    processor = SecurePaymentProcessor()

    # Simulation Data (Sensitive data handled as transient dictionary)
    mock_card = {
        "number": "4111222233334444",
        "expiry": "12/28",
        "cvv": "123",
        "holder": "JOHN DOE"
    }

    print("--- Initiating Transaction ---")
    auth_response = processor.authorize(mock_card, 250.00)
    print(f"Status: {auth_response.status.value} | ID: {auth_response.transaction_id}")

    if auth_response.status == TransactionStatus.AUTHORIZED:
        print("\n--- Capturing Funds ---")
        capture_response = processor.capture(auth_response.transaction_id)
        print(f"Final Status: {capture_response.status.value} | Msg: {capture_response.message}")