#!/bin/bash
# NORS OS - System Hardening Script
# License: GPLv3
# Description: Applies massive security hardening configurations to the local Linux system.

echo "[*] NORS OS System Hardening Utility"
echo "[*] Warning: This will modify critical system configurations."
sleep 2

# 1. Network Hardening (sysctl)
echo "[+] Hardening networking stack (sysctl.conf)..."
cat <<EOF | sudo tee -a /etc/sysctl.conf
# NORS Hardening
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.tcp_rfc1337 = 1
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.yama.ptrace_scope = 1
EOF
sudo sysctl -p

# 2. SSH Hardening
echo "[+] Securing SSH Server..."
if [ -f /etc/ssh/sshd_config ]; then
    sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
    sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
    sudo sed -i 's/X11Forwarding yes/X11Forwarding no/g' /etc/ssh/sshd_config
    sudo echo "AllowTcpForwarding no" >> /etc/ssh/sshd_config
    sudo systemctl restart sshd
fi

# 3. UFW Firewall Configuration
echo "[+] Configuring Uncomplicated Firewall (UFW)..."
sudo apt-get install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp # Allow SSH initially, user can modify
sudo ufw --force enable

# 4. Securing Shared Memory
echo "[+] Securing /dev/shm..."
echo "tmpfs /dev/shm tmpfs defaults,noexec,nosuid 0 0" | sudo tee -a /etc/fstab

# 5. Disable unused file systems
echo "[+] Disabling legacy filesystems..."
cat <<EOF | sudo tee /etc/modprobe.d/nors-fs.conf
install cramfs /bin/true
install freevxfs /bin/true
install jffs2 /bin/true
install hfs /bin/true
install hfsplus /bin/true
install squashfs /bin/true
install udf /bin/true
EOF

echo "[+] Hardening complete. Please reboot for all changes to take effect."
