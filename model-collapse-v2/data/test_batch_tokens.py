#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Measure token counts of batch files to verify they fit within API limits.
Uses character count as a conservative estimate for token count (chars/4).
"""

import argparse
import json
import os
import sys
from pathlib import Path
from statistics import median


def estimate_tokens(content: str) -> int:
    """Estimate token count from character count. Conservative estimate."""
    return len(content) // 4


def analyze_batch_files(directory: str, token_limit: int) -> None:
    """Analyze all batch files in directory and report token counts."""
    batch_dir = Path(directory)

    if not batch_dir.exists():
        print(f"Error: Directory does not exist: {directory}", file=sys.stderr)
        sys.exit(1)

    # Find all JSON batch files
    batch_files = sorted(batch_dir.glob("*.jsonl")) + sorted(batch_dir.glob("*.json"))

    if not batch_files:
        print(f"No batch files found in {directory}", file=sys.stderr)
        sys.exit(1)

    results = []

    for batch_file in batch_files:
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                content = f.read()

            char_count = len(content)
            estimated_tokens = estimate_tokens(content)
            over_limit = estimated_tokens > token_limit

            # For JSONL, also count number of requests
            line_count = len([l for l in content.split('\n') if l.strip()])

            results.append({
                'filename': batch_file.name,
                'chars': char_count,
                'tokens': estimated_tokens,
                'lines': line_count,
                'over_limit': over_limit,
            })
        except Exception as e:
            print(f"Error reading {batch_file.name}: {e}", file=sys.stderr)

    if not results:
        print("No batch files could be read", file=sys.stderr)
        sys.exit(1)

    # Calculate statistics
    token_counts = [r['tokens'] for r in results]
    avg_tokens = sum(token_counts) / len(token_counts)
    med_tokens = median(token_counts)
    max_tokens = max(token_counts)
    max_file = next(r for r in results if r['tokens'] == max_tokens)
    over_limit_count = sum(1 for r in results if r['over_limit'])

    # Print results table
    print(f"\n{'Batch File':<40} {'Chars':>12} {'Tokens':>10} {'Lines':>8} {'Over {token_limit}K?':>12}")
    print("-" * 85)

    for result in sorted(results, key=lambda x: x['tokens'], reverse=True):
        over = "YES" if result['over_limit'] else "no"
        print(f"{result['filename']:<40} {result['chars']:>12,} {result['tokens']:>10,} {result['lines']:>8} {over:>12}")

    # Print summary
    print("\n" + "=" * 85)
    print(f"Summary Statistics (Token Limit: {token_limit:,})")
    print("=" * 85)
    print(f"Total files:        {len(results)}")
    print(f"Over limit:         {over_limit_count}")
    print(f"Average tokens:     {avg_tokens:,.0f}")
    print(f"Median tokens:      {med_tokens:,.0f}")
    print(f"Largest batch:      {max_file['filename']}")
    print(f"  - Tokens:         {max_tokens:,}")
    print(f"  - Chars:          {max_file['chars']:,}")
    print(f"  - Lines:          {max_file['lines']}")
    print(f"  - Under limit?    {'YES' if not max_file['over_limit'] else 'NO'}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Measure token counts of batch files"
    )
    parser.add_argument(
        "--dir",
        default="/private/tmp/claude/relevance/",
        help="Directory containing batch files (default: /private/tmp/claude/relevance/)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=25000,
        help="Token limit to check against (default: 25000)"
    )

    args = parser.parse_args()
    analyze_batch_files(args.dir, args.limit)


if __name__ == "__main__":
    main()
