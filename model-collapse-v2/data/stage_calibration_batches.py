# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stage calibration batches for 3 independent Haiku coders.
Each coder gets the same 50 posts in the same order."""

import json
from pathlib import Path

SAMPLE_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/calibration_sample.json")
BATCH_DIR = Path("/private/tmp/claude/coding/calibration")
BATCH_DIR.mkdir(parents=True, exist_ok=True)

with open(SAMPLE_PATH) as f:
    sample = json.load(f)

# Build batch content: each post as a coding unit
batch_posts = []
for s in sample:
    post = {
        "post_id": s["post_id"],
        "cu_id": s["cu_id"],
        "epoch": s["epoch"],
        "citation_type": s["citation_type"],
        "created_at": s["created_at"],
        "text": s["text"],
    }
    # Include context if available (for pass 2 later; pass 1 = post-only)
    if s.get("parent_text"):
        post["parent_text"] = s["parent_text"]
    if s.get("quoted_text"):
        post["quoted_text"] = s["quoted_text"]
    batch_posts.append(post)

# Stage for 3 coders — same input, different result files
for coder_id in range(1, 4):
    batch_file = BATCH_DIR / f"calibration_coder_{coder_id}.json"
    result_file = BATCH_DIR / f"calibration_results_coder_{coder_id}.json"

    with open(batch_file, 'w') as f:
        json.dump(batch_posts, f, indent=2)

    print(f"Coder {coder_id}: {batch_file} ({len(batch_posts)} posts)")
    print(f"  Results → {result_file}")

print(f"\nTotal: {len(batch_posts)} posts × 3 coders = {len(batch_posts) * 3} coding tasks")
