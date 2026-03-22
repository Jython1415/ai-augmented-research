#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["atproto", "httpx[socks]", "python-dotenv"]
# ///

import sqlite3
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from atproto import Client
import argparse


def create_post_context_table(db_path: str) -> None:
    """Create post_context table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_context (
            post_id INTEGER PRIMARY KEY,
            parent_text TEXT,
            parent_author TEXT,
            quoted_text TEXT,
            quoted_author TEXT,
            has_external_link INTEGER DEFAULT 0,
            fetched_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (post_id) REFERENCES posts(id)
        )
    """)
    conn.commit()
    conn.close()


def get_posts_without_context(db_path: str, limit: int = None) -> list:
    """Query posts that don't have context yet."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if limit:
        cursor.execute("""
            SELECT p.id, p.uri FROM posts p
            LEFT JOIN post_context pc ON p.id = pc.post_id
            WHERE pc.post_id IS NULL
            ORDER BY p.id
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT p.id, p.uri FROM posts p
            LEFT JOIN post_context pc ON p.id = pc.post_id
            WHERE pc.post_id IS NULL
            ORDER BY p.id
        """)

    posts = cursor.fetchall()
    conn.close()
    return posts


def insert_post_context(db_path: str, post_id: int, parent_text: str = None,
                       parent_author: str = None, quoted_text: str = None,
                       quoted_author: str = None, has_external_link: int = 0) -> None:
    """Insert or update post context."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO post_context
        (post_id, parent_text, parent_author, quoted_text, quoted_author, has_external_link)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (post_id, parent_text, parent_author, quoted_text, quoted_author, has_external_link))
    conn.commit()
    conn.close()


def fetch_post_thread(client: Client, uri: str) -> dict:
    """Fetch post thread with parent and quoted post context."""
    context = {
        "parent_text": None,
        "parent_author": None,
        "quoted_text": None,
        "quoted_author": None,
        "has_external_link": 0,
        "error": None
    }

    try:
        time.sleep(0.15)
        response = client.app.bsky.feed.get_post_thread({
            "uri": uri,
            "depth": 0,
            "parentHeight": 1
        })
        thread = response.thread

        # Extract parent text and author
        if hasattr(thread, 'parent') and thread.parent and hasattr(thread.parent, 'post') and thread.parent.post:
            try:
                context["parent_text"] = thread.parent.post.record.text
                context["parent_author"] = thread.parent.post.author.handle
            except Exception as e:
                pass

        # Extract quoted post text and author
        if hasattr(thread, 'post') and thread.post and hasattr(thread.post, 'record') and thread.post.record:
            embed = getattr(thread.post.record, 'embed', None)
            if embed:
                embed_dict = embed.model_dump()

                # Check for external link
                if 'external' in str(embed_dict.get('py_type', '')).lower():
                    context["has_external_link"] = 1

                # Check for quote post
                if 'record' in embed_dict and embed_dict['record']:
                    quote_uri = embed_dict['record'].get('uri')
                    if quote_uri:
                        try:
                            time.sleep(0.15)
                            quoted_response = client.app.bsky.feed.get_post_thread({
                                "uri": quote_uri,
                                "depth": 0,
                                "parentHeight": 0
                            })
                            context["quoted_text"] = quoted_response.thread.post.record.text
                            context["quoted_author"] = quoted_response.thread.post.author.handle
                        except Exception as e:
                            # Silently fail on quoted post fetch
                            pass

    except Exception as e:
        context["error"] = str(e)

    return context


def main():
    parser = argparse.ArgumentParser(description="Fetch parent and quoted post context for all posts")
    parser.add_argument("--db", type=str, default="/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db",
                       help="Path to posts.db")
    parser.add_argument("--limit", type=int, default=None,
                       help="Max posts to process")
    parser.add_argument("--skip-quotes", action="store_true",
                       help="Skip fetching quoted posts (faster, parent-only)")

    args = parser.parse_args()

    # Load environment
    env_path = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/.env")
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)

    # Initialize client
    username = os.getenv("BSKY_HANDLE")
    password = os.getenv("BSKY_APP_PASSWORD")

    if not username or not password:
        print("Error: BSKY_HANDLE or BSKY_APP_PASSWORD not set in .env")
        sys.exit(1)

    client = Client()
    try:
        client.login(username, password)
    except Exception as e:
        print(f"Error: Failed to login to Bluesky: {e}")
        sys.exit(1)

    # Create table
    create_post_context_table(args.db)

    # Get posts without context
    posts = get_posts_without_context(args.db, args.limit)
    total = len(posts)

    if total == 0:
        print("No posts need context fetching")
        return

    print(f"Fetching context for {total} posts...")

    stats = {
        "with_parent": 0,
        "with_quote": 0,
        "errors": 0,
        "processed": 0
    }

    for idx, (post_id, uri) in enumerate(posts, 1):
        context = fetch_post_thread(client, uri)

        if args.skip_quotes:
            context["quoted_text"] = None
            context["quoted_author"] = None

        insert_post_context(
            args.db,
            post_id,
            parent_text=context["parent_text"],
            parent_author=context["parent_author"],
            quoted_text=context["quoted_text"],
            quoted_author=context["quoted_author"],
            has_external_link=context["has_external_link"]
        )

        if context["parent_text"]:
            stats["with_parent"] += 1
        if context["quoted_text"]:
            stats["with_quote"] += 1
        if context["error"]:
            stats["errors"] += 1

        stats["processed"] += 1

        # Progress output
        if idx % 100 == 0 or idx == total:
            print(f"[{idx}/{total}] Fetched context: {stats['with_parent']} with parent, "
                  f"{stats['with_quote']} with quote, {stats['errors']} errors")

    print("\n=== Final Summary ===")
    print(f"Total processed: {stats['processed']}")
    print(f"Posts with parent: {stats['with_parent']}")
    print(f"Posts with quoted post: {stats['with_quote']}")
    print(f"Errors encountered: {stats['errors']}")


if __name__ == "__main__":
    main()
