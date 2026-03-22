#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import sqlite3
import argparse
import sys
from pathlib import Path
from typing import Optional
from collections import defaultdict

# Citation type priority (higher = stronger signal)
CITATION_TYPE_PRIORITY = {
    'link': 3,
    'author_name': 2,
    'title_phrase': 1,
    'indirect': 0,
}

# Known paper identifiers
ARXIV_IDS = ['2305.17493']
DOI_IDS = ['10.1038/s41586-024-07566-y']
NATURE_URLS = ['nature.com/articles/s41586-024-07566']


def determine_citation_type(search_term: Optional[str], text: str) -> str:
    """
    Determine citation type based on search_term_matched and text content.

    Priority (highest to lowest):
    1. 'link' - arxiv URL, DOI, or known paper URLs in text
    2. 'author_name' - "shumailov" search term or in text
    3. 'title_phrase' - specific title phrases
    4. 'indirect' - everything else
    """
    types_found = []

    # Check for 'link' type (highest priority)
    if search_term:
        if 'arxiv.org' in search_term.lower() or any(arxiv in search_term for arxiv in ARXIV_IDS):
            types_found.append('link')
        elif 'doi' in search_term.lower() or any(doi in search_term for doi in DOI_IDS):
            types_found.append('link')

    text_lower = text.lower()
    if any(arxiv in text_lower for arxiv in ARXIV_IDS):
        types_found.append('link')
    if any(doi in text_lower for doi in DOI_IDS):
        types_found.append('link')
    if any(url in text_lower for url in NATURE_URLS):
        types_found.append('link')

    # Check for 'author_name' type
    if search_term and 'shumailov' in search_term.lower():
        types_found.append('author_name')
    if 'shumailov' in text_lower:
        types_found.append('author_name')

    # Check for 'title_phrase' type
    title_phrases = [
        'trained on recursively generated',
        'ai models collapse',
        'model collapse paper',
        'model collapse nature',
        'recursive training collapse',
    ]

    if search_term:
        search_term_lower = search_term.lower()
        for phrase in title_phrases:
            if phrase in search_term_lower:
                types_found.append('title_phrase')
                break

    for phrase in title_phrases:
        if phrase in text_lower:
            types_found.append('title_phrase')
            break

    # If no specific type found, use 'indirect'
    if not types_found:
        return 'indirect'

    # Return the highest priority type found
    unique_types = list(set(types_found))
    unique_types.sort(key=lambda t: CITATION_TYPE_PRIORITY[t], reverse=True)
    return unique_types[0]


def build_citation_units(db_path: str, dry_run: bool = False) -> None:
    """Build citation_unit records from relevant posts."""
    db_path = Path(db_path)

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Fetch all relevant posts
        cursor.execute("""
            SELECT id, uri, author_did, author_handle, created_at, text, search_term_matched
            FROM posts
            WHERE relevant = 1
            ORDER BY created_at DESC
        """)

        relevant_posts = cursor.fetchall()
        total_relevant = len(relevant_posts)

        # Count citation units by type
        citation_counts = defaultdict(int)
        citations_to_insert = []

        for post in relevant_posts:
            citation_type = determine_citation_type(
                post['search_term_matched'],
                post['text']
            )

            citation_counts[citation_type] += 1
            citations_to_insert.append({
                'anchor_post_uri': post['uri'],
                'author_did': post['author_did'],
                'author_handle': post['author_handle'],
                'created_at': post['created_at'],
                'citation_type': citation_type,
                'search_term_source': post['search_term_matched'],
            })

        # Display dry-run summary or insert
        print(f"Total relevant posts: {total_relevant}")
        print(f"Citation units to create: {len(citations_to_insert)}")
        print("\nBreakdown by citation_type:")
        for citation_type in ['link', 'author_name', 'title_phrase', 'indirect']:
            count = citation_counts[citation_type]
            print(f"  {citation_type}: {count}")

        if not dry_run:
            print("\nInserting citation units...")
            for citation in citations_to_insert:
                cursor.execute("""
                    INSERT OR IGNORE INTO citation_units
                    (anchor_post_uri, author_did, author_handle, created_at, citation_type, search_term_source)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    citation['anchor_post_uri'],
                    citation['author_did'],
                    citation['author_handle'],
                    citation['created_at'],
                    citation['citation_type'],
                    citation['search_term_source'],
                ))

            conn.commit()

            # Count final result
            cursor.execute("SELECT COUNT(*) as count FROM citation_units")
            final_count = cursor.fetchone()['count']
            print(f"\nTotal citation_units in database: {final_count}")
        else:
            print("\n(Dry-run mode: no changes written)")

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='Build citation_unit records from relevant posts'
    )
    parser.add_argument(
        '--db',
        default='/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db',
        help='Path to posts database'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without writing'
    )

    args = parser.parse_args()

    build_citation_units(args.db, args.dry_run)


if __name__ == '__main__':
    main()
