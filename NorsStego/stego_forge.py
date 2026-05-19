#!/usr/bin/env python3
# NorsStego - Payload Hiding via LSB Steganography
# License: GPLv3
import sys
import argparse
from PIL import Image

def embed_payload(image_path, payload_path, output_path):
    print(f"[*] Embedding {payload_path} into {image_path}...")
    try:
        img = Image.open(image_path).convert("RGB")
        with open(payload_path, "rb") as f:
            payload = f.read()
            
        payload += b"<NORS_EOF>" # delimiter
        
        # Convert payload to binary string
        binary_payload = ''.join([format(byte, '08b') for byte in payload])
        data_len = len(binary_payload)
        
        pixels = list(img.getdata())
        new_pixels = []
        
        data_idx = 0
        for pixel in pixels:
            r, g, b = pixel
            if data_idx < data_len:
                r = (r & 254) | int(binary_payload[data_idx])
                data_idx += 1
            if data_idx < data_len:
                g = (g & 254) | int(binary_payload[data_idx])
                data_idx += 1
            if data_idx < data_len:
                b = (b & 254) | int(binary_payload[data_idx])
                data_idx += 1
            new_pixels.append((r, g, b))
            
        new_img = Image.new("RGB", img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_path, format="PNG")
        print(f"[+] Successfully saved stego image to {output_path}")
        
    except Exception as e:
        print(f"[-] Error: {e}")

def extract_payload(image_path, output_path):
    print(f"[*] Extracting payload from {image_path}...")
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())
        
        binary_data = ""
        for r, g, b in pixels:
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
            
        # Group by 8 bits
        bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        extracted = bytearray()
        for b in bytes_data:
            if len(b) == 8:
                extracted.append(int(b, 2))
                
        # Look for delimiter
        delimiter = b"<NORS_EOF>"
        idx = extracted.find(delimiter)
        if idx != -1:
            payload = extracted[:idx]
            with open(output_path, "wb") as f:
                f.write(payload)
            print(f"[+] Successfully extracted payload to {output_path}")
        else:
            print("[-] No payload found or delimiter missing.")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NorsStego - LSB Image Steganography")
    parser.add_argument("mode", choices=["embed", "extract"])
    parser.add_argument("-i", "--image", required=True, help="Target image (PNG recommended)")
    parser.add_argument("-p", "--payload", help="Payload file to embed")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    
    args = parser.parse_args()
    if args.mode == "embed":
        if not args.payload:
            print("[-] Payload required for embedding.")
            sys.exit(1)
        embed_payload(args.image, args.payload, args.output)
    elif args.mode == "extract":
        extract_payload(args.image, args.output)
