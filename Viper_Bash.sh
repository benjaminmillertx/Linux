#!/bin/bash

VAULT_FILE="$HOME/.password_vault.txt"

# Create vault file if it doesn't exist
[ ! -f "$VAULT_FILE" ] && touch "$VAULT_FILE"

generate_password() {
    openssl rand -base64 16
}

add_entry() {
    read -p "Website: " website
    read -p "Username: " username
    password=$(generate_password)
    echo "$website | $username | $password" >> "$VAULT_FILE"
    echo "Password generated and stored for $website."
}

view_entries() {
    if [ ! -s "$VAULT_FILE" ]; then
        echo "Vault is empty."
    else
        echo "Stored Credentials:"
        cat "$VAULT_FILE"
    fi
}

while true; do
    echo -e "\n--- Password Vault ---"
    echo "1. Add new password"
    echo "2. View all entries"
    echo "3. Exit"
    read -p "Choose an option: " choice

    case $choice in
        1) add_entry ;;
        2) view_entries ;;
        3) exit 0 ;;
        *) echo "Invalid choice." ;;
    esac
done
#  How to Run on Linux

# Save as password_vault.sh.


# Make executable:
# chmod +x password_vault.sh

Run:
./password_vault.sh

