#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Import classification results from subagent JSON outputs back into SQLite.

Usage: uv run --script import_results.py [--results-dir /tmp/claude/results] [--dry-run]
"""

import argparse
import glob
import json
import sqlite3
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="/tmp/claude/results")
    parser.add_argument("--db", default="/Users/Joshua/agent/model-collapse-study/data/posts.db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result_files = sorted(glob.glob(os.path.join(args.results_dir, "result_*.json")))
    print(f"Found {len(result_files)} result files")

    if not result_files:
        print("No result files found. Check --results-dir path.")
        return

    conn = sqlite3.connect(args.db)
    total_updated = 0
    total_relevant = 0
    total_not_relevant = 0
    errors = 0

    for rf in result_files:
        try:
            with open(rf) as f:
                results = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"  ERROR reading {rf}: {e}")
            errors += 1
            continue

        for item in results:
            post_id = item.get("id")
            is_relevant = item.get("is_relevant")
            confidence = item.get("confidence")

            if post_id is None or is_relevant is None:
                errors += 1
                continue

            is_relevant_int = 1 if is_relevant else 0

            if is_relevant_int:
                total_relevant += 1
            else:
                total_not_relevant += 1

            if not args.dry_run:
                conn.execute(
                    "UPDATE posts SET is_relevant = ?, relevance_confidence = ? WHERE id = ?",
                    (is_relevant_int, confidence, post_id),
                )
            total_updated += 1

    if not args.dry_run:
        conn.commit()

    conn.close()

    print(f"\nResults:")
    print(f"  Total classified: {total_updated}")
    print(f"  Relevant: {total_relevant}")
    print(f"  Not relevant: {total_not_relevant}")
    print(f"  Errors: {errors}")
    if args.dry_run:
        print("  (DRY RUN - no DB changes made)")


if __name__ == "__main__":
    main()
