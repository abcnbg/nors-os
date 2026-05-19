#!/usr/bin/env python3
# NorsDeobfuscator - Automated JS & PS1 Code Deobfuscator
# License: GPLv3
import sys
import re

def deobfuscate_powershell(code):
    print("[*] Attempting PowerShell Deobfuscation...")
    # Remove backticks used for obfuscation (e.g., e`c`h`o -> echo)
    cleaned = code.replace("`", "")
    
    # Simple base64 detection
    if "-enc" in cleaned.lower() or "-encodedcommand" in cleaned.lower():
        print("[!] Detected Base64 Encoded Payload.")
        try:
            import base64
            parts = cleaned.split()
            for i, p in enumerate(parts):
                if p.lower() in ["-enc", "-encodedcommand"] and i + 1 < len(parts):
                    decoded = base64.b64decode(parts[i+1]).decode('utf-16le')
                    print(f"[+] Decoded Payload:\n{decoded}")
        except Exception as e:
            print("[-] Base64 decoding failed.")
            
    return cleaned

def deobfuscate_js(code):
    print("[*] Attempting JavaScript Deobfuscation...")
    # Extremely basic unescaping (real deobfuscation requires AST parsing)
    import urllib.parse
    cleaned = urllib.parse.unquote(code)
    
    # Hex decoding
    cleaned = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), cleaned)
    return cleaned

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python js_ps_deobfuscator.py <type: ps/js> <file>")
        sys.exit(1)
        
    lang = sys.argv[1].lower()
    file_path = sys.argv[2]
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
            
        if lang == "ps":
            res = deobfuscate_powershell(code)
            print("\n--- Cleaned Code ---\n" + res)
        elif lang == "js":
            res = deobfuscate_js(code)
            print("\n--- Cleaned Code ---\n" + res)
        else:
            print("[-] Unsupported type. Use 'ps' or 'js'.")
    except Exception as e:
        print(f"[-] Error reading file: {e}")
