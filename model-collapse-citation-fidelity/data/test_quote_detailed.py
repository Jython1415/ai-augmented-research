# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "atproto",
#     "httpx[socks]",
# ]
# ///
"""
Detailed analysis of quote posts in the Bluesky API.
Focuses on understanding the JSON structure returned by the API.
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

if not username or not password:
    raise ValueError("Missing BSKY_HANDLE or BSKY_APP_PASSWORD in .env")

print(f"Logging in as {username}...")
client.login(username, password)
print("Logged in successfully!\n")

# Connect to database
db_path = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get some posts to analyze
cursor.execute("""
    SELECT uri FROM posts LIMIT 20
""")
posts = [row[0] for row in cursor.fetchall()]
print(f"Analyzing {len(posts)} random posts...\n")

quote_post_count = 0
external_count = 0
image_count = 0
media_count = 0

for idx, uri in enumerate(posts[:10], 1):
    try:
        response = client.app.bsky.feed.get_post_thread({"uri": uri, "depth": 0, "parentHeight": 1})
        thread = response.thread
        post = thread.post

        print(f"[{idx}] URI: {uri}")

        # Get the raw data structure
        try:
            # Try to get the record and embed info
            record = post.record if hasattr(post, 'record') else None
            if record:
                # Check for embed in the record
                embed_attr = getattr(record, 'embed', None)
                if embed_attr:
                    print(f"    Found record.embed: {type(embed_attr).__name__}")

                    # Try to dump it
                    if hasattr(embed_attr, 'model_dump'):
                        embed_dict = embed_attr.model_dump()
                    else:
                        embed_dict = vars(embed_attr) if embed_attr else {}

                    print(f"    Embed keys: {list(embed_dict.keys())}")

                    # Look for quote structure
                    if 'quote' in embed_dict and embed_dict['quote']:
                        quote_post_count += 1
                        print(f"    *** HAS QUOTE POST ***")
                        quote = embed_dict['quote']
                        if isinstance(quote, dict):
                            print(f"        Quote URI: {quote.get('uri', 'N/A')}")
                            if 'record' in quote:
                                rec = quote['record']
                                if 'value' in rec:
                                    val = rec['value']
                                    if isinstance(val, dict) and 'text' in val:
                                        print(f"        Quoted text: {val['text'][:80]}")

                    if 'external' in embed_dict and embed_dict['external']:
                        external_count += 1
                        ext = embed_dict['external']
                        if isinstance(ext, dict):
                            print(f"    External link: {ext.get('uri', 'N/A')}")

                    if 'images' in embed_dict and embed_dict['images']:
                        image_count += 1
                        print(f"    Images: {len(embed_dict['images'])}")

                    if 'media' in embed_dict and embed_dict['media']:
                        media_count += 1
                        print(f"    Has media")

        except Exception as e:
            print(f"    Error parsing embed: {e}")

        print()

    except Exception as e:
        print(f"[{idx}] ERROR: {e}\n")

# Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Posts analyzed: {len(posts[:10])}")
print(f"Posts with quote embeds: {quote_post_count}")
print(f"Posts with external links: {external_count}")
print(f"Posts with images: {image_count}")
print(f"Posts with media: {media_count}")

conn.close()
