"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import hashlib
import hmac
import json
import base64

# Create a new RSA key pair
def create_key_pair():
    try:
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return key
    except Exception as e:
        print(f"Error creating key pair: {e}")

# Create a new EC key pair
def create_ec_key_pair():
    try:
        key = ec.generate_private_key(
            ec.SECP256R1(),
            default_backend()
        )
        return key
    except Exception as e:
        print(f"Error creating EC key pair: {e}")

# Get the private key as PEM
def get_private_key_pem(key):
    try:
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    except Exception as e:
        print(f"Error getting private key as PEM: {e}")

# Get the public key as PEM
def get_public_key_pem(key):
    try:
        return key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    except Exception as e:
        print(f"Error getting public key as PEM: {e}")

# Create a new blockchain node
class BlockchainNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.chain = []
        self.transactions = []

    def get_latest_block(self):
        return self.chain[-1] if self.chain else None

    def add_block(self, block):
        self.chain.append(block)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

# Create a new block
class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data
        }).encode()).hexdigest()

# Create a new transaction
class Transaction:
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.signature = self.sign_transaction()

    def sign_transaction(self):
        # Using ECDSA signature scheme
        key = create_ec_key_pair()
        signature = key.sign(
            json.dumps({
                'sender': self.sender,
                'receiver': self.receiver,
                'amount': self.amount,
                'timestamp': self.timestamp
            }).encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature)

# Main function
def main():
    # Create a new blockchain node
    node = BlockchainNode('Node 1')

    # Create a new key pair
    key = create_key_pair()

    # Get the private key as PEM
    private_key_pem = get_private_key_pem(key)

    # Get the public key as PEM
    public_key_pem = get_public_key_pem(key)

    # Create a new transaction
    transaction = Transaction('Alice', 'Bob', 10.0, '2024-03-16 10:30:00')

    # Add the transaction to the blockchain node
    node.add_transaction(transaction)

    # Create a new block
    block = Block(0, '0', '2024-03-16 10:30:00', {
        'transactions': [transaction]
    })

    # Add the block to the blockchain node
    node.add_block(block)

    # Print the blockchain node data
    print(json.dumps({
        'node_id': node.node_id,
        'chain': node.chain,
        'transactions': node.transactions
    }, indent=4))

if __name__ == "__main__":
    main()