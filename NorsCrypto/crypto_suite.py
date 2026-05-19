#!/usr/bin/env python3
# NorsCrypto - Universal Cryptography & Hash Utility
# License: GPLv3
import hashlib
import base64
import argparse
from cryptography.fernet import Fernet
import rsa

class NorsCrypto:
    @staticmethod
    def identify_hash(hash_str):
        print(f"[*] Analyzing hash: {hash_str}")
        length = len(hash_str)
        if length == 32: return "MD5"
        if length == 40: return "SHA-1"
        if length == 64: return "SHA-256"
        if length == 128: return "SHA-512"
        if hash_str.startswith("$2"): return "Bcrypt"
        return "Unknown"

    @staticmethod
    def generate_hashes(text):
        print(f"[*] Generating hashes for: {text}")
        data = text.encode()
        print(f"  MD5:     {hashlib.md5(data).hexdigest()}")
        print(f"  SHA-1:   {hashlib.sha1(data).hexdigest()}")
        print(f"  SHA-256: {hashlib.sha256(data).hexdigest()}")
        print(f"  SHA-512: {hashlib.sha512(data).hexdigest()}")
        print(f"  Base64:  {base64.b64encode(data).decode()}")

    @staticmethod
    def symmetric_encrypt(text, key=None):
        if not key:
            key = Fernet.generate_key()
            print(f"[!] Generated new Symmetric Key: {key.decode()}")
        f = Fernet(key)
        encrypted = f.encrypt(text.encode())
        print(f"[+] Encrypted Data: {encrypted.decode()}")

    @staticmethod
    def asymmetric_generate():
        print("[*] Generating RSA Keypair (2048-bit)...")
        pubkey, privkey = rsa.newkeys(2048)
        print("\n--- PUBLIC KEY ---")
        print(pubkey.save_pkcs1().decode())
        print("--- PRIVATE KEY ---")
        print(privkey.save_pkcs1().decode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🦅 NorsCrypto - Cryptography Suite")
    subparsers = parser.add_subparsers(dest="command")
    
    id_parser = subparsers.add_parser("identify", help="Identify a hash type")
    id_parser.add_argument("hash", type=str)
    
    hash_parser = subparsers.add_parser("hash", help="Generate multiple hashes for a string")
    hash_parser.add_argument("text", type=str)
    
    enc_parser = subparsers.add_parser("encrypt", help="Symmetric encryption (Fernet)")
    enc_parser.add_argument("text", type=str)
    enc_parser.add_argument("--key", type=str, help="Optional encryption key")
    
    rsa_parser = subparsers.add_parser("rsa", help="Generate RSA Keypair")
    
    args = parser.parse_args()
    
    if args.command == "identify":
        print(f"[+] Probable Hash Type: {NorsCrypto.identify_hash(args.hash)}")
    elif args.command == "hash":
        NorsCrypto.generate_hashes(args.text)
    elif args.command == "encrypt":
        NorsCrypto.symmetric_encrypt(args.text, args.key.encode() if args.key else None)
    elif args.command == "rsa":
        NorsCrypto.asymmetric_generate()
    else:
        parser.print_help()
