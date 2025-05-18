#!/bin/bash

echo "[*] RocketRecover - Deleted File Recovery Tool"
echo "[*] Made by Benjamin Hunter Miller - GNU Project"

read -p "Enter SSH target (e.g., user@192.168.1.10): " TARGET

# Check SSH
echo "[*] Checking SSH access..."
if ! ssh -q "$TARGET" exit; then
    echo "[!] SSH connection failed."
    exit 1
fi

echo "[*] SSH connection established."

# Detect OS
echo "[*] Detecting remote OS..."
OS_TYPE=$(ssh "$TARGET" 'uname -a || ver || systeminfo | findstr /B /C:"OS Name"')

if echo "$OS_TYPE" | grep -qi "Linux"; then
    echo "[+] Linux system detected."

    ssh "$TARGET" '
        echo "[*] Listing disks..."
        lsblk
        read -p "Enter the disk (e.g., /dev/sda1): " DISK

        echo "[*] Installing tools (if needed)..."
        sudo apt update -y && sudo apt install extundelete testdisk -y

        echo "[*] Attempting recovery using extundelete..."
        sudo umount $DISK 2>/dev/null
        mkdir -p RECOVERED_FILES
        sudo extundelete $DISK --restore-all --output-dir RECOVERED_FILES || echo "[!] extundelete failed."

        echo "[*] Attempting recovery using photorec (carving)..."
        sudo photorec /log /d RECOVERED_FILES /cmd $DISK options,search
    '

elif echo "$OS_TYPE" | grep -qi "Darwin"; then
    echo "[+] macOS system detected (APFS)."

    ssh "$TARGET" '
        echo "[*] Installing Homebrew photorec if needed..."
        which photorec || brew install testdisk

        echo "[*] Running photorec..."
        sudo photorec
    '

elif echo "$OS_TYPE" | grep -qi "Microsoft"; then
    echo "[+] Windows system detected (likely WSL or WinSSH)."

    ssh "$TARGET" '
        echo "[!] Native deleted file recovery not supported over SSH on Windows."
        echo "[*] Recommended: Use FTK Imager or Autopsy on a raw image."
    '

elif ssh "$TARGET" 'cat /etc/lsb-release 2>/dev/null | grep -i chrome' > /dev/null; then
    echo "[+] Chrome OS system detected (Developer Mode assumed)."

    ssh "$TARGET" '
        echo "[*] Installing tools..."
        sudo apt update -y && sudo apt install testdisk -y

        echo "[*] Running photorec..."
        sudo photorec
    '
else
    echo "[!] Unknown or unsupported OS."
    exit 1
fi

echo "[*] Recovery attempt complete."

🔧 How to Use
Save as rocket-recover.sh

Make executable:

bash
Copy
Edit
chmod +x rocket-recover.sh
Run it:

bash
Copy
Edit
./rocket-recover.sh
🧠 Features:
Automatically detects OS

Uses photorec, extundelete, or testdisk where applicable

Modular to extend later (e.g., raw image extraction, remote copy, logs)

Minimal user input needed
