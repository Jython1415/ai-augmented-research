#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Create a balanced ICR sample with known positives AND negatives for narrow scope calibration.
Need roughly 50/50 split to get meaningful Krippendorff's alpha."""

import json
import random
import sqlite3

random.seed(42)

DB = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"
OUTPUT = "/private/tmp/claude/relevance/icr_sample_v2.json"
SAMPLE_SIZE = 50

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# Get LIKELY POSITIVE posts (high-signal search terms or text mentions)
likely_positives = conn.execute("""
    SELECT p.id, p.text, p.search_term_matched,
           pc.parent_text, pc.quoted_text
    FROM posts p
    LEFT JOIN post_context pc ON p.id = pc.post_id
    WHERE p.search_term_matched IN ('arxiv.org/abs/2305.17493', '10.1038/s41586-024-07566-y', 'shumailov', 'trained on recursively generated')
       OR LOWER(p.text) LIKE '%shumailov%'
       OR p.text LIKE '%2305.17493%'
       OR p.text LIKE '%s41586-024-07566%'
    ORDER BY RANDOM()
    LIMIT 25
""").fetchall()

# Get LIKELY NEGATIVE posts (broad/metaphorical terms)
likely_negatives = conn.execute("""
    SELECT p.id, p.text, p.search_term_matched,
           pc.parent_text, pc.quoted_text
    FROM posts p
    LEFT JOIN post_context pc ON p.id = pc.post_id
    WHERE p.search_term_matched IN ('model collapse', 'AI ouroboros', 'Habsburg AI', 'AI eating itself', 'AI feeding on itself', 'digital inbreeding')
       AND LOWER(p.text) NOT LIKE '%shumailov%'
       AND p.text NOT LIKE '%2305.17493%'
       AND p.text NOT LIKE '%s41586-024-07566%'
    ORDER BY RANDOM()
    LIMIT 25
""").fetchall()

sample = list(likely_positives) + list(likely_negatives)
random.shuffle(sample)

# Trim to exact size
sample = sample[:SAMPLE_SIZE]

output = {
    "batch_id": "icr_calibration_v2",
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

# Report
pos_count = len(likely_positives)
neg_count = len(likely_negatives)
term_counts = {}
for post in sample:
    t = post["search_term_matched"]
    term_counts[t] = term_counts.get(t, 0) + 1

print(f"ICR v2 sample created: {len(sample)} posts")
print(f"  Likely positives: {pos_count}")
print(f"  Likely negatives: {neg_count}")
print(f"Output: {OUTPUT}")
print("\nDistribution by search term:")
for t, c in sorted(term_counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

conn.close()
