#!/bin/bash
# NORS OS - Automated ISO Build Script
# License: GPLv3
# Description: Uses live-build to generate the NORS OS ISO.

set -e

# Configuration Variables
DISTRIBUTION="sid"
ARCHITECTURE="amd64"
ISO_NAME="nors-os-beta-amd64.iso"
WORK_DIR="nors-build"
PACKAGES_LIST="../packages.list"

echo "[*] Initializing NORS OS build environment..."

# Install prerequisites
sudo apt-get update
sudo apt-get install -y live-build debootstrap squashfs-tools

# Clean previous build
if [ -d "$WORK_DIR" ]; then
    echo "[*] Cleaning previous build directory..."
    sudo rm -rf "$WORK_DIR"
fi

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "[*] Configuring live-build..."
lb config \
    --distribution $DISTRIBUTION \
    --architecture $ARCHITECTURE \
    --archive-areas "main contrib non-free non-free-firmware" \
    --iso-application "NORS OS" \
    --iso-publisher "NORS Project" \
    --iso-volume "NORS_OS_LIVE" \
    --image-name $ISO_NAME \
    --debian-installer live \
    --debian-installer-distribution $DISTRIBUTION

echo "[*] Copying package lists..."
mkdir -p config/package-lists
cp "$PACKAGES_LIST" config/package-lists/nors.list.chroot

echo "[*] Integrating NORS OS Custom Tools and Interface..."
# إنشاء المجلد الذي سيتم نسخه إلى جذر النظام النهائي (/)
mkdir -p config/includes.chroot/opt/NORS_OS
mkdir -p config/includes.chroot/usr/share/applications

# نسخ كل الأدوات التي قمنا بصناعتها إلى مجلد /opt/NORS_OS داخل النظام
cp -r ../NorsTrigger ../NorsMonitor ../NorsScanner ../NorsReporter ../NorsDefender ../Scripts ../NorsStudio ../NorsPayloadObfuscator ../WebDashboard ../NorsLabs ../NorsAuditor ../NorsAcademy ../NorsVPN ../NorsC2 ../NorsWifi ../NorsFuzzer ../NorsStego ../NorsOSINT ../NorsForensics ../NorsCloud ../NorsSandbox ../NorsPhish ../NorsCrypto ../NorsHardware ../NorsZeroTrust ../NorsAD ../NorsStress ../NorsReconAutomator ../NorsDeobfuscator ../NorsInstaller config/includes.chroot/opt/NORS_OS/

# إضافة أيقونة التثبيت لسطح المكتب
mkdir -p config/includes.chroot/etc/skel/Desktop
cp ../NorsInstaller/install-nors.desktop config/includes.chroot/etc/skel/Desktop/
cp ../NorsInstaller/install-nors.desktop config/includes.chroot/usr/share/applications/

# نسخ سمة كيدي (KDE Theme)
mkdir -p config/includes.chroot/usr/share/color-schemes/
cp ../KDE_Theme/NorsDream/colors config/includes.chroot/usr/share/color-schemes/NorsDream.colors

echo "[*] Starting ISO build (This will take a while)..."
sudo lb build

echo "[+] Build complete! ISO should be available in $WORK_DIR"
