import hashlib
import secrets
import time
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional
from enum import Enum

class ComplianceStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    FLAGGED = "FLAGGED"

@dataclass
class CurrencyConfig:
    code: str
    symbol: str
    exchange_rate_to_usd: Decimal
    is_active: bool

@dataclass
class InternationalTransaction:
    transaction_id: str
    amount_local: Decimal
    currency_code: str
    amount_usd: Decimal
    sender_country: str
    receiver_country: str
    timestamp: float
    status: str = "PENDING"
    compliance_notes: List[str] = field(default_factory=list)

class InternationalPaymentProcessor:
    def __init__(self):
        # Mock exchange rates and regulatory settings
        self.exchange_rates: Dict[str, CurrencyConfig] = {
            "USD": CurrencyConfig("USD", "$", Decimal("1.0"), True),
            "EUR": CurrencyConfig("EUR", "€", Decimal("1.08"), True),
            "GBP": CurrencyConfig("GBP", "£", Decimal("1.27"), True),
            "JPY": CurrencyConfig("JPY", "¥", Decimal("0.0066"), True),
            "INR": CurrencyConfig("INR", "₹", Decimal("0.012"), True)
        }
        # Sanctioned country list (Mock for AML/KYC compliance)
        self.sanctioned_countries = ["COUNTRY_X", "COUNTRY_Y"]

    def _verify_compliance(self, sender_country: str, receiver_country: str, amount_usd: Decimal) -> ComplianceStatus:
        if sender_country in self.sanctioned_countries or receiver_country in self.sanctioned_countries:
            return ComplianceStatus.FAILED
        
        # Threshold for enhanced due diligence (e.g., $10,000+)
        if amount_usd >= Decimal("10000.00"):
            return ComplianceStatus.FLAGGED
            
        return ComplianceStatus.PASSED

    def _convert_to_usd(self, amount: Decimal, currency_code: str) -> Decimal:
        if currency_code not in self.exchange_rates:
            raise ValueError(f"Unsupported currency: {currency_code}")
        
        rate = self.exchange_rates[currency_code].exchange_rate_to_usd
        return (amount * rate).quantize(Decimal("0.01"))

    def process_cross_border_payment(
        self, 
        amount: float, 
        currency: str, 
        origin: str, 
        destination: str
    ) -> InternationalTransaction:
        
        amt_decimal = Decimal(str(amount))
        amt_usd = self._convert_to_usd(amt_decimal, currency)
        
        tx_id = f"INTL-{secrets.token_hex(8).upper()}"
        compliance = self._verify_compliance(origin, destination, amt_usd)
        
        transaction = InternationalTransaction(
            transaction_id=tx_id,
            amount_local=amt_decimal,
            currency_code=currency,
            amount_usd=amt_usd,
            sender_country=origin,
            receiver_country=destination,
            timestamp=time.time()
        )

        if compliance == ComplianceStatus.FAILED:
            transaction.status = "REJECTED_BY_COMPLIANCE"
            transaction.compliance_notes.append("Sanctioned region detected.")
        elif compliance == ComplianceStatus.FLAGGED:
            transaction.status = "HELD_FOR_REVIEW"
            transaction.compliance_notes.append("Large transaction: Requires AML verification.")
        else:
            transaction.status = "SUCCESS"
            transaction.compliance_notes.append("Automatic regulatory clearance granted.")

        return transaction

# --- Execution Example ---
if __name__ == "__main__":
    processor = InternationalPaymentProcessor()

    payments = [
        {"amount": 100.0, "currency": "EUR", "from": "Germany", "to": "USA"},
        {"amount": 15000.0, "currency": "GBP", "from": "UK", "to": "France"},
        {"amount": 500.0, "currency": "INR", "from": "India", "to": "COUNTRY_X"},
    ]

    print(f"{'ID':<15} | {'FROM':<8} | {'TO':<8} | {'USD AMT':<10} | {'STATUS'}")
    print("-" * 65)

    for p in payments:
        res = processor.process_cross_border_payment(
            p["amount"], p["currency"], p["from"], p["to"]
        )
        print(f"{res.transaction_id:<15} | {res.sender_country:<8} | {res.receiver_country:<8} | ${res.amount_usd:<9} | {res.status}")
        if res.compliance_notes:
            for note in res.compliance_notes:
                print(f"  > Note: {note}")