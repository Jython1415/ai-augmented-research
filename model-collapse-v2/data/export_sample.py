#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Export a stratified sample of posts for relevance testing.

Exports posts proportionally to search term counts, with a minimum of 2 posts
per search term to ensure all terms are represented in the sample.
"""

import sqlite3
import json
import argparse
import sys
from pathlib import Path
from typing import Optional


def get_search_term_counts(db_path: str) -> dict[str, int]:
    """Get count of posts for each search term."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT search_term_matched, COUNT(*) as count FROM posts "
        "WHERE search_term_matched IS NOT NULL "
        "GROUP BY search_term_matched ORDER BY count DESC"
    )
    counts = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return counts


def calculate_stratified_sample(
    term_counts: dict[str, int], total_sample_size: int
) -> dict[str, int]:
    """
    Calculate sample size per search term using stratified sampling.

    Allocates samples proportionally to term counts, but ensures a minimum
    of 2 samples per term to cover all terms.
    """
    num_terms = len(term_counts)
    min_per_term = 2

    # Minimum allocation: 2 per term
    minimum_total = num_terms * min_per_term

    if total_sample_size < minimum_total:
        # If sample size is smaller than minimum allocation, adjust down
        adjusted_min = max(1, total_sample_size // num_terms)
        allocation = {term: adjusted_min for term in term_counts}
        # Distribute remainder
        remainder = total_sample_size - sum(allocation.values())
        for term in list(allocation.keys())[:remainder]:
            allocation[term] += 1
        return allocation

    # Start with minimum allocation
    allocation = {term: min_per_term for term in term_counts}
    remaining = total_sample_size - minimum_total

    # Distribute remaining samples proportionally
    total_count = sum(term_counts.values())
    for term, count in term_counts.items():
        proportion = count / total_count
        additional = round(proportion * remaining)
        allocation[term] += additional

    # Fine-tune to match exact sample size
    current_total = sum(allocation.values())
    if current_total > total_sample_size:
        # Remove from largest allocations
        terms_by_alloc = sorted(
            allocation.items(), key=lambda x: x[1], reverse=True
        )
        for term, _ in terms_by_alloc:
            if current_total <= total_sample_size:
                break
            if allocation[term] > min_per_term:
                allocation[term] -= 1
                current_total -= 1
    elif current_total < total_sample_size:
        # Add to largest allocations
        terms_by_count = sorted(
            term_counts.items(), key=lambda x: x[1], reverse=True
        )
        for term, _ in terms_by_count:
            if current_total >= total_sample_size:
                break
            allocation[term] += 1
            current_total += 1

    return allocation


def export_sample(
    db_path: str, output_dir: str, sample_size: int
) -> None:
    """
    Export stratified sample to JSON file.

    Args:
        db_path: Path to posts.db
        output_dir: Directory to write sample.json
        sample_size: Total sample size to export
    """
    # Get search term counts
    term_counts = get_search_term_counts(db_path)

    if not term_counts:
        print("Error: No posts with search_term_matched found in database.")
        sys.exit(1)

    print(f"Total posts in database: {sum(term_counts.values())}")
    print(f"Search terms found: {len(term_counts)}")
    print()

    # Calculate stratified allocation
    allocation = calculate_stratified_sample(term_counts, sample_size)

    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Collect samples
    samples = []

    for term, num_to_sample in sorted(allocation.items()):
        cursor.execute(
            "SELECT id, text, created_at, author_handle, search_term_matched "
            "FROM posts WHERE search_term_matched = ? "
            "ORDER BY RANDOM() LIMIT ?",
            (term, num_to_sample)
        )
        rows = cursor.fetchall()

        for row in rows:
            samples.append({
                "id": row["id"],
                "text": row["text"],
                "created_at": row["created_at"],
                "author_handle": row["author_handle"],
                "search_term_matched": row["search_term_matched"]
            })

        actual_count = len(rows)
        print(f"  {term}: {actual_count}/{num_to_sample} samples")

    conn.close()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Write JSON
    sample_file = output_path / "sample.json"
    with open(sample_file, "w") as f:
        json.dump(samples, f, indent=2)

    print()
    print(f"✓ Exported {len(samples)} posts to {sample_file}")
    print()
    print("Summary:")
    print(f"  Total samples: {len(samples)}")
    print(f"  Sample size requested: {sample_size}")

    # Count by term in export
    export_counts = {}
    for sample in samples:
        term = sample["search_term_matched"]
        export_counts[term] = export_counts.get(term, 0) + 1

    print("\n  Samples per search term:")
    for term in sorted(export_counts.keys()):
        print(f"    {term}: {export_counts[term]}")


def main():
    parser = argparse.ArgumentParser(
        description="Export stratified sample of posts for relevance testing"
    )
    parser.add_argument(
        "--db",
        default="/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db",
        help="Path to posts.db (default: /Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db)"
    )
    parser.add_argument(
        "--output-dir",
        default="/private/tmp/claude/relevance_sample",
        help="Output directory for sample.json (default: /private/tmp/claude/relevance_sample)"
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=50,
        help="Total sample size to export (default: 50)"
    )

    args = parser.parse_args()

    # Verify database exists
    if not Path(args.db).exists():
        print(f"Error: Database not found at {args.db}")
        sys.exit(1)

    export_sample(args.db, args.output_dir, args.sample_size)


if __name__ == "__main__":
    main()
