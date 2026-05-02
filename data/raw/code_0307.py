"""
Auto-generated Python code
Scenario : Blockchain & Cryptocurrency
Prompt   : response_000.txt
Run      : 1
"""

# Import necessary libraries
from web3 import Web3
import json
import os
from cryptography.fernet import Fernet

# Set up Ethereum node connection (local or service like Infura)
def setup_ethereum_node(api_key):
    """Set up Ethereum node connection."""
    provider = Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{api_key}')
    web3 = Web3(provider)
    return web3

# Create a digital wallet
def create_wallet(web3):
    """Create a digital wallet."""
    account = web3.eth.account.create()
    return {
        'address': account.address,
        'private_key': account.private_key.hex()
    }

# Get the balance of a wallet
def get_balance(web3, address):
    """Get the balance of a wallet."""
    balance = web3.eth.get_balance(address)
    return web3.fromWei(balance, 'ether')

# Send a transaction
def send_transaction(web3, sender_private_key, to_address, amount):
    """Send a transaction."""
    sender_account = web3.eth.account.from_key(sender_private_key)
    nonce = web3.eth.getTransactionCount(sender_account.address)
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': web3.toWei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei('50', 'gwei')
    }

    signed_tx = web3.eth.account.sign_transaction(tx, sender_private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Encrypt private key
def encrypt_private_key(private_key):
    """Encrypt private key."""
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(private_key.encode())
    return key, cipher_text

# Decrypt private key
def decrypt_private_key(key, cipher_text):
    """Decrypt private key."""
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text.decode()

# Example usage
if __name__ == "__main__":
    # Set up Ethereum node connection
    api_key = 'YOUR_INFURA_API_KEY'
    web3 = setup_ethereum_node(api_key)

    # Create a digital wallet
    wallet = create_wallet(web3)
    print(f"New Wallet Address: {wallet['address']}")

    # Get the balance of the wallet
    balance = get_balance(web3, wallet['address'])
    print(f"Balance: {balance} ETH")

    # Encrypt private key
    key, cipher_text = encrypt_private_key(wallet['private_key'])
    print(f"Encrypted Private Key: {cipher_text}")

    # Decrypt private key
    decrypted_private_key = decrypt_private_key(key, cipher_text)
    print(f"Decrypted Private Key: {decrypted_private_key}")

    # Send a transaction
    try:
        # Note: Sending transaction requires real ETH; proceed with care!
        # tx_hash = send_transaction(web3, wallet['private_key'], 'recipient_address_here', 0.01)
        # print(f"Transaction sent with hash: {tx_hash}")
        pass
    except Exception as e:
        print(f"Error sending transaction: {e}")