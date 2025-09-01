import json
import secrets
import string
import os

VAULT_FILE = "password_vault.json"

# Load existing vault or create new one
def load_vault():
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    return {}

# Save vault data to file
def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)

# Generate secure random password
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# Add new entry to vault
def add_entry(vault):
    website = input("Website: ")
    username = input("Username: ")
    password = generate_password()
    vault[website] = {"username": username, "password": password}
    save_vault(vault)
    print(f"Password for {website} generated and stored.")

# View stored passwords
def view_entries(vault):
    if not vault:
        print("Vault is empty.")
        return
    for website, creds in vault.items():
        print(f"Website: {website}")
        print(f"  Username: {creds['username']}")
        print(f"  Password: {creds['password']}\n")

def main():
    vault = load_vault()
    while True:
        print("\n--- Password Vault ---")
        print("1. Add new password")
        print("2. View all entries")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_entry(vault)
        elif choice == "2":
            view_entries(vault)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
