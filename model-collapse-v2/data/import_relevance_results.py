#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import argparse
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def find_result_files(results_dir: Path) -> list[Path]:
    """Find all results_*.json files that haven't been imported yet."""
    return sorted([
        f for f in results_dir.glob('results_*.json')
        if not f.name.endswith('.imported.json')
    ])


def import_results_file(
    conn: sqlite3.Connection,
    results_file: Path,
    dry_run: bool = False
) -> tuple[int, int, list[int], int]:
    """
    Import classifications from a results file.
    Returns: (relevant_count, not_relevant_count, missing_ids, already_classified_count)
    """
    with open(results_file, 'r') as f:
        data = json.load(f)

    batch_id = data.get('batch_id', '')
    classifications = data.get('classifications', [])

    relevant_count = 0
    not_relevant_count = 0
    missing_ids = []
    already_classified_count = 0
    now = datetime.now().isoformat()

    cursor = conn.cursor()

    for classification in classifications:
        post_id = classification['id']
        relevant = classification['relevant']
        rationale = classification.get('rationale', '')

        # Check if post exists in database
        cursor.execute('SELECT id, relevant FROM posts WHERE id = ?', (post_id,))
        result = cursor.fetchone()
        if not result:
            missing_ids.append(post_id)
            continue

        # Check if post already classified
        if result['relevant'] is not None:
            already_classified_count += 1
            continue

        if not dry_run:
            cursor.execute('''
                UPDATE posts
                SET relevant = ?,
                    relevance_rationale = ?,
                    relevance_classified_at = ?
                WHERE id = ? AND relevant IS NULL
            ''', (1 if relevant else 0, rationale, now, post_id))

        if relevant:
            relevant_count += 1
        else:
            not_relevant_count += 1

    if not dry_run:
        conn.commit()

    return relevant_count, not_relevant_count, missing_ids, already_classified_count


def rename_imported_file(results_file: Path) -> None:
    """Rename results file to mark it as imported."""
    imported_file = results_file.parent / (results_file.name.replace('.json', '.imported.json'))
    try:
        results_file.rename(imported_file)
    except FileNotFoundError:
        pass  # Already processed by another import


def count_unclassified(conn: sqlite3.Connection) -> int:
    """Count posts that remain unclassified."""
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM posts WHERE relevant IS NULL')
    return cursor.fetchone()[0]


def main():
    parser = argparse.ArgumentParser(
        description='Import relevance classification results back into the database'
    )
    parser.add_argument(
        '--db',
        default='/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db',
        help='Path to posts database'
    )
    parser.add_argument(
        '--results-dir',
        default='/private/tmp/claude/relevance/',
        help='Directory containing results files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be imported without writing'
    )
    parser.add_argument(
        '--file',
        help='Import a single specific results file (instead of scanning the directory)',
    )

    args = parser.parse_args()

    # Determine which files to import
    if args.file:
        result_files = [Path(args.file)]
    else:
        results_dir = Path(args.results_dir)
        if not results_dir.exists():
            print(f'Results directory does not exist: {results_dir}')
            return
        # Find result files
        result_files = find_result_files(results_dir)

    if not result_files:
        print('No result files to import')
        return

    # Connect to database
    conn = get_db_connection(args.db)

    try:
        total_relevant = 0
        total_not_relevant = 0
        total_already_classified = 0
        all_missing_ids = []
        files_imported = 0

        for results_file in result_files:
            print(f'Importing {results_file.name}...')
            relevant, not_relevant, missing, already_classified = import_results_file(
                conn, results_file, dry_run=args.dry_run
            )

            total_relevant += relevant
            total_not_relevant += not_relevant
            total_already_classified += already_classified
            all_missing_ids.extend(missing)

            if not args.dry_run:
                rename_imported_file(results_file)
            files_imported += 1

        # Print summary
        print('\nImport Summary:')
        print(f'Files imported: {files_imported}')
        print(f'Posts marked relevant: {total_relevant}')
        print(f'Posts marked not relevant: {total_not_relevant}')
        print(f'Posts already classified (skipped): {total_already_classified}')

        if all_missing_ids:
            print(f'Posts in results not found in DB: {len(all_missing_ids)}')
            print(f'  IDs: {all_missing_ids[:10]}' + (f' ... and {len(all_missing_ids) - 10} more' if len(all_missing_ids) > 10 else ''))

        # Count remaining unclassified
        unclassified = count_unclassified(conn)
        print(f'\nPosts remaining unclassified: {unclassified}')

        if args.dry_run:
            print('\n(DRY RUN - no changes were made)')

    finally:
        conn.close()


if __name__ == '__main__':
    main()
