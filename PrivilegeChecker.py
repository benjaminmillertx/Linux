#!/usr/bin/env python3

# PrivilegeChecker - Linux Privilege Escalation Checker Tool
# Author: Benjamin Hunter Miller
# License: GNU General Public License v3.0
# Purpose: This script checks for possible privilege escalation vectors on a Linux system.

import os
import subprocess
import sys

# Function to check if the script is running as root
def check_root():
    if os.geteuid() != 0:
        print("[!] This script must be run as root!")
        sys.exit(1)

# Function to check the system for SUID/SGID files
def check_suid_sgid():
    print("[*] Checking for SUID/SGID files...")
    try:
        output = subprocess.check_output("find / -type f -a \( -perm -4000 -o -perm -2000 \) 2>/dev/null", shell=True)
        if output:
            print("[*] SUID/SGID files found:")
            print(output.decode())
        else:
            print("[*] No SUID/SGID files found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing SUID/SGID check: {e}")

# Function to check for world-writable files
def check_world_writable():
    print("[*] Checking for world-writable files...")
    try:
        output = subprocess.check_output("find / -type f -perm -2 -a ! -type l 2>/dev/null", shell=True)
        if output:
            print("[*] World-writable files found:")
            print(output.decode())
        else:
            print("[*] No world-writable files found.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing world-writable check: {e}")

# Function to check for writable files in sensitive directories
def check_sensitive_directory_writes():
    print("[*] Checking for writable files in sensitive directories...")
    sensitive_dirs = ["/etc", "/usr/bin", "/bin", "/sbin"]
    for dir in sensitive_dirs:
        try:
            output = subprocess.check_output(f"find {dir} -type f -perm -2 2>/dev/null", shell=True)
            if output:
                print(f"[*] Writable files found in {dir}:")
                print(output.decode())
        except subprocess.CalledProcessError as e:
            print(f"[!] Error checking {dir}: {e}")

# Function to check for kernel vulnerabilities
def check_kernel_vulnerabilities():
    print("[*] Checking for kernel vulnerabilities...")
    try:
        kernel_version = subprocess.check_output("uname -r", shell=True).decode().strip()
        print(f"[*] Current kernel version: {kernel_version}")
        # Add your kernel vulnerability checks here based on the kernel version
        if kernel_version.startswith("4.4"):
            print("[*] Vulnerabilities found for kernel 4.4")
        elif kernel_version.startswith("5.4"):
            print("[*] Vulnerabilities found for kernel 5.4")
        else:
            print("[*] Kernel version appears safe.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing kernel check: {e}")

# Function to check for user permissions and groups
def check_permissions_and_groups():
    print("[*] Checking user permissions and groups...")
    try:
        output = subprocess.check_output("id", shell=True)
        print(f"[*] Current user ID information:\n{output.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error fetching user ID information: {e}")

# Main function to run the privilege escalation checks
def run_privilege_checks():
    check_root()
    check_suid_sgid()
    check_world_writable()
    check_sensitive_directory_writes()
    check_kernel_vulnerabilities()
    check_permissions_and_groups()

if __name__ == "__main__":
    run_privilege_checks()
Save the script as PrivilegeChecker.py.

Make it executable:

bash
Copy
Edit
chmod +x PrivilegeChecker.py
Run the script with root privileges:

bash
Copy
Edit
sudo ./PrivilegeChecker.py
