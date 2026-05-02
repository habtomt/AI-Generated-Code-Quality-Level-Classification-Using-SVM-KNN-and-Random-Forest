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
        self.address = hashlib.sha256(self.private_key.encode()).hexdigest()


class NFT:
    def __init__(self, creator, metadata):
        self.token_id = str(uuid.uuid4())
        self.creator = creator
        self.owner = creator
        self.metadata = metadata
        self.hash = self.compute_hash()

    def compute_hash(self):
        data = f"{self.token_id}{self.creator}{self.metadata}"
        return hashlib.sha256(data.encode()).hexdigest()


class Marketplace:
    def __init__(self):
        self.blockchain = Blockchain()
        self.wallets: Dict[str, Wallet] = {}
        self.balances: Dict[str, float] = {}
        self.nfts: Dict[str, NFT] = {}
        self.listings: Dict[str, Dict] = {}

    def create_wallet(self):
        wallet = Wallet()
        self.wallets[wallet.address] = wallet
        self.balances[wallet.address] = 0.0
        return wallet.address

    def deposit(self, address, amount):
        self.balances[address] += amount
        self.blockchain.add_transaction(Transaction("DEPOSIT", {"address": address, "amount": amount}))

    def mint_nft(self, creator, metadata):
        nft = NFT(creator, metadata)
        self.nfts[nft.token_id] = nft
        self.blockchain.add_transaction(Transaction("MINT", {
            "token_id": nft.token_id,
            "creator": creator,
            "metadata": metadata
        }))
        return nft.token_id

    def list_nft(self, owner, token_id, price):
        nft = self.nfts.get(token_id)
        if not nft or nft.owner != owner:
            return False

        self.listings[token_id] = {
            "owner": owner,
            "price": price
        }

        self.blockchain.add_transaction(Transaction("LIST", {
            "token_id": token_id,
            "price": price
        }))
        return True

    def buy_nft(self, buyer, token_id):
        listing = self.listings.get(token_id)
        nft = self.nfts.get(token_id)

        if not listing or not nft:
            return False

        price = listing["price"]
        seller = listing["owner"]

        if self.balances.get(buyer, 0) < price:
            return False

        self.balances[buyer] -= price
        self.balances[seller] += price

        nft.owner = buyer
        del self.listings[token_id]

        self.blockchain.add_transaction(Transaction("BUY", {
            "token_id": token_id,
            "from": seller,
            "to": buyer,
            "price": price
        }))
        return True

    def transfer_nft(self, sender, receiver, token_id):
        nft = self.nfts.get(token_id)
        if not nft or nft.owner != sender:
            return False

        nft.owner = receiver

        self.blockchain.add_transaction(Transaction("TRANSFER_NFT", {
            "token_id": token_id,
            "from": sender,
            "to": receiver
        }))
        return True

    def verify_nft(self, token_id):
        nft = self.nfts.get(token_id)
        if not nft:
            return False
        return nft.hash == nft.compute_hash()

    def mine(self):
        return self.blockchain.mine()


if __name__ == "__main__":
    market = Marketplace()

    user1 = market.create_wallet()
    user2 = market.create_wallet()

    market.deposit(user1, 1000)
    market.deposit(user2, 500)

    token_id = market.mint_nft(user1, {"name": "Digital Art", "rarity": "Unique"})

    market.list_nft(user1, token_id, 300)
    market.buy_nft(user2, token_id)

    market.transfer_nft(user2, user1, token_id)

    market.mine()

    print("Balances:", market.balances)
    print("NFT Owner:", market.nfts[token_id].owner)
    print("NFT Verified:", market.verify_nft(token_id))