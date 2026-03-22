# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "atproto",
#     "httpx[socks]",
# ]
# ///
"""
Deep dive into quote post JSON structure.
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

# Get some posts that definitely have embeds
cursor.execute("""
    SELECT uri FROM posts LIMIT 50
""")
posts = [row[0] for row in cursor.fetchall()]

found_quote = False
found_record_embed = False

for uri in posts:
    if found_quote and found_record_embed:
        break

    try:
        response = client.app.bsky.feed.get_post_thread({"uri": uri, "depth": 0, "parentHeight": 1})
        thread = response.thread
        post = thread.post

        record = post.record if hasattr(post, 'record') else None
        if record:
            embed_attr = getattr(record, 'embed', None)
            if embed_attr:
                if hasattr(embed_attr, 'model_dump'):
                    embed_dict = embed_attr.model_dump()
                else:
                    embed_dict = vars(embed_attr) if embed_attr else {}

                # Look for 'record' key which indicates quote post
                if 'record' in embed_dict and embed_dict['record'] and not found_record_embed:
                    found_record_embed = True
                    print("=" * 80)
                    print(f"FOUND POST WITH 'record' EMBED: {uri}")
                    print("=" * 80)
                    print(f"Post text: {post.record.text[:100]}")
                    print(f"\nEmbed 'record' type: {type(embed_dict['record'])}")
                    print(f"Embed 'record' content:\n{json.dumps(embed_dict['record'], indent=2, default=str)}")
                    print()

    except Exception as e:
        pass

conn.close()
