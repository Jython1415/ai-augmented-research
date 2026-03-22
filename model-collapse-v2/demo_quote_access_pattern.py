# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "atproto",
#     "httpx[socks]",
# ]
# ///
"""
Demonstration of the working pattern to extract quoted post text from Bluesky API.

This shows the exact API structure and how to access the quoted post content.
"""

import sqlite3
import json
from pathlib import Path
from atproto import Client

# Load credentials
env_path = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/.env")
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            env_vars[key] = value

# Initialize client
client = Client()
username = env_vars.get("BSKY_HANDLE")
password = env_vars.get("BSKY_APP_PASSWORD")

print(f"Logging in as {username}...")
client.login(username, password)
print("Logged in successfully!\n")

# Connect to database
db_path = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Find posts with quote embeds
print("=" * 80)
print("DEMONSTRATION: Working Pattern for Accessing Quoted Post Text")
print("=" * 80)
print()

cursor.execute("SELECT uri FROM posts LIMIT 200")
posts = [row[0] for row in cursor.fetchall()]

quote_count = 0
for uri in posts:
    if quote_count >= 3:  # Show 3 examples
        break

    try:
        # Step 1: Fetch the post thread
        response = client.app.bsky.feed.get_post_thread({
            "uri": uri,
            "depth": 0,      # Don't fetch thread depth (saves API calls)
            "parentHeight": 1 # Only get immediate parent if it's a reply
        })
        thread = response.thread
        post = thread.post

        # Step 2: Access the embed
        record = post.record
        embed = getattr(record, 'embed', None)

        if not embed:
            continue

        # Step 3: Convert to dict for easier access
        if hasattr(embed, 'model_dump'):
            embed_dict = embed.model_dump()
        else:
            embed_dict = vars(embed)

        # Step 4: Check if this is a quote post
        if 'record' not in embed_dict or not embed_dict['record']:
            continue

        quote_count += 1
        print(f"Example {quote_count}:")
        print(f"=" * 80)
        print(f"Original post URI: {post.uri}")
        print(f"Original post text: {post.record.text}\n")

        # Step 5: Access the quoted post info
        quote_ref = embed_dict['record']
        print(f"Quoted post reference:")
        print(f"  URI: {quote_ref.get('uri')}")
        print(f"  CID: {quote_ref.get('cid')}")

        # Step 6: To get the quoted post's TEXT, we need to fetch it separately
        # because the API returns just the reference, not the full post content
        quoted_uri = quote_ref.get('uri')
        if quoted_uri:
            print(f"\nFetching the quoted post's full content...")
            try:
                # Use get_post_thread to fetch the quoted post
                quoted_response = client.app.bsky.feed.get_post_thread({
                    "uri": quoted_uri,
                    "depth": 0,
                    "parentHeight": 0
                })
                quoted_post = quoted_response.thread.post

                print(f"\nQuoted post details:")
                print(f"  Author: {quoted_post.author.handle}")
                print(f"  Text: {quoted_post.record.text}")
                print(f"  Created: {quoted_post.record.created_at}")

                # Check if quoted post has its own embeds
                quoted_embed = getattr(quoted_post.record, 'embed', None)
                if quoted_embed:
                    print(f"  Has embed: Yes")
                else:
                    print(f"  Has embed: No")

            except Exception as e:
                print(f"  Error fetching quoted post: {e}")

        print()

    except Exception as e:
        continue

conn.close()

print("=" * 80)
print("SUMMARY OF WORKING PATTERN")
print("=" * 80)
print("""
To extract quoted post text from the Bluesky API:

1. Fetch post thread:
   response = client.app.bsky.feed.get_post_thread({
       "uri": uri,
       "depth": 0,
       "parentHeight": 1
   })
   post = response.thread.post

2. Access the embed:
   embed = getattr(post.record, 'embed', None)
   if not embed:
       return  # No embed

3. Convert to dict:
   embed_dict = embed.model_dump()  # or vars(embed)

4. Check for quote post (look for 'record' key):
   if 'record' not in embed_dict or not embed_dict['record']:
       return  # Not a quote post

5. Get the quoted post reference:
   quote_ref = embed_dict['record']
   quoted_uri = quote_ref.get('uri')

6. Fetch the full quoted post:
   quoted_response = client.app.bsky.feed.get_post_thread({
       "uri": quoted_uri,
       "depth": 0,
       "parentHeight": 0
   })
   quoted_post = quoted_response.thread.post
   quoted_text = quoted_post.record.text

NOTE: The API returns a strongRef (URI + CID) for quoted posts, not the full
content. You must fetch the quoted post separately to get its text.

EMBED TYPES IN BLUESKY:
- 'record': Quote post (contains URI/CID of quoted post)
- 'external': External link with preview
- 'images': Image attachments (array)
- 'media': Video/GIF media

Multiple embed types can coexist (e.g., quote + images).
""")
