#!/usr/bin/env python3
"""
Fetch Bluesky author profiles and store them in database.

/// script
requires-python = ">=3.11"
dependencies = ["httpx"]
///
"""

import sqlite3
import time
import json
from datetime import datetime
from pathlib import Path

import httpx

DB_PATH = Path(__file__).parent / "posts.db"
BLUESKY_API_URL = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile"
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def init_database():
    """Create author_profiles table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS author_profiles (
                did TEXT PRIMARY KEY,
                handle TEXT,
                display_name TEXT,
                description TEXT,
                followers_count INTEGER,
                follows_count INTEGER,
                posts_count INTEGER,
                created_at TEXT,
                fetched_at TEXT
            )
        """)
        conn.commit()


def get_unique_author_dids():
    """Get all unique author DIDs from citation_units via posts table."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT DISTINCT p.author_did
            FROM posts p
            JOIN citation_units cu ON p.uri = cu.anchor_post_uri
            ORDER BY p.author_did
        """)
        return [row[0] for row in cursor.fetchall()]


def get_existing_author_dids():
    """Get DIDs that already have profiles in the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT did FROM author_profiles")
        return {row[0] for row in cursor.fetchall()}


def fetch_profile(did: str, client: httpx.Client) -> dict | None:
    """Fetch a profile from Bluesky API."""
    try:
        response = client.get(BLUESKY_API_URL, params={"actor": did}, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (404, 410):
            # Account deleted or suspended
            return None
        raise
    except Exception as e:
        print(f"  Error fetching {did}: {e}")
        return None


def save_profile(did: str, profile_data: dict | None):
    """Save profile to database."""
    with sqlite3.connect(DB_PATH) as conn:
        if profile_data is None:
            # Deleted/suspended account
            conn.execute(
                """
                INSERT INTO author_profiles
                (did, handle, display_name, description, followers_count,
                 follows_count, posts_count, created_at, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    did,
                    "[deleted]",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    datetime.now().isoformat(),
                ),
            )
        else:
            # Extract profile fields
            conn.execute(
                """
                INSERT INTO author_profiles
                (did, handle, display_name, description, followers_count,
                 follows_count, posts_count, created_at, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    profile_data.get("did"),
                    profile_data.get("handle"),
                    profile_data.get("displayName"),
                    profile_data.get("description"),
                    profile_data.get("followersCount"),
                    profile_data.get("followsCount"),
                    profile_data.get("postsCount"),
                    profile_data.get("createdAt"),
                    datetime.now().isoformat(),
                ),
            )
        conn.commit()


def main():
    """Fetch all author profiles."""
    init_database()

    # Get DIDs to fetch
    all_dids = get_unique_author_dids()
    existing_dids = get_existing_author_dids()
    dids_to_fetch = [did for did in all_dids if did not in existing_dids]

    print(f"Total unique authors: {len(all_dids)}")
    print(f"Already fetched: {len(existing_dids)}")
    print(f"To fetch: {len(dids_to_fetch)}")
    print()

    if not dids_to_fetch:
        print("All profiles already fetched.")
        return

    fetched = 0
    skipped = 0
    errors = 0

    with httpx.Client() as client:
        for i, did in enumerate(dids_to_fetch, 1):
            try:
                profile = fetch_profile(did, client)
                save_profile(did, profile)

                if profile is None:
                    print(f"  [{i}] {did} - [deleted/suspended]")
                else:
                    print(f"  [{i}] {profile.get('handle')} - {did}")

                fetched += 1

                if i % 10 == 0:
                    print(f"  Progress: {i}/{len(dids_to_fetch)} fetched")

                # Rate limiting
                time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                print(f"  [{i}] {did} - ERROR: {e}")
                errors += 1

    print()
    print("=== Summary ===")
    print(f"Fetched: {fetched}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"Total profiles in database: {len(existing_dids) + fetched}")


if __name__ == "__main__":
    main()
