# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "atproto",
#     "httpx[socks]",
# ]
# ///
"""
Comprehensive analysis of embeds in posts database.
Estimates percentage of quote posts, external links, images.
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

# Get total posts
cursor.execute("SELECT COUNT(*) FROM posts")
total_posts = cursor.fetchone()[0]
print(f"Total posts in database: {total_posts}\n")

# Sample posts (stratified: some from beginning, middle, end to reduce API load)
cursor.execute("""
    SELECT uri FROM posts
    WHERE id % 100 = 0  -- Sample every 100th post
    LIMIT 100
""")
sample_posts = [row[0] for row in cursor.fetchall()]
print(f"Sample size: {len(sample_posts)} posts\n")

# Analysis results
stats = {
    'total_sampled': 0,
    'with_embed': 0,
    'quote_posts': 0,
    'external_links': 0,
    'images': 0,
    'media': 0,
    'multiple_embeds': 0,
    'errors': 0
}

# Track sample posts for detailed reporting
sample_details = []

print("=" * 80)
print("ANALYZING POSTS")
print("=" * 80)

for idx, uri in enumerate(sample_posts, 1):
    try:
        response = client.app.bsky.feed.get_post_thread({"uri": uri, "depth": 0, "parentHeight": 1})
        thread = response.thread
        post = thread.post

        stats['total_sampled'] += 1

        record = post.record if hasattr(post, 'record') else None
        if not record:
            continue

        embed_attr = getattr(record, 'embed', None)
        if not embed_attr:
            continue

        stats['with_embed'] += 1

        # Get embed as dict
        if hasattr(embed_attr, 'model_dump'):
            embed_dict = embed_attr.model_dump()
        else:
            embed_dict = vars(embed_attr) if embed_attr else {}

        embed_types_found = []

        # Check for quote posts
        # In atproto API, quote posts have 'record' key with a strongRef
        if 'record' in embed_dict and embed_dict['record']:
            stats['quote_posts'] += 1
            embed_types_found.append('quote')

        # Check for external links
        if 'external' in embed_dict and embed_dict['external']:
            stats['external_links'] += 1
            embed_types_found.append('external')

        # Check for images
        if 'images' in embed_dict and embed_dict['images']:
            stats['images'] += 1
            embed_types_found.append('images')

        # Check for media
        if 'media' in embed_dict and embed_dict['media']:
            stats['media'] += 1
            embed_types_found.append('media')

        # Track multiple embeds
        if len(embed_types_found) > 1:
            stats['multiple_embeds'] += 1

        # Store first few samples for detailed output
        if idx <= 10 and embed_types_found:
            sample_details.append({
                'uri': uri,
                'text': post.record.text[:80],
                'embed_types': embed_types_found
            })

        if idx % 20 == 0:
            print(f"  [{idx}/{len(sample_posts)}] Processed {idx} posts...")

    except Exception as e:
        stats['errors'] += 1
        if idx <= 10:
            print(f"  [{idx}] ERROR: {e}")

print()
print("=" * 80)
print("RESULTS")
print("=" * 80)
print(f"\nSample statistics:")
print(f"  Total sampled: {stats['total_sampled']}")
print(f"  With embed: {stats['with_embed']}")
print(f"  Errors: {stats['errors']}")

if stats['with_embed'] > 0:
    print(f"\nEmbed breakdown (of {stats['with_embed']} posts with embeds):")
    print(f"  Quote posts: {stats['quote_posts']} ({100*stats['quote_posts']/stats['with_embed']:.1f}%)")
    print(f"  External links: {stats['external_links']} ({100*stats['external_links']/stats['with_embed']:.1f}%)")
    print(f"  Images: {stats['images']} ({100*stats['images']/stats['with_embed']:.1f}%)")
    print(f"  Media: {stats['media']} ({100*stats['media']/stats['with_embed']:.1f}%)")
    print(f"  Multiple embeds: {stats['multiple_embeds']}")

# Scale to full database
print(f"\nEstimated scale for full database ({total_posts} posts):")
if stats['total_sampled'] > 0:
    embed_percentage = 100 * stats['with_embed'] / stats['total_sampled']
    print(f"  Estimated posts with embeds: ~{int(total_posts * embed_percentage / 100)} ({embed_percentage:.1f}%)")

    if stats['with_embed'] > 0:
        quote_percentage = 100 * stats['quote_posts'] / stats['total_sampled']
        external_percentage = 100 * stats['external_links'] / stats['total_sampled']
        image_percentage = 100 * stats['images'] / stats['total_sampled']

        print(f"  Estimated quote posts: ~{int(total_posts * quote_percentage / 100)} ({quote_percentage:.1f}%)")
        print(f"  Estimated external links: ~{int(total_posts * external_percentage / 100)} ({external_percentage:.1f}%)")
        print(f"  Estimated images: ~{int(total_posts * image_percentage / 100)} ({image_percentage:.1f}%)")

print(f"\nSample posts with embeds (first 10):")
for detail in sample_details[:10]:
    print(f"  {detail['uri']}")
    print(f"    Text: {detail['text']}")
    print(f"    Embed types: {', '.join(detail['embed_types'])}")

conn.close()
