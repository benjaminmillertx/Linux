#!/bin/bash

# SmartEnum - Linux Smart Enumeration Tool
# Author: Benjamin Hunter Miller
# License: GNU General Public License v3.0
# Purpose: This script is designed to help identify privilege escalation vectors on a Linux system.

# Check for root privileges
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "[!] This script must be run as root!"
        exit 1
    fi
}

# Display system information
display_system_info() {
    echo "[*] Gathering system information..."
    echo "System hostname: $(hostname)"
    echo "Kernel version: $(uname -r)"
    echo "Architecture: $(uname -m)"
    echo "Uptime: $(uptime -p)"
    echo "CPU info: $(lscpu | grep 'Model name')"
    echo "Memory info: $(free -h | grep 'Mem')"
    echo "Disk usage: $(df -h)"
}

# Check for SUID and SGID files
check_suid_sgid() {
    echo "[*] Checking for SUID/SGID files..."
    find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -la {} \; 2>/dev/null
}

# Check for world-writable files
check_world_writable() {
    echo "[*] Checking for world-writable files..."
    find / -type f -perm -2 -exec ls -la {} \; 2>/dev/null
}

# Check for potentially dangerous files in sensitive directories
check_sensitive_dirs() {
    echo "[*] Checking for writable files in sensitive directories..."
    sensitive_dirs=("/etc" "/usr/bin" "/bin" "/sbin")
    for dir in "${sensitive_dirs[@]}"; do
        echo "[*] Checking $dir..."
        find $dir -type f -perm -2 2>/dev/null
    done
}

# Check for open network ports
check_open_ports() {
    echo "[*] Checking for open network ports..."
    ss -tuln
}

# Check for cron jobs
check_cron_jobs() {
    echo "[*] Checking for cron jobs..."
    cat /etc/crontab
    ls -la /var/spool/cron/crontabs
}

# Check for available kernel exploits
check_kernel_exploits() {
    echo "[*] Checking for kernel vulnerabilities..."
    kernel_version=$(uname -r)
    if [[ "$kernel_version" =~ "4.4" ]]; then
        echo "[!] Kernel version $kernel_version has known vulnerabilities!"
    else
        echo "[*] Kernel version $kernel_version appears safe."
    fi
}

# Check for user groups and permissions
check_user_groups() {
    echo "[*] Checking user groups..."
    id
    echo "[*] Checking for users with sudo access..."
    grep -i sudo /etc/group
}

# Main function to run the enumeration checks
run_enumeration() {
    check_root
    display_system_info
    check_suid_sgid
    check_world_writable
    check_sensitive_dirs
    check_open_ports
    check_cron_jobs
    check_kernel_exploits
    check_user_groups
}

# Execute the script
run_enumeration

How to Use:
Save the script as SmartEnum.sh.

Make it executable:

bash
Copy
Edit
chmod +x SmartEnum.sh
Run it as root:

bash
Copy
Edit
sudo ./SmartEnum.sh
Ethical Use:
This script is for ethical penetration testing and should only be run on systems where you have explicit permission. Unauthorized use may be illegal and can result in severe consequences.

This tool is licensed under the GNU General Public License v3.0, and you should only distribute or modify it according to the terms of that license.
