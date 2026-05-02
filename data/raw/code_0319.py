"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
import hashlib
import time
from typing import Dict, List
import json
from flask import Flask, jsonify, request

# Initialize the Flask app
app = Flask(__name__)

# Define a class for the blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the genesis block
        genesis_block = {
            'index': 1,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'hash': self.hash_block('0', [])
        }
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Dict:
        # Get the latest block in the chain
        return self.chain[-1]

    def add_transaction(self, sender: str, receiver: str, amount: float) -> None:
        # Add a new transaction to the list of transactions
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})

    def hash_block(self, previous_hash: str, transactions: List) -> str:
        # Hash the block using SHA-256
        block_string = json.dumps({'previous_hash': previous_hash, 'transactions': transactions}, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, previous_hash: str, transactions: List) -> str:
        # Perform proof of work to validate the block
        nonce = 0
        while True:
            block_string = json.dumps({'previous_hash': previous_hash, 'transactions': transactions, 'nonce': nonce}, sort_keys=True)
            hash_value = hashlib.sha256(block_string.encode()).hexdigest()
            if hash_value.startswith('0000'):
                return nonce
            nonce += 1

    def add_block(self) -> None:
        # Add a new block to the chain
        previous_block = self.get_latest_block()
        previous_hash = previous_block['hash']
        transactions_copy = self.transactions.copy()
        self.transactions.clear()  # Clear the transactions list
        nonce = self.proof_of_work(previous_hash, transactions_copy)
        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': transactions_copy,
            'previous_hash': previous_hash,
            'hash': self.hash_block(previous_hash, transactions_copy),
            'nonce': nonce
        }
        self.chain.append(new_block)

# Create a new blockchain
blockchain = Blockchain()

# Define a class for the user
class User:
    def __init__(self, name: str, balance: float = 0.0):
        self.name = name
        self.balance = balance

    def deposit(self, amount: float) -> None:
        # Deposit money into the user's account
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        # Withdraw money from the user's account
        if amount > self.balance:
            raise ValueError('Insufficient balance')
        self.balance -= amount

# Define a class for the lending platform
class LendingPlatform:
    def __init__(self):
        self.users = {}

    def create_user(self, name: str) -> User:
        # Create a new user
        user = User(name)
        self.users[name] = user
        return user

    def lend(self, lender: str, borrower: str, amount: float) -> None:
        # Lend money from one user to another
        lender_user = self.users[lender]
        borrower_user = self.users[borrower]
        if lender_user.balance < amount:
            raise ValueError('Lender has insufficient balance')
        lender_user.withdraw(amount)
        borrower_user.deposit(amount)

    def trade(self, seller: str, buyer: str, asset: str, price: float) -> None:
        # Trade an asset between two users
        seller_user = self.users[seller]
        buyer_user = self.users[buyer]
        if seller_user.balance < price:
            raise ValueError('Seller has insufficient balance')
        seller_user.withdraw(price)
        buyer_user.deposit(price)

# Create a new lending platform
lending_platform = LendingPlatform()

# Define routes for the Flask app
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    user = lending_platform.create_user(name)
    return jsonify({'name': user.name, 'balance': user.balance})

@app.route('/lend', methods=['POST'])
def lend():
    data = request.get_json()
    lender = data['lender']
    borrower = data['borrower']
    amount = data['amount']
    lending_platform.lend(lender, borrower, amount)
    blockchain.add_transaction(lender, borrower, amount)
    blockchain.add_block()
    return jsonify({'message': 'Lending successful'})

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()
    seller = data['seller']
    buyer = data['buyer']
    asset = data['asset']
    price = data['price']
    lending_platform.trade(seller, buyer, asset, price)
    blockchain.add_transaction(seller, buyer, price)
    blockchain.add_block()
    return jsonify({'message': 'Trading successful'})

if __name__ == '__main__':
    app.run(debug=True)