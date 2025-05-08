#!/bin/bash

# NetSleuth - Network Reconnaissance Tool

target=$1

if [ -z "$target" ]; then
  echo "Usage: ./NetSleuth.sh <target>"
  exit 1
fi

# Function to perform Nmap scan
port_scan() {
  echo "Performing port scan on $target"
  nmap -p- $target
}

# Function to analyze open services
service_analysis() {
  echo "Analyzing open services on $target"
  nmap -sV $target
}

# Perform scans in parallel
port_scan &
service_analysis &

wait
echo "Network reconnaissance complete."
