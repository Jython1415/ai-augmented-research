#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["atproto"]
# ///
"""
Collect Bluesky posts about model collapse using AT Protocol API.

Searches for multiple terms related to model collapse, deduplicates by URI,
and stores results in SQLite database.

Environment variables required:
  BSKY_HANDLE: Bluesky handle (e.g., user.bsky.social)
  BSKY_APP_PASSWORD: App password for authentication
"""

import os
import sqlite3
import time
from datetime import datetime
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


def post_exists(conn: sqlite3.Connection, uri: str) -> bool:
    """Check if post already exists in database."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM posts WHERE uri = ?", (uri,))
    return cursor.fetchone() is not None


def insert_post(
    conn: sqlite3.Connection,
    uri: str,
    cid: str,
    text: str,
    created_at: str,
    author_did: str,
    author_handle: str,
    reply_to_uri: Optional[str],
    search_term: str,
) -> bool:
    """Insert post into database. Returns True if inserted, False if skipped (duplicate)."""
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO posts
            (uri, cid, text, created_at, author_did, author_handle, reply_to_uri, source, search_term_matched)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                uri,
                cid,
                text,
                created_at,
                author_did,
                author_handle,
                reply_to_uri,
                "api",
                search_term,
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # URI already exists - deduplicate
        return False


def extract_reply_uri(post) -> Optional[str]:
    """Extract reply parent URI if this post is a reply."""
    if hasattr(post, "reply") and post.reply:
        if hasattr(post.reply, "parent") and post.reply.parent:
            return post.reply.parent.uri
    return None


def search_posts(
    client: Client,
    search_term: str,
    since_date: str = "2023-05-01T00:00:00Z",
    limit_per_page: int = 100,
    max_requests: int = None,
) -> list:
    """
    Search for posts using a single search term with pagination.

    Args:
        client: Authenticated AT Protocol client
        search_term: Search query string
        since_date: ISO 8601 date string for start of range
        limit_per_page: Posts per request (max 100)
        max_requests: Maximum number of requests (None for unlimited)

    Yields:
        Post objects from search results
    """
    cursor = None
    request_count = 0
    posts_this_term = 0

    print(f"\n🔍 Searching for: '{search_term}'")

    while True:
        if max_requests and request_count >= max_requests:
            print(f"  Reached max requests limit ({max_requests})")
            break

        try:
            # Small delay to respect rate limits (3000 req / 5 min = 1 req per 0.1s)
            time.sleep(0.15)

            response = client.app.bsky.feed.search_posts(
                {
                    "q": search_term,
                    "since": since_date,
                    "cursor": cursor,
                    "limit": limit_per_page,
                }
            )

            request_count += 1
            posts = response.posts if response.posts else []

            if not posts:
                print(f"  No results on request {request_count}")
                break

            print(f"  Request {request_count}: {len(posts)} posts")
            posts_this_term += len(posts)

            for post in posts:
                yield post, search_term

            # Check for next page
            if response.cursor:
                cursor = response.cursor
            else:
                print(f"  ✓ Reached end of results for '{search_term}' ({posts_this_term} posts)")
                break

        except Exception as e:
            print(f"  ✗ Error during search: {e}")
            break

    return posts_this_term


def main():
    """Main collection workflow."""
    # Configuration
    search_terms = [
        "model collapse",
        "tail collapse",
        "shumailov",
        "training on synthetic data",
        "trained on AI-generated",
        "recursive training",
    ]
    db_path = "/Users/Joshua/agent/model-collapse-study/data/posts.db"
    since_date = "2023-05-01T00:00:00Z"

    # Setup
    print("=" * 60)
    print("Model Collapse Post Collector")
    print("=" * 60)

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

    # Connect to database
    try:
        conn = get_db_connection(db_path)
        print(f"✓ Connected to database: {db_path}")
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        return 1

    # Collect posts
    total_collected = 0
    total_duplicates = 0
    start_time = datetime.now()

    try:
        for search_term in search_terms:
            term_collected = 0
            term_duplicates = 0

            for post, matched_term in search_posts(client, search_term, since_date):
                try:
                    # Extract post data
                    uri = post.uri
                    cid = post.cid
                    text = post.record.text
                    created_at = post.record.created_at
                    author_did = post.author.did
                    author_handle = post.author.handle
                    reply_to_uri = extract_reply_uri(post.record)

                    # Check for duplicate and insert
                    if post_exists(conn, uri):
                        term_duplicates += 1
                        total_duplicates += 1
                    else:
                        if insert_post(
                            conn,
                            uri,
                            cid,
                            text,
                            created_at,
                            author_did,
                            author_handle,
                            reply_to_uri,
                            matched_term,
                        ):
                            term_collected += 1
                            total_collected += 1

                except Exception as e:
                    print(f"    ✗ Error processing post: {e}")
                    continue

            if term_collected > 0 or term_duplicates > 0:
                summary = f"  ✓ {search_term}: {term_collected} new, {term_duplicates} duplicates"
                print(summary)

    except KeyboardInterrupt:
        print("\n⏸ Collection interrupted by user")
    except Exception as e:
        print(f"✗ Unexpected error during collection: {e}")
        return 1
    finally:
        conn.close()

    # Summary
    elapsed = datetime.now() - start_time
    print("\n" + "=" * 60)
    print(f"✓ Collection complete in {elapsed}")
    print(f"  Total collected: {total_collected}")
    print(f"  Total duplicates: {total_duplicates}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
