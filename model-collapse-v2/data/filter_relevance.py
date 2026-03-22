#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic", "httpx[socks]"]
# ///

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_unclassified_posts(conn: sqlite3.Connection, limit: int | None = None) -> list[dict]:
    """Fetch unclassified posts from the database."""
    query = "SELECT id, text, search_term_matched FROM posts WHERE relevant IS NULL ORDER BY id"
    if limit:
        query += f" LIMIT {limit}"

    cursor = conn.cursor()
    cursor.execute(query)
    posts = [dict(row) for row in cursor.fetchall()]
    return posts


def is_auto_accepted(post: dict) -> bool:
    """Check if a post should be auto-accepted based on high-signal search terms."""
    high_signal_terms = [
        "arxiv.org/abs/2305.17493",
        "10.1038/s41586-024-07566-y",
        "trained on recursively generated",
        "shumailov",
    ]

    search_term = post.get("search_term_matched", "")
    text = post.get("text", "")

    for term in high_signal_terms:
        if term.lower() in search_term.lower() or term.lower() in text.lower():
            return True
    return False


def format_posts_for_api(posts: list[dict]) -> str:
    """Format posts for API submission."""
    message = "Here are posts to classify. Respond with ONLY a JSON array.\n\n"

    for i, post in enumerate(posts, 1):
        post_id = post["id"]
        search_term = post.get("search_term_matched", "")
        text = post["text"][:500]  # Truncate to 500 chars

        message += f"Post {i} (ID: {post_id}, search_term: {search_term}):\n{text}\n\n"

    return message


def classify_posts_batch(client: Anthropic, posts: list[dict]) -> list[dict]:
    """Send a batch of posts to Haiku for classification."""
    system_prompt = """You are classifying Bluesky posts for a research study about how people cite the paper "AI models collapse when trained on recursively generated data" by Shumailov et al. (2024), published in Nature.

For each post, determine: Does this post reference, cite, or engage with the findings of this specific paper (or the concept it popularized)?

A post is RELEVANT if it:
- Directly links to or mentions the paper, its authors, or its title
- Discusses model collapse as a consequence of training AI on AI-generated data (the paper's core finding)
- Uses metaphors popularized by coverage of this paper (Habsburg AI, AI ouroboros, AI eating itself) in the context of AI training data quality
- References the specific claim that AI models degrade when trained on synthetic/AI-generated data

A post is NOT RELEVANT if it:
- Uses "model collapse" in a non-AI context (economics, healthcare, philosophy, mode collapse in GANs)
- Discusses AI generally without connecting to the recursive training / synthetic data degradation concept
- Uses metaphors like "ouroboros" or "eating itself" about AI but NOT about training data quality
- Is about a completely different topic that happens to match search keywords

For each post, respond with a JSON array of objects with keys: "id" (the post ID), "relevant" (true/false), "rationale" (one sentence explaining why)."""

    user_message = format_posts_for_api(posts)

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        response_text = response.content[0].text

        # Try to extract JSON array from response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if not json_match:
            print(f"⚠️  Warning: Could not find JSON array in response", file=sys.stderr)
            return []

        json_str = json_match.group(0)
        classifications = json.loads(json_str)

        return classifications

    except json.JSONDecodeError as e:
        print(f"⚠️  Warning: Failed to parse JSON response: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"⚠️  Warning: API call failed: {e}", file=sys.stderr)
        return []


def retry_classify_posts_batch(client: Anthropic, posts: list[dict], max_retries: int = 1) -> list[dict]:
    """Classify posts with retry logic."""
    for attempt in range(max_retries + 1):
        result = classify_posts_batch(client, posts)
        if result:
            return result

        if attempt < max_retries:
            print(f"  Retrying in 2 seconds...", file=sys.stderr)
            time.sleep(2)

    return []


def update_post_classification(conn: sqlite3.Connection, post_id: int, relevant: int, rationale: str) -> None:
    """Update a post's classification in the database."""
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE posts
           SET relevant = ?, relevance_rationale = ?, relevance_classified_at = datetime('now')
           WHERE id = ?""",
        (relevant, rationale, post_id),
    )
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Classify posts for relevance to Shumailov et al. (2024)")
    parser.add_argument(
        "--db",
        default="/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db",
        help="Path to the posts database",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of posts to classify",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of posts per API call",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show classifications without writing to DB",
    )

    args = parser.parse_args()

    # Verify database exists
    if not Path(args.db).exists():
        print(f"Error: Database not found at {args.db}", file=sys.stderr)
        sys.exit(1)

    # Initialize API client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Load unclassified posts
    conn = get_db_connection(args.db)
    posts = get_unclassified_posts(conn, args.limit)

    if not posts:
        print("No unclassified posts found.")
        conn.close()
        return

    print(f"Found {len(posts)} unclassified posts.")

    # Separate auto-accepted and API-classified posts
    auto_accepted = []
    api_classify = []

    for post in posts:
        if is_auto_accepted(post):
            auto_accepted.append(post)
        else:
            api_classify.append(post)

    total_relevant = 0
    total_not_relevant = 0

    # Process auto-accepted posts
    if auto_accepted:
        print(f"\nAuto-accepting {len(auto_accepted)} posts from high-signal search terms...")
        for post in auto_accepted:
            if not args.dry_run:
                update_post_classification(
                    conn,
                    post["id"],
                    1,
                    "auto-accepted: high-signal search term",
                )
            total_relevant += 1
        print(f"  Auto-accepted {len(auto_accepted)} posts as relevant")

    # Process API-classified posts
    if api_classify:
        total_batches = (len(api_classify) + args.batch_size - 1) // args.batch_size
        print(f"\nClassifying {len(api_classify)} posts via API ({total_batches} batches)...")

        for batch_num in range(0, len(api_classify), args.batch_size):
            batch = api_classify[batch_num : batch_num + args.batch_size]
            batch_index = batch_num // args.batch_size + 1

            classifications = retry_classify_posts_batch(client, batch)

            if not classifications:
                print(
                    f"  [{batch_index}/{total_batches}] ⚠️  Failed to classify batch, skipping",
                    file=sys.stderr,
                )
                continue

            batch_relevant = 0
            batch_not_relevant = 0

            for classification in classifications:
                post_id = classification.get("id")
                relevant = classification.get("relevant", False)
                rationale = classification.get("rationale", "")

                # Find the post to validate it exists
                post_exists = any(p["id"] == post_id for p in batch)
                if not post_exists:
                    continue

                if not args.dry_run:
                    update_post_classification(conn, post_id, 1 if relevant else 0, rationale)

                if relevant:
                    batch_relevant += 1
                    total_relevant += 1
                else:
                    batch_not_relevant += 1
                    total_not_relevant += 1

            print(
                f"  [{batch_index}/{total_batches}] Classified {len(batch)} posts: "
                f"{batch_relevant} relevant, {batch_not_relevant} not relevant"
            )

            # Rate limiting between batches
            if batch_num + args.batch_size < len(api_classify):
                time.sleep(0.5)

    # Summary
    print(f"\n=== Summary ===")
    print(f"Total classified: {total_relevant + total_not_relevant}")
    print(f"Total relevant: {total_relevant}")
    print(f"Total not relevant: {total_not_relevant}")

    conn.close()


if __name__ == "__main__":
    main()
