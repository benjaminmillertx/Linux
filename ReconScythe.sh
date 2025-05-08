#!/bin/bash

# ReconScythe - Automated reconnaissance tool for Penetration Testing

# Dependencies: nmap, whois, dig

target=$1

if [ -z "$target" ]; then
  echo "Usage: ./ReconScythe.sh <target>"
  exit 1
fi

echo "Running Reconnaissance on $target..."

# Function to perform Nmap scan
nmap_scan() {
  nmap -sV -O $target
}

# Function to get DNS information
dns_info() {
  dig $target
}

# Function to gather WHOIS data
whois_info() {
  whois $target
}

# Perform scans in parallel
echo "Performing Nmap Scan..."
nmap_scan &
echo "Gathering DNS Info..."
dns_info &
echo "Fetching WHOIS Info..."
whois_info &

# Wait for all background tasks to finish
wait
echo "Reconnaissance complete."
