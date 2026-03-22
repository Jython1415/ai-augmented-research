#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Create a stratified 50-post sample for ICR calibration.
Ensures representation across search terms and difficulty levels."""

import json
import random
import sqlite3

random.seed(42)  # Reproducible

DB = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"
OUTPUT = "/private/tmp/claude/relevance/icr_sample.json"
SAMPLE_SIZE = 50

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# Get all non-auto-accepted posts with context
rows = conn.execute("""
    SELECT p.id, p.text, p.search_term_matched,
           pc.parent_text, pc.quoted_text
    FROM posts p
    LEFT JOIN post_context pc ON p.id = pc.post_id
    WHERE p.relevant IS NULL
    ORDER BY p.id
""").fetchall()

# Group by search term
by_term = {}
for r in rows:
    term = r["search_term_matched"]
    by_term.setdefault(term, []).append(dict(r))

# Stratified sampling: at least 1 from each term, rest proportional
sample = []
terms_with_posts = {t: posts for t, posts in by_term.items() if posts}

# First pass: 1 from each term
for term, posts in terms_with_posts.items():
    picked = random.choice(posts)
    sample.append(picked)
    posts.remove(picked)

# Second pass: fill remaining proportionally
remaining = SAMPLE_SIZE - len(sample)
total_remaining = sum(len(posts) for posts in terms_with_posts.values())

for term, posts in sorted(terms_with_posts.items(), key=lambda x: len(x[1]), reverse=True):
    if remaining <= 0:
        break
    n = max(0, round(len(posts) / total_remaining * remaining))
    if n > 0:
        picked = random.sample(posts, min(n, len(posts)))
        sample.extend(picked)

# Trim to exact size
sample = sample[:SAMPLE_SIZE]
random.shuffle(sample)

# Format output
output = {
    "batch_id": "icr_calibration",
    "posts": []
}

for post in sample:
    output["posts"].append({
        "id": post["id"],
        "text": post["text"][:500] if post["text"] else "",
        "search_term": post["search_term_matched"],
        "parent_text": (post["parent_text"] or "")[:500] or None,
        "quoted_text": (post["quoted_text"] or "")[:500] or None,
    })

with open(OUTPUT, "w") as f:
    json.dump(output, f, indent=2)

# Report distribution
term_counts = {}
for post in sample:
    t = post["search_term_matched"]
    term_counts[t] = term_counts.get(t, 0) + 1

print(f"ICR sample created: {len(sample)} posts")
print(f"Output: {OUTPUT}")
print("\nDistribution by search term:")
for t, c in sorted(term_counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

conn.close()
