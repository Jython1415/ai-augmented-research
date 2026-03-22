#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["atproto", "httpx[socks]"]
# ///
"""
Collect Bluesky posts about Shumailov et al. (2024) model collapse paper.

Searches for citations of "AI models collapse when trained on recursively generated data"
(Nature 631, 755-759) using multiple search terms and stores results in SQLite database.

Two modes:
  --experiment: Mini-experiment mode. For each search term, fetch first 2 pages
                (up to 200 posts), print sample posts, report counts. No database writes.
  (default):    Full collection mode. Paginate through all results, store in database.

Environment variables required:
  BSKY_HANDLE: Bluesky handle (e.g., user.bsky.social)
  BSKY_APP_PASSWORD: App password for authentication
"""

import argparse
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from atproto import Client


# Search terms for Shumailov et al. (2024) model collapse paper
# Refined through 3 rounds of mini-experiments (signal-to-noise testing)
SEARCH_TERMS = [
    # Tier 1: Direct paper references (high signal)
    "arxiv.org/abs/2305.17493",                 # arXiv URL
    "10.1038/s41586-024-07566-y",               # DOI
    "shumailov",                                # Author name
    "trained on recursively generated",         # Nature title fragment

    # Tier 2: Targeted terms (good signal, some noise)
    "AI models collapse",                       # Nature title fragment
    "model collapse paper",                     # People referencing "the paper"
    "model collapse nature",                    # People referencing Nature pub
    "recursive training collapse",              # Technical description

    # Tier 2b: Metaphorical/informal references (Phase 2.5 discovery)
    "Habsburg AI",                              # Dynastic inbreeding metaphor
    "digital inbreeding",                       # Genetic/demographic term
    "self-consuming generative",                # Self-referential AI
    "synthetic data collapse",                  # Specific mechanism
    "AI eating itself",                         # Vivid colloquial reference
    "AI ouroboros",                             # Mythological metaphor
    "AI feeding on itself",                     # Behavioral description

    # Tier 3: Broad coverage (noisy, needed for indirect citations)
    "model collapse",                           # General term
]


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
    max_pages: Optional[int] = None,
) -> tuple[list, int]:
    """
    Search for posts using a single search term with pagination.

    Args:
        client: Authenticated AT Protocol client
        search_term: Search query string
        since_date: ISO 8601 date string for start of range
        limit_per_page: Posts per request (max 100)
        max_pages: Maximum number of pages to fetch (None for unlimited)

    Returns:
        Tuple of (list of (post, search_term) tuples, total posts found)
    """
    cursor = None
    request_count = 0
    all_posts = []

    while True:
        if max_pages and request_count >= max_pages:
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
                break

            for post in posts:
                all_posts.append((post, search_term))

            # Check for next page
            if response.cursor:
                cursor = response.cursor
            else:
                break

        except Exception as e:
            print(f"  ✗ Error during search: {e}")
            break

    return all_posts, len(all_posts)


def format_post_text(text: str, max_length: int = 200) -> str:
    """Format post text for display, truncating if needed."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def run_experiment_mode(client: Client, since_date: str) -> int:
    """
    Run mini-experiment mode: fetch 2 pages per term, print samples, no DB writes.

    Args:
        client: Authenticated AT Protocol client
        since_date: ISO 8601 date string for start of range

    Returns:
        Exit code (0 for success)
    """
    print("\n" + "=" * 80)
    print("EXPERIMENT MODE: Signal-to-noise testing")
    print("=" * 80)
    print(f"Fetching first 2 pages (~200 posts) per search term\n")

    experiment_results = []

    for search_term in SEARCH_TERMS:
        print(f"\n🔍 Searching: '{search_term}'")

        try:
            posts, total_found = search_posts(
                client,
                search_term,
                since_date=since_date,
                limit_per_page=100,
                max_pages=2  # Only 2 pages for experiment
            )

            print(f"   Total found (first 2 pages): {total_found}")

            # Show first 5 post samples
            if posts:
                print(f"   Sample posts:")
                for i, (post, _) in enumerate(posts[:5], 1):
                    text = post.record.text
                    formatted = format_post_text(text, max_length=200)
                    print(f"     {i}. {formatted}")
            else:
                print(f"   (no posts)")

            experiment_results.append({
                "term": search_term,
                "count": total_found,
                "posts": posts,
            })

        except Exception as e:
            print(f"   ✗ Error: {e}")
            experiment_results.append({
                "term": search_term,
                "count": 0,
                "posts": [],
            })

    # Summary table
    print("\n" + "=" * 80)
    print("EXPERIMENT SUMMARY")
    print("=" * 80)
    print(f"{'Search Term':<45} {'Posts Found':<15}")
    print("-" * 80)

    total_posts = 0
    for result in experiment_results:
        print(f"{result['term']:<45} {result['count']:<15}")
        total_posts += result['count']

    print("-" * 80)
    print(f"{'TOTAL':<45} {total_posts:<15}")
    print("=" * 80)
    print("\nNote: Experiment mode does NOT write to database")
    print("Use default mode to collect all posts\n")

    return 0


def run_full_collection_mode(
    client: Client,
    db_path: str,
    since_date: str,
) -> int:
    """
    Run full collection mode: paginate through all results, store in database.

    Args:
        client: Authenticated AT Protocol client
        db_path: Path to SQLite database
        since_date: ISO 8601 date string for start of range

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Create database path and ensure parent directory exists
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 80)
    print("FULL COLLECTION MODE")
    print("=" * 80)
    print(f"Database: {db_path}")
    print(f"Since: {since_date}\n")

    # Connect to database
    try:
        conn = get_db_connection(str(db_path))
        print(f"✓ Connected to database")
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        return 1

    # Collect posts
    total_collected = 0
    total_duplicates = 0
    start_time = datetime.now()

    try:
        for search_term in SEARCH_TERMS:
            print(f"\n🔍 Searching: '{search_term}'")
            term_collected = 0
            term_duplicates = 0

            try:
                posts, total_found = search_posts(
                    client,
                    search_term,
                    since_date=since_date,
                    limit_per_page=100,
                    max_pages=None  # All pages
                )

                print(f"   Total found: {total_found}")

                for post, matched_term in posts:
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
                        print(f"      ✗ Error processing post: {e}")
                        continue

                if term_collected > 0 or term_duplicates > 0:
                    summary = f"   ✓ {term_collected} new, {term_duplicates} duplicates"
                    print(summary)
                else:
                    print(f"   (no new posts)")

            except Exception as e:
                print(f"   ✗ Error during search: {e}")
                continue

    except KeyboardInterrupt:
        print("\n⏸ Collection interrupted by user")
    except Exception as e:
        print(f"✗ Unexpected error during collection: {e}")
        return 1
    finally:
        conn.close()

    # Summary
    elapsed = datetime.now() - start_time
    print("\n" + "=" * 80)
    print("COLLECTION COMPLETE")
    print("=" * 80)
    print(f"Time elapsed: {elapsed}")
    print(f"Total collected: {total_collected}")
    print(f"Total duplicates: {total_duplicates}")
    print("=" * 80 + "\n")

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Collect Bluesky posts citing Shumailov et al. (2024) model collapse paper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run experiment mode (2 pages per term, no database writes)
  uv run --script collect_posts.py --experiment

  # Run full collection mode (all results, store in default database)
  uv run --script collect_posts.py

  # Run full collection with custom database path
  uv run --script collect_posts.py --db /custom/path/posts.db

  # Run full collection with custom date range
  uv run --script collect_posts.py --since 2024-01-01T00:00:00Z
        """,
    )

    parser.add_argument(
        "--experiment",
        action="store_true",
        help="Run mini-experiment mode (fetch 2 pages per term, print samples, no DB writes)",
    )

    parser.add_argument(
        "--db",
        default="/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db",
        help="Path to SQLite database file (full collection mode only)",
    )

    parser.add_argument(
        "--since",
        default="2023-05-01T00:00:00Z",
        help="ISO 8601 date string for start of search range (default: 2023-05-01)",
    )

    args = parser.parse_args()

    # Setup
    print("=" * 80)
    print("Shumailov et al. (2024) Model Collapse Citation Collector")
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
    if args.experiment:
        return run_experiment_mode(client, args.since)
    else:
        return run_full_collection_mode(client, args.db, args.since)


if __name__ == "__main__":
    sys.exit(main())
