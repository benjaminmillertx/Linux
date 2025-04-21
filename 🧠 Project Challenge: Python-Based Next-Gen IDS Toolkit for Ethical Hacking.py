📚 Overview:

Build an advanced Intrusion Detection Toolkit with Python capable of:

    Real-time packet sniffing & filtering

    Log-based anomaly detection

    Dictionary-based password audit simulation

    Optional: Alert generation or live dashboards

Each script should work independently or be combined into a unified modular IDS system.
🧪 Challenge 1: Real-Time Packet Sniffer & Suspicious Traffic Detector
✅ Goal:

Develop a real-time sniffer using Scapy that:

    Logs source/destination IPs, ports, protocols

    Filters by TCP, UDP, or custom criteria

    Flags suspicious activity (e.g., port scans, repeated SYNs)

🔧 Requirements:

    scapy, datetime

    Optional: GeoIP lookup using geoip2 or ipinfo.io

🔍 Sample Advanced Features:

    Detect SYN floods by tracking excessive SYNs from same IP

    Track top talkers (most active IPs)

    Packet rate threshold alerts

🧩 Code Snippet:

from scapy.all import sniff, IP, TCP
from collections import defaultdict
from datetime import datetime

syn_counts = defaultdict(int)

def detect(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        timestamp = datetime.now().strftime("%H:%M:%S")

        if TCP in packet:
            flags = packet[TCP].flags
            if flags == 'S':  # SYN packet
                syn_counts[ip_src] += 1
                if syn_counts[ip_src] > 20:
                    print(f"[ALERT 🚨] Possible SYN Flood from {ip_src} at {timestamp}")

        print(f"[{timestamp}] {ip_src} -> {ip_dst}")

sniff(prn=detect, store=0)

🧪 Challenge 2: Web Server Log Anomaly Detector
✅ Goal:

Parse Apache/Nginx logs, detect anomalies like:

    Brute-force login attempts

    SQL injection patterns

    IPs generating high request volume

🔧 Requirements:

    re, collections, optionally pandas or matplotlib

🧩 Code Snippet:

import re
from collections import Counter

log_path = "access.log"
ip_pattern = r"\d{1,3}(?:\.\d{1,3}){3}"
injection_pattern = r"(UNION|SELECT|DROP|--|OR\s+1=1)"

def analyze_logs():
    with open(log_path, 'r') as f:
        logs = f.readlines()

    ips = [re.search(ip_pattern, line).group() for line in logs if re.search(ip_pattern, line)]
    suspect_lines = [line for line in logs if re.search(injection_pattern, line, re.IGNORECASE)]

    print("\n[TOP IPs]")
    for ip, count in Counter(ips).most_common(5):
        print(f"{ip}: {count} requests")

    print("\n[SUSPICIOUS ENTRIES]")
    for line in suspect_lines:
        print(line.strip())

analyze_logs()

🧪 Challenge 3: Parallel Password Cracker Simulator (Dictionary Attack)
✅ Goal:

Perform a simulated dictionary attack against a dummy HTTP login using multithreading.
🔧 Requirements:

    requests, concurrent.futures, optionally argparse

🧩 Code Snippet:

import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost/login"
USERNAME = "admin"

def try_password(password):
    data = {"username": USERNAME, "password": password.strip()}
    r = requests.post(URL, data=data)
    if "Welcome" in r.text or r.status_code == 200:
        print(f"[✔️] Password found: {password.strip()}")
        return True
    return False

def main():
    with open("passwords.txt") as f:
        passwords = f.readlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(try_password, passwords)

if __name__ == '__main__':
    main()

🔥 Bonus Challenge (Optional)

Unify all scripts into a Modular IDS Dashboard using:

    Tkinter or Flask for GUI/web interface

    Real-time graphs using matplotlib or plotly

    Alert logs for detected threats

📦 Directory Structure

nextgen_ids/
├── packet_sniffer.py
├── log_analyzer.py
├── password_cracker.py
├── passwords.txt
├── access.log
└── dashboard/ (optional)

✅ Deliverables:

    packet_sniffer.py: Real-time TCP analysis + anomaly alerts

    log_analyzer.py: Web log anomaly detector

    password_cracker.py: Simulated dictionary attack tool

    README.md: Explain each script and ethical boundaries

⚠️ Ethical Reminder

These scripts are built strictly for ethical testing and educational use:

    Never scan or target systems without explicit permission.

    Log analysis must be on systems you own or are authorized to audit.
