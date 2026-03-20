#!/usr/bin/env python3
"""
Normalize coding results from V2 to V3 enum values.

Handles:
- claim_strength: casual/share → neutral_share, moderate/mention → substantive_mention, authoritative/strong → authoritative_claim
- paper_fidelity and field_accuracy: Keep accurate/partially_accurate/misrepresentation/inaccurate as-is
- CRITICAL: If claim_strength is neutral_share (after normalization), set paper_fidelity and field_accuracy to not_applicable
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def normalize_claim_strength(value: str) -> str:
    """Normalize claim_strength from V2 to V3 values."""
    if value is None:
        return None

    value_lower = value.lower().strip()

    # Map casual/share variants to neutral_share
    if value_lower in ("casual", "share", "neutral_share"):
        return "neutral_share"

    # Map moderate/mention variants to substantive_mention
    if value_lower in ("moderate", "mention", "substantive_mention"):
        return "substantive_mention"

    # Map authoritative/strong variants to authoritative_claim
    if value_lower in ("authoritative", "strong", "authoritative_claim"):
        return "authoritative_claim"

    # If no match, return original (might already be V3 or an unexpected value)
    return value


def normalize_post(post: Dict[str, Any]) -> tuple[Dict[str, Any], bool]:
    """
    Normalize a single post's coding values.

    Returns: (normalized_post, was_changed)
    """
    changed = False
    normalized = post.copy()

    # Normalize claim_strength
    old_claim_strength = normalized.get("claim_strength")
    new_claim_strength = normalize_claim_strength(old_claim_strength)
    if new_claim_strength != old_claim_strength:
        normalized["claim_strength"] = new_claim_strength
        changed = True

    # If claim_strength is neutral_share, set paper_fidelity and field_accuracy to not_applicable
    if normalized.get("claim_strength") == "neutral_share":
        old_paper_fidelity = normalized.get("paper_fidelity")
        old_field_accuracy = normalized.get("field_accuracy")

        if old_paper_fidelity != "not_applicable":
            normalized["paper_fidelity"] = "not_applicable"
            normalized["paper_fidelity_reasoning"] = "Neutral share — no claim to evaluate"
            changed = True

        if old_field_accuracy != "not_applicable":
            normalized["field_accuracy"] = "not_applicable"
            normalized["field_accuracy_reasoning"] = "Neutral share — no claim to evaluate"
            changed = True

    return normalized, changed


def normalize_file(file_path: Path) -> tuple[int, int]:
    """
    Normalize a single results file.

    Returns: (total_posts, posts_changed)
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON in {file_path}: {e}")
        return 0, 0

    if not isinstance(data, list):
        print(f"ERROR: {file_path} does not contain a JSON array")
        return 0, 0

    normalized_data = []
    posts_changed = 0

    for post in data:
        normalized_post, was_changed = normalize_post(post)
        normalized_data.append(normalized_post)
        if was_changed:
            posts_changed += 1

    # Write back to file
    try:
        with open(file_path, 'w') as f:
            json.dump(normalized_data, f, indent=2)
    except Exception as e:
        print(f"ERROR: Failed to write {file_path}: {e}")
        return len(data), 0

    return len(data), posts_changed


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 normalize_coding_results.py <directory>")
        print("Normalizes all results_*.json files in the directory")
        sys.exit(1)

    directory = Path(sys.argv[1])

    if not directory.exists():
        print(f"ERROR: Directory does not exist: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        print(f"ERROR: Not a directory: {directory}")
        sys.exit(1)

    # Find all results_*.json files
    result_files = sorted(directory.glob("results_*.json"))

    if not result_files:
        print(f"No results_*.json files found in {directory}")
        sys.exit(1)

    print(f"Found {len(result_files)} results files to normalize")
    print()

    total_posts = 0
    total_changed = 0

    for file_path in result_files:
        posts, changed = normalize_file(file_path)
        total_posts += posts
        total_changed += changed

        if changed > 0:
            print(f"✓ {file_path.name}: {changed}/{posts} posts normalized")
        else:
            print(f"  {file_path.name}: no changes needed")

    print()
    print(f"Summary: {total_changed}/{total_posts} total posts normalized across {len(result_files)} files")


if __name__ == "__main__":
    main()
