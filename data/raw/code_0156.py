import hashlib

class IdentitySystem:
    def __init__(self):
        self.registry = {} # {public_address: hashed_identity}

    def _hash_data(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def register_identity(self, user_address, full_name, id_number):
        # Only store the hash to ensure privacy
        identity_hash = self._hash_data(f"{full_name}{id_number}")
        self.registry[user_address] = identity_hash
        print(f"Identity registered for address {user_address}")

    def verify_identity(self, user_address, full_name, id_number):
        if user_address not in self.registry:
            return False
        
        check_hash = self._hash_data(f"{full_name}{id_number}")
        is_valid = self.registry[user_address] == check_hash
        print(f"Verification for {user_address}: {'SUCCESS' if is_valid else 'FAILED'}")
        return is_valid

# Execution
ids = IdentitySystem()
user_wallet = "0xABC123"

# Registration
ids.register_identity(user_wallet, "John Doe", "123456789")

# Verification attempts
ids.verify_identity(user_wallet, "John Doe", "123456789") # Correct
ids.verify_identity(user_wallet, "John Doe", "000000000") # Incorrect