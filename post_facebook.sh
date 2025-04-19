#!/bin/bash
source .env

echo "📝 Enter Facebook post content:"
read POST_TEXT

if [ -z "$POST_TEXT" ]; then echo "❌ Post content cannot be empty!"; exit 1; fi

echo "📘 Posting to Facebook..."
curl -s -X POST "https://graph.facebook.com/$FB_PAGE_ID/feed" \
     -d "message=$POST_TEXT" \
     -d "access_token=$FB_ACCESS_TOKEN" \
     -o /dev/null
echo "✅ Facebook post complete."
