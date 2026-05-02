import hashlib
import json
import time
import uuid
from typing import List, Dict


class Transaction:
    def __init__(self, tx_type, data):
        self.tx_id = str(uuid.uuid4())
        self.tx_type = tx_type
        self.data = data
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "tx_id": self.tx_id,
            "tx_type": self.tx_type,
            "data": self.data,
            "timestamp": self.timestamp
        }


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append(Block(0, [], "0"))

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, tx: Transaction):
        self.pending_transactions.append(tx)

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine(self):
        if not self.pending_transactions:
            return None

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=last_block.hash
        )

        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block


class Wallet:
    def __init__(self):
        self.private_key = uuid.uuid4().hex
        self.address = self.generate_address()

    def generate_address(self):
        return hashlib.sha256(self.private_key.encode()).hexdigest()


class DeFiPlatform:
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallets: Dict[str, Wallet] = {}
        self.balances: Dict[str, float] = {}
        self.loans: List[Dict] = []
        self.orders: List[Dict] = []

    def create_wallet(self):
        wallet = Wallet()
        self.wallets[wallet.address] = wallet
        self.balances[wallet.address] = 0.0
        return wallet.address

    def deposit(self, address, amount):
        self.balances[address] += amount
        self.blockchain.add_transaction(Transaction("DEPOSIT", {"address": address, "amount": amount}))

    def transfer(self, sender, receiver, amount):
        if self.balances.get(sender, 0) < amount:
            return False

        self.balances[sender] -= amount
        self.balances[receiver] += amount

        self.blockchain.add_transaction(Transaction("TRANSFER", {
            "from": sender,
            "to": receiver,
            "amount": amount
        }))
        return True

    def lend(self, lender, borrower, amount, interest):
        if self.balances.get(lender, 0) < amount:
            return False

        self.balances[lender] -= amount
        self.balances[borrower] += amount

        loan = {
            "loan_id": str(uuid.uuid4()),
            "lender": lender,
            "borrower": borrower,
            "amount": amount,
            "interest": interest,
            "repaid": False
        }

        self.loans.append(loan)
        self.blockchain.add_transaction(Transaction("LEND", loan))
        return loan["loan_id"]

    def repay_loan(self, borrower, loan_id):
        for loan in self.loans:
            if loan["loan_id"] == loan_id and not loan["repaid"]:
                total = loan["amount"] * (1 + loan["interest"])
                if self.balances.get(borrower, 0) < total:
                    return False

                self.balances[borrower] -= total
                self.balances[loan["lender"]] += total
                loan["repaid"] = True

                self.blockchain.add_transaction(Transaction("REPAY", loan))
                return True
        return False

    def place_order(self, trader, order_type, amount, price):
        order = {
            "order_id": str(uuid.uuid4()),
            "trader": trader,
            "type": order_type,
            "amount": amount,
            "price": price
        }
        self.orders.append(order)
        self.blockchain.add_transaction(Transaction("ORDER", order))
        return order["order_id"]

    def match_orders(self):
        buys = [o for o in self.orders if o["type"] == "BUY"]
        sells = [o for o in self.orders if o["type"] == "SELL"]

        for buy in buys:
            for sell in sells:
                if buy["price"] >= sell["price"] and buy["amount"] == sell["amount"]:
                    buyer = buy["trader"]
                    seller = sell["trader"]
                    total_cost = buy["amount"] * sell["price"]

                    if self.balances.get(buyer, 0) < total_cost:
                        continue

                    self.balances[buyer] -= total_cost
                    self.balances[seller] += total_cost

                    self.orders.remove(buy)
                    self.orders.remove(sell)

                    self.blockchain.add_transaction(Transaction("TRADE", {
                        "buyer": buyer,
                        "seller": seller,
                        "amount": buy["amount"],
                        "price": sell["price"]
                    }))
                    return True
        return False

    def mine(self):
        return self.blockchain.mine()


if __name__ == "__main__":
    platform = DeFiPlatform()

    user1 = platform.create_wallet()
    user2 = platform.create_wallet()

    platform.deposit(user1, 1000)
    platform.deposit(user2, 500)

    platform.transfer(user1, user2, 200)

    loan_id = platform.lend(user2, user1, 100, 0.1)
    platform.repay_loan(user1, loan_id)

    platform.place_order(user1, "BUY", 10, 5)
    platform.place_order(user2, "SELL", 10, 5)
    platform.match_orders()

    platform.mine()

    print("Balances:", platform.balances)
    print("Blockchain length:", len(platform.blockchain.chain))