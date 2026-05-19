#!/bin/bash
# NorsForensics - Automated Memory & Timeline Capture
# License: GPLv3
# Requires: lime, volatility3, sleuthkit

echo "🦅 NorsForensics - Live Response & Acquisition"

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root."
  exit 1
fi

DEST_DIR="/var/log/nors_forensics_$(date +%s)"
mkdir -p "$DEST_DIR"
echo "[*] Data will be saved to $DEST_DIR"

echo "[*] Collecting System Information..."
uname -a > "$DEST_DIR/system_info.txt"
uptime >> "$DEST_DIR/system_info.txt"
ps aux > "$DEST_DIR/process_list.txt"
netstat -tulpn > "$DEST_DIR/network_connections.txt"

echo "[*] Dumping Kernel Routing Table & ARP..."
route -n > "$DEST_DIR/routing_table.txt"
arp -a > "$DEST_DIR/arp_cache.txt"

echo "[*] Saving bash history of all users..."
for user_dir in /home/* /root; do
    if [ -f "$user_dir/.bash_history" ]; then
        cp "$user_dir/.bash_history" "$DEST_DIR/$(basename $user_dir)_bash_history.txt"
    fi
done

echo "[*] Warning: Memory acquisition requires LiME module."
echo "[*] Creating file system timeline (Requires Sleuthkit/mac-robber)..."
if command -v mac-robber &> /dev/null; then
    mac-robber / > "$DEST_DIR/fs_timeline.mactime"
    echo "[+] Timeline created."
else
    echo "[-] mac-robber not found, skipping timeline generation."
fi

echo "[+] Forensics acquisition complete."
tar -czf "$DEST_DIR.tar.gz" -C "$DEST_DIR" .
echo "[+] Archive saved as $DEST_DIR.tar.gz"
