#!/usr/bin/env python3
"""
Modern MAC Address Changer using `ip` command
=============================================
Changes the MAC address of a network interface using the modern `ip` command instead of deprecated `ifconfig`.

Author: Benjamin Hunter Miller
License: GNU
"""

import subprocess
import re
import sys

def change_mac(interface: str, new_mac: str) -> None:
    """
    Changes the MAC address of a given network interface.

    :param interface: Network interface name (e.g., 'eth0', 'wlan0')
    :param new_mac: New MAC address in format XX:XX:XX:XX:XX:XX
    """
    print(f"[INFO] Bringing down interface '{interface}'...")
    subprocess.run(["ip", "link", "set", interface, "down"], check=True)

    print(f"[INFO] Setting MAC address of '{interface}' to '{new_mac}'...")
    subprocess.run(["ip", "link", "set", interface, "address", new_mac], check=True)

    print(f"[INFO] Bringing interface '{interface}' back up...")
    subprocess.run(["ip", "link", "set", interface, "up"], check=True)

    print(f"[SUCCESS] MAC address for '{interface}' changed to '{new_mac}'.")

def is_valid_mac(mac: str) -> bool:
    """
    Validates the MAC address format.

    :param mac: MAC address string
    :return: True if valid, False otherwise
    """
    return re.fullmatch(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", mac) is not None

if __name__ == "__main__":
    interface = "eth0"
    new_mac = "00:55:21:47:29:67"

    if len(sys.argv) == 3:
        interface = sys.argv[1]
        new_mac = sys.argv[2]
    else:
        print(f"[INFO] Using default interface '{interface}' and MAC '{new_mac}'")
        print("Usage: python3 mac_changer.py <interface> <new_mac>")

    if not is_valid_mac(new_mac):
        print("[ERROR] Invalid MAC address format. Use format XX:XX:XX:XX:XX:XX")
        sys.exit(1)

    try:
        change_mac(interface, new_mac)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")
        sys.exit(1)
💡 Example
bash
Copy
Edit
python3 mac_changer.py wlan0 02:11:33:44:55:66
This script will only work with root privileges, so remember to use sudo:

bash
Copy
Edit
sudo python3 mac_changer.py eth0 02:11:22:33:44:55
