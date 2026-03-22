#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "atproto",
#     "httpx[socks]",
#     "python-dotenv",
# ]
# ///
"""
Test new candidate search terms for model collapse posts on Bluesky.
Identifies unique posts not already in the collection.
"""

import os
import sqlite3
import sys
from pathlib import Path

from atproto import Client
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

BSKY_HANDLE = os.getenv("BSKY_HANDLE")
BSKY_APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")
DB_PATH = Path(__file__).parent / "posts.db"

# Candidate terms to test
CANDIDATE_TERMS = [
    "Habsburg AI",
    "model autophagy",
    "curse of recursion",
    "AI eating itself",
    "digital inbreeding",
    "self-consuming generative",
    "AI cannibalism",
    "trained on AI data",
    "AI trained on AI",
    "data collapse AI",
    "synthetic data collapse",
    "AI ouroboros",
    "AI feeding on itself",
]


def load_existing_uris() -> set:
    """Load all existing post URIs from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT uri FROM posts")
    uris = {row[0] for row in cursor.fetchall()}
    conn.close()
    return uris


def search_bluesky(client: Client, term: str, pages: int = 2) -> list:
    """Search Bluesky for a term and return all posts from specified pages."""
    posts = []
    cursor = None

    for page in range(pages):
        try:
            params = {"q": term, "limit": 50}
            if cursor:
                params["cursor"] = cursor

            response = client.app.bsky.feed.search_posts(params)

            if response.posts:
                posts.extend(response.posts)
                if response.cursor:
                    cursor = response.cursor
                else:
                    break
            else:
                break
        except Exception as e:
            print(f"  Error fetching page {page + 1}: {e}")
            break

    return posts


def main():
    """Main execution."""
    if not BSKY_HANDLE or not BSKY_APP_PASSWORD:
        print("Error: BSKY_HANDLE and BSKY_APP_PASSWORD not set in .env")
        sys.exit(1)

    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)

    # Load existing URIs
    print("Loading existing posts from database...")
    existing_uris = load_existing_uris()
    print(f"Found {len(existing_uris)} existing posts in database\n")

    # Authenticate with Bluesky
    print("Authenticating with Bluesky...")
    client = Client()
    try:
        client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)
        print(f"Authenticated as {BSKY_HANDLE}\n")
    except Exception as e:
        print(f"Error authenticating: {e}")
        sys.exit(1)

    # Test each candidate term
    results = {}
    for term in CANDIDATE_TERMS:
        print(f"Testing: '{term}'")
        posts = search_bluesky(client, term, pages=2)

        unique_posts = [p for p in posts if p.uri not in existing_uris]
        results[term] = {
            "total": len(posts),
            "unique": len(unique_posts),
            "posts": unique_posts,
        }

        print(f"  Total results: {len(posts)}")
        print(f"  Unique (not in DB): {len(unique_posts)}")

        # Print up to 5 unique posts
        if unique_posts:
            print(f"  Sample unique posts:")
            for i, post in enumerate(unique_posts[:5], 1):
                text = post.record.text[:100].replace("\n", " ")
                author = post.author.handle
                print(f"    {i}. @{author}: {text}...")
        print()

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_results = sum(r["total"] for r in results.values())
    total_unique = sum(r["unique"] for r in results.values())

    print(f"Total posts found: {total_results}")
    print(f"Total unique posts: {total_unique}")
    print()

    # Sort by number of unique posts
    sorted_results = sorted(
        results.items(), key=lambda x: x[1]["unique"], reverse=True
    )
    print("Results by unique count:")
    for term, data in sorted_results:
        print(f"  {term:30s} | Total: {data['total']:3d} | Unique: {data['unique']:3d}")


if __name__ == "__main__":
    main()
