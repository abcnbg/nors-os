#!/bin/bash
# NorsReconAutomator - Massive Subdomain & Asset Discovery Pipeline
# License: GPLv3

DOMAIN=$1
if [ -z "$DOMAIN" ]; then
    echo "Usage: ./recon_pipeline.sh <domain.com>"
    exit 1
fi

OUT_DIR="nors_recon_$DOMAIN"
mkdir -p "$OUT_DIR"

echo "🦅 NorsReconAutomator - Target: $DOMAIN"

echo "[*] Step 1: Passive Subdomain Enumeration (Simulated Amass/Sublist3r)..."
# Simulated commands
sleep 2
echo "api.dev.$DOMAIN" > "$OUT_DIR/subdomains.txt"
echo "staging.$DOMAIN" >> "$OUT_DIR/subdomains.txt"
echo "vpn.$DOMAIN" >> "$OUT_DIR/subdomains.txt"
echo "[+] Found 3 subdomains."

echo "[*] Step 2: Resolving Active Hosts..."
sleep 1
cp "$OUT_DIR/subdomains.txt" "$OUT_DIR/alive_hosts.txt"

echo "[*] Step 3: Fast Port Scanning (Simulated Nmap/Masscan)..."
sleep 2
echo "[+] api.dev.$DOMAIN - Ports 80, 443, 8080 open" > "$OUT_DIR/ports.log"
echo "[+] vpn.$DOMAIN - Ports 443, 1194 open" >> "$OUT_DIR/ports.log"

echo "[*] Step 4: Web Screenshots (Simulated EyeWitness)..."
sleep 1
mkdir -p "$OUT_DIR/screenshots"
echo "[+] Screenshots captured."

echo "[+] Reconnaissance Pipeline Complete! Results stored in $OUT_DIR/"
