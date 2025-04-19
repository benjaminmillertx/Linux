#!/bin/bash
source .env

echo "📝 Enter Instagram caption:"
read POST_TEXT
echo "🌐 Enter public image URL:"
read IMAGE_URL

if [ -z "$POST_TEXT" ] || [ -z "$IMAGE_URL" ]; then echo "❌ Caption and image URL required!"; exit 1; fi

# Step 1: Create media object
echo "📸 Creating Instagram media..."
MEDIA_ID=$(curl -s -X POST "https://graph.facebook.com/v18.0/$IG_USER_ID/media" \
    -d "caption=$POST_TEXT" \
    -d "image_url=$IMAGE_URL" \
    -d "access_token=$FB_ACCESS_TOKEN" | jq -r '.id')

# Step 2: Publish media
curl -s -X POST "https://graph.facebook.com/v18.0/$IG_USER_ID/media_publish" \
    -d "creation_id=$MEDIA_ID" \
    -d "access_token=$FB_ACCESS_TOKEN" \
    -o /dev/null
echo "✅ Instagram post complete."

💼 post_linkedin.sh

#!/bin/bash
source .env

echo "📝 Enter LinkedIn post content:"
read POST_TEXT

if [ -z "$POST_TEXT" ]; then echo "❌ Post content cannot be empty!"; exit 1; fi

echo "💼 Posting to LinkedIn..."
curl -s -X POST "https://api.linkedin.com/v2/ugcPosts" \
     -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{
           \"author\": \"urn:li:person:$LINKEDIN_USER_URN\",
           \"lifecycleState\": \"PUBLISHED\",
           \"specificContent\": {
             \"com.linkedin.ugc.ShareContent\": {
               \"shareCommentary\": { \"text\": \"$POST_TEXT\" },
               \"shareMediaCategory\": \"NONE\"
             }
           },
           \"visibility\": {
             \"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"
           }
         }" \
     -o /dev/null
echo "✅ LinkedIn post complete."
