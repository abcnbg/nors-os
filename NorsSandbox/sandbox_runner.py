#!/usr/bin/env python3
# NorsSandbox - Lightweight Malware Analysis Sandbox Manager
# License: GPLv3
import os
import sys
import subprocess
import time
import json

def create_sandbox(name):
    print(f"[*] Creating isolated Firejail sandbox container: {name}")
    config = f"""
    # NorsSandbox Profile
    net none
    private
    private-dev
    private-tmp
    noroot
    caps.drop all
    seccomp
    """
    profile_path = f"/tmp/{name}.profile"
    with open(profile_path, 'w') as f:
        f.write(config)
    print("[+] Profile created successfully.")
    return profile_path

def run_malware(binary_path, profile_path):
    if not os.path.exists(binary_path):
        print("[-] Binary not found.")
        return
        
    print(f"[*] Executing {binary_path} inside NorsSandbox with strace hooking...")
    
    # Run firejail, wrap with strace to log system calls made by malware
    log_file = f"/tmp/malware_strace_{int(time.time())}.log"
    cmd = [
        "firejail", f"--profile={profile_path}", "--quiet",
        "strace", "-o", log_file, "-f", "-e", "trace=network,file,process",
        binary_path
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[*] Waiting 15 seconds for behavioral analysis...")
        time.sleep(15)
        process.kill()
        print(f"[+] Process terminated. Analyzing logs in {log_file}...")
        
        analyze_logs(log_file)
    except Exception as e:
        print(f"[-] Sandbox execution error: {e}")

def analyze_logs(log_file):
    if not os.path.exists(log_file): return
    
    print("\n====== BEHAVIORAL ANALYSIS RESULTS ======")
    files_touched = set()
    processes_created = set()
    
    with open(log_file, 'r') as f:
        for line in f:
            if "openat" in line or "open" in line:
                parts = line.split('"')
                if len(parts) > 1:
                    files_touched.add(parts[1])
            elif "execve" in line:
                parts = line.split('"')
                if len(parts) > 1:
                    processes_created.add(parts[1])
                    
    print("\n[+] Files Modified/Accessed:")
    for file in list(files_touched)[:10]:
        print(f"  - {file}")
    
    print("\n[+] Processes Executed:")
    for proc in processes_created:
        print(f"  - {proc}")
    print("=========================================\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sandbox_runner.py <malware_executable>")
        sys.exit(1)
        
    print("🦅 NorsSandbox - Automated Dynamic Analysis")
    prof = create_sandbox("malware_test")
    run_malware(sys.argv[1], prof)
