#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["atproto", "httpx[socks]"]
# ///
"""
Fetch thread context for citation units using the Bluesky API.

For each citation unit, fetches the full thread structure including:
- Parent chain (up to 5 levels for non-author parents, unlimited for author's own)
- The anchor post itself
- Author's self-replies (follow-up posts by same author)
- Direct reply children (1 level)

Thread context is stored in the thread_context table with relationship types:
- 'parent', 'grandparent', etc. for ancestor posts
- 'self_reply' for author's own follow-up posts
- 'reply_child' for direct replies to the anchor post

Environment variables required:
  BSKY_HANDLE: Bluesky handle (e.g., user.bsky.social)
  BSKY_APP_PASSWORD: App password for authentication

Usage:
  # Fetch thread context for 10 citation units that don't have context yet
  uv run --script fetch_thread_context.py

  # Fetch thread context for up to 50 units
  uv run --script fetch_thread_context.py --limit 50

  # Test mode: fetch and print context for a single post URI
  uv run --script fetch_thread_context.py --test-uri at://did:plc:.../app.bsky.feed.post/...

  # Dry run: show what would be fetched without writing to database
  uv run --script fetch_thread_context.py --limit 5 --dry-run
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from atproto import Client


def get_credentials() -> tuple[str, str]:
    """Load credentials from environment variables."""
    handle = os.getenv("BSKY_HANDLE")
    password = os.getenv("BSKY_APP_PASSWORD")

    if not handle or not password:
        raise ValueError(
            "Missing credentials. Set BSKY_HANDLE and BSKY_APP_PASSWORD environment variables."
        )

    return handle, password


def init_client(handle: str, password: str) -> Client:
    """Initialize and authenticate AT Protocol client."""
    client = Client()
    client.login(handle, password)
    print(f"✓ Authenticated as {handle}")
    return client


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Get SQLite database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_citation_units_needing_context(
    conn: sqlite3.Connection, limit: int
) -> list[tuple[int, str, str]]:
    """
    Get citation units that don't have thread context yet.

    Returns list of (id, anchor_post_uri, author_did) tuples.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT cu.id, cu.anchor_post_uri, cu.author_did
        FROM citation_units cu
        LEFT JOIN thread_context tc ON cu.id = tc.citation_unit_id
        WHERE tc.citation_unit_id IS NULL
        LIMIT ?
        """,
        (limit,)
    )
    return cursor.fetchall()


def extract_thread_context(
    thread_view,
    anchor_uri: str,
    anchor_author_did: str
) -> list[dict]:
    """
    Extract structured context from a thread view.

    Returns list of context post dicts with keys:
    - post_uri
    - post_cid
    - post_text
    - post_created_at
    - author_did
    - author_handle
    - relationship ('parent', 'self_reply', 'reply_child')
    - depth (distance from anchor post)
    """
    context_posts = []

    # Process parent chain (ancestors)
    parent_depth = 0
    current = thread_view

    while hasattr(current, 'parent') and current.parent:
        parent_depth += 1
        parent_view = current.parent

        # parent_view is a ThreadViewPost — data is under .post
        if not hasattr(parent_view, 'post') or not parent_view.post:
            break

        is_author_post = (parent_view.post.author.did == anchor_author_did)

        # Include: author's own parents (unlimited), or up to 5 levels of non-author parents
        if is_author_post or parent_depth <= 5:
            context_posts.append({
                "post_uri": parent_view.post.uri,
                "post_cid": parent_view.post.cid,
                "post_text": parent_view.post.record.text,
                "post_created_at": parent_view.post.record.created_at,
                "author_did": parent_view.post.author.did,
                "author_handle": parent_view.post.author.handle,
                "relationship": "parent",
                "depth": parent_depth,
            })

        current = parent_view

    # Reverse parent chain so they appear in chronological order (oldest first)
    context_posts.reverse()

    # Process direct replies (children) - 1 level only
    if hasattr(thread_view, 'replies') and thread_view.replies:
        for reply in thread_view.replies:
            # Check if this is a ThreadViewPost (has .post attribute)
            if not hasattr(reply, 'post') or not reply.post:
                continue

            is_self_reply = (reply.post.author.did == anchor_author_did)
            relationship = "self_reply" if is_self_reply else "reply_child"

            context_posts.append({
                "post_uri": reply.post.uri,
                "post_cid": reply.post.cid,
                "post_text": reply.post.record.text,
                "post_created_at": reply.post.record.created_at,
                "author_did": reply.post.author.did,
                "author_handle": reply.post.author.handle,
                "relationship": relationship,
                "depth": 1,
            })

    return context_posts


def fetch_thread(
    client: Client,
    post_uri: str,
    depth: int = 10,
    parent_height: int = 10
):
    """
    Fetch a thread from the Bluesky API.

    Args:
        client: Authenticated AT Protocol client
        post_uri: The post URI to fetch thread for
        depth: How many levels of replies to fetch (default 10)
        parent_height: How many levels of ancestors to fetch (default 10)

    Returns:
        ThreadViewPost object, or None if fetch fails
    """
    try:
        time.sleep(0.15)  # Rate limiting: 0.15s between requests

        response = client.app.bsky.feed.get_post_thread(
            {
                "uri": post_uri,
                "depth": depth,
                "parentHeight": parent_height,
            }
        )

        return response.thread

    except Exception as e:
        print(f"    ✗ Error fetching thread for {post_uri}: {e}")
        return None


def store_context_posts(
    conn: sqlite3.Connection,
    citation_unit_id: int,
    context_posts: list[dict]
) -> int:
    """
    Store context posts in the database.

    Returns the number of posts successfully stored.
    """
    cursor = conn.cursor()
    stored = 0

    for post in context_posts:
        try:
            cursor.execute(
                """
                INSERT INTO thread_context
                (citation_unit_id, post_uri, post_cid, post_text, post_created_at,
                 author_did, author_handle, relationship, depth)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    citation_unit_id,
                    post["post_uri"],
                    post["post_cid"],
                    post["post_text"],
                    post["post_created_at"],
                    post["author_did"],
                    post["author_handle"],
                    post["relationship"],
                    post["depth"],
                )
            )
            stored += 1
        except sqlite3.IntegrityError:
            # Post already exists for this citation unit - skip
            pass
        except Exception as e:
            print(f"      ✗ Error storing context post {post['post_uri']}: {e}")

    conn.commit()
    return stored


def format_context_for_display(context_posts: list[dict]) -> str:
    """Format context posts for stdout display."""
    output = []
    output.append("\n" + "=" * 80)
    output.append("THREAD CONTEXT")
    output.append("=" * 80)

    # Group by relationship type for readability
    by_relationship = {}
    for post in context_posts:
        rel = post["relationship"]
        if rel not in by_relationship:
            by_relationship[rel] = []
        by_relationship[rel].append(post)

    # Display in order: parents, anchor, self-replies, reply children
    order = ["parent", "self_reply", "reply_child"]

    for rel_type in order:
        if rel_type not in by_relationship:
            continue

        posts = by_relationship[rel_type]

        if rel_type == "parent":
            output.append("\n📜 PARENT CHAIN (predecessors):")
        elif rel_type == "self_reply":
            output.append("\n✍️  AUTHOR'S SELF-REPLIES (follow-ups):")
        elif rel_type == "reply_child":
            output.append("\n💬 DIRECT REPLIES (responses):")

        for post in posts:
            depth_label = f"[ancestor {post['depth']}]" if rel_type == "parent" else ""
            output.append(f"\n  {post['author_handle']} {depth_label}")
            output.append(f"  URI: {post['post_uri']}")
            output.append(f"  Created: {post['post_created_at']}")

            # Format text for display
            text = post["post_text"]
            if len(text) > 200:
                text = text[:200] + "..."
            output.append(f"  Text: {text}")

    output.append("\n" + "=" * 80 + "\n")
    return "\n".join(output)


def run_test_mode(client: Client, test_uri: str) -> int:
    """
    Test mode: fetch and print thread context for a single post.

    Args:
        client: Authenticated AT Protocol client
        test_uri: Post URI to test

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("\n" + "=" * 80)
    print("TEST MODE: Fetching thread context")
    print("=" * 80)
    print(f"Post URI: {test_uri}\n")

    # Fetch the thread
    print("Fetching thread...")
    thread = fetch_thread(client, test_uri, depth=10, parent_height=10)

    if not thread:
        print("✗ Failed to fetch thread")
        return 1

    # Extract context — thread is a ThreadViewPost, data under .post
    anchor_author_did = thread.post.author.did
    context_posts = extract_thread_context(thread, test_uri, anchor_author_did)

    # Display
    print(format_context_for_display(context_posts))
    print(f"✓ Fetched {len(context_posts)} context posts")

    return 0


def run_full_mode(
    client: Client,
    db_path: str,
    limit: int,
    dry_run: bool = False
) -> int:
    """
    Main mode: fetch thread context for citation units and store in database.

    Args:
        client: Authenticated AT Protocol client
        db_path: Path to SQLite database
        limit: Maximum number of citation units to process
        dry_run: If True, show what would be fetched without writing to DB

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Connect to database
    try:
        conn = get_db_connection(str(db_path))
        print(f"✓ Connected to database: {db_path}")
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        return 1

    # Get citation units needing context
    try:
        units = get_citation_units_needing_context(conn, limit)
        print(f"✓ Found {len(units)} citation units needing context\n")
    except Exception as e:
        print(f"✗ Error querying citation units: {e}")
        conn.close()
        return 1

    if not units:
        print("No citation units found needing context")
        conn.close()
        return 0

    # Process each citation unit
    print("=" * 80)
    print("FETCHING THREAD CONTEXT")
    print("=" * 80)
    if dry_run:
        print("(DRY RUN - no database writes)\n")

    total_processed = 0
    total_context_posts = 0
    start_time = datetime.now()

    try:
        for unit_id, anchor_uri, author_did in units:
            total_processed += 1

            print(f"\n[{total_processed}/{len(units)}] Processing citation unit {unit_id}")
            print(f"      Anchor: {anchor_uri}")
            print(f"      Author: {author_did}")

            # Fetch the thread
            thread = fetch_thread(client, anchor_uri, depth=10, parent_height=10)

            if not thread:
                print(f"      ✗ Failed to fetch thread")
                continue

            # Extract context
            context_posts = extract_thread_context(thread, anchor_uri, author_did)
            print(f"      ✓ Extracted {len(context_posts)} context posts")

            if context_posts:
                # Show relationship breakdown
                rel_counts = {}
                for post in context_posts:
                    rel = post["relationship"]
                    rel_counts[rel] = rel_counts.get(rel, 0) + 1

                for rel, count in rel_counts.items():
                    print(f"         - {count} {rel}")

            # Store in database (unless dry run)
            if not dry_run:
                try:
                    stored = store_context_posts(conn, unit_id, context_posts)
                    print(f"      ✓ Stored {stored} posts in database")
                except Exception as e:
                    print(f"      ✗ Error storing context: {e}")

            total_context_posts += len(context_posts)

    except KeyboardInterrupt:
        print("\n⏸ Fetch interrupted by user")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        conn.close()
        return 1
    finally:
        conn.close()

    # Summary
    elapsed = datetime.now() - start_time
    print("\n" + "=" * 80)
    print("FETCH COMPLETE")
    print("=" * 80)
    print(f"Time elapsed: {elapsed}")
    print(f"Citation units processed: {total_processed}")
    print(f"Total context posts fetched: {total_context_posts}")
    if dry_run:
        print("(DRY RUN - database was not modified)")
    print("=" * 80 + "\n")

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch thread context for citation units using the Bluesky API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch context for 10 citation units (default)
  uv run --script fetch_thread_context.py

  # Fetch context for up to 50 units
  uv run --script fetch_thread_context.py --limit 50

  # Test mode: fetch and display context for a single post
  uv run --script fetch_thread_context.py --test-uri at://did:plc:xyz/app.bsky.feed.post/abc123

  # Dry run: show what would be fetched without writing to database
  uv run --script fetch_thread_context.py --limit 5 --dry-run
        """,
    )

    parser.add_argument(
        "--db",
        default="/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db",
        help="Path to SQLite database file (default: posts.db in data directory)",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of citation units to process in one run (default: 10)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fetched without writing to database",
    )

    parser.add_argument(
        "--test-uri",
        help="Test mode: fetch and display context for a single post URI (no database writes)",
    )

    args = parser.parse_args()

    # Setup
    print("=" * 80)
    print("Thread Context Fetcher for Bluesky Citations")
    print("=" * 80)

    # Load credentials
    try:
        handle, password = get_credentials()
    except ValueError as e:
        print(f"✗ {e}")
        return 1

    # Connect to AT Protocol
    try:
        client = init_client(handle, password)
    except Exception as e:
        print(f"✗ Failed to authenticate: {e}")
        return 1

    # Run appropriate mode
    if args.test_uri:
        return run_test_mode(client, args.test_uri)
    else:
        return run_full_mode(client, args.db, args.limit, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
