#!/bin/bash

# ==========================================
# 🕵️ OSINT Toolkit Launcher (Buscador + Null Byte)
# Author: Benjamin Hunter Miller
# ==========================================

TOOLS=(
    "theHarvester"
    "Maltego"
    "SpiderFoot"
    "Recon-ng"
    "Sherlock"
    "GHunt"
    "Photon"
    "Infoga"
    "Email2phonenumber"
    "twint"
)

TOOL_COMMANDS=(
    "theHarvester -d example.com -b all"
    "maltego"  # Ensure GUI environment
    "spiderfoot -l 127.0.0.1:5001"
    "recon-ng"
    "python3 sherlock username"
    "python3 ghunt.py login"
    "python3 photon.py -u https://example.com -o photon_results"
    "python3 infoga.py -t test@example.com --source all"
    "python3 email2phonenumber.py -e test@example.com"
    "python3 twint -u username"
)

# UI
echo "===================================="
echo "   🕵️ OSINT Terminal Launcher"
echo "   Based on Buscador & Null Byte"
echo "   by Benjamin Miller"
echo "===================================="
echo "Available Tools:"

for i in "${!TOOLS[@]}"; do
    printf "%2d. %s\n" "$((i + 1))" "${TOOLS[$i]}"
done

echo " A. Launch ALL (⚠️ heavy!)"
echo " Q. Quit"
echo
read -p "Select a tool to launch: " CHOICE

launch_tool() {
    CMD="${TOOL_COMMANDS[$1]}"
    echo "🚀 Launching: ${TOOLS[$1]}"
    gnome-terminal -- bash -c "$CMD; exec bash" 2>/dev/null ||
    xterm -e "$CMD; bash" 2>/dev/null ||
    konsole -e "$CMD" 2>/dev/null ||
    echo "⚠️ Could not open terminal for: ${TOOLS[$1]}"
}

if [[ "$CHOICE" =~ ^[Qq]$ ]]; then
    echo "👋 Bye, OSINT sleuth!"
    exit 0
elif [[ "$CHOICE" =~ ^[Aa]$ ]]; then
    for i in "${!TOOLS[@]}"; do
        launch_tool "$i"
    done
elif [[ "$CHOICE" =~ ^[1-9]$|10 ]]; then
    launch_tool "$((CHOICE - 1))"
else
    echo "❌ Invalid option."
    exit 1
fi

🧰 Tools Breakdown
Tool	Purpose
theHarvester	Emails, subdomains, names, IPs
Maltego	Link analysis, relationships
SpiderFoot	Web-based automation engine
Recon-ng	Recon framework with modules
Sherlock	Username hunting across platforms
GHunt	OSINT on Gmail/Google accounts
Photon	Crawler for open web intel
Infoga	Email enumeration
Email2phonenumber	Tries to map emails to phone numbers
twint	Twitter scraping (no API needed)
🧑‍💻 Setup Notes

    Most Python tools must be installed manually or cloned:

git clone https://github.com/sherlock-project/sherlock.git
git clone https://github.com/mxrch/GHunt.git
git clone https://github.com/s0md3v/Photon.git
git clone https://github.com/m4ll0k/Infoga.git

Consider running in a virtual environment.
