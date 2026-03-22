#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Export posts from SQLite into batch JSON files for subagent classification.

Usage: uv run --script export_batches.py [--batch-size 100] [--output-dir /tmp/claude/batches]
"""

import argparse
import json
import sqlite3
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--output-dir", default="/tmp/claude/batches")
    parser.add_argument("--db", default="/Users/Joshua/agent/model-collapse-study/data/posts.db")
    parser.add_argument("--uncoded-only", action="store_true", default=True,
                        help="Only export posts not yet coded")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    if args.uncoded_only:
        rows = conn.execute(
            "SELECT id, text, created_at FROM posts WHERE is_relevant IS NULL ORDER BY id"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, text, created_at FROM posts ORDER BY id"
        ).fetchall()

    print(f"Total posts to export: {len(rows)}")

    batch_num = 0
    for i in range(0, len(rows), args.batch_size):
        batch = [dict(r) for r in rows[i:i + args.batch_size]]
        batch_file = os.path.join(args.output_dir, f"batch_{batch_num:04d}.json")
        with open(batch_file, "w") as f:
            json.dump(batch, f, indent=2)
        batch_num += 1

    print(f"Exported {batch_num} batches of up to {args.batch_size} posts each")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
