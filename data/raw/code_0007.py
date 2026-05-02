import hashlib
import time
import uuid
from typing import List, Dict


class Product:
    def __init__(self, name, origin):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.origin = origin
        self.history = []
        self.add_event("CREATED", origin)

    def add_event(self, status, location):
        event = {
            "status": status,
            "location": location,
            "timestamp": time.time()
        }
        self.history.append(event)

    def get_hash(self):
        data = f"{self.product_id}{self.name}{self.origin}{self.history}"
        return hashlib.sha256(data.encode()).hexdigest()


class Transaction:
    def __init__(self, product_id, action, actor):
        self.tx_id = str(uuid.uuid4())
        self.product_id = product_id
        self.action = action
        self.actor = actor
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "tx_id": self.tx_id,
            "product_id": self.product_id,
            "action": self.action,
            "actor": self.actor,
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
        data = str(self.index) + str([tx.to_dict() for tx in self.transactions]) + self.previous_hash + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()


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

    def add_transaction(self, tx: Transaction):
        self.pending_transactions.append(tx)

    def proof_of_work(self, block: Block):
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


class SmartContract:
    def __init__(self, contract_id, conditions: Dict, actions: Dict):
        self.contract_id = contract_id
        self.conditions = conditions
        self.actions = actions
        self.is_executed = False

    def evaluate(self, context: Dict):
        for key, value in self.conditions.items():
            if context.get(key) != value:
                return False
        return True

    def execute(self, context: Dict):
        if self.is_executed:
            return None
        if not self.evaluate(context):
            return None

        self.is_executed = True
        return self.actions


class SupplyChainSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.products: Dict[str, Product] = {}
        self.contracts: Dict[str, SmartContract] = {}

    def create_product(self, name, origin):
        product = Product(name, origin)
        self.products[product.product_id] = product
        self.blockchain.add_transaction(Transaction(product.product_id, "CREATE_PRODUCT", origin))
        return product.product_id

    def transfer_product(self, product_id, new_location):
        product = self.products.get(product_id)
        if not product:
            return False

        product.add_event("TRANSFER", new_location)
        self.blockchain.add_transaction(Transaction(product_id, "TRANSFER", new_location))
        self.evaluate_contracts(product_id, new_location)
        return True

    def verify_product(self, product_id):
        product = self.products.get(product_id)
        if not product:
            return False

        original_hash = product.get_hash()
        recalculated_hash = product.get_hash()
        return original_hash == recalculated_hash

    def create_contract(self, conditions: Dict, actions: Dict):
        contract_id = str(uuid.uuid4())
        contract = SmartContract(contract_id, conditions, actions)
        self.contracts[contract_id] = contract
        return contract_id

    def evaluate_contracts(self, product_id, location):
        context = {
            "product_id": product_id,
            "location": location
        }

        for contract in self.contracts.values():
            result = contract.execute(context)
            if result:
                action = result.get("action")
                if action == "MARK_DELIVERED":
                    self.products[product_id].add_event("DELIVERED", location)
                    self.blockchain.add_transaction(Transaction(product_id, "DELIVERED", location))

    def mine(self):
        return self.blockchain.mine()


if __name__ == "__main__":
    system = SupplyChainSystem()

    product_id = system.create_product("Laptop", "Factory A")

    contract_id = system.create_contract(
        conditions={"location": "Warehouse B"},
        actions={"action": "MARK_DELIVERED"}
    )

    system.transfer_product(product_id, "Warehouse B")
    system.mine()

    print("Product Verified:", system.verify_product(product_id))
    print("Product History:", system.products[product_id].history)