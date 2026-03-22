#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Export relevant posts into batch JSON files for Pass 2 full coding.

Usage: uv run --script export_pass2_batches.py [--batch-size 50] [--output-dir /tmp/claude/pass2_batches]
"""

import argparse
import json
import sqlite3
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--output-dir", default="/tmp/claude/pass2_batches")
    parser.add_argument("--db", default="/Users/Joshua/agent/model-collapse-study/data/posts.db")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    # Only export relevant posts that haven't been fully coded yet
    rows = conn.execute(
        """SELECT id, text, created_at, search_term_matched
           FROM posts
           WHERE is_relevant = 1 AND claim_type IS NULL
           ORDER BY id"""
    ).fetchall()

    print(f"Total relevant posts to code: {len(rows)}")

    batch_num = 0
    for i in range(0, len(rows), args.batch_size):
        batch = [dict(r) for r in rows[i:i + args.batch_size]]
        batch_file = os.path.join(args.output_dir, f"p2batch_{batch_num:04d}.json")
        with open(batch_file, "w") as f:
            json.dump(batch, f, indent=2)
        batch_num += 1

    print(f"Exported {batch_num} batches of up to {args.batch_size} posts each")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
