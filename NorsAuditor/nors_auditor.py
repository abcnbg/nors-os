#!/usr/bin/env python3
# NorsAuditor - Static Application Security Testing (SAST) Scanner
# License: GPLv3
# Description: Scans source code directories for hardcoded secrets and dangerous patterns.

import os
import re
import sys

# Threat signatures
SIGNATURES = {
    "Hardcoded AWS Key": r"(?i)AKIA[0-9A-Z]{16}",
    "Hardcoded Password": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^\s]+['\"]",
    "Private Key": r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----",
    "Dangerous Function (C/C++)": r"\b(strcpy|sprintf|gets|system)\s*\(",
    "Dangerous Function (PHP)": r"\b(eval|exec|shell_exec|passthru|system)\s*\(",
    "SQL Injection Vector": r"SELECT\s+.*?\s+FROM\s+.*?\s+WHERE\s+.*?=\s*['\"].*\+.*"
}

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line_no, line in enumerate(lines, 1):
                for sig_name, pattern in SIGNATURES.items():
                    if re.search(pattern, line):
                        findings.append((line_no, sig_name, line.strip()))
    except Exception as e:
        pass
    return findings

def audit_directory(target_dir):
    print(f"[*] NorsAuditor - SAST Scanning: {target_dir}")
    print("[*] Checking for secrets and dangerous patterns...\n")
    
    total_findings = 0
    scanned_files = 0
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            # Skip hidden files and binaries
            if file.startswith('.') or file.endswith(('.exe', '.dll', '.so', '.iso', '.zip')):
                continue
                
            filepath = os.path.join(root, file)
            scanned_files += 1
            
            findings = scan_file(filepath)
            if findings:
                print(f"[\033[91m!\033[0m] VULNERABILITIES IN: {filepath}")
                for line_no, sig, context in findings:
                    print(f"  Line {line_no:4d} | \033[93m{sig}\033[0m | {context[:80]}")
                    total_findings += 1
                print("-" * 60)

    print(f"\n[*] Audit Complete. Scanned {scanned_files} files. Found {total_findings} potential issues.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nors_auditor.py <directory_to_scan>")
        sys.exit(1)
    
    target = sys.argv[1]
    if os.path.isdir(target):
        audit_directory(target)
    else:
        print("[-] Target must be a directory.")
