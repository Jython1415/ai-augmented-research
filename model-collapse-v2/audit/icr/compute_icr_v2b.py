#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["krippendorff", "numpy"]
# ///

"""Compute Krippendorff's alpha for ICR v2b calibration (balanced sample)."""

import json
import numpy as np
import krippendorff

CODER_FILES = [
    "/private/tmp/claude/relevance/icr_v2b_coder1.json",
    "/private/tmp/claude/relevance/icr_v2b_coder2.json",
    "/private/tmp/claude/relevance/icr_v2b_coder3.json",
]

coders = []
for path in CODER_FILES:
    with open(path) as f:
        data = json.load(f)
    mapping = {}
    for c in data["classifications"]:
        mapping[c["id"]] = 1 if c["relevant"] else 0
    coders.append(mapping)

all_ids = sorted(set().union(*[set(c.keys()) for c in coders]))
print(f"Posts coded: {len(all_ids)}")
print(f"Coders: {len(coders)}")

reliability_data = np.full((len(coders), len(all_ids)), np.nan)
for i, coder in enumerate(coders):
    for j, post_id in enumerate(all_ids):
        if post_id in coder:
            reliability_data[i, j] = coder[post_id]

alpha = krippendorff.alpha(reliability_data, level_of_measurement="nominal")

print(f"\nKrippendorff's alpha: {alpha:.4f}")
if alpha >= 0.800:
    print("STRONG agreement -- proceed with confidence")
elif alpha >= 0.667:
    print("ACCEPTABLE agreement -- proceed with caution")
else:
    print("BELOW THRESHOLD -- revise instructions")

agreements = 0
disagreements = []
for j, post_id in enumerate(all_ids):
    values = [reliability_data[i, j] for i in range(len(coders)) if not np.isnan(reliability_data[i, j])]
    if len(set(values)) == 1:
        agreements += 1
    else:
        disagreements.append(post_id)

print(f"\nFull agreement: {agreements}/{len(all_ids)} ({100*agreements/len(all_ids):.1f}%)")
print(f"Disagreements: {len(disagreements)}")

if disagreements:
    print("\nDisagreed post IDs and coder votes:")
    for post_id in disagreements:
        votes = []
        for i, coder_data in enumerate(coders):
            if post_id in coder_data:
                votes.append(f"coder{i+1}={'R' if coder_data[post_id] else 'NR'}")
        print(f"  ID {post_id}: {', '.join(votes)}")

print("\nPer-coder relevant counts:")
for i, coder in enumerate(coders):
    relevant = sum(1 for v in coder.values() if v == 1)
    print(f"  Coder {i+1}: {relevant}/{len(coder)} relevant ({100*relevant/len(coder):.1f}%)")
