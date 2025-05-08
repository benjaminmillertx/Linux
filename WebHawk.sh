#!/bin/bash

# WebHawk - Web Application Vulnerability Scanner

target=$1

if [ -z "$target" ]; then
  echo "Usage: ./WebHawk.sh <target>"
  exit 1
fi

# Function to check for SQL Injection
check_sql_injection() {
  echo "Checking for SQL Injection on $target"
  curl -s $target'\' OR 1=1 --data "param=1" | grep -i "error"
}

# Function to check for Cross-Site Scripting (XSS)
check_xss() {
  echo "Checking for XSS vulnerabilities on $target"
  curl -s $target -G --data "param=<script>alert('XSS')</script>" | grep -i "<script>alert('XSS')</script>"
}

# Check vulnerabilities
check_sql_injection &
check_xss &

wait
echo "Vulnerability scan complete."
