# 🦅 NORS OS

NORS OS is a specialized Linux distribution for Penetration Testing and Reverse Engineering, combining the power of Kali Linux tools with the elegance of a custom Windows 11-like UI via KDE Plasma.

## 🌟 Features
- **NorsDream UI**: A custom, glassmorphism-inspired theme for KDE Plasma.
- **800+ Pre-installed Tools**: The best of info-sec, pre-categorized.
- **Native Windows App Support**: Pre-configured Wine & Bottles environment for tools like IDA Pro and Burp Suite Pro.
- **Nors Exclusive Tools**: NorsTrigger, NorsMonitor, and NorsScanner.

## 📂 Repository Contents
- `build_iso.sh`: Automated script to build the NORS OS Live ISO using `live-build`.
- `packages.list`: Comprehensive list of apt packages included in the distro.
- `NorsTrigger/`: Metasploit payload generation GUI (Python/PyQt5).
- `NorsMonitor/`: System resource monitor (C++/Qt).
- `KDE_Theme/`: Visual assets and color schemes (NorsDream).
- `setup_wine_bottles.sh`: Script to initialize the Windows compatibility layer.

## 🚀 Building the ISO
1. Ensure you are on a Debian-based system (Debian Sid/Ubuntu recommended).
2. Run `sudo ./build_iso.sh`.
3. Wait for the process to complete. The ISO will be output in the `nors-build` directory.

## 📜 License
All scripts and exclusive NORS tools are licensed under the **GPLv3**.
*Note: This system is intended strictly for educational and authorized penetration testing purposes.*
