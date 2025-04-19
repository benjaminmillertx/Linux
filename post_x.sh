#!/bin/bash
source .env

echo "📝 Enter X (Twitter) post content:"
read POST_TEXT

if [ -z "$POST_TEXT" ]; then echo "❌ Post content cannot be empty!"; exit 1; fi

echo "🐦 Posting to X..."
curl -s -X POST "https://api.twitter.com/2/tweets" \
     -H "Authorization: Bearer $X_BEARER_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"text\":\"$POST_TEXT\"}" \
     -o /dev/null
echo "✅ X post complete."
