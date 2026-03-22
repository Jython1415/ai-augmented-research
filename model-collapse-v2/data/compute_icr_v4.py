# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""Compute Krippendorff's alpha for V4 distortion tag coding results.
Compares 3 independent coders across 8 binary distortion tags."""

import json
import numpy as np
import sys
from pathlib import Path
from collections import Counter

RESULTS_DIR = Path("/private/tmp/claude/coding/calibration")
DEFAULT_CODER_FILES = [
    RESULTS_DIR / "v4_results_coder_1.json",
    RESULTS_DIR / "v4_results_coder_2.json",
    RESULTS_DIR / "v4_results_coder_3.json",
]

DISTORTION_TAGS = [
    "certainty_inflation",
    "scope_inflation",
    "temporal_overclaim",
    "causal_conflation",
    "mechanism_omission",
    "mitigation_blindness",
    "definitional_conflation",
    "sensationalism",
]

CLAIM_STRENGTH_VALUES = ["neutral_share", "substantive_mention", "authoritative_claim"]


def krippendorff_alpha_nominal(reliability_data):
    """
    Compute Krippendorff's alpha for nominal data.

    reliability_data: list of lists, shape [n_coders][n_units]
        Values are category labels (strings). None = missing.
    """
    n_coders = len(reliability_data)
    n_units = len(reliability_data[0])

    # Build value-count matrix per unit
    all_values = set()
    for coder in reliability_data:
        for v in coder:
            if v is not None:
                all_values.add(v)

    values = sorted(all_values)
    value_to_idx = {v: i for i, v in enumerate(values)}
    n_values = len(values)

    # n_ck: for each unit, count of each value
    n_ck = np.zeros((n_units, n_values))
    for coder in reliability_data:
        for u, v in enumerate(coder):
            if v is not None:
                n_ck[u, value_to_idx[v]] += 1

    # m_u: number of coders who coded each unit
    m_u = n_ck.sum(axis=1)

    # Filter to units with at least 2 coders
    valid = m_u >= 2
    if valid.sum() == 0:
        return float('nan'), {}

    n_ck = n_ck[valid]
    m_u = m_u[valid]
    n_valid = valid.sum()

    # Total number of paired judgments
    n_total = m_u.sum()

    # Observed disagreement (D_o)
    D_o = 0
    for u in range(n_valid):
        if m_u[u] <= 1:
            continue
        disagreements = 0
        for c in range(n_values):
            disagreements += n_ck[u, c] * (m_u[u] - n_ck[u, c])
        D_o += disagreements / (m_u[u] - 1)
    D_o /= n_total

    # Expected disagreement (D_e)
    n_c = n_ck.sum(axis=0)
    D_e = 0
    for c in range(n_values):
        for k in range(n_values):
            if c != k:
                D_e += n_c[c] * n_c[k]
    D_e /= (n_total * (n_total - 1))

    if D_e == 0:
        return 1.0, {}

    alpha = 1 - D_o / D_e

    dist = {values[i]: int(n_c[i]) for i in range(n_values)}

    return alpha, dist


def krippendorff_alpha_binary(reliability_data):
    """
    Compute Krippendorff's alpha for binary data (True/False).
    reliability_data: list of lists, shape [n_coders][n_units]
        Values are boolean (True/False). None = missing.
    """
    n_coders = len(reliability_data)
    n_units = len(reliability_data[0])

    # Build 2x2 matrix: for each unit, count True/False
    all_values = {True, False}
    value_to_idx = {True: 1, False: 0}
    n_values = 2

    # n_ck: for each unit, count of each value
    n_ck = np.zeros((n_units, n_values))
    for coder in reliability_data:
        for u, v in enumerate(coder):
            if v is not None:
                n_ck[u, value_to_idx[v]] += 1

    # m_u: number of coders who coded each unit
    m_u = n_ck.sum(axis=1)

    # Filter to units with at least 2 coders
    valid = m_u >= 2
    if valid.sum() == 0:
        return float('nan'), {}

    n_ck = n_ck[valid]
    m_u = m_u[valid]
    n_valid = valid.sum()

    # Total number of paired judgments
    n_total = m_u.sum()

    # Observed disagreement (D_o)
    D_o = 0
    for u in range(n_valid):
        if m_u[u] <= 1:
            continue
        disagreements = 0
        for c in range(n_values):
            disagreements += n_ck[u, c] * (m_u[u] - n_ck[u, c])
        D_o += disagreements / (m_u[u] - 1)
    D_o /= n_total

    # Expected disagreement (D_e)
    n_c = n_ck.sum(axis=0)
    D_e = 0
    for c in range(n_values):
        for k in range(n_values):
            if c != k:
                D_e += n_c[c] * n_c[k]
    D_e /= (n_total * (n_total - 1))

    if D_e == 0:
        return 1.0, {}

    alpha = 1 - D_o / D_e

    dist = {True: int(n_c[1]), False: int(n_c[0])}

    return alpha, dist


def load_results(coder_files=None):
    """Load and validate all 3 coder results."""
    if coder_files is None:
        coder_files = DEFAULT_CODER_FILES

    coders = []
    for f in coder_files:
        if not f.exists():
            print(f"WARNING: {f.name} not found")
            continue
        with open(f) as fh:
            data = json.load(fh)
        # Index by post_id
        by_post = {r["post_id"]: r for r in data}
        coders.append(by_post)
        print(f"Loaded {f.name}: {len(data)} results")

    return coders


def compute_pairwise_agreement(coders, all_post_ids, field):
    """Compute pairwise agreement for a field (binary or categorical)."""
    results = []
    for i in range(len(coders)):
        for j in range(i+1, len(coders)):
            agree = sum(
                1 for pid in all_post_ids
                if pid in coders[i] and pid in coders[j]
                and coders[i][pid].get(field) == coders[j][pid].get(field)
            )
            total = sum(
                1 for pid in all_post_ids
                if pid in coders[i] and pid in coders[j]
            )
            if total > 0:
                pct = agree / total * 100
                results.append((i+1, j+1, agree, total, pct))
    return results


def count_true_values(coders, all_post_ids, field):
    """Count how many posts each coder marked as True for a field."""
    counts = []
    for i, coder in enumerate(coders):
        count = sum(
            1 for pid in all_post_ids
            if pid in coder and coder[pid].get(field) is True
        )
        counts.append(count)
    return counts


def find_disagreements(coders, all_post_ids, field):
    """Find posts where coders disagree on a field."""
    disagreements = []
    for pid in all_post_ids:
        values = []
        for coder in coders:
            if pid in coder:
                v = coder[pid].get(field)
                values.append(v)

        if len(set(values)) > 1:
            disagreements.append({
                "post_id": pid,
                "values": values,
            })

    return disagreements


def main():
    # Parse command-line arguments for coder file paths
    coder_files = None
    if len(sys.argv) > 1:
        coder_files = [Path(f) for f in sys.argv[1:4]]

    coders = load_results(coder_files)
    if len(coders) < 2:
        print("Need at least 2 coders to compute alpha")
        return

    # Get all post_ids coded by at least 1 coder
    all_post_ids = sorted(set().union(*(c.keys() for c in coders)))
    print(f"\nTotal unique post_ids: {len(all_post_ids)}\n")

    # Check completeness
    for i, coder in enumerate(coders):
        missing = [pid for pid in all_post_ids if pid not in coder]
        if missing:
            print(f"Coder {i+1} missing {len(missing)} posts")

    # =========================================================================
    # CLAIM STRENGTH (nominal, same as V3)
    # =========================================================================
    print("\n" + "=" * 80)
    print("CLAIM STRENGTH (Nominal)")
    print("=" * 80)

    reliability_data = []
    for coder in coders:
        coder_values = []
        for pid in all_post_ids:
            if pid in coder:
                val = coder[pid].get("claim_strength")
                if val and val in CLAIM_STRENGTH_VALUES:
                    coder_values.append(val)
                else:
                    coder_values.append(None)
            else:
                coder_values.append(None)
        reliability_data.append(coder_values)

    alpha, dist = krippendorff_alpha_nominal(reliability_data)

    if alpha >= 0.800:
        interp = "STRONG"
    elif alpha >= 0.667:
        interp = "TENTATIVE (acceptable with caveats)"
    else:
        interp = "UNACCEPTABLE — revise codebook"

    print(f"\nα = {alpha:.3f} — {interp}")
    print(f"Distribution: {dist}")

    # Pairwise agreement
    for i, j, agree, total, pct in compute_pairwise_agreement(coders, all_post_ids, "claim_strength"):
        print(f"  Coder {i} vs {j}: {agree}/{total} = {pct:.1f}%")

    # =========================================================================
    # DISTORTION TAGS (binary)
    # =========================================================================
    print("\n" + "=" * 80)
    print("DISTORTION TAGS (Binary)")
    print("=" * 80)

    summary_rows = []

    for tag in DISTORTION_TAGS:
        # Build reliability matrix for this tag
        reliability_data = []
        for coder in coders:
            coder_values = []
            for pid in all_post_ids:
                if pid in coder:
                    val = coder[pid].get(tag)
                    coder_values.append(val)
                else:
                    coder_values.append(None)
            reliability_data.append(coder_values)

        alpha, dist = krippendorff_alpha_binary(reliability_data)

        # Pairwise agreement
        agree_results = compute_pairwise_agreement(coders, all_post_ids, tag)
        avg_agree_pct = np.mean([r[4] for r in agree_results]) if agree_results else 0

        # Count TRUE values per coder
        true_counts = count_true_values(coders, all_post_ids, tag)

        # Count disagreements
        disagreements = find_disagreements(coders, all_post_ids, tag)

        summary_rows.append({
            "tag": tag,
            "alpha": alpha,
            "agree_pct": avg_agree_pct,
            "true_counts": true_counts,
            "n_disagree": len(disagreements),
            "disagreements": disagreements,
        })

    # Print summary table
    print("\n" + "-" * 100)
    print(f"{'Tag':<30} | {'α':<6} | {'Agree%':<7} | {'C1-T':<5} | {'C2-T':<5} | {'C3-T':<5} | {'Disagree':<8}")
    print("-" * 100)
    for row in summary_rows:
        alpha_str = f"{row['alpha']:.3f}" if not np.isnan(row['alpha']) else "NaN  "
        print(f"{row['tag']:<30} | {alpha_str:<6} | {row['agree_pct']:>6.1f}% | "
              f"{row['true_counts'][0]:>4} | {row['true_counts'][1]:>4} | {row['true_counts'][2]:>4} | {row['n_disagree']:>8}")

    # =========================================================================
    # DISAGREEMENT DETAILS (show first 5 per tag)
    # =========================================================================
    print("\n" + "=" * 80)
    print("DISAGREEMENT DETAILS (first 5 per tag)")
    print("=" * 80)

    for row in summary_rows:
        if row['disagreements']:
            print(f"\n{row['tag']}: {row['n_disagree']} disagreements")
            for d in row['disagreements'][:5]:
                print(f"  Post {d['post_id']}: C1={d['values'][0]}, C2={d['values'][1]}, C3={d['values'][2]}")

    # =========================================================================
    # OVERALL "ANY DISTORTION" AGREEMENT
    # =========================================================================
    print("\n" + "=" * 80)
    print("OVERALL 'ANY DISTORTION' AGREEMENT")
    print("=" * 80)

    reliability_data = []
    for coder in coders:
        coder_values = []
        for pid in all_post_ids:
            if pid in coder:
                has_any = any(coder[pid].get(tag) for tag in DISTORTION_TAGS)
                coder_values.append(has_any)
            else:
                coder_values.append(None)
        reliability_data.append(coder_values)

    alpha, dist = krippendorff_alpha_binary(reliability_data)

    if alpha >= 0.800:
        interp = "STRONG"
    elif alpha >= 0.667:
        interp = "TENTATIVE (acceptable with caveats)"
    else:
        interp = "UNACCEPTABLE — revise codebook"

    print(f"\nα = {alpha:.3f} — {interp}")
    print(f"Distribution (any distortion): {dist}")

    # Pairwise agreement
    for i in range(len(coders)):
        for j in range(i+1, len(coders)):
            agree = sum(
                1 for pid in all_post_ids
                if pid in coders[i] and pid in coders[j]
                and (any(coders[i][pid].get(tag) for tag in DISTORTION_TAGS)
                     == any(coders[j][pid].get(tag) for tag in DISTORTION_TAGS))
            )
            total = sum(
                1 for pid in all_post_ids
                if pid in coders[i] and pid in coders[j]
            )
            if total > 0:
                print(f"  Coder {i+1} vs {j+1}: {agree}/{total} = {agree/total:.1%}")

    # =========================================================================
    # TAG COUNT DISTRIBUTION
    # =========================================================================
    print("\n" + "=" * 80)
    print("TAG COUNT DISTRIBUTION (how many posts have 0, 1, 2, 3+ tags)")
    print("=" * 80)

    for i, coder in enumerate(coders):
        tag_counts = Counter()
        for pid in all_post_ids:
            if pid in coder:
                n_tags = sum(1 for tag in DISTORTION_TAGS if coder[pid].get(tag) is True)
                tag_counts[n_tags] += 1

        print(f"\nCoder {i+1}:")
        for n in sorted(tag_counts.keys()):
            print(f"  {n} tags: {tag_counts[n]} posts")


if __name__ == "__main__":
    main()
