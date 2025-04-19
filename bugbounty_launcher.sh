#!/bin/bash

# ================================
# 🐞 Bug Bounty Toolkit Launcher
# Author: Benjamin Hunter Miller
# ================================

# ---------- CONFIG ----------
TOOLS=(
    "nmap"               # 1. Port scanner
    "subfinder"          # 2. Subdomain discovery
    "httpx"              # 3. HTTP probing
    "nuclei"             # 4. Vulnerability scanner
    "gf"                 # 5. Pattern searcher
    "waybackurls"        # 6. URL archive fetcher
    "dirsearch"          # 7. Directory brute-forcer
    "sqlmap"             # 8. SQL injection tester
    "ffuf"               # 9. Fuzzer
    "burpsuite"          #10. Interception proxy
)

TOOL_COMMANDS=(
    "nmap -A scanme.nmap.org"
    "subfinder -d example.com -silent"
    "httpx -l urls.txt -status-code"
    "nuclei -l urls.txt"
    "cat urls.txt | gf sqli"
    "waybackurls example.com"
    "python3 dirsearch.py -u https://example.com -e php,html"
    "sqlmap -u 'https://example.com/page.php?id=1' --batch"
    "ffuf -u https://example.com/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
    "burpsuite"
)

# ---------- UI ----------
echo "=============================="
echo "     🐞 Bug Bounty Launcher"
echo "         by Benjamin Miller"
echo "=============================="
echo "Pick a tool to launch:"
echo

for i in "${!TOOLS[@]}"; do
    printf "%2d. %s\n" "$((i + 1))" "${TOOLS[$i]}"
done

echo " A. Launch ALL tools"
echo " Q. Quit"
echo
read -p "Your choice: " CHOICE

# ---------- LAUNCH ----------
launch_tool() {
    CMD="${TOOL_COMMANDS[$1]}"
    echo "🚀 Launching: ${TOOLS[$1]}"
    gnome-terminal -- bash -c "$CMD; exec bash" 2>/dev/null ||
    xterm -e "$CMD; bash" 2>/dev/null ||
    konsole -e "$CMD" 2>/dev/null ||
    echo "⚠️  Could not open terminal for: ${TOOLS[$1]}"
}

if [[ "$CHOICE" =~ ^[Qq]$ ]]; then
    echo "👋 Exiting. Happy hacking!"
    exit 0
elif [[ "$CHOICE" =~ ^[Aa]$ ]]; then
    for i in "${!TOOLS[@]}"; do
        launch_tool "$i"
    done
elif [[ "$CHOICE" =~ ^[1-9]$|10 ]]; then
    launch_tool "$((CHOICE - 1))"
else
    echo "❌ Invalid input"
    exit 1
fi

🛠️ Setup

    Make executable:

chmod +x bugbounty_launcher.sh

Run it:

./bugbounty_launcher.sh

Customize:

    Change tool commands or paths to match your local setup.

    Add more tools by extending the TOOLS and TOOL_COMMANDS arrays.
