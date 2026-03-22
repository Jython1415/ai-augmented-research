# /// script
# requires-python = ">=3.11"
# ///
"""Apply verification results to the database.
Flips confirmed false positives to relevant=0 and updates rationale."""

import sqlite3

DB_PATH = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"

# Confirmed false positives from verification pass
confirmed_fps = [
    # Different papers (17)
    155, 158, 564, 825, 827, 832, 3468, 3470, 3471,
    4098, 4099, 4100, 4101, 4102, 4103, 4116, 6570,
    # Different topics (6)
    581,   # OpenAI pricing (wheresyoured.at)
    1342,  # Tailwind business model collapse
    1890,  # TechCrunch about LLM bubble
    2293,  # Brain-AI alignment arxiv paper
    3490,  # JAMA medical EMR article
    5581,  # Substack business collapse
    # Manual review FPs (6)
    583,   # Peak AI newsletter, not model collapse
    591,   # LiveScience world model robustness (different collapse type)
    705,   # "the first paper" — too vague, no specific identification
    3687,  # Concept description only, no URL or citation
    3726,  # IBM Granite LoRA feature, not citing the paper
    3887,  # Concept description only, no URL or citation
]

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")

# Verify these are currently relevant=1
current = conn.execute(
    f"SELECT id, relevant FROM posts WHERE id IN ({','.join('?' * len(confirmed_fps))})",
    confirmed_fps
).fetchall()

currently_relevant = [r[0] for r in current if r[1] == 1]
not_relevant = [r[0] for r in current if r[1] != 1]

print(f"Confirmed false positives: {len(confirmed_fps)}")
print(f"Currently marked relevant: {len(currently_relevant)}")
if not_relevant:
    print(f"WARNING: Already not relevant: {not_relevant}")

# Update: set relevant=0 and append verification note to rationale
for pid in currently_relevant:
    conn.execute(
        "UPDATE posts SET relevant = 0, relevance_rationale = relevance_rationale || ' [VERIFICATION: false positive]' WHERE id = ?",
        (pid,)
    )

conn.commit()

# Verify final counts
total = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
relevant = conn.execute("SELECT COUNT(*) FROM posts WHERE relevant = 1").fetchone()[0]
not_rel = conn.execute("SELECT COUNT(*) FROM posts WHERE relevant = 0").fetchone()[0]
unclass = conn.execute("SELECT COUNT(*) FROM posts WHERE relevant IS NULL").fetchone()[0]

print(f"\nUpdated {len(currently_relevant)} posts to not relevant")
print(f"\nFinal counts:")
print(f"  Total: {total}")
print(f"  Relevant: {relevant}")
print(f"  Not relevant: {not_rel}")
print(f"  Unclassified: {unclass}")

conn.close()
