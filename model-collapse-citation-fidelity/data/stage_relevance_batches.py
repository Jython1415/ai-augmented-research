#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def auto_accept_high_signal_posts(conn: sqlite3.Connection) -> int:
    """Auto-accept Tier 1 high-signal posts and return count.

    Two categories:
    1. Search term matches: posts found via high-signal search terms
    2. News coverage URLs: posts whose text, parent_text, or quoted_text
       contains a verified news coverage URL about Shumailov et al.
    """
    # Category 1: High-signal search terms
    high_signal_terms = [
        'arxiv.org/abs/2305.17493',
        '10.1038/s41586-024-07566-y',
        'trained on recursively generated',
        'shumailov'
    ]

    # Category 2: Verified news coverage URL domains/paths
    # These are articles confirmed to be specifically about Shumailov et al.
    news_coverage_urls = [
        # Nature
        'nature.com/articles/s41586-024-07566-y',
        'nature.com/articles/d41586-024-02420-7',
        'nature.com/articles/d41586-024-03023-y',
        'nature.com/articles/s41586-025-08905-3',
        # Major tech press
        'techcrunch.com/2024/07/24/model-collapse',
        'theregister.com/2024/07/25/ai_will_eat_itself',
        'gizmodo.com/ai-learning-from-its-own-nonsense',
        'euronews.com/next/2024/07/31/new-study-warns-of-model-collapse',
        'bigthink.com/the-future/ai-model-collapse',
        'freethink.com/robots-ai/model-collapse-synthetic-data',
        'techxplore.com/news/2024-07-ai-collapse-llms',
        'heise.de/en/news/Model-collapse-how-synthetic-data',
        'bloomberg.com/news/articles/2024-08-05/ai-model-collapse',
        'technologyreview.com/2024/07/24/1095263/',
        'venturebeat.com/ai/the-ai-feedback-loop',
        'techtarget.com/whatis/feature/Model-collapse-explained',
        # Newspapers
        'nytimes.com/interactive/2024/08/26/upshot/ai-synthetic-data',
        'theglobeandmail.com/business/article-training-ai-models-generated-data',
        # Science press
        'scientificamerican.com/article/ai-generated-data-can-poison',
        'popsci.com/technology/ai-trained-on-ai-gibberish',
        'theconversation.com/what-is-model-collapse',
        'cosmosmagazine.com/technology/ai/training-ai-models-on-machine-generated',
        'gigazine.net/gsc_news/en/20240725-ai-collapse',
        'mindmatters.ai/2024/08/ai-going-mad-the-model-collapse',
        'singularityhub.com/2024/07/25/this-is-what-could-happen',
        'singularityhub.com/2024/08/27/what-is-model-collapse',
        # International
        'abc.net.au/news/2024-08-25/what-is-model-collapse',
        'axios.com/2023/08/28/ai-content-flood-model-collapse',
        'axios.com/2024/07/27/synthetic-ai-data-effects',
        # Long-form
        'noemamag.com/the-ai-powered-web-is-eating-itself',
        # Academic/professional
        'cacm.acm.org/news/the-collapse-of-gpt',
        'jolt.law.harvard.edu/digest/model-collapse',
        'blogs.sas.com/content/iml/2024/07/31/synthetic-data-model-collapse',
        # University
        'chch.ox.ac.uk/news/could-machine-learning-models',
        'cs.ox.ac.uk/news/2356-full',
        'ischool.berkeley.edu/news/2024/hany-farid-reflects-model-collapse',
        # Discussion
        'news.ycombinator.com/item?id=41058194',
        'tech.slashdot.org/story/24/07/26/0016252/',
        # Reference
        'en.wikipedia.org/wiki/Model_collapse',
    ]

    auto_accepted = 0
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    # Auto-accept by search term
    for term in high_signal_terms:
        cursor.execute('''
            UPDATE posts
            SET relevant = 1,
                relevance_rationale = ?,
                relevance_classified_at = ?
            WHERE relevant IS NULL
            AND search_term_matched LIKE ?
        ''', ('auto-accepted: high-signal search term', now, f'%{term}%'))
        auto_accepted += cursor.rowcount

    # Auto-accept by news coverage URL in post text
    for url_fragment in news_coverage_urls:
        cursor.execute('''
            UPDATE posts
            SET relevant = 1,
                relevance_rationale = ?,
                relevance_classified_at = ?
            WHERE relevant IS NULL
            AND text LIKE ?
        ''', (f'auto-accepted: news coverage URL ({url_fragment})', now,
              f'%{url_fragment}%'))
        auto_accepted += cursor.rowcount

    # Auto-accept by news coverage URL in parent_text or quoted_text
    for url_fragment in news_coverage_urls:
        cursor.execute('''
            UPDATE posts
            SET relevant = 1,
                relevance_rationale = ?,
                relevance_classified_at = ?
            WHERE relevant IS NULL
            AND id IN (
                SELECT post_id FROM post_context
                WHERE parent_text LIKE ? OR quoted_text LIKE ?
            )
        ''', (f'auto-accepted: news coverage URL in context ({url_fragment})',
              now, f'%{url_fragment}%', f'%{url_fragment}%'))
        auto_accepted += cursor.rowcount

    conn.commit()
    return auto_accepted


def get_unclassified_posts(conn: sqlite3.Connection) -> list[dict]:
    """Query remaining unclassified posts."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.text, p.search_term_matched,
               pc.parent_text, pc.quoted_text
        FROM posts p
        LEFT JOIN post_context pc ON p.id = pc.post_id
        WHERE p.relevant IS NULL
        ORDER BY p.id
    ''')

    posts = []
    for row in cursor.fetchall():
        posts.append({
            'id': row['id'],
            'text': row['text'][:500] if row['text'] else '',
            'search_term': row['search_term_matched'] or '',
            'parent_text': row['parent_text'][:500] if row['parent_text'] else None,
            'quoted_text': row['quoted_text'][:500] if row['quoted_text'] else None,
        })

    return posts


def stage_batches(
    posts: list[dict],
    batch_size: int,
    output_dir: Path
) -> int:
    """Write posts to batch files and return number of batches created."""
    output_dir.mkdir(parents=True, exist_ok=True)

    num_batches = (len(posts) + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = start_idx + batch_size
        batch_posts = posts[start_idx:end_idx]

        batch_data = {
            'batch_id': f'batch_{batch_num + 1:03d}',
            'posts': batch_posts
        }

        batch_file = output_dir / f'batch_{batch_num + 1:03d}.json'
        with open(batch_file, 'w') as f:
            json.dump(batch_data, f, indent=2)

    return num_batches


def main():
    parser = argparse.ArgumentParser(
        description='Stage unclassified posts into batches for relevance classification'
    )
    parser.add_argument(
        '--db',
        default='/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db',
        help='Path to posts database'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='Posts per batch'
    )
    parser.add_argument(
        '--output-dir',
        default='/private/tmp/claude/relevance/',
        help='Output directory for batch files'
    )

    args = parser.parse_args()

    # Connect to database
    conn = get_db_connection(args.db)

    try:
        # Auto-accept high-signal posts
        auto_accepted = auto_accept_high_signal_posts(conn)
        print(f'Auto-accepted: {auto_accepted} posts')

        # Get remaining unclassified posts
        posts = get_unclassified_posts(conn)

        if not posts:
            print('No unclassified posts remaining')
            return

        # Stage batches
        output_dir = Path(args.output_dir)
        num_batches = stage_batches(posts, args.batch_size, output_dir)

        # Print summary
        print(f'Total batches staged: {num_batches}')
        print(f'Posts per batch: {args.batch_size}')
        print(f'Output directory: {output_dir}')
        print(f'Total posts staged: {len(posts)}')

    finally:
        conn.close()


if __name__ == '__main__':
    main()
