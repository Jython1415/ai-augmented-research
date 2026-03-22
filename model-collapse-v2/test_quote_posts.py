#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "atproto",
#     "httpx[socks]",
# ]
# ///

import sqlite3
from pathlib import Path
from atproto import Client

# Load credentials from .env
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

# Query 1: Posts that look like they might have quotes or embeds
print("=" * 80)
print("QUERY 1: Posts with quote/RT indicators")
print("=" * 80)
cursor.execute("""
    SELECT uri FROM posts
    WHERE text LIKE '%quote%' OR text LIKE '%RT%' OR text LIKE '%this%'
    ORDER BY RANDOM()
    LIMIT 5
""")
quote_posts = [row[0] for row in cursor.fetchall()]
print(f"Found {len(quote_posts)} posts with quote indicators:")
for uri in quote_posts:
    print(f"  {uri}")

# Query 2: Posts with reply_to_uri (likely replies)
print("\n" + "=" * 80)
print("QUERY 2: Reply posts")
print("=" * 80)
cursor.execute("""
    SELECT uri FROM posts
    WHERE reply_to_uri IS NOT NULL
    ORDER BY RANDOM()
    LIMIT 5
""")
reply_posts = [row[0] for row in cursor.fetchall()]
print(f"Found {len(reply_posts)} reply posts:")
for uri in reply_posts:
    print(f"  {uri}")

# Combine and process all posts
all_posts = quote_posts + reply_posts
embed_count = 0
embed_types = {}

print("\n" + "=" * 80)
print("FETCHING AND INSPECTING POSTS")
print("=" * 80)

for idx, uri in enumerate(all_posts, 1):
    try:
        print(f"\n[{idx}/{len(all_posts)}] Fetching: {uri}")

        response = client.app.bsky.feed.get_post_thread({"uri": uri, "depth": 0, "parentHeight": 1})
        thread = response.thread
        post = thread.post

        print(f"  Text: {post.record.text[:80]}")

        has_embed = hasattr(post, 'embed') and post.embed is not None
        print(f"  Has embed: {has_embed}")

        if has_embed:
            embed_count += 1
            embed_type_name = type(post.embed).__name__
            embed_types[embed_type_name] = embed_types.get(embed_type_name, 0) + 1
            print(f"  Embed type: {embed_type_name}")

            # Dump the entire embed structure as JSON
            try:
                embed_dict = post.embed.model_dump() if hasattr(post.embed, 'model_dump') else vars(post.embed)
                print(f"  Embed structure keys: {list(embed_dict.keys())}")

                # Check for quote post structure
                if 'quote' in embed_dict:
                    quote_data = embed_dict['quote']
                    print(f"    QUOTE FOUND!")
                    print(f"    Quote URI: {quote_data.get('uri', 'N/A')}")
                    if 'record' in quote_data:
                        quoted_record = quote_data['record']
                        if 'value' in quoted_record and 'text' in quoted_record['value']:
                            print(f"    Quoted text: {quoted_record['value']['text'][:100]}")

                # Check for external links
                if 'external' in embed_dict:
                    external = embed_dict['external']
                    print(f"    External URL: {external.get('uri', 'N/A')}")

                # Check for images
                if 'images' in embed_dict:
                    images = embed_dict['images']
                    print(f"    Images count: {len(images) if isinstance(images, list) else 'N/A'}")

                # Check for media
                if 'media' in embed_dict:
                    print(f"    Has media")

            except Exception as e:
                print(f"  Error inspecting embed: {e}")

    except Exception as e:
        print(f"  ERROR: {e}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total posts sampled: {len(all_posts)}")
print(f"Posts with embeds: {embed_count}")
print(f"Percentage with embeds: {(embed_count / len(all_posts) * 100):.1f}%")
print(f"\nEmbed types found:")
for embed_type, count in sorted(embed_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {embed_type}: {count}")

conn.close()
