import hashlib
import json
import time
import uuid
from typing import List


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
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
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine(self):
        if not self.pending_transactions:
            return False

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=last_block.hash
        )

        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block.index


class Wallet:
    def __init__(self):
        self.private_key = uuid.uuid4().hex
        self.public_key = self.generate_public_key()
        self.balance = 0

    def generate_public_key(self):
        return hashlib.sha256(self.private_key.encode()).hexdigest()

    def sign_transaction(self, transaction_data):
        return hashlib.sha256((self.private_key + json.dumps(transaction_data)).encode()).hexdigest()


class CryptoSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallets = {}

    def create_wallet(self):
        wallet = Wallet()
        self.wallets[wallet.public_key] = wallet
        return wallet.public_key

    def get_balance(self, public_key):
        balance = 0
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender == public_key:
                    balance -= tx.amount
                if tx.receiver == public_key:
                    balance += tx.amount
        return balance

    def create_transaction(self, sender, receiver, amount):
        if self.get_balance(sender) < amount:
            return False

        transaction = Transaction(sender, receiver, amount)
        self.blockchain.add_transaction(transaction)
        return True

    def mine_pending_transactions(self):
        return self.blockchain.mine()


if __name__ == "__main__":
    system = CryptoSystem()

    wallet1 = system.create_wallet()
    wallet2 = system.create_wallet()

    system.blockchain.add_transaction(Transaction("SYSTEM", wallet1, 100))
    system.mine_pending_transactions()

    system.create_transaction(wallet1, wallet2, 25)
    system.mine_pending_transactions()

    print("Wallet1 Balance:", system.get_balance(wallet1))
    print("Wallet2 Balance:", system.get_balance(wallet2))