#!/usr/bin/env python3
"""
Comprehensive analysis of V3 coding data using separate coding_pass1 and coding_pass2 tables.
"""

import sqlite3
import numpy as np
from scipy.stats import spearmanr
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "posts.db"
FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Connect to database
conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 80)
print("V3 COMPREHENSIVE ANALYSIS")
print("=" * 80)

# ============================================================================
# 1. SUMMARY STATISTICS
# ============================================================================
print("\n1. SUMMARY STATISTICS")
print("-" * 80)

# Pass 1 data
cursor.execute("""
    SELECT cp1.*, cu.epoch, cu.citation_type
    FROM coding_pass1 cp1
    JOIN citation_units cu ON cp1.citation_unit_id = cu.id
""")
pass1_rows = cursor.fetchall()
pass1_data = [dict(row) for row in pass1_rows]
print(f"\nPass 1: {len(pass1_data)} citation units")

if pass1_data:
    claim_strengths = [row['claim_strength'] for row in pass1_data]
    paper_fidelities = [row['paper_fidelity'] for row in pass1_data]
    field_accuracies = [row['field_accuracy'] for row in pass1_data]
    epochs = [row['epoch'] for row in pass1_data]
    citation_types = [row['citation_type'] for row in pass1_data]

    print(f"\nPass 1 Claim Strength Distribution:")
    for val, count in Counter(claim_strengths).most_common():
        print(f"  {val}: {count} ({100*count/len(claim_strengths):.1f}%)")

    print(f"\nPass 1 Paper Fidelity Distribution:")
    for val, count in Counter(paper_fidelities).most_common():
        print(f"  {val}: {count} ({100*count/len(paper_fidelities):.1f}%)")

    print(f"\nPass 1 Field Accuracy Distribution:")
    for val, count in Counter(field_accuracies).most_common():
        print(f"  {val}: {count} ({100*count/len(field_accuracies):.1f}%)")

    print(f"\nPass 1 Epoch Distribution:")
    epoch_counts = Counter(epochs)
    for epoch in sorted([e for e in epoch_counts.keys() if e is not None], key=lambda x: (x is None, x)):
        count = epoch_counts[epoch]
        print(f"  {epoch}: {count} ({100*count/len(epochs):.1f}%)")
    if None in epoch_counts:
        print(f"  None: {epoch_counts[None]} ({100*epoch_counts[None]/len(epochs):.1f}%)")

    print(f"\nPass 1 Citation Type Distribution:")
    for ctype, count in Counter(citation_types).most_common():
        print(f"  {ctype}: {count} ({100*count/len(citation_types):.1f}%)")

# Pass 2 data
cursor.execute("""
    SELECT cp2.*
    FROM coding_pass2 cp2
""")
pass2_rows = cursor.fetchall()
pass2_data = [dict(row) for row in pass2_rows]
print(f"\n\nPass 2: {len(pass2_data)} records")

if pass2_data:
    claim_strengths_p2 = [row['claim_strength'] for row in pass2_data]
    paper_fidelities_p2 = [row['paper_fidelity'] for row in pass2_data]
    field_accuracies_p2 = [row['field_accuracy'] for row in pass2_data]

    print(f"\nPass 2 Claim Strength Distribution:")
    for val, count in Counter(claim_strengths_p2).most_common():
        print(f"  {val}: {count} ({100*count/len(claim_strengths_p2):.1f}%)")

    print(f"\nPass 2 Paper Fidelity Distribution:")
    for val, count in Counter(paper_fidelities_p2).most_common():
        print(f"  {val}: {count} ({100*count/len(paper_fidelities_p2):.1f}%)")

    print(f"\nPass 2 Field Accuracy Distribution:")
    for val, count in Counter(field_accuracies_p2).most_common():
        print(f"  {val}: {count} ({100*count/len(field_accuracies_p2):.1f}%)")

# ============================================================================
# 2. EPOCH TRENDS (Pass 1 only)
# ============================================================================
print("\n\n2. EPOCH TRENDS (Pass 1)")
print("-" * 80)

if pass1_data:
    epochs_set = sorted([e for e in set(epochs) if e is not None])
    dimensions = {
        'claim_strength': claim_strengths,
        'paper_fidelity': paper_fidelities,
        'field_accuracy': field_accuracies
    }

    for dim_name, dim_values in dimensions.items():
        print(f"\n{dim_name.upper()} by Epoch:")
        for epoch in epochs_set:
            epoch_values = [dim_values[i] for i, e in enumerate(epochs) if e == epoch]
            if epoch_values:
                value_counts = Counter(epoch_values)
                print(f"  Epoch {epoch}:")
                for val, count in sorted(value_counts.items()):
                    pct = 100 * count / len(epoch_values)
                    print(f"    {val}: {count} ({pct:.1f}%)")

# ============================================================================
# 3. TWO-PASS COMPARISON
# ============================================================================
print("\n\n3. TWO-PASS COMPARISON")
print("-" * 80)

if pass1_data and pass2_data:
    # Create mapping from Pass 1 to Pass 2
    pass1_by_id = {row['citation_unit_id']: row for row in pass1_data}
    pass2_by_id = {row['citation_unit_id']: row for row in pass2_data}

    # Find common citation unit IDs
    common_ids = set(pass1_by_id.keys()) & set(pass2_by_id.keys())
    print(f"\nCommon citation units (in both passes): {len(common_ids)}")

    if common_ids:
        # Calculate agreement for each dimension
        for dim in ['claim_strength', 'paper_fidelity', 'field_accuracy']:
            p1_vals = [pass1_by_id[cid][dim] for cid in common_ids]
            p2_vals = [pass2_by_id[cid][dim] for cid in common_ids]

            agreement = sum(1 for p1, p2 in zip(p1_vals, p2_vals) if p1 == p2)
            agreement_pct = 100 * agreement / len(common_ids)

            print(f"\n{dim.upper()} Agreement:")
            print(f"  Exact agreement: {agreement}/{len(common_ids)} ({agreement_pct:.1f}%)")

            # Confusion matrix
            unique_vals = sorted(set(p1_vals + p2_vals))
            print(f"  Confusion matrix (Pass 1 rows, Pass 2 cols):")
            print("    ", end="")
            for val in unique_vals:
                print(f"{str(val):>12}", end="")
            print()

            for val1 in unique_vals:
                print(f"  {val1:<10}", end="")
                for val2 in unique_vals:
                    count = sum(1 for p1, p2 in zip(p1_vals, p2_vals) if p1 == val1 and p2 == val2)
                    print(f"{count:>12}", end="")
                print()

            # Direction of change
            increases = sum(1 for p1, p2 in zip(p1_vals, p2_vals)
                           if str(p2) > str(p1))
            decreases = sum(1 for p1, p2 in zip(p1_vals, p2_vals)
                           if str(p2) < str(p1))
            stays_same = len(common_ids) - increases - decreases

            print(f"  Direction of change:")
            print(f"    Increased: {increases} ({100*increases/len(common_ids):.1f}%)")
            print(f"    Decreased: {decreases} ({100*decreases/len(common_ids):.1f}%)")
            print(f"    No change: {stays_same} ({100*stays_same/len(common_ids):.1f}%)")

            # Cohen's Kappa (simplified)
            if len(unique_vals) >= 2:
                po = agreement / len(common_ids)  # proportion observed
                # Rough expected agreement
                p1_dist = Counter(p1_vals)
                p2_dist = Counter(p2_vals)
                pe = sum((p1_dist[v] / len(p1_vals)) * (p2_dist[v] / len(p2_vals))
                        for v in unique_vals if v in p1_dist and v in p2_dist)
                kappa = (po - pe) / (1 - pe) if pe < 1 else 0
                print(f"  Cohen's Kappa (simplified): {kappa:.3f}")

# ============================================================================
# 4. AUTHOR DEMOGRAPHICS
# ============================================================================
print("\n\n4. AUTHOR DEMOGRAPHICS")
print("-" * 80)

cursor.execute("SELECT did, handle, display_name, bio, followers_count FROM author_profiles")
authors = cursor.fetchall()
print(f"\nTotal authors: {len(authors)}")

# Bio keyword categorization
keywords = {
    'researcher': ['researcher', 'phd', 'professor', 'postdoc', 'research', 'academic'],
    'journalist': ['journalist', 'writer', 'editor', 'media', 'news'],
    'developer': ['engineer', 'developer', 'programmer', 'software', 'code'],
    'ai_ml': ['ai', 'ml', 'machine learning', 'deep learning', 'nlp', 'llm', 'ai engineer'],
    'student': ['student', 'undergrad', 'grad student', 'phd student'],
}

categories = defaultdict(int)
uncategorized = 0

for author in authors:
    bio_text = (author['bio'] or '').lower()
    name = (author['display_name'] or '').lower()
    bio = bio_text + ' ' + name

    categorized = False
    for cat, kws in keywords.items():
        if any(kw in bio for kw in kws):
            categories[cat] += 1
            categorized = True
            break

    if not categorized:
        uncategorized += 1

print(f"\nAuthor Categories:")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    pct = 100 * count / len(authors)
    print(f"  {cat}: {count} ({pct:.1f}%)")
print(f"  other: {uncategorized} ({100*uncategorized/len(authors):.1f}%)")

# ============================================================================
# 5. REPEAT CITERS
# ============================================================================
print("\n\n5. REPEAT CITERS")
print("-" * 80)

cursor.execute("""
    SELECT author_did, COUNT(*) as count
    FROM citation_units
    GROUP BY author_did
    HAVING count > 1
    ORDER BY count DESC
""")
repeat_citers = cursor.fetchall()
print(f"\nAuthors with >1 citation unit: {len(repeat_citers)}")

if repeat_citers:
    print(f"\nTop 20 repeat citers:")
    for i, row in enumerate(repeat_citers[:20], 1):
        print(f"  {i}. {row['author_did']}: {row['count']} citation units")

    total_repeats = sum(row['count'] for row in repeat_citers)
    pct_of_total = 100 * total_repeats / len(pass1_data)
    print(f"\nRepeat citations account for {total_repeats}/{len(pass1_data)} ({pct_of_total:.1f}%) of all Pass 1 data")

# ============================================================================
# 6. REACH ANALYSIS
# ============================================================================
print("\n\n6. REACH ANALYSIS (Followers vs Accuracy)")
print("-" * 80)

cursor.execute("""
    SELECT DISTINCT cu.author_did, ap.followers_count, cp1.paper_fidelity, cp1.field_accuracy
    FROM citation_units cu
    LEFT JOIN author_profiles ap ON cu.author_did = ap.did
    LEFT JOIN coding_pass1 cp1 ON cu.id = cp1.citation_unit_id
    WHERE ap.followers_count IS NOT NULL
""")
reach_data = cursor.fetchall()

if reach_data:
    followers = []
    paper_fidelities_reach = []
    field_accuracies_reach = []

    for row in reach_data:
        if row['followers_count'] is not None and row['followers_count'] > 0:
            followers.append(row['followers_count'])
            # Convert to numeric for correlation (treating as ordinal)
            fid_map = {'accurate': 3, 'partially_accurate': 2, 'misrepresentation': 1, None: 0}
            paper_fidelities_reach.append(fid_map.get(row['paper_fidelity'], 0))
            field_accuracies_reach.append(fid_map.get(row['field_accuracy'], 0))

    print(f"\nRecords with follower data: {len(followers)}")
    if followers:
        print(f"Mean followers: {np.mean(followers):.0f}")
        print(f"Median followers: {np.median(followers):.0f}")
        print(f"Min followers: {np.min(followers):.0f}")
        print(f"Max followers: {np.max(followers):.0f}")

        if len(followers) > 2:
            corr_pf, p_pf = spearmanr(followers, paper_fidelities_reach)
            corr_fa, p_fa = spearmanr(followers, field_accuracies_reach)
            print(f"\nSpearman correlations (followers vs accuracy):")
            print(f"  Paper Fidelity: r={corr_pf:.3f}, p={p_pf:.3f}")
            print(f"  Field Accuracy: r={corr_fa:.3f}, p={p_fa:.3f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

conn.close()
