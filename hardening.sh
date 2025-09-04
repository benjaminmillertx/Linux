#!/bin/bash
# Linux Quick Security Hardening Script
# Author: Benjamin Miller

echo "=== Updating System ==="
sudo apt update && sudo apt upgrade -y   # Debian/Ubuntu
# sudo yum update -y                     # RHEL/CentOS
# sudo dnf update -y                     # Fedora

echo "=== Removing Unnecessary Packages ==="
sudo apt autoremove -y

echo "=== Creating Non-Root Admin User ==="
read -p "Enter new admin username: " ADMINUSER
sudo adduser $ADMINUSER
sudo usermod -aG sudo $ADMINUSER

echo "=== SSH Hardening ==="
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

echo "=== Installing Fail2Ban ==="
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

echo "=== Firewall Configuration ==="
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp  # SSH port
sudo ufw enable
sudo ufw status verbose

echo "=== User and Permission Hardening ==="
sudo deluser olduser 2>/dev/null
sudo groupdel oldgroup 2>/dev/null
sudo usermod -L olduser 2>/dev/null
sudo apt install libpam-pwquality -y
sudo sed -i '/pam_pwquality.so/ s/$/ retry=3 minlen=12/' /etc/pam.d/common-password

echo "=== Service Hardening ==="
sudo systemctl list-unit-files | grep enabled
# Disable unnecessary services manually:
# sudo systemctl disable service_name

echo "=== AppArmor Installation ==="
sudo apt install apparmor apparmor-profiles -y
sudo systemctl enable apparmor
sudo systemctl start apparmor

echo "=== File System Hardening ==="
sudo chmod 700 /root
sudo chmod 600 /etc/shadow
sudo chmod 644 /etc/passwd
echo "tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev 0 0" | sudo tee -a /etc/fstab

echo "=== Logging and Monitoring ==="
sudo apt install auditd audispd-plugins -y
sudo systemctl enable auditd
sudo systemctl start auditd

echo "=== Network Hardening ==="
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv4.tcp_syncookies=1
sudo sysctl -w net.ipv4.conf.all.rp_filter=1
sudo sysctl -p

echo "=== Unattended Security Updates ==="
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades

echo "=== SUID/SGID Check ==="
find / -perm /6000 -type f -exec ls -ld {} \;

echo "=== Malware and Rootkit Detection ==="
sudo apt install clamav rkhunter -y
sudo freshclam
sudo clamscan -r /
sudo rkhunter --update
sudo rkhunter --checkall

echo "=== Backup Setup (Example) ==="
# Replace /important/data and /backup/location with your paths
# rsync -av --delete /important/data /backup/location

echo "=== Optional: Two-Factor SSH Authentication ==="
# sudo apt install libpam-google-authenticator -y
# google-authenticator

echo "=== Optional: Disk Encryption (LUKS) ==="
# sudo cryptsetup luksFormat /dev/sdx
# sudo cryptsetup luksOpen /dev/sdx secure_disk

echo "=== Linux Hardening Script Complete ==="

How to Use

Save it as hardening.sh:

nano hardening.sh
# Paste content and save

Make it executable:

chmod +x hardening.sh

Run it:

sudo ./hardening.sh
