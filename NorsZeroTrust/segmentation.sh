#!/bin/bash
# NorsZeroTrust - Micro-segmentation & Lockdown Script
# License: GPLv3
# Description: Instantly drops all network traffic and enforces a strict whitelist policy.

echo "🦅 NorsZeroTrust - Network Lockdown Enforcer"

if [ "$EUID" -ne 0 ]; then
  echo "[-] Must run as root."
  exit 1
fi

echo "[!] WARNING: This will drop ALL inbound and outbound connections not explicitly whitelisted."
read -p "Are you sure you want to activate Zero Trust Mode? (y/n): " confirm

if [[ "$confirm" != "y" ]]; then
    echo "Aborted."
    exit 0
fi

echo "[*] Flushing existing iptables rules..."
iptables -F
iptables -X

echo "[*] Setting default DROP policies..."
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

echo "[*] Allowing loopback (localhost) traffic..."
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

echo "[*] Allowing established and related connections..."
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Example: Whitelist specific essential services
echo "[*] Whitelisting DNS (UDP 53)..."
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT

echo "[*] Whitelisting Nors C2 Communications (TCP 8443)..."
iptables -A OUTPUT -p tcp --dport 8443 -j ACCEPT
iptables -A INPUT -p tcp --dport 8443 -j ACCEPT

# Drop invalid packets
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

echo "[+] Zero Trust policy enforced. System is dark to unauthorized traffic."
iptables -L -v -n
