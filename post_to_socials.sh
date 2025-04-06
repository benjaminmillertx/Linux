#!/bin/bash

################################################################################
# Script Name: post_to_socials.sh
# Description: Posts a message to both Facebook and Twitter from the terminal.
# Author: Benjamin Hunter Miller
# Date: April 6, 2025
################################################################################

# ========== CONFIGURATION ==========
# Replace these with your actual credentials

# Facebook Page ID and Access Token (get from Facebook Graph API)
FB_PAGE_ID="YOUR_FACEBOOK_PAGE_ID"
FB_ACCESS_TOKEN="YOUR_FACEBOOK_ACCESS_TOKEN"

# Twitter Bearer Token (get from Twitter Developer Portal)
TW_BEARER_TOKEN="YOUR_TWITTER_BEARER_TOKEN"

# ========== FUNCTION TO POST TO FACEBOOK ==========
post_to_facebook() {
    echo "📘 Posting to Facebook..."
    curl -s -X POST "https://graph.facebook.com/$FB_PAGE_ID/feed" \
        -d "message=$1" \
        -d "access_token=$FB_ACCESS_TOKEN" \
        -o /dev/null
    echo "✅ Facebook post complete."
}

# ========== FUNCTION TO POST TO TWITTER ==========
post_to_twitter() {
    echo "🐦 Posting to Twitter..."
    curl -s -X POST "https://api.twitter.com/2/tweets" \
        -H "Authorization: Bearer $TW_BEARER_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"text\":\"$1\"}" \
        -o /dev/null
    echo "✅ Twitter post complete."
}

# ========== MAIN SCRIPT ==========
echo "==============================="
echo "  Social Media Post Publisher"
echo "      by Benjamin Miller"
echo "==============================="

# Prompt user for the post text
read -p "📝 Enter the post content: " POST_TEXT

# Simple validation
if [ -z "$POST_TEXT" ]; then
    echo "❌ Error: Post content cannot be empty!"
    exit 1
fi

# Confirm before posting
echo "🚀 Ready to post this message: \"$POST_TEXT\""
read -p "Do you want to proceed? (y/n): " CONFIRM

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    post_to_facebook "$POST_TEXT"
    post_to_twitter "$POST_TEXT"
    echo "🎉 All done!"
else
    echo "❌ Post canceled."
fi
✅ Instructions
Create the script file:

bash
Copy
Edit
nano post_to_socials.sh
Paste the code above, replace credentials with your own.

Make it executable:

bash
Copy
Edit
chmod +x post_to_socials.sh
Run it:

bash
Copy
Edit
./post_to_socials.sh
🔐 Tips for Production Use
Store credentials in a .env file and use source .env to load them securely.

Consider logging responses from the APIs.

Use jq for better JSON parsing if needed.
