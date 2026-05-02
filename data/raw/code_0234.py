import uuid
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

class RefundStatus(Enum):
    REQUESTED = "REQUESTED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PROCESSED = "PROCESSED"
    REJECTED = "REJECTED"

@dataclass
class RefundRequest:
    refund_id: str
    original_transaction_id: str
    user_id: str
    amount: float
    reason: str
    status: RefundStatus = RefundStatus.REQUESTED
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

class RefundSystem:
    def __init__(self):
        # Mock databases
        self._transaction_ledger: Dict[str, dict] = {
            "TXN_001": {"user_id": "U123", "amount": 150.00, "status": "CAPTURED"},
            "TXN_002": {"user_id": "U456", "amount": 85.50, "status": "CAPTURED"},
            "TXN_003": {"user_id": "U123", "amount": 20.00, "status": "CAPTURED"}
        }
        self._refunds: Dict[str, RefundRequest] = {}

    def request_refund(self, transaction_id: str, reason: str) -> Optional[str]:
        if transaction_id not in self._transaction_ledger:
            return None
        
        tx = self._transaction_ledger[transaction_id]
        refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
        
        request = RefundRequest(
            refund_id=refund_id,
            original_transaction_id=transaction_id,
            user_id=tx["user_id"],
            amount=tx["amount"],
            reason=reason
        )
        
        self._refunds[refund_id] = request
        return refund_id

    def process_pending_refunds(self):
        for refund_id, refund in self._refunds.items():
            if refund.status == RefundStatus.REQUESTED:
                refund.status = RefundStatus.PENDING
                refund.updated_at = time.time()
                self._execute_bank_transfer(refund)

    def _execute_bank_transfer(self, refund: RefundRequest):
        # Mock communication with payment gateway
        print(f"Communicating with Bank for Refund: {refund.refund_id}...")
        time.sleep(0.1) 
        
        refund.status = RefundStatus.PROCESSED
        refund.updated_at = time.time()
        
        # Update original record
        tx_id = refund.original_transaction_id
        self._transaction_ledger[tx_id]["status"] = "REFUNDED"
        self._transaction_ledger[tx_id]["refund_ref"] = refund.refund_id

    def get_refund_status(self, refund_id: str) -> dict:
        refund = self._refunds.get(refund_id)
        if not refund:
            return {"error": "Not found"}
        
        return {
            "id": refund.refund_id,
            "status": refund.status.value,
            "amount": refund.amount,
            "last_update": datetime.fromtimestamp(refund.updated_at).strftime('%Y-%m-%d %H:%M:%S')
        }

# --- Demo Execution ---
if __name__ == "__main__":
    system = RefundSystem()

    print("--- 1. Submitting Refund Request ---")
    rid = system.request_refund("TXN_001", "Product arrived damaged")
    if rid:
        print(f"Refund Created: {rid}")
        status_check = system.get_refund_status(rid)
        print(f"Current State: {status_check['status']}")

    print("\n--- 2. Batch Processing Refunds ---")
    system.process_pending_refunds()

    print("\n--- 3. Final Verification ---")
    final_status = system.get_refund_status(rid)
    print(f"Final Status: {final_status['status']}")
    print(f"Processed At: {final_status['last_update']}")
    
    print("\nUpdated Ledger Record for TXN_001:")
    print(system._transaction_ledger["TXN_001"])