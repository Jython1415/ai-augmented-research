#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
SQLite database initialization for model collapse citation study (Round 2).

Supports: posts, citation units, thread context, author profiles, coding passes,
and search experiment tracking.

Usage:
    uv run --script init_db.py
    uv run --script init_db.py --db /path/to/custom.db
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def init_database(db_path: str) -> None:
    """Initialize SQLite database with schema for model collapse study."""

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 1. Posts table - raw collected posts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uri TEXT UNIQUE NOT NULL,
            cid TEXT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            author_did TEXT NOT NULL,
            author_handle TEXT,
            author_display_name TEXT,
            reply_to_uri TEXT,
            source TEXT DEFAULT 'api',
            search_term_matched TEXT,
            collected_at TEXT DEFAULT (datetime('now')),
            relevant INTEGER,
            relevance_rationale TEXT,
            relevance_classified_at TEXT
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_author_did ON posts(author_did)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_search_term ON posts(search_term_matched)")

    # 2. Citation units table - each citation event
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citation_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anchor_post_uri TEXT NOT NULL UNIQUE,
            author_did TEXT NOT NULL,
            author_handle TEXT,
            created_at TEXT,
            citation_type TEXT CHECK(citation_type IN ('link', 'author_name', 'title_phrase', 'indirect')),
            search_term_source TEXT,
            created_at_recorded TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_citation_units_author ON citation_units(author_did)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_citation_units_type ON citation_units(citation_type)")

    # 3. Thread context table - context posts for each citation unit
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thread_context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation_unit_id INTEGER NOT NULL,
            post_uri TEXT NOT NULL,
            post_cid TEXT,
            post_text TEXT,
            post_created_at TEXT,
            author_did TEXT,
            author_handle TEXT,
            relationship TEXT CHECK(relationship IN ('self_reply', 'parent', 'grandparent', 'quoted', 'reply_child')),
            depth INTEGER,
            fetched_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (citation_unit_id) REFERENCES citation_units(id),
            UNIQUE(citation_unit_id, post_uri)
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_thread_context_citation_unit ON thread_context(citation_unit_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_thread_context_relationship ON thread_context(relationship)")

    # 4. Author profiles table - author demographics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS author_profiles (
            did TEXT PRIMARY KEY,
            handle TEXT,
            display_name TEXT,
            bio TEXT,
            followers_count INTEGER,
            follows_count INTEGER,
            posts_count INTEGER,
            fetched_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # 5. Coding pass 1 table - post-only coding
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_pass1 (
            citation_unit_id INTEGER PRIMARY KEY,
            paper_fidelity TEXT CHECK(paper_fidelity IN ('accurate', 'partially_accurate', 'misrepresentation')),
            field_accuracy TEXT CHECK(field_accuracy IN ('accurate', 'partially_accurate', 'oversimplified', 'inaccurate')),
            claim_strength TEXT CHECK(claim_strength IN ('casual', 'moderate', 'authoritative')),
            rationale TEXT,
            coded_at TEXT DEFAULT (datetime('now')),
            agent_id TEXT,
            FOREIGN KEY (citation_unit_id) REFERENCES citation_units(id)
        )
    """)

    # 6. Coding pass 2 table - with-context coding
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_pass2 (
            citation_unit_id INTEGER PRIMARY KEY,
            paper_fidelity TEXT CHECK(paper_fidelity IN ('accurate', 'partially_accurate', 'misrepresentation')),
            field_accuracy TEXT CHECK(field_accuracy IN ('accurate', 'partially_accurate', 'oversimplified', 'inaccurate')),
            claim_strength TEXT CHECK(claim_strength IN ('casual', 'moderate', 'authoritative')),
            rationale TEXT,
            coded_at TEXT DEFAULT (datetime('now')),
            agent_id TEXT,
            FOREIGN KEY (citation_unit_id) REFERENCES citation_units(id)
        )
    """)

    # 7. Search experiments table - mini-experiment tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_term TEXT NOT NULL,
            total_results INTEGER,
            relevant_count INTEGER,
            irrelevant_count INTEGER,
            signal_to_noise REAL,
            notes TEXT,
            tested_at TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_experiments_term ON search_experiments(search_term)")

    conn.commit()
    conn.close()

    print(f"✓ Database initialized: {db_path}")
    print(f"  Tables: posts, citation_units, thread_context, author_profiles, coding_pass1, coding_pass2, search_experiments")
    print(f"  All indices created")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize SQLite database for model collapse citation study"
    )
    parser.add_argument(
        "--db",
        default="/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db",
        help="Path to SQLite database file"
    )

    args = parser.parse_args()

    try:
        init_database(args.db)
        return 0
    except Exception as e:
        print(f"Error initializing database: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
