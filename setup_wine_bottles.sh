#!/bin/bash
# NORS OS - Wine & Bottles Security Tools Setup
# License: GPLv3

echo "[*] Setting up Bottles and Wine environment for NORS OS..."

# Install Bottles via Flatpak (assuming flatpak is installed)
if ! command -v flatpak &> /dev/null; then
    echo "[-] Flatpak not found. Installing..."
    sudo apt-get update && sudo apt-get install -y flatpak
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
fi

echo "[*] Installing Bottles..."
flatpak install -y flathub com.usebottles.bottles

echo "[*] Configuring default Wine prefix for security tools..."
WINEPREFIX="$HOME/.nors_wine_prefix"
export WINEPREFIX

if [ ! -d "$WINEPREFIX" ]; then
    wineboot -u
fi

echo "[*] Installing essential Windows dependencies (.NET 4.8, VC++, DirectX)..."
# Using winetricks
winetricks -q dotnet48 vcrun2015 d3dcompiler_43 dxvk

echo "[*] Downloading Python for Windows (useful for some RE scripts)..."
wget https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -O /tmp/python_installer.exe
wine /tmp/python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

echo "[+] Wine and Bottles setup complete."
