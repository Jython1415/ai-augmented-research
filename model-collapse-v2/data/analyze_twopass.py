#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "numpy",
#     "scipy",
# ]
# ///

import sqlite3
import numpy as np
from scipy.stats import chi2_contingency
from collections import defaultdict
import sys

DB_PATH = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"
OUTPUT_PATH = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/figures/twopass_stats.txt"

def cohens_kappa(confusion_matrix):
    """Compute Cohen's kappa from confusion matrix."""
    n = confusion_matrix.sum()
    po = np.trace(confusion_matrix) / n  # observed agreement

    # Expected agreement by chance
    pe = 0
    for i in range(confusion_matrix.shape[0]):
        pe += (confusion_matrix[i, :].sum() / n) * (confusion_matrix[:, i].sum() / n)

    if pe == 1:
        return 1.0 if po == 1 else 0.0
    return (po - pe) / (1 - pe)

def mcnemar_test(confusion_matrix):
    """
    Perform McNemar test on off-diagonal elements.
    Returns (chi2_stat, p_value).
    """
    # Off-diagonal sum: b + c where b is upper-right, c is lower-left
    b = np.triu(confusion_matrix, k=1).sum()
    c = np.tril(confusion_matrix, k=-1).sum()

    if b + c == 0:
        return (0.0, 1.0)

    # McNemar test statistic
    chi2_stat = ((b - c) ** 2) / (b + c)

    # Get p-value from chi2 distribution with 1 df
    from scipy.stats import chi2
    p_value = 1 - chi2.cdf(chi2_stat, df=1)

    return (chi2_stat, p_value)

def get_data():
    """Query Pass 1 and Pass 2 data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get Pass 1 from coding_pass1 table
    cursor.execute("""
        SELECT citation_unit_id, claim_strength, paper_fidelity, field_accuracy
        FROM coding_pass1
        ORDER BY citation_unit_id
    """)
    pass1_rows = cursor.fetchall()
    pass1_data = {row[0]: {'claim_strength': row[1], 'paper_fidelity': row[2], 'field_accuracy': row[3]}
                  for row in pass1_rows}

    # Get Pass 2 from coding_pass2
    cursor.execute("""
        SELECT citation_unit_id, claim_strength, paper_fidelity, field_accuracy
        FROM coding_pass2
        ORDER BY citation_unit_id
    """)
    pass2_rows = cursor.fetchall()
    pass2_data = {row[0]: {'claim_strength': row[1], 'paper_fidelity': row[2], 'field_accuracy': row[3]}
                  for row in pass2_rows}

    conn.close()

    # Join on ID
    common_ids = set(pass1_data.keys()) & set(pass2_data.keys())
    print(f"Pass 1 records: {len(pass1_data)}")
    print(f"Pass 2 records: {len(pass2_data)}")
    print(f"Common IDs: {len(common_ids)}\n")

    return pass1_data, pass2_data, common_ids

def analyze_dimension(dimension_name, pass1_data, pass2_data, common_ids):
    """Analyze a single dimension."""
    print("=" * 70)
    print(f"DIMENSION: {dimension_name.upper()}")
    print("=" * 70)

    # Collect values
    pass1_values = []
    pass2_values = []
    changes = defaultdict(int)

    for cid in sorted(common_ids):
        p1_val = pass1_data[cid][dimension_name]
        p2_val = pass2_data[cid][dimension_name]
        pass1_values.append(p1_val)
        pass2_values.append(p2_val)

        if p1_val != p2_val:
            changes[f"{p1_val}→{p2_val}"] += 1

    # Get unique categories
    all_categories = sorted(set(pass1_values + pass2_values))
    print(f"Categories: {all_categories}\n")

    # Build confusion matrix (Pass 1 rows × Pass 2 columns)
    cat_to_idx = {cat: i for i, cat in enumerate(all_categories)}
    confusion_matrix = np.zeros((len(all_categories), len(all_categories)), dtype=int)

    for p1_val, p2_val in zip(pass1_values, pass2_values):
        i = cat_to_idx[p1_val]
        j = cat_to_idx[p2_val]
        confusion_matrix[i, j] += 1

    # Print confusion matrix
    print("Confusion Matrix (Pass 1 rows × Pass 2 columns):")
    print("Pass1\\Pass2", end="")
    for cat in all_categories:
        print(f"\t{cat}", end="")
    print()

    for i, row_cat in enumerate(all_categories):
        print(row_cat, end="")
        for j in range(len(all_categories)):
            print(f"\t{confusion_matrix[i, j]}", end="")
        print()
    print()

    # Compute statistics
    n_total = len(common_ids)
    n_agreement = np.trace(confusion_matrix)
    pct_agreement = 100 * n_agreement / n_total
    pct_changed = 100 * (n_total - n_agreement) / n_total

    kappa = cohens_kappa(confusion_matrix)
    chi2_stat, p_value = mcnemar_test(confusion_matrix)

    print(f"Total records: {n_total}")
    print(f"Agreement: {n_agreement} ({pct_agreement:.1f}%)")
    print(f"Changed: {n_total - n_agreement} ({pct_changed:.1f}%)")
    print(f"Cohen's kappa: {kappa:.4f}")
    print(f"McNemar chi2: {chi2_stat:.4f}, p-value: {p_value:.6f}")
    print()

    # Direction of changes
    if changes:
        print("Changes (top patterns):")
        sorted_changes = sorted(changes.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_changes[:15]:
            pct = 100 * count / (n_total - n_agreement)
            print(f"  {pattern}: {count} cases ({pct:.1f}% of changes)")
    print()

    return {
        'confusion_matrix': confusion_matrix,
        'categories': all_categories,
        'n_total': n_total,
        'n_agreement': n_agreement,
        'pct_agreement': pct_agreement,
        'pct_changed': pct_changed,
        'kappa': kappa,
        'chi2': chi2_stat,
        'p_value': p_value,
        'changes': dict(sorted_changes) if changes else {}
    }

def main():
    pass1_data, pass2_data, common_ids = get_data()

    results = {}
    for dim in ['claim_strength', 'paper_fidelity', 'field_accuracy']:
        results[dim] = analyze_dimension(dim, pass1_data, pass2_data, common_ids)

    # Save summary
    with open(OUTPUT_PATH, 'w') as f:
        for dim in ['claim_strength', 'paper_fidelity', 'field_accuracy']:
            res = results[dim]
            f.write("=" * 70 + "\n")
            f.write(f"DIMENSION: {dim.upper()}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Categories: {res['categories']}\n\n")

            f.write("Confusion Matrix (Pass 1 rows × Pass 2 columns):\n")
            f.write("Pass1\\Pass2")
            for cat in res['categories']:
                f.write(f"\t{cat}")
            f.write("\n")

            for i, row_cat in enumerate(res['categories']):
                f.write(f"{row_cat}")
                for j in range(len(res['categories'])):
                    f.write(f"\t{res['confusion_matrix'][i, j]}")
                f.write("\n")
            f.write("\n")

            f.write(f"Total records: {res['n_total']}\n")
            f.write(f"Agreement: {res['n_agreement']} ({res['pct_agreement']:.1f}%)\n")
            f.write(f"Changed: {res['n_total'] - res['n_agreement']} ({res['pct_changed']:.1f}%)\n")
            f.write(f"Cohen's kappa: {res['kappa']:.4f}\n")
            f.write(f"McNemar chi2: {res['chi2']:.4f}, p-value: {res['p_value']:.6f}\n")
            f.write("\n")

            if res['changes']:
                f.write("Changes (top patterns):\n")
                for pattern, count in sorted(res['changes'].items(), key=lambda x: x[1], reverse=True)[:15]:
                    pct = 100 * count / (res['n_total'] - res['n_agreement'])
                    f.write(f"  {pattern}: {count} cases ({pct:.1f}% of changes)\n")
            f.write("\n")

    print("Summary saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
