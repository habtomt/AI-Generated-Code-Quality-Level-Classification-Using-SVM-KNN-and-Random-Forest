#!/usr/bin/env python3

import os
import sys
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()


def get_cipher():
    key = load_key()
    return Fernet(key)


def encrypt_file(file_path):
    cipher = get_cipher()

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = cipher.encrypt(data)

    out_path = file_path + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted)

    print(f"Encrypted: {out_path}")


def decrypt_file(file_path):
    cipher = get_cipher()

    with open(file_path, "rb") as f:
        data = f.read()

    decrypted = cipher.decrypt(data)

    out_path = file_path.replace(".enc", ".dec")
    with open(out_path, "wb") as f:
        f.write(decrypted)

    print(f"Decrypted: {out_path}")


def send_file(file_path):
    cipher = get_cipher()

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = cipher.encrypt(data)

    packet_path = "transit_packet.bin"
    with open(packet_path, "wb") as f:
        f.write(encrypted)

    print(f"File encrypted for transit: {packet_path}")


def receive_file(packet_path):
    cipher = get_cipher()

    with open(packet_path, "rb") as f:
        data = f.read()

    decrypted = cipher.decrypt(data)

    out_path = "received_file"
    with open(out_path, "wb") as f:
        f.write(decrypted)

    print(f"File received and decrypted: {out_path}")


def menu():
    print("""
Commands:
  genkey
  encrypt <file>
  decrypt <file.enc>
  send <file>
  receive <packet>
  exit
""")


def main():
    menu()

    while True:
        cmd = input("> ").strip().split()

        if not cmd:
            continue

        action = cmd[0]

        if action == "exit":
            break

        elif action == "genkey":
            generate_key()
            print("Key generated")

        elif action == "encrypt" and len(cmd) == 2:
            encrypt_file(cmd[1])

        elif action == "decrypt" and len(cmd) == 2:
            decrypt_file(cmd[1])

        elif action == "send" and len(cmd) == 2:
            send_file(cmd[1])

        elif action == "receive" and len(cmd) == 2:
            receive_file(cmd[1])

        else:
            print("Invalid command")


if __name__ == "__main__":
    main()