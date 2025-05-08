#!/bin/bash

# SystemEnum - A comprehensive system enumeration tool
# Author: Benjamin Hunter Miller
# License: GNU General Public License v3.0
# Purpose: This script performs a comprehensive check of various system configurations for security assessment.
#          It collects information like user details, system logs, network configurations, etc.

# Function to check user and group details
check_users_groups() {
    echo "Checking users and groups:"
    cat /etc/passwd | awk -F: '{ print $1 " -> " $3 " -> " $4 " -> " $7 }'
    echo
}

# Function to check system version
check_version() {
    echo "Checking system version:"
    uname -a
    cat /etc/os-release
    echo
}

# Function to check for world-writable files
check_world_writable_files() {
    echo "Checking for world-writable files:"
    find / -type f -perm -0002 -exec ls -l {} \; 2>/dev/null
    echo
}

# Function to check for setuid binaries
check_setuid() {
    echo "Checking for setuid binaries:"
    find / -type f -perm -4000 -exec ls -l {} \; 2>/dev/null
    echo
}

# Function to check for cron jobs
check_cron_jobs() {
    echo "Checking for cron jobs:"
    crontab -l
    ls -la /etc/cron.d/
    echo
}

# Function to check open ports
check_open_ports() {
    echo "Checking open ports:"
    netstat -tuln
    echo
}

# Function to check kernel version and patch status
check_kernel() {
    echo "Checking kernel version and patch status:"
    uname -r
    dmesg | grep -i "vuln"
    echo
}

# Main function to run all checks
run_checks() {
    check_users_groups
    check_version
    check_world_writable_files
    check_setuid
    check_cron_jobs
    check_open_ports
    check_kernel
}

# Execute the checks
run_checks

echo "System enumeration completed by Benjamin Hunter Miller."

Usage:
Save the script as SystemEnum.sh.

Ensure the script is executable:

bash
Copy
Edit
chmod +x SystemEnum.sh
Run it on a Linux system:

bash
Copy
Edit
./SystemEnum.sh
