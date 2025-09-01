#!/bin/bash
# Bash Email Reader with Search
# By Benjamin Miller

IMAP_SERVER="imap.example.com"
EMAIL="you@example.com"
PASSWORD="your_app_password"

MAIL_DIR="$HOME/.bashmail"
mkdir -p "$MAIL_DIR"

fetch_emails() {
    echo "[*] Fetching last 20 emails..."
    curl -s --url "imaps://$IMAP_SERVER/INBOX" \
         --user "$EMAIL:$PASSWORD" \
         --request "FETCH 1:20 BODY[TEXT]" > "$MAIL_DIR/mail.txt"

    if [[ -s "$MAIL_DIR/mail.txt" ]]; then
        echo "[*] Emails saved to $MAIL_DIR/mail.txt"
    else
        echo "[!] Failed to fetch emails."
    fi
}

search_emails() {
    read -p "Enter search keyword: " keyword
    if [[ -f "$MAIL_DIR/mail.txt" ]]; then
        grep -i -C 3 "$keyword" "$MAIL_DIR/mail.txt" | less
    else
        echo "[!] No emails found. Fetch first."
    fi
}

view_emails() {
    if [[ -f "$MAIL_DIR/mail.txt" ]]; then
        less "$MAIL_DIR/mail.txt"
    else
        echo "[!] No emails to view. Fetch first."
    fi
}

menu() {
    while true; do
        clear
        echo "=== Bash Email Client ==="
        echo "1) Fetch Emails"
        echo "2) View Emails"
        echo "3) Search Emails"
        echo "4) Quit"
        read -p "Choose: " choice
        case $choice in
            1) fetch_emails ;;
            2) view_emails ;;
            3) search_emails ;;
            4) exit 0 ;;
            *) echo "Invalid option"; sleep 1 ;;
        esac
    done
}

menu
