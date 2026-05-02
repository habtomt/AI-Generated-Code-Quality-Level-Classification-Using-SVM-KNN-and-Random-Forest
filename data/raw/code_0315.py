"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_003.txt
Run      : 2
"""

# Importing required libraries
import hashlib
import json
import time
from typing import Dict, List
from uuid import uuid4

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self) -> Dict:
        """
        Create the genesis block
        """
        return {
            'index': 1,
            'timestamp': time.time(),
            'previous_hash': '0',
            'hash': self.calculate_hash(1, '0', time.time())
        }

    def calculate_hash(self, index: int, previous_hash: str, timestamp: float) -> str:
        """
        Calculate the hash of a block
        """
        return hashlib.sha256(f'{index}{previous_hash}{timestamp}'.encode()).hexdigest()

    def get_latest_block(self) -> Dict:
        """
        Get the latest block in the chain
        """
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float) -> None:
        """
        Add a transaction to the pending transactions list
        """
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)

    def mine_block(self, miner: str) -> None:
        """
        Mine a new block and add it to the chain
        """
        if not self.pending_transactions:
            raise Exception('No pending transactions')

        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'previous_hash': self.get_latest_block()['hash'],
            'transactions': self.pending_transactions,
            'miner': miner,
            'reward': self.mining_reward
        }

        new_block['hash'] = self.calculate_hash(
            len(self.chain) + 1,
            self.get_latest_block()['hash'],
            time.time()
        )

        self.chain.append(new_block)
        self.pending_transactions = []

    def verify_chain(self) -> bool:
        """
        Verify the integrity of the chain
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block['hash'] != self.calculate_hash(
                current_block['index'],
                previous_block['hash'],
                current_block['timestamp']
            ):
                return False
        return True


class NFT:
    def __init__(self, name: str, description: str, owner: str):
        self.name = name
        self.description = description
        self.owner = owner
        self.token_id = str(uuid4())

    def mint(self, blockchain: Blockchain, owner: str) -> None:
        """
        Mint a new NFT
        """
        blockchain.add_transaction(self.owner, owner, 0)
        blockchain.mine_block('Miner')
        self.owner = owner

    def transfer(self, blockchain: Blockchain, new_owner: str) -> None:
        """
        Transfer ownership of the NFT
        """
        blockchain.add_transaction(self.owner, new_owner, 0)
        blockchain.mine_block('Miner')
        self.owner = new_owner


class Marketplace:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.nfts = {}

    def add_nft(self, nft: NFT) -> None:
        """
        Add a new NFT to the marketplace
        """
        self.nfts[nft.token_id] = nft

    def buy_nft(self, token_id: str, buyer: str) -> None:
        """
        Buy an NFT
        """
        if token_id not in self.nfts:
            raise Exception('NFT not found')

        nft = self.nfts[token_id]
        if nft.owner == buyer:
            raise Exception('You already own this NFT')

        nft.transfer(self.blockchain, buyer)

    def sell_nft(self, token_id: str, seller: str, price: float) -> None:
        """
        Sell an NFT
        """
        if token_id not in self.nfts:
            raise Exception('NFT not found')

        nft = self.nfts[token_id]
        if nft.owner != seller:
            raise Exception('You do not own this NFT')

        # Simulate a transaction
        self.blockchain.add_transaction(seller, 'Marketplace', price)
        self.blockchain.mine_block('Miner')


# Create a blockchain
blockchain = Blockchain()

# Create a marketplace
marketplace = Marketplace(blockchain)

# Create some NFTs
nft1 = NFT('NFT 1', 'This is NFT 1', 'Owner 1')
nft2 = NFT('NFT 2', 'This is NFT 2', 'Owner 2')

# Add NFTs to the marketplace
marketplace.add_nft(nft1)
marketplace.add_nft(nft2)

# Mint NFTs
nft1.mint(blockchain, 'Owner 1')
nft2.mint(blockchain, 'Owner 2')

# Sell NFTs
marketplace.sell_nft(nft1.token_id, 'Owner 1', 10.0)
marketplace.sell_nft(nft2.token_id, 'Owner 2', 20.0)

# Buy NFTs
marketplace.buy_nft(nft1.token_id, 'Buyer 1')
marketplace.buy_nft(nft2.token_id, 'Buyer 2')

# Verify the chain
print(blockchain.verify_chain())