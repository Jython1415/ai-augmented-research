#!/usr/bin/env python3
"""
/// script
requires-python = ">=3.10"
dependencies = [
    "sqlite3",
]
///
"""

import sqlite3
from collections import Counter, defaultdict
import sys

DB_PATH = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"
OUTPUT_FILE = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/analysis_output_v4.txt"

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


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_coding_data():
    """Fetch all coding_v4 records with citation unit info."""
    conn = connect_db()
    query = """
    SELECT
        cv.id,
        cv.citation_unit_id,
        cv.claim_strength,
        cv.certainty_inflation,
        cv.scope_inflation,
        cv.temporal_overclaim,
        cv.causal_conflation,
        cv.mechanism_omission,
        cv.mitigation_blindness,
        cv.definitional_conflation,
        cv.sensationalism,
        cv.epoch,
        cu.citation_type
    FROM coding_v4 cv
    JOIN citation_units cu ON cv.citation_unit_id = cu.id
    ORDER BY cv.epoch, cv.citation_unit_id
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


def compute_distortion_tags(row):
    """Extract distortion tags from a row as a list."""
    tags = []
    for tag in DISTORTION_TAGS:
        if row[tag] == 1:
            tags.append(tag)
    return tags


def has_any_distortion(tags):
    """Check if there's at least one distortion tag."""
    return len(tags) > 0


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def main():
    rows = get_all_coding_data()

    output_lines = []

    # ========== OVERALL STATISTICS ==========
    print_section("OVERALL STATISTICS")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("  OVERALL STATISTICS")
    output_lines.append("=" * 80)

    # Claim strength distribution
    claim_strengths = Counter(row["claim_strength"] for row in rows)
    total_rows = len(rows)
    print(f"\nTotal coded entries: {total_rows}")
    output_lines.append(f"\nTotal coded entries: {total_rows}")

    print("\nClaim Strength Distribution:")
    output_lines.append("\nClaim Strength Distribution:")
    for strength in ["neutral_share", "substantive_mention", "authoritative_claim"]:
        count = claim_strengths.get(strength, 0)
        pct = (count / total_rows * 100) if total_rows > 0 else 0
        print(f"  {strength:30s}: {count:4d} ({pct:5.1f}%)")
        output_lines.append(f"  {strength:30s}: {count:4d} ({pct:5.1f}%)")

    # Distortion tag frequencies (overall)
    tag_counts = defaultdict(int)
    substantive_rows = [r for r in rows if r["claim_strength"] == "substantive_mention"]
    substantive_count = len(substantive_rows)

    for row in substantive_rows:
        tags = compute_distortion_tags(row)
        for tag in tags:
            tag_counts[tag] += 1

    print(f"\nSubstantive posts: {substantive_count}")
    output_lines.append(f"\nSubstantive posts: {substantive_count}")

    print("\nDistortion Tag Frequencies (among substantive posts):")
    output_lines.append("\nDistortion Tag Frequencies (among substantive posts):")
    for tag in DISTORTION_TAGS:
        count = tag_counts[tag]
        pct = (count / substantive_count * 100) if substantive_count > 0 else 0
        print(f"  {tag:30s}: {count:4d} ({pct:5.1f}%)")
        output_lines.append(f"  {tag:30s}: {count:4d} ({pct:5.1f}%)")

    # Any distortion rate
    substantive_with_distortion = sum(1 for r in substantive_rows if len(compute_distortion_tags(r)) > 0)
    any_distortion_rate = (substantive_with_distortion / substantive_count * 100) if substantive_count > 0 else 0
    print(f"\nAny distortion rate (substantive): {substantive_with_distortion}/{substantive_count} ({any_distortion_rate:.1f}%)")
    output_lines.append(f"\nAny distortion rate (substantive): {substantive_with_distortion}/{substantive_count} ({any_distortion_rate:.1f}%)")

    # ========== TAG CO-OCCURRENCE ==========
    print_section("TAG CO-OCCURRENCE MATRIX")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("  TAG CO-OCCURRENCE MATRIX")
    output_lines.append("=" * 80)

    # Build co-occurrence matrix
    cooccurrence = defaultdict(lambda: defaultdict(int))
    for row in substantive_rows:
        tags = compute_distortion_tags(row)
        for i, tag1 in enumerate(tags):
            for tag2 in tags:
                cooccurrence[tag1][tag2] += 1

    # Print matrix header
    print("\nTags appearing together (count):\n")
    output_lines.append("\nTags appearing together (count):\n")

    # Print as matrix (simplified version - just pairs)
    print("  Tag 1                      | Tag 2                      | Count")
    output_lines.append("  Tag 1                      | Tag 2                      | Count")
    print("  " + "-" * 75)
    output_lines.append("  " + "-" * 75)

    tag_pairs = set()
    for tag1 in sorted(DISTORTION_TAGS):
        for tag2 in sorted(DISTORTION_TAGS):
            if tag1 < tag2 and cooccurrence[tag1][tag2] > 0:
                count = cooccurrence[tag1][tag2]
                print(f"  {tag1:26s} | {tag2:26s} | {count:4d}")
                output_lines.append(f"  {tag1:26s} | {tag2:26s} | {count:4d}")

    # ========== EPOCH BREAKDOWN ==========
    print_section("EPOCH BREAKDOWN")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("  EPOCH BREAKDOWN")
    output_lines.append("=" * 80)

    epochs = sorted(set(row["epoch"] for row in rows if row["epoch"]))
    epoch_data = defaultdict(list)
    for row in rows:
        if row["epoch"]:
            epoch_data[row["epoch"]].append(row)

    for epoch in epochs:
        epoch_rows = epoch_data[epoch]
        epoch_count = len(epoch_rows)

        print(f"\nEpoch {epoch}: {epoch_count} citation units")
        output_lines.append(f"\nEpoch {epoch}: {epoch_count} citation units")

        # Claim strength for this epoch
        epoch_claim_strengths = Counter(r["claim_strength"] for r in epoch_rows)
        print(f"  Claim Strength Distribution:")
        output_lines.append(f"  Claim Strength Distribution:")
        for strength in ["neutral_share", "substantive_mention", "authoritative_claim"]:
            count = epoch_claim_strengths.get(strength, 0)
            pct = (count / epoch_count * 100) if epoch_count > 0 else 0
            print(f"    {strength:28s}: {count:4d} ({pct:5.1f}%)")
            output_lines.append(f"    {strength:28s}: {count:4d} ({pct:5.1f}%)")

        # Tag frequencies for substantive posts in this epoch
        epoch_substantive = [r for r in epoch_rows if r["claim_strength"] == "substantive_mention"]
        epoch_substantive_count = len(epoch_substantive)
        epoch_tag_counts = defaultdict(int)

        for row in epoch_substantive:
            tags = compute_distortion_tags(row)
            for tag in tags:
                epoch_tag_counts[tag] += 1

        print(f"  Distortion Tags (n={epoch_substantive_count} substantive):")
        output_lines.append(f"  Distortion Tags (n={epoch_substantive_count} substantive):")
        for tag in DISTORTION_TAGS:
            count = epoch_tag_counts[tag]
            pct = (count / epoch_substantive_count * 100) if epoch_substantive_count > 0 else 0
            print(f"    {tag:28s}: {count:4d} ({pct:5.1f}%)")
            output_lines.append(f"    {tag:28s}: {count:4d} ({pct:5.1f}%)")

        # Any distortion rate for this epoch
        epoch_with_distortion = sum(1 for r in epoch_substantive if len(compute_distortion_tags(r)) > 0)
        epoch_any_rate = (epoch_with_distortion / epoch_substantive_count * 100) if epoch_substantive_count > 0 else 0
        print(f"  Any distortion rate: {epoch_with_distortion}/{epoch_substantive_count} ({epoch_any_rate:.1f}%)")
        output_lines.append(f"  Any distortion rate: {epoch_with_distortion}/{epoch_substantive_count} ({epoch_any_rate:.1f}%)")

    # ========== MEAN DISTORTION COUNT BY EPOCH ==========
    print_section("MEAN DISTORTION COUNT BY EPOCH (Substantive Posts Only)")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("  MEAN DISTORTION COUNT BY EPOCH (Substantive Posts Only)")
    output_lines.append("=" * 80)

    print()
    output_lines.append("")
    for epoch in epochs:
        epoch_rows = epoch_data[epoch]
        epoch_substantive = [r for r in epoch_rows if r["claim_strength"] == "substantive_mention"]

        distortion_counts = [len(compute_distortion_tags(r)) for r in epoch_substantive]
        if distortion_counts:
            mean_distortion = sum(distortion_counts) / len(distortion_counts)
            min_d = min(distortion_counts)
            max_d = max(distortion_counts)
            print(f"  Epoch {epoch}: {mean_distortion:.2f} (min={min_d}, max={max_d})")
            output_lines.append(f"  Epoch {epoch}: {mean_distortion:.2f} (min={min_d}, max={max_d})")

    # ========== CITATION TYPE × DISTORTION ==========
    print_section("CITATION TYPE × DISTORTION ANALYSIS")
    output_lines.append("\n" + "=" * 80)
    output_lines.append("  CITATION TYPE × DISTORTION ANALYSIS")
    output_lines.append("=" * 80)

    citation_types = sorted(set(r["citation_type"] for r in rows if r["citation_type"]))
    for ctype in citation_types:
        type_rows = [r for r in rows if r["citation_type"] == ctype]
        type_substantive = [r for r in type_rows if r["claim_strength"] == "substantive_mention"]
        type_count = len(type_substantive)

        print(f"\n{ctype} (n={type_count} substantive):")
        output_lines.append(f"\n{ctype} (n={type_count} substantive):")

        for tag in DISTORTION_TAGS:
            count = sum(1 for r in type_substantive if compute_distortion_tags(r).count(tag) > 0)
            pct = (count / type_count * 100) if type_count > 0 else 0
            print(f"  {tag:28s}: {count:4d} ({pct:5.1f}%)")
            output_lines.append(f"  {tag:28s}: {count:4d} ({pct:5.1f}%)")

        type_with_distortion = sum(1 for r in type_substantive if len(compute_distortion_tags(r)) > 0)
        type_any_rate = (type_with_distortion / type_count * 100) if type_count > 0 else 0
        print(f"  Any distortion: {type_with_distortion}/{type_count} ({type_any_rate:.1f}%)")
        output_lines.append(f"  Any distortion: {type_with_distortion}/{type_count} ({type_any_rate:.1f}%)")

    # Write output file
    print_section("OUTPUT FILE")
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(output_lines))
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
