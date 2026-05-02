import hashlib
import time
import json

class SupplyChainBlock:
    def __init__(self, index, product_id, product_name, status, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.product_id = product_id
        self.product_name = product_name
        self.status = status
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.product_id}{self.status}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

class SupplyChainManager:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.statuses = ["Manufactured", "In Transit", "Delivered"]

    def create_genesis_block(self):
        return SupplyChainBlock(0, "0", "Genesis Product", "None", "0")

    def update_product_status(self, product_id, product_name, status_index):
        if status_index >= len(self.statuses): return
        
        prev_block = self.chain[-1]
        new_block = SupplyChainBlock(
            len(self.chain), 
            product_id, 
            product_name, 
            self.statuses[status_index], 
            prev_block.hash
        )
        self.chain.append(new_block)
        print(f"Update: Product {product_id} is now {self.statuses[status_index]}")

    def verify_authenticity(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True

# Execution
scm = SupplyChainManager()
scm.update_product_status("P101", "Smartphone", 0)
scm.update_product_status("P101", "Smartphone", 1)
scm.update_product_status("P101", "Smartphone", 2)

print(f"Chain Valid: {scm.verify_authenticity()}")