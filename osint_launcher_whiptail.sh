#!/bin/bash

# ==========================================
# 🕵️ OSINT Toolkit Launcher (Whiptail UI)
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
    "maltego"  # GUI environment
    "spiderfoot -l 127.0.0.1:5001"
    "recon-ng"
    "python3 sherlock/sherlock.py username"
    "python3 GHunt/ghunt.py login"
    "python3 Photon/photon.py -u https://example.com -o photon_results"
    "python3 Infoga/infoga.py -t test@example.com --source all"
    "python3 email2phonenumber.py -e test@example.com"
    "python3 twint -u username"
)

launch_tool() {
    CMD="${TOOL_COMMANDS[$1]}"
    echo "🚀 Launching: ${TOOLS[$1]}"
    gnome-terminal -- bash -c "$CMD; exec bash" 2>/dev/null ||
    xterm -e "$CMD; bash" 2>/dev/null ||
    konsole -e "$CMD" 2>/dev/null ||
    echo "⚠️ Could not open terminal for: ${TOOLS[$1]}"
}

# Create whiptail menu string
MENU_ITEMS=()
for i in "${!TOOLS[@]}"; do
    MENU_ITEMS+=($i "${TOOLS[$i]}")
done

MENU_CHOICE=$(whiptail --title "🕵️ OSINT Terminal Launcher" \
    --menu "Select a tool to launch:" 20 60 12 \
    "${MENU_ITEMS[@]}" \
    A "Launch ALL (⚠️ heavy)" \
    Q "Quit" 3>&1 1>&2 2>&3)

EXIT_STATUS=$?

if [ $EXIT_STATUS -ne 0 ]; then
    echo "❌ Cancelled."
    exit 1
fi

case "$MENU_CHOICE" in
    Q)
        echo "👋 Bye, OSINT sleuth!"
        exit 0
        ;;
    A)
        for i in "${!TOOLS[@]}"; do
            launch_tool "$i"
        done
        ;;
    *)
        launch_tool "$MENU_CHOICE"
        ;;
esac

🧑‍🔧 To Run:

    Save it as osint_launcher_whiptail.sh

    Make it executable:

chmod +x osint_launcher_whiptail.sh

Run it:

    ./osint_launcher_whiptail.sh

🔧 Dependencies

    Make sure whiptail is installed:

sudo apt install whiptail
