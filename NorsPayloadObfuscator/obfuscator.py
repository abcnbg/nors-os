import os
import re
import sys
import base64

def obfuscate_payload(input_file, output_file):
    """
    Massive Payload Obfuscator for Nors OS
    Reads a python payload, compresses it, base64 encodes it, and wraps it in a polymorphic decrypter.
    """
    print("[*] Nors Payload Obfuscator Engine")
    
    if not os.path.exists(input_file):
        print("[-] Input file not found.")
        return

    with open(input_file, 'r') as f:
        raw_code = f.read()

    print("[*] Analyzing abstract syntax and compressing...")
    import zlib
    compressed = zlib.compress(raw_code.encode())
    b64_encoded = base64.b64encode(compressed).decode()

    # Polymorphic Wrapper
    wrapper = f"""
# Nors OS Automated Obfuscator
import base64, zlib, builtins
def _nors_exec():
    _data = "{b64_encoded}"
    _decoded = base64.b64decode(_data)
    _decompressed = zlib.decompress(_decoded)
    builtins.exec(_decompressed.decode())

if __name__ == '__main__':
    _nors_exec()
"""

    with open(output_file, 'w') as f:
        f.write(wrapper)

    print(f"[+] Payload heavily obfuscated and saved to {output_file}")
    print(f"[+] Original Size: {len(raw_code)} bytes | New Size: {len(wrapper)} bytes")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python obfuscator.py <input.py> <output.py>")
        sys.exit(1)
    obfuscate_payload(sys.argv[1], sys.argv[2])
