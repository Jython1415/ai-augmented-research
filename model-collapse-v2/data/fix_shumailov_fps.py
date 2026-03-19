# /// script
# requires-python = ">=3.11"
# ///
"""Fix false positives: posts about Shumailov's OTHER papers + non-English + no-signal posts.
These were auto-accepted because 'shumailov' was a high-signal search term,
but they are about his other research (backdoors, prompt injection, privacy, etc.),
not the model collapse paper (2305.17493 / Nature 631, 755-759)."""

import sqlite3

DB_PATH = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"

# False positives: Shumailov's OTHER papers (not model collapse)
other_paper_fps = [
    # Arxiv bot posts for non-model-collapse papers
    83,   # Buffer Overflow in MoE (2402.05526)
    82,   # Architectural Neural Backdoors (2402.06957)
    79,   # Locking ML Models into Hardware (2405.20990)
    78,   # False Sense of Safety (2407.02551)
    71,   # Stealing User Prompts from MoE (2410.22884)
    70,   # Breach By A Thousand Leaks (2407.02551)
    67,   # Beyond Labeling Oracles (openreview)
    66,   # Trusted ML Models Private Inference (2501.08970)
    61,   # Interpreting Repeated Token Phenomenon (2503.08908)
    60,   # Defeating Prompt Injections (2503.18813)
    59,   # Defeating Prompt Injections (2503.18813)
    58,   # LLMs Verbatim Reproduce Malicious Sequences (2503.17578)
    57,   # Defeating Prompt Injections (2503.18813) - arxiv bot format
    56,   # SEA forensics system (2308.11845)
    55,   # Watermarking Input Repetition Masking (2504.12229)
    53,   # Fixing 7,400 Bugs for $1 (2505.13103)
    52,   # Defending Gemini Against Prompt Injections (2505.14534)
    51,   # Defending Gemini Against Prompt Injections (2505.14534)
    50,   # Architectural Backdoors (2505.18323)
    49,   # Strong Membership Inference Attacks (2505.18773)
    48,   # Architectural Backdoors (2505.18323)
    47,   # ML Supply Chain Problem (2505.22778)
    46,   # Cascading Adversarial Bias (2505.24842)
    45,   # Generalized Gaussian Mechanism (2506.12553)
    44,   # Generalized Gaussian Mechanism (2506.12553)
    43,   # Reasoning Poisoning Attacks (2509.05739)
    42,   # Reasoning Poisoning Attacks (2509.05739)
    40,   # Extracting alignment data (2510.18554)
    39,   # Soft Instruction De-escalation (2510.21057)
    38,   # Soft Instruction De-escalation (2510.21057)
    35,   # ceLLMate Browser Agents (2512.12594)
    34,   # ceLLMate Browser Agents (2512.12594)
    33,   # Iterative Deployment Planning (2512.24940)
    32,   # CaMeLs Computer Use Agents (2601.09923)
    31,   # Thought-Transfer Poisoning (2601.19061)
    29,   # Kraken EM Side-Channel Attacks (2603.02891)
    86,   # LLM Censorship (2307.10719) — arxiv ID in text, no URL
    36,   # Membership Inference Attacks collaboration
    68,   # Conference lineup — no model collapse content
]

# No citation signal — search matched but text doesn't contain "shumailov"
no_signal_fps = [
    77,   # "Ope" — just an exclamation, no shumailov in text
    54,   # AI content consumption complaint — no shumailov in text
]

# Non-English (correct topic but excluded per English-only decision)
non_english = [
    74,   # Spanish post about Shumailov's Nature findings
]

all_fps = other_paper_fps + no_signal_fps + non_english

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")

# Verify these are currently relevant=1
current = conn.execute(
    f"SELECT id, relevant FROM posts WHERE id IN ({','.join('?' * len(all_fps))})",
    all_fps
).fetchall()

currently_relevant = [r[0] for r in current if r[1] == 1]
not_relevant = [r[0] for r in current if r[1] != 1]
missing = set(all_fps) - {r[0] for r in current}

print(f"Posts to fix: {len(all_fps)}")
print(f"  Other paper FPs: {len(other_paper_fps)}")
print(f"  No citation signal: {len(no_signal_fps)}")
print(f"  Non-English: {len(non_english)}")
print(f"Currently marked relevant: {len(currently_relevant)}")
if not_relevant:
    print(f"WARNING: Already not relevant: {not_relevant}")
if missing:
    print(f"WARNING: Not found in DB: {missing}")

# Update: set relevant=0 and append verification note
for pid in currently_relevant:
    if pid in non_english:
        note = " [POST-VERIFICATION: non-English exclusion]"
    elif pid in no_signal_fps:
        note = " [POST-VERIFICATION: no citation signal in text]"
    else:
        note = " [POST-VERIFICATION: wrong Shumailov paper]"

    conn.execute(
        "UPDATE posts SET relevant = 0, relevance_rationale = relevance_rationale || ? WHERE id = ?",
        (note, pid)
    )

conn.commit()

# Also remove citation units for these posts
uris = conn.execute(
    f"SELECT id, uri FROM posts WHERE id IN ({','.join('?' * len(all_fps))})",
    all_fps
).fetchall()

uri_map = {r[0]: r[1] for r in uris}
cu_ids_removed = []
for pid in currently_relevant:
    uri = uri_map.get(pid)
    if uri:
        # Get citation_unit_id before deleting
        cu = conn.execute("SELECT id FROM citation_units WHERE anchor_post_uri = ?", (uri,)).fetchone()
        if cu:
            cu_id = cu[0]
            # Delete thread context first (FK constraint)
            conn.execute("DELETE FROM thread_context WHERE citation_unit_id = ?", (cu_id,))
            conn.execute("DELETE FROM citation_units WHERE id = ?", (cu_id,))
            cu_ids_removed.append(cu_id)

conn.commit()
print(f"\nRemoved {len(cu_ids_removed)} citation units and their thread context")

# Final counts
total = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
relevant = conn.execute("SELECT COUNT(*) FROM posts WHERE relevant = 1").fetchone()[0]
not_rel = conn.execute("SELECT COUNT(*) FROM posts WHERE relevant = 0").fetchone()[0]
unclass = conn.execute("SELECT COUNT(*) FROM posts WHERE relevant IS NULL").fetchone()[0]
cu_count = conn.execute("SELECT COUNT(*) FROM citation_units").fetchone()[0]
tc_count = conn.execute("SELECT COUNT(*) FROM thread_context").fetchone()[0]

print(f"\nUpdated {len(currently_relevant)} posts to not relevant")
print(f"\nFinal counts:")
print(f"  Total posts: {total}")
print(f"  Relevant: {relevant}")
print(f"  Not relevant: {not_rel}")
print(f"  Unclassified: {unclass}")
print(f"  Citation units: {cu_count}")
print(f"  Thread context: {tc_count}")

conn.close()
