#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Import Pass 2 coding results from subagent JSON outputs back into SQLite.

Usage: uv run --script import_pass2_results.py [--results-dir /tmp/claude/pass2_results] [--dry-run]
"""

import argparse
import glob
import json
import sqlite3
import os


VALID_CLAIM_TYPES = {"empirical", "predictive", "normative", "meta-commentary"}
VALID_SOURCE_CITED = {"nature_paper", "other_paper", "news_article", "none", "quote_post"}
VALID_CAVEATING = {"strong_hedge", "weak_hedge", "none"}
VALID_ACCURACY = {"accurate", "oversimplified", "wrong", "unfalsifiable"}
VALID_AWARENESS = {"cites_post_2024_nuance", "only_cites_original", "no_citations"}
VALID_DEPTH = {"substantive_claim", "passing_mention", "share_signal_boost"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="/tmp/claude/pass2_results")
    parser.add_argument("--db", default="/Users/Joshua/agent/model-collapse-study/data/posts.db")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result_files = sorted(glob.glob(os.path.join(args.results_dir, "p2result_*.json")))
    print(f"Found {len(result_files)} result files")

    if not result_files:
        print("No result files found.")
        return

    conn = sqlite3.connect(args.db)
    total_updated = 0
    errors = 0
    depth_counts = {}

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
            if post_id is None:
                errors += 1
                continue

            claim_type = item.get("claim_type", "")
            source_cited = item.get("source_cited", "")
            caveating_level = item.get("caveating_level", "")
            accuracy = item.get("accuracy", "")
            literature_awareness = item.get("literature_awareness", "")
            depth = item.get("depth", "")
            rationale = item.get("coding_rationale", "")
            minimal = 1 if item.get("minimal_content", False) else 0

            # Track depth distribution
            depth_counts[depth] = depth_counts.get(depth, 0) + 1

            if not args.dry_run:
                conn.execute(
                    """UPDATE posts SET
                       claim_type = ?, source_cited = ?, caveating_level = ?,
                       accuracy = ?, literature_awareness = ?, depth = ?,
                       coding_rationale = ?, minimal_content = ?
                       WHERE id = ?""",
                    (claim_type, source_cited, caveating_level,
                     accuracy, literature_awareness, depth,
                     rationale, minimal, post_id),
                )
            total_updated += 1

    if not args.dry_run:
        conn.commit()
    conn.close()

    print(f"\nResults:")
    print(f"  Total coded: {total_updated}")
    print(f"  Errors: {errors}")
    print(f"  Depth distribution: {depth_counts}")
    if args.dry_run:
        print("  (DRY RUN - no DB changes made)")


if __name__ == "__main__":
    main()
