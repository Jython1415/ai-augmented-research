# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build stratified calibration sample for ICR: 50 posts across epochs and citation types."""

import sqlite3
import json
import random
from pathlib import Path

random.seed(42)  # Reproducible sample

DB_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")
OUTPUT_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/calibration_sample.json")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

# Epoch boundaries
EPOCHS = [
    (2, None, '2024-04-01'),
    (3, '2024-04-01', '2024-07-01'),
    (4, '2024-07-01', '2024-10-01'),
    (5, '2024-10-01', '2025-03-01'),
    (6, '2025-03-01', None),
]

# Target: ~10 per epoch, total 50
# Epoch 3 only has 9 posts, so take all 9
TARGETS = {2: 10, 3: 9, 4: 10, 5: 11, 6: 10}

sample = []

for epoch_num, start, end in EPOCHS:
    target = TARGETS[epoch_num]

    where = "WHERE 1=1"
    params = []
    if start:
        where += " AND cu.created_at >= ?"
        params.append(start)
    if end:
        where += " AND cu.created_at < ?"
        params.append(end)

    rows = conn.execute(f"""
        SELECT cu.id as cu_id, cu.anchor_post_uri, cu.citation_type, cu.created_at,
               p.id as post_id, p.text, p.search_term_matched, p.relevance_rationale,
               pc.parent_text, pc.quoted_text,
               (SELECT GROUP_CONCAT(tc.post_text, '|||')
                FROM thread_context tc
                WHERE tc.citation_unit_id = cu.id AND tc.relationship = 'parent'
                ORDER BY tc.depth) as parent_chain,
               (SELECT GROUP_CONCAT(tc.post_text, '|||')
                FROM thread_context tc
                WHERE tc.citation_unit_id = cu.id AND tc.relationship = 'self_reply'
                ORDER BY tc.depth) as self_replies
        FROM citation_units cu
        JOIN posts p ON p.uri = cu.anchor_post_uri
        LEFT JOIN post_context pc ON p.id = pc.post_id
        {where}
        ORDER BY RANDOM()
    """, params).fetchall()

    # Take up to target, trying to get citation type diversity
    by_type = {}
    for r in rows:
        ct = r['citation_type']
        if ct not in by_type:
            by_type[ct] = []
        by_type[ct].append(r)

    # Round-robin across types
    selected = []
    types = list(by_type.keys())
    random.shuffle(types)
    idx = 0
    while len(selected) < target and any(by_type.values()):
        ct = types[idx % len(types)]
        if by_type[ct]:
            selected.append(by_type[ct].pop(0))
        idx += 1
        # Remove empty types
        types = [t for t in types if by_type.get(t)]
        if not types:
            break

    for r in selected:
        sample.append({
            "cu_id": r['cu_id'],
            "post_id": r['post_id'],
            "epoch": epoch_num,
            "citation_type": r['citation_type'],
            "created_at": r['created_at'],
            "text": r['text'],
            "parent_text": r['parent_text'],
            "quoted_text": r['quoted_text'],
            "parent_chain": r['parent_chain'],
            "self_replies": r['self_replies'],
        })

conn.close()

# Summary
print(f"Calibration sample: {len(sample)} posts")
epoch_counts = {}
type_counts = {}
for s in sample:
    epoch_counts[s['epoch']] = epoch_counts.get(s['epoch'], 0) + 1
    type_counts[s['citation_type']] = type_counts.get(s['citation_type'], 0) + 1

print(f"By epoch: {dict(sorted(epoch_counts.items()))}")
print(f"By type: {dict(sorted(type_counts.items()))}")

# Save
with open(OUTPUT_PATH, 'w') as f:
    json.dump(sample, f, indent=2)

print(f"\nSaved to {OUTPUT_PATH}")
