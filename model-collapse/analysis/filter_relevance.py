#!/usr/bin/env python3
"""
/// script
requires-python = ">=3.8"
dependencies = ["anthropic"]
///
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

from anthropic import Anthropic


def init_database(db_path: str) -> None:
    """Initialize database columns if they don't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add columns if they don't exist
    cursor.execute("""
        PRAGMA table_info(posts)
    """)
    columns = {row[1] for row in cursor.fetchall()}

    if "is_relevant" not in columns:
        cursor.execute("ALTER TABLE posts ADD COLUMN is_relevant INTEGER")
        conn.commit()
        print("Added is_relevant column")

    if "relevance_confidence" not in columns:
        cursor.execute("ALTER TABLE posts ADD COLUMN relevance_confidence REAL")
        conn.commit()
        print("Added relevance_confidence column")

    conn.close()


def get_unclassified_posts(db_path: str, limit: int = None) -> list[dict]:
    """Fetch posts that haven't been classified yet."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT id, text, search_term_matched FROM posts WHERE is_relevant IS NULL"

    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    posts = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return posts


def classify_post(client: Anthropic, post_text: str) -> dict:
    """Classify a single post using Claude API."""
    prompt = f"""You are classifying whether a Bluesky post is relevant to "model collapse" discourse — the phenomenon where AI models degrade when trained on synthetic/AI-generated data.

A post is RELEVANT if it:
- Discusses model collapse, AI training on AI-generated data, or recursive training degradation
- References the Shumailov et al. paper, "Habsburg AI", or "Model Autophagy Disorder"
- Makes claims about AI models degrading from synthetic data
- Discusses training data quality in the context of AI-generated contamination

A post is NOT RELEVANT if it:
- Uses "collapse" in a different context (economic collapse, building collapse, etc.)
- Discusses "tail" in non-ML context
- Discusses synthetic data but NOT in context of model degradation
- Is about recursive algorithms but not recursive training on generated data

Post text: {post_text}

Respond with ONLY a JSON object:
{{"relevant": true/false, "confidence": 0.0-1.0, "reason": "brief reason"}}"""

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            result = json.loads(response_text)
            return result

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}", file=sys.stderr)
            print(f"Response text: {response_text}", file=sys.stderr)
            return {"relevant": False, "confidence": 0.0, "reason": "JSON parsing error"}

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                print(f"API error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                print(f"API error after {max_retries} attempts: {e}", file=sys.stderr)
                return {"relevant": False, "confidence": 0.0, "reason": "API error"}

    return {"relevant": False, "confidence": 0.0, "reason": "Max retries exceeded"}


def update_post_classification(db_path: str, post_id: int, classification: dict) -> None:
    """Update post with classification result."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    is_relevant = 1 if classification["relevant"] else 0
    confidence = classification.get("confidence", 0.0)

    cursor.execute(
        "UPDATE posts SET is_relevant = ?, relevance_confidence = ? WHERE id = ?",
        (is_relevant, confidence, post_id)
    )
    conn.commit()
    conn.close()


def get_summary_stats(db_path: str) -> dict:
    """Get summary statistics about classifications."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM posts WHERE is_relevant = 1")
    relevant_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posts WHERE is_relevant = 0")
    not_relevant_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT search_term_matched, COUNT(*) as count,
               SUM(CASE WHEN is_relevant = 1 THEN 1 ELSE 0 END) as relevant_count
        FROM posts
        WHERE is_relevant IS NOT NULL
        GROUP BY search_term_matched
    """)
    by_search_term = cursor.fetchall()

    conn.close()

    return {
        "relevant": relevant_count,
        "not_relevant": not_relevant_count,
        "by_search_term": by_search_term
    }


def main():
    parser = argparse.ArgumentParser(description="Classify Bluesky posts for model collapse relevance")
    parser.add_argument("--dry-run", action="store_true", help="Process only 10 posts for testing")
    parser.add_argument("--limit", type=int, help="Process only N posts")
    args = parser.parse_args()

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Database path
    db_path = "/Users/Joshua/agent/model-collapse-study/data/posts.db"

    if not Path(db_path).exists():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize database
    init_database(db_path)

    # Determine processing limit
    limit = None
    if args.dry_run:
        limit = 10
        print("Running in dry-run mode (10 posts)")
    elif args.limit:
        limit = args.limit
        print(f"Processing up to {limit} posts")

    # Get unclassified posts
    posts = get_unclassified_posts(db_path, limit)

    if not posts:
        print("No unclassified posts found")
        sys.exit(0)

    print(f"Found {len(posts)} posts to classify")

    # Initialize client
    client = Anthropic()

    # Process in batches
    batch_size = 50
    processed = 0

    for batch_start in range(0, len(posts), batch_size):
        batch_end = min(batch_start + batch_size, len(posts))
        batch = posts[batch_start:batch_end]

        print(f"Processing batch {batch_start // batch_size + 1} ({batch_start + 1}-{batch_end} of {len(posts)})")

        for post in batch:
            try:
                classification = classify_post(client, post["text"])
                update_post_classification(db_path, post["id"], classification)
                processed += 1

                status = "RELEVANT" if classification["relevant"] else "NOT RELEVANT"
                confidence = classification.get("confidence", 0)
                print(f"  [{processed}/{len(posts)}] {status} (confidence: {confidence:.2f})")

                # Small delay between requests to avoid rate limiting
                time.sleep(0.1)

            except Exception as e:
                print(f"Error processing post {post['id']}: {e}", file=sys.stderr)

        # Batch delay
        if batch_end < len(posts):
            time.sleep(1)

    # Print summary
    print("\n" + "=" * 60)
    print("CLASSIFICATION SUMMARY")
    print("=" * 60)

    stats = get_summary_stats(db_path)

    print(f"Total relevant posts: {stats['relevant']}")
    print(f"Total not relevant posts: {stats['not_relevant']}")

    print("\nBreakdown by search term:")
    for search_term, total, relevant in stats['by_search_term']:
        not_relevant = total - relevant if relevant else total
        print(f"  {search_term}: {relevant} relevant, {not_relevant} not relevant (total: {total})")

    print(f"\nProcessed {processed} posts in this run")


if __name__ == "__main__":
    main()
