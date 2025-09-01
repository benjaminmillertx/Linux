#!/usr/bin/env python3
"""
Terminal Email Client (IMAP)
Author: Benjamin Miller
"""

import imaplib
import email
from email.header import decode_header
import re

# Configuration
IMAP_SERVER = "imap.example.com"
EMAIL_ACCOUNT = "you@example.com"
PASSWORD = "your_app_password"

def connect_mailbox():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        mail.select("inbox")
        return mail
    except Exception as e:
        print(f"[!] Connection error: {e}")
        exit(1)

def fetch_emails(limit=10):
    mail = connect_mailbox()
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()[-limit:]

    emails = []
    for eid in email_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")
                body = get_body(msg)
                emails.append({"subject": subject, "body": body})
    mail.close()
    mail.logout()
    return emails

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return msg.get_payload(decode=True).decode(errors="ignore")
    return ""

def search_emails(keyword, emails):
    print(f"[*] Searching for '{keyword}'...\n")
    found = False
    for e in emails:
        if re.search(keyword, e["subject"], re.IGNORECASE) or re.search(keyword, e["body"], re.IGNORECASE):
            print("="*50)
            print(f"Subject: {e['subject']}\n")
            print(e['body'][:500])  # show first 500 chars
            print("="*50 + "\n")
            found = True
    if not found:
        print("[!] No matches found.")

def main():
    print("=== Python Email Client ===")
    emails = fetch_emails()
    while True:
        print("\n1) View All Subjects\n2) Search Emails\n3) Quit")
        choice = input("Select: ")
        if choice == "1":
            for e in emails:
                print(f"- {e['subject']}")
        elif choice == "2":
            kw = input("Keyword: ")
            search_emails(kw, emails)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
# Usage

chmod +x email_client.py
./email_client.py


