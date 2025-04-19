#!/bin/bash

source .env

# ========== UTILS ==========
prompt_text() {
    echo "📝 Enter post content:"
    read POST_TEXT
    if [ -z "$POST_TEXT" ]; then
        echo "❌ Post content is required!"
        exit 1
    fi
}

prompt_image_path() {
    echo "🖼️  Enter full image path:"
    read IMAGE_PATH
    if [ ! -f "$IMAGE_PATH" ]; then
        echo "❌ File not found!"
        exit 1
    fi
}

# ========== FACEBOOK ==========
post_to_facebook() {
    echo "📘 Posting to Facebook..."
    curl -s -X POST "https://graph.facebook.com/$FB_PAGE_ID/feed" \
        -d "message=$POST_TEXT" \
        -d "access_token=$FB_ACCESS_TOKEN" \
        -o /dev/null
    echo "✅ Facebook post complete."
}

# ========== X (TWITTER) ==========
post_to_x() {
    echo "🐦 Posting to X..."
    curl -s -X POST "https://api.twitter.com/2/tweets" \
        -H "Authorization: Bearer $X_BEARER_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"text\":\"$POST_TEXT\"}" \
        -o /dev/null
    echo "✅ X post complete."
}

# ========== INSTAGRAM ==========
post_to_instagram() {
    prompt_image_path
    echo "📸 Uploading image to Instagram..."
    MEDIA_ID=$(curl -s -X POST "https://graph.facebook.com/v18.0/$IG_USER_ID/media" \
        -d "caption=$POST_TEXT" \
        -d "image_url=$INSTAGRAM_IMAGE_URL" \
        -d "access_token=$FB_ACCESS_TOKEN" | jq -r '.id')

    curl -s -X POST "https://graph.facebook.com/v18.0/$IG_USER_ID/media_publish" \
        -d "creation_id=$MEDIA_ID" \
        -d "access_token=$FB_ACCESS_TOKEN" \
        -o /dev/null
    echo "✅ Instagram post complete."
}

# ========== LINKEDIN ==========
post_to_linkedin() {
    echo "📸 Add image? (y/n):"
    read IMAGE_YN
    if [[ "$IMAGE_YN" =~ ^[Yy]$ ]]; then
        prompt_image_path

        echo "📤 Registering image upload with LinkedIn..."
        REGISTER_RESPONSE=$(curl -s -X POST "https://api.linkedin.com/v2/assets?action=registerUpload" \
            -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{
                \"registerUploadRequest\": {
                    \"recipes\": [\"urn:li:digitalmediaRecipe:feedshare-image\"],
                    \"owner\": \"urn:li:person:$LINKEDIN_USER_URN\",
                    \"serviceRelationships\": [{
                        \"relationshipType\": \"OWNER\",
                        \"identifier\": \"urn:li:userGeneratedContent\"
                    }]
                }
            }")

        UPLOAD_URL=$(echo "$REGISTER_RESPONSE" | jq -r '.value.uploadMechanism["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"].uploadUrl')
        ASSET_URN=$(echo "$REGISTER_RESPONSE" | jq -r '.value.asset')

        curl -s -X PUT "$UPLOAD_URL" \
            -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
            -H "Content-Type: image/jpeg" \
            --data-binary "@$IMAGE_PATH" \
            -o /dev/null

        echo "💼 Posting to LinkedIn with image..."
        curl -s -X POST "https://api.linkedin.com/v2/ugcPosts" \
            -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{
                \"author\": \"urn:li:person:$LINKEDIN_USER_URN\",
                \"lifecycleState\": \"PUBLISHED\",
                \"specificContent\": {
                    \"com.linkedin.ugc.ShareContent\": {
                        \"shareCommentary\": { \"text\": \"$POST_TEXT\" },
                        \"shareMediaCategory\": \"IMAGE\",
                        \"media\": [{
                            \"status\": \"READY\",
                            \"media\": \"$ASSET_URN\",
                            \"title\": { \"text\": \"Upload\" }
                        }]
                    }
                },
                \"visibility\": {
                    \"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"
                }
            }" \
            -o /dev/null
    else
        echo "💼 Posting text-only to LinkedIn..."
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
    fi
    echo "✅ LinkedIn post complete."
}

# ========== MAIN MENU ==========
clear
echo "==============================="
echo "  🛰️  Social Media Terminal App"
echo "     by Benjamin Miller"
echo "==============================="

prompt_text

echo ""
echo "📡 Choose where to post:"
echo "1. Facebook"
echo "2. X (Twitter)"
echo "3. Instagram"
echo "4. LinkedIn"
echo "5. All"
read -p "Enter choice: " CHOICE

case $CHOICE in
    1) post_to_facebook ;;
    2) post_to_x ;;
    3) post_to_instagram ;;
    4) post_to_linkedin ;;
    5)
        post_to_facebook
        post_to_x
        post_to_instagram
        post_to_linkedin
        ;;
    *) echo "❌ Invalid choice." ;;
esac

echo "🎉 Done!"
