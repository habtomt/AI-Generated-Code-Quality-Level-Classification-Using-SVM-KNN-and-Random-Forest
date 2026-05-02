import hashlib
import json
import time
import binascii
from typing import List, Dict, Any

class CryptoWallet:
    def __init__(self, owner: str):
        self.owner = owner
        # Simulating key generation using SHA256 of the owner's name
        self.private_key = binascii.hexlify(hashlib.sha256(owner.encode()).digest()).decode()
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()
        self.balance = 0.0

    def sign_transaction(self, recipient_pub_key: str, amount: float) -> str:
        transaction_data = f"{self.public_key}{recipient_pub_key}{amount}{time.time()}"
        signature = hashlib.sha256((transaction_data + self.private_key).encode()).hexdigest()
        return signature

class Transaction:
    def __init__(self, sender_pub_key: str, recipient_pub_key: str, amount: float, signature: str):
        self.sender_pub_key = sender_pub_key
        self.recipient_pub_key = recipient_pub_key
        self.amount = amount
        self.signature = signature
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender_pub_key,
            "recipient": self.recipient_pub_key,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = [tx.to_dict() for tx in transactions]
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions: List[Transaction] = []
        self.wallets: Dict[str, CryptoWallet] = {}

    def create_genesis_block(self) -> Block:
        return Block(0, [], "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def register_wallet(self, owner: str) -> CryptoWallet:
        wallet = CryptoWallet(owner)
        self.wallets[wallet.public_key] = wallet
        return wallet

    def add_transaction(self, sender_wallet: CryptoWallet, recipient_pub_key: str, amount: float) -> bool:
        if sender_wallet.balance < amount:
            print(f"Transaction failed: Insufficient funds for {sender_wallet.owner}")
            return False

        signature = sender_wallet.sign_transaction(recipient_pub_key, amount)
        new_tx = Transaction(sender_wallet.public_key, recipient_pub_key, amount, signature)
        
        self.pending_transactions.append(new_tx)
        return True

    def process_pending_transactions(self, miner_address: str):
        new_block = Block(len(self.chain), self.pending_transactions, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        
        print(f"Block successfully mined! Hash: {new_block.hash}")
        self.chain.append(new_block)

        # Update balances based on transactions in the block
        for tx in self.pending_transactions:
            if tx.sender_pub_key in self.wallets:
                self.wallets[tx.sender_pub_key].balance -= tx.amount
            if tx.recipient_pub_key in self.wallets:
                self.wallets[tx.recipient_pub_key].balance += tx.amount

        self.pending_transactions = []

# Usage Example
if __name__ == "__main__":
    network = Blockchain()

    # Create Wallets
    alice = network.register_wallet("Alice")
    bob = network.register_wallet("Bob")

    # Fund Alice for demonstration
    alice.balance = 500.0
    print(f"Initial State -> Alice: {alice.balance}, Bob: {bob.balance}")

    # Process Payment
    print("\nExecuting transaction...")
    if network.add_transaction(alice, bob.public_key, 150.0):
        network.process_pending_transactions("Miner-Node-1")

    print(f"Final State -> Alice: {alice.balance}, Bob: {bob.balance}")