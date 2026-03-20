#!/usr/bin/env python3
"""
Author demographics and reach analysis with V3 data.
"""

import sqlite3
from collections import defaultdict, Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

DB_PATH = Path(__file__).parent / "posts.db"
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 80)
print("AUTHOR DEMOGRAPHICS AND REACH ANALYSIS (V3)")
print("=" * 80)

# ============================================================================
# 1. AUTHOR DEMOGRAPHICS
# ============================================================================
print("\n1. AUTHOR DEMOGRAPHICS AND ROLE CATEGORIZATION")
print("-" * 80)

role_keywords = {
    "researcher/academic": ["professor", "phd", "researcher", "postdoc", "university", "academic"],
    "journalist/media": ["journalist", "reporter", "editor", "writer", "columnist"],
    "developer/tech": ["developer", "engineer", "programmer", "software", "tech", "data scientist"],
    "AI/ML specific": ["ai", "machine learning", "ml", "deep learning", "nlp"],
    "student": ["student", "studying", "grad student"],
}

cursor.execute("""
    SELECT DISTINCT cu.author_did, ap.bio, ap.followers_count, ap.handle, ap.display_name
    FROM citation_units cu
    LEFT JOIN author_profiles ap ON cu.author_did = ap.did
""")

authors_data = cursor.fetchall()
print(f"Total unique authors: {len(authors_data)}")

author_roles = defaultdict(set)
authors_with_bio = 0
authors_without_bio = 0

for row in authors_data:
    author_did = row["author_did"]
    bio = row["bio"]

    if bio:
        authors_with_bio += 1
        bio_lower = bio.lower()
        has_role = False

        for role, keywords in role_keywords.items():
            for keyword in keywords:
                if keyword in bio_lower:
                    author_roles[author_did].add(role)
                    has_role = True

        if not has_role:
            author_roles[author_did].add("other")
    else:
        authors_without_bio += 1
        author_roles[author_did].add("unknown")

print(f"Authors with bio: {authors_with_bio}")
print(f"Authors without bio: {authors_without_bio}")

role_counter = Counter()
for roles in author_roles.values():
    for role in roles:
        role_counter[role] += 1

print("\nRole Distribution (authors can have multiple roles):")
for role, count in role_counter.most_common():
    percentage = (count / len(authors_data)) * 100
    print(f"  {role}: {count} ({percentage:.1f}%)")

# ============================================================================
# 2. REPEAT CITER ANALYSIS
# ============================================================================
print("\n2. REPEAT CITER ANALYSIS")
print("-" * 80)

cursor.execute("""
    SELECT author_did, COUNT(*) as citation_count
    FROM citation_units
    GROUP BY author_did
    HAVING citation_count > 1
    ORDER BY citation_count DESC
""")

repeat_citers = cursor.fetchall()
print(f"Authors who cited the paper multiple times: {len(repeat_citers)}")

print("\nTop 10 Repeat Citers:")
for i, row in enumerate(repeat_citers[:10], 1):
    author_did = row["author_did"]
    count = row["citation_count"]

    cursor.execute("""
        SELECT cu.id, cp1.paper_fidelity, cp1.field_accuracy, cp1.claim_strength, cu.created_at
        FROM citation_units cu
        LEFT JOIN coding_pass1 cp1 ON cu.id = cp1.citation_unit_id
        WHERE cu.author_did = ?
        ORDER BY cu.created_at
    """, (author_did,))

    citations = cursor.fetchall()
    print(f"\n  {i}. Author {author_did[:8]}... ({count} citations)")

    for j, cite in enumerate(citations, 1):
        paper_fidelity = cite["paper_fidelity"] or "N/A"
        field_accuracy = cite["field_accuracy"] or "N/A"
        claim_strength = cite["claim_strength"] or "N/A"
        print(f"     Citation {j}: fidelity={paper_fidelity}, accuracy={field_accuracy}, strength={claim_strength}")

# ============================================================================
# 3. REACH CORRELATION ANALYSIS
# ============================================================================
print("\n3. REACH CORRELATION ANALYSIS")
print("-" * 80)

cursor.execute("""
    SELECT
        cu.id,
        cp1.paper_fidelity,
        cp1.field_accuracy,
        cu.author_did,
        ap.followers_count
    FROM citation_units cu
    LEFT JOIN coding_pass1 cp1 ON cu.id = cp1.citation_unit_id
    LEFT JOIN author_profiles ap ON cu.author_did = ap.did
    WHERE ap.followers_count IS NOT NULL
""")

correlation_data = cursor.fetchall()
print(f"Citation units with follower data: {len(correlation_data)}")

fidelity_map = {"accurate": 3, "partially_accurate": 2, "misrepresentation": 1, "not_applicable": None}
field_accuracy_map = {"accurate": 4, "partially_accurate": 3, "inaccurate": 2, "not_applicable": None}

followers = []
fidelity_scores = []
field_accuracy_scores = []

for row in correlation_data:
    followers.append(row["followers_count"])

    fidelity = fidelity_map.get(row["paper_fidelity"])
    if fidelity is not None:
        fidelity_scores.append(fidelity)

    field_acc = field_accuracy_map.get(row["field_accuracy"])
    if field_acc is not None:
        field_accuracy_scores.append(field_acc)

min_len = min(len(followers), len(fidelity_scores), len(field_accuracy_scores))
followers = followers[:min_len]
fidelity_scores = fidelity_scores[:min_len]
field_accuracy_scores = field_accuracy_scores[:min_len]

if len(followers) > 2 and len(fidelity_scores) > 2:
    corr_fidelity, p_fidelity = spearmanr(followers, fidelity_scores)
    print(f"\nSpearman correlation (followers vs paper_fidelity):")
    print(f"  r = {corr_fidelity:.4f}, p-value = {p_fidelity:.4f}")
else:
    print(f"\nInsufficient data for fidelity correlation")

if len(followers) > 2 and len(field_accuracy_scores) > 2:
    corr_field, p_field = spearmanr(followers, field_accuracy_scores)
    print(f"\nSpearman correlation (followers vs field_accuracy):")
    print(f"  r = {corr_field:.4f}, p-value = {p_field:.4f}")
else:
    print(f"\nInsufficient data for field_accuracy correlation")

# ============================================================================
# 4. VISUALIZATIONS
# ============================================================================
print("\n4. GENERATING VISUALIZATIONS")
print("-" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax1 = axes[0]
ax1.scatter(followers, fidelity_scores, alpha=0.6, s=60, color="steelblue")
ax1.set_xlabel("Author Followers (log scale)", fontsize=11)
ax1.set_ylabel("Paper Fidelity\n(3=accurate, 2=partial, 1=misrep)", fontsize=11)
ax1.set_title(f"Author Reach vs Paper Fidelity\n(r={corr_fidelity:.3f}, p={p_fidelity:.3f})" if 'corr_fidelity' in locals() else "Author Reach vs Paper Fidelity", fontsize=12)
ax1.set_xscale("log")
ax1.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.scatter(followers, field_accuracy_scores, alpha=0.6, s=60, color="darkgreen")
ax2.set_xlabel("Author Followers (log scale)", fontsize=11)
ax2.set_ylabel("Field Accuracy\n(4=accurate, 3=partial, 2=inaccurate)", fontsize=11)
ax2.set_title(f"Author Reach vs Field Accuracy\n(r={corr_field:.3f}, p={p_field:.3f})" if 'corr_field' in locals() else "Author Reach vs Field Accuracy", fontsize=12)
ax2.set_xscale("log")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "reach_vs_accuracy.png", dpi=300, bbox_inches="tight")
print(f"  Saved: reach_vs_accuracy.png")
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))

cursor.execute("SELECT followers_count FROM author_profiles WHERE followers_count > 0")
all_followers = [row[0] for row in cursor.fetchall()]

ax.hist(all_followers, bins=50, color="coral", edgecolor="black", alpha=0.7)
ax.set_xlabel("Followers (log scale)", fontsize=11)
ax.set_ylabel("Number of Authors", fontsize=11)
ax.set_title("Distribution of Author Followers", fontsize=12)
ax.set_xscale("log")
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "author_followers.png", dpi=300, bbox_inches="tight")
print(f"  Saved: author_followers.png")
plt.close()

# ============================================================================
# 5. SUMMARY STATISTICS
# ============================================================================
print("\n5. SUMMARY STATISTICS")
print("-" * 80)

print(f"\nFollower Statistics (all authors with data):")
print(f"  Mean: {np.mean(all_followers):,.0f}")
print(f"  Median: {np.median(all_followers):,.0f}")
print(f"  Std Dev: {np.std(all_followers):,.0f}")
print(f"  Min: {np.min(all_followers):,.0f}")
print(f"  Max: {np.max(all_followers):,.0f}")

cursor.execute("""
    SELECT cp1.paper_fidelity, COUNT(*) as count
    FROM coding_pass1 cp1
    WHERE cp1.paper_fidelity IS NOT NULL AND cp1.paper_fidelity != 'not_applicable'
    GROUP BY cp1.paper_fidelity
    ORDER BY count DESC
""")
print(f"\nPaper Fidelity Distribution (excluding N/A):")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

cursor.execute("""
    SELECT cp1.field_accuracy, COUNT(*) as count
    FROM coding_pass1 cp1
    WHERE cp1.field_accuracy IS NOT NULL AND cp1.field_accuracy != 'not_applicable'
    GROUP BY cp1.field_accuracy
    ORDER BY count DESC
""")
print(f"\nField Accuracy Distribution (excluding N/A):")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

conn.close()
