#!/bin/bash

# ==========================================
# 🔎 Simple Username Context Finder
# Author: Benjamin Hunter Miller
# ==========================================

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <url>"
    echo "Example: $0 johndoe https://example.com/about"
    exit 1
fi

USERNAME=$1
URL=$2

# Download page content
HTML=$(curl -sL "$URL")

# Strip HTML tags, collapse lines
TEXT=$(echo "$HTML" | sed 's/<[^>]*>//g' | tr '\n' ' ')

# Find and display all sentences with username
echo "🔍 Searching for '$USERNAME' on $URL..."
echo "========================================"
echo "$TEXT" | grep -oE '[^.!?]*'"$USERNAME"'[^.!?]*[.!?]' | sed "s/$USERNAME/\x1b[1;31m$USERNAME\x1b[0m/g"

if [ $? -ne 0 ]; then
    echo "⚠️ No matching sentences found."
fi

🧪 Example

./find_username_context.sh johndoe https://example.com/team

🧰 Dependencies

Just curl, grep, sed, and tr. No Python or heavy installs. Works on most Linux distros out of the box.
