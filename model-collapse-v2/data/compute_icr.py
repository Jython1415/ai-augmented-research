# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""Compute Krippendorff's alpha for calibration coding results.
Compares 3 independent coders across 3 dimensions."""

import json
import numpy as np
from pathlib import Path
from collections import Counter

RESULTS_DIR = Path("/private/tmp/claude/coding/calibration")
CODER_FILES = [
    RESULTS_DIR / "v3r3_results_coder_1.json",
    RESULTS_DIR / "v3r3_results_coder_2.json",
    RESULTS_DIR / "v3r3_results_coder_3.json",
]

DIMENSIONS = {
    "claim_strength": ["neutral_share", "substantive_mention", "authoritative_claim"],
    "paper_fidelity": ["accurate", "partially_accurate", "misrepresentation", "not_applicable"],
    "field_accuracy": ["accurate", "partially_accurate", "inaccurate", "not_applicable"],
}


def krippendorff_alpha_nominal(reliability_data):
    """
    Compute Krippendorff's alpha for nominal data.

    reliability_data: list of lists, shape [n_coders][n_units]
        Values are category labels (strings). None = missing.
    """
    n_coders = len(reliability_data)
    n_units = len(reliability_data[0])

    # Build value-count matrix per unit
    # For each unit, count how many coders assigned each value
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
    # For each unit: sum over value pairs c!=k of n_uc * n_uk / (m_u * (m_u - 1))
    # For nominal: delta(c,k) = 0 if c==k, 1 if c!=k
    # D_o = (1/N) * sum_u [1/(m_u-1)] * sum_c n_uc * (m_u - n_uc)
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
    # Based on marginal frequencies
    n_c = n_ck.sum(axis=0)  # total count per value across all units
    D_e = 0
    for c in range(n_values):
        for k in range(n_values):
            if c != k:
                D_e += n_c[c] * n_c[k]
    D_e /= (n_total * (n_total - 1))

    if D_e == 0:
        return 1.0, {}  # Perfect agreement

    alpha = 1 - D_o / D_e

    # Distribution info
    dist = {values[i]: int(n_c[i]) for i in range(n_values)}

    return alpha, dist


def load_results():
    """Load and validate all 3 coder results."""
    coders = []
    for f in CODER_FILES:
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


def main():
    coders = load_results()
    if len(coders) < 2:
        print("Need at least 2 coders to compute alpha")
        return

    # Get all post_ids coded by at least 1 coder
    all_post_ids = sorted(set().union(*(c.keys() for c in coders)))
    print(f"\nTotal unique post_ids: {len(all_post_ids)}")

    # Check completeness
    for i, coder in enumerate(coders):
        missing = [pid for pid in all_post_ids if pid not in coder]
        if missing:
            print(f"Coder {i+1} missing {len(missing)} posts: {missing[:5]}...")

    # Compute alpha per dimension
    print("\n" + "=" * 60)
    print("KRIPPENDORFF'S ALPHA RESULTS")
    print("=" * 60)

    for dim, valid_values in DIMENSIONS.items():
        # Build reliability matrix
        reliability_data = []
        for coder in coders:
            coder_values = []
            for pid in all_post_ids:
                if pid in coder:
                    val = coder[pid].get(dim)
                    if val and val in valid_values:
                        coder_values.append(val)
                    else:
                        coder_values.append(None)
                else:
                    coder_values.append(None)
            reliability_data.append(coder_values)

        alpha, dist = krippendorff_alpha_nominal(reliability_data)

        # Interpretation
        if alpha >= 0.800:
            interp = "STRONG"
        elif alpha >= 0.667:
            interp = "TENTATIVE (acceptable with caveats)"
        else:
            interp = "UNACCEPTABLE — revise codebook"

        print(f"\n{dim}:")
        print(f"  α = {alpha:.3f} — {interp}")
        print(f"  Distribution: {dist}")

        # Agreement matrix (pairwise)
        for i in range(len(coders)):
            for j in range(i+1, len(coders)):
                agree = sum(
                    1 for pid in all_post_ids
                    if pid in coders[i] and pid in coders[j]
                    and coders[i][pid].get(dim) == coders[j][pid].get(dim)
                )
                total = sum(
                    1 for pid in all_post_ids
                    if pid in coders[i] and pid in coders[j]
                )
                if total > 0:
                    print(f"  Coder {i+1} vs {j+1}: {agree}/{total} = {agree/total:.1%}")

    # Disagreement analysis
    print("\n" + "=" * 60)
    print("DISAGREEMENT DETAILS")
    print("=" * 60)

    for dim in DIMENSIONS:
        disagreements = []
        for pid in all_post_ids:
            values = []
            reasonings = []
            for i, coder in enumerate(coders):
                if pid in coder:
                    v = coder[pid].get(dim, "MISSING")
                    r = coder[pid].get(f"{dim}_reasoning", "")
                    values.append(v)
                    reasonings.append(r)

            if len(set(values)) > 1:
                disagreements.append({
                    "post_id": pid,
                    "values": values,
                    "reasonings": reasonings,
                })

        if disagreements:
            print(f"\n{dim}: {len(disagreements)} disagreements")
            for d in disagreements[:10]:
                print(f"  Post {d['post_id']}: {d['values']}")
                for i, r in enumerate(d['reasonings']):
                    if r:
                        print(f"    Coder {i+1}: {r[:100]}")


if __name__ == "__main__":
    main()
