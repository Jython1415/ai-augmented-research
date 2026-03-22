# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Summary statistics and epoch trend analysis for model collapse citation study."""

import sqlite3
import json
from pathlib import Path
from collections import Counter

DB_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")
FIGURES_DIR = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/figures")
FIGURES_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

# === PASS 1 DATA (from citation_units) ===
pass1 = conn.execute("""
    SELECT cu.id, cu.claim_strength, cu.paper_fidelity, cu.field_accuracy, cu.epoch,
           cu.citation_type, cu.created_at
    FROM citation_units cu
    WHERE cu.coding_pass = 1
""").fetchall()

# === PASS 2 DATA (from coding_pass2) ===
pass2 = conn.execute("""
    SELECT cp2.citation_unit_id as id, cp2.claim_strength, cp2.paper_fidelity,
           cp2.field_accuracy, cu.epoch,
           cu.citation_type, cu.created_at
    FROM coding_pass2 cp2
    JOIN citation_units cu ON cu.id = cp2.citation_unit_id
""").fetchall()

# === AUTHOR DATA ===
authors = conn.execute("""
    SELECT ap.*, p.uri
    FROM author_profiles ap
    JOIN posts p ON p.author_did = ap.did
    JOIN citation_units cu ON cu.anchor_post_uri = p.uri
""").fetchall()

print("=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

for pass_name, data in [("Pass 1 (post-only)", pass1), ("Pass 2 (with-context)", pass2)]:
    print(f"\n### {pass_name} (n={len(data)})")

    for dim in ["claim_strength", "paper_fidelity", "field_accuracy"]:
        counts = Counter(r[dim] for r in data)
        total = sum(counts.values())
        print(f"\n  {dim}:")
        for val, n in sorted(counts.items()):
            print(f"    {val}: {n} ({n/total*100:.1f}%)")

    # By epoch
    print(f"\n  By epoch:")
    epoch_counts = Counter(r["epoch"] for r in data if r["epoch"] is not None)
    for epoch, n in sorted(epoch_counts.items()):
        print(f"    Epoch {epoch}: {n}")
    if any(r["epoch"] is None for r in data):
        null_count = sum(1 for r in data if r["epoch"] is None)
        print(f"    (NULL): {null_count}")

    # By citation type
    print(f"\n  By citation type:")
    type_counts = Counter(r["citation_type"] for r in data if r["citation_type"] is not None)
    for ct, n in sorted(type_counts.items()):
        print(f"    {ct}: {n}")

# === TWO-PASS COMPARISON ===
print("\n" + "=" * 60)
print("TWO-PASS COMPARISON")
print("=" * 60)

pass1_by_id = {r["id"]: r for r in pass1}
pass2_by_id = {r["id"]: r for r in pass2}

common_ids = set(pass1_by_id.keys()) & set(pass2_by_id.keys())
print(f"\nCUs in both passes: {len(common_ids)}")

for dim in ["claim_strength", "paper_fidelity", "field_accuracy"]:
    changed = 0
    changes = []
    for cid in common_ids:
        v1 = pass1_by_id[cid][dim]
        v2 = pass2_by_id[cid][dim]
        if v1 != v2:
            changed += 1
            changes.append((v1, v2))

    print(f"\n  {dim}: {changed}/{len(common_ids)} changed ({changed/len(common_ids)*100:.1f}%)")
    if changes:
        change_counts = Counter(changes)
        for (v1, v2), n in change_counts.most_common(5):
            print(f"    {v1} → {v2}: {n}")

# === AUTHOR STATS ===
print("\n" + "=" * 60)
print("AUTHOR STATISTICS")
print("=" * 60)
print(f"\nTotal unique authors: {len(set(r['did'] for r in authors))}")

# Follower stats
followers = [r["followers_count"] for r in authors if r["followers_count"] is not None]
if followers:
    import numpy as np
    print(f"Followers: median={np.median(followers):.0f}, mean={np.mean(followers):.0f}, max={max(followers)}")

conn.close()
print("\nDone.")
