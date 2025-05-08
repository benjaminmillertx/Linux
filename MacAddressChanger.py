#!/usr/bin/env python3
"""
MAC Address Changer Script
===========================
This script allows you to change the MAC address of a network interface on Unix-based systems.

Author: Benjamin Hunter Miller
License: GNU
"""

import subprocess
import re
import sys

def change_mac(interface: str, new_mac: str) -> None:
    """
    Changes the MAC address of the specified network interface.

    :param interface: Name of the network interface (e.g., 'eth0', 'wlan0')
    :param new_mac: New MAC address to assign
    """
    print(f"[INFO] Shutting down interface {interface}...")
    subprocess.run(["ifconfig", interface, "down"], check=True)

    print(f"[INFO] Changing MAC address of {interface} to {new_mac}...")
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)

    print(f"[INFO] Bringing interface {interface} back up...")
    subprocess.run(["ifconfig", interface, "up"], check=True)

    print(f"[SUCCESS] MAC address for {interface} changed to {new_mac}")

def is_valid_mac(mac: str) -> bool:
    """
    Validates the MAC address format.

    :param mac: MAC address string to validate
    :return: True if valid, False otherwise
    """
    return re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac) is not None

if __name__ == "__main__":
    # Default values (you can modify these or allow user input)
    interface = "eth0"
    new_mac = "00:55:21:47:29:67"

    # Optional: Accept arguments from command line
    if len(sys.argv) == 3:
        interface = sys.argv[1]
        new_mac = sys.argv[2]
    else:
        print(f"[INFO] Using default interface '{interface}' and MAC '{new_mac}'")
        print("Usage: python3 mac_changer.py <interface> <new_mac>")

    if not is_valid_mac(new_mac):
        print("[ERROR] Invalid MAC address format. Please use format: XX:XX:XX:XX:XX:XX")
        sys.exit(1)

    try:
        change_mac(interface, new_mac)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")
        sys.exit(1)
💡 Example Usage
bash
Copy
Edit
# Change MAC on eth0 to 00:55:21:47:29:67
python3 mac_changer.py eth0 00:55:21:47:29:67
