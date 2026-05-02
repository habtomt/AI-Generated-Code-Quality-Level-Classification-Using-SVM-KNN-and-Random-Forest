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


class Identity:
    def __init__(self, name, email):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.verified = False
        self.identity_hash = self.compute_hash()

    def compute_hash(self):
        data = f"{self.user_id}{self.name}{self.email}"
        return hashlib.sha256(data.encode()).hexdigest()


class IdentitySystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.identities: Dict[str, Identity] = {}
        self.verifiers = set()

    def register_identity(self, name, email):
        identity = Identity(name, email)
        self.identities[identity.user_id] = identity

        self.blockchain.add_transaction(Transaction("REGISTER_IDENTITY", {
            "user_id": identity.user_id,
            "hash": identity.identity_hash
        }))
        return identity.user_id

    def add_verifier(self, verifier_id):
        self.verifiers.add(verifier_id)

    def verify_identity(self, verifier_id, user_id):
        if verifier_id not in self.verifiers:
            return False

        identity = self.identities.get(user_id)
        if not identity:
            return False

        identity.verified = True

        self.blockchain.add_transaction(Transaction("VERIFY_IDENTITY", {
            "user_id": user_id,
            "verifier": verifier_id
        }))
        return True

    def check_identity(self, user_id):
        identity = self.identities.get(user_id)
        if not identity:
            return False

        return identity.identity_hash == identity.compute_hash()

    def get_identity_status(self, user_id):
        identity = self.identities.get(user_id)
        if not identity:
            return None
        return {
            "verified": identity.verified,
            "hash_valid": self.check_identity(user_id)
        }

    def mine(self):
        return self.blockchain.mine()


if __name__ == "__main__":
    system = IdentitySystem()

    user_id = system.register_identity("Alice", "alice@example.com")

    verifier = "GOV_AUTHORITY"
    system.add_verifier(verifier)

    system.verify_identity(verifier, user_id)
    system.mine()

    status = system.get_identity_status(user_id)

    print("Identity Status:", status)
    print("Blockchain Length:", len(system.blockchain.chain))