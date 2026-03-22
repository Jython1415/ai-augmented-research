# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Import V4 coding results into coding_v4 table."""

import sqlite3
import json
import argparse
from pathlib import Path

DB_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")
VALID_CLAIM_STRENGTHS = {"neutral_share", "substantive_mention", "authoritative_claim"}


def get_citation_unit_id(post_id: int) -> int | None:
    """Look up citation_unit_id from post_id."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT cu.id FROM citation_units cu
        JOIN posts p ON p.uri = cu.anchor_post_uri
        WHERE p.id = ?
    """
    result = conn.execute(query, (post_id,)).fetchone()
    conn.close()
    return result[0] if result else None


def import_results(file_or_dir: Path) -> tuple[int, int, list[str]]:
    """Import V4 results from JSON file(s).

    Returns: (imported_count, skipped_count, error_list)
    """
    conn = sqlite3.connect(DB_PATH)
    imported = 0
    skipped = 0
    errors = []

    # Collect all JSON files (results_batch_*.json only)
    json_files = []
    if file_or_dir.is_file():
        json_files = [file_or_dir]
    elif file_or_dir.is_dir():
        json_files = sorted(file_or_dir.glob("results_batch_*.json"))
    else:
        errors.append(f"Path does not exist: {file_or_dir}")
        conn.close()
        return imported, skipped, errors

    for json_file in json_files:
        try:
            with open(json_file) as f:
                results = json.load(f)
                if not isinstance(results, list):
                    results = [results]

            for result in results:
                try:
                    # Validate required fields
                    post_id = result.get("post_id")
                    claim_strength = result.get("claim_strength")

                    if not post_id:
                        errors.append(f"Missing post_id in {json_file}")
                        continue

                    if not claim_strength:
                        errors.append(f"Missing claim_strength for post_id {post_id}")
                        continue

                    if claim_strength not in VALID_CLAIM_STRENGTHS:
                        errors.append(
                            f"Invalid claim_strength '{claim_strength}' for post_id {post_id}. "
                            f"Must be one of: {', '.join(VALID_CLAIM_STRENGTHS)}"
                        )
                        continue

                    # Look up citation_unit_id
                    cu_id = get_citation_unit_id(post_id)
                    if cu_id is None:
                        errors.append(f"Could not find citation_unit_id for post_id {post_id}")
                        continue

                    # Convert bools to 0/1
                    row_data = {
                        "citation_unit_id": cu_id,
                        "claim_strength": claim_strength,
                        "certainty_inflation": 1 if result.get("certainty_inflation", False) else 0,
                        "scope_inflation": 1 if result.get("scope_inflation", False) else 0,
                        "temporal_overclaim": 1 if result.get("temporal_overclaim", False) else 0,
                        "causal_conflation": 1 if result.get("causal_conflation", False) else 0,
                        "mechanism_omission": 1 if result.get("mechanism_omission", False) else 0,
                        "mitigation_blindness": 1 if result.get("mitigation_blindness", False) else 0,
                        "definitional_conflation": 1 if result.get("definitional_conflation", False) else 0,
                        "sensationalism": 1 if result.get("sensationalism", False) else 0,
                        "distortion_reasoning": result.get("distortion_reasoning"),
                        "epoch": result.get("epoch"),
                    }

                    # Try to insert
                    try:
                        conn.execute(
                            """INSERT INTO coding_v4
                            (citation_unit_id, claim_strength, certainty_inflation, scope_inflation,
                             temporal_overclaim, causal_conflation, mechanism_omission, mitigation_blindness,
                             definitional_conflation, sensationalism, distortion_reasoning, epoch)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (row_data["citation_unit_id"], row_data["claim_strength"],
                             row_data["certainty_inflation"], row_data["scope_inflation"],
                             row_data["temporal_overclaim"], row_data["causal_conflation"],
                             row_data["mechanism_omission"], row_data["mitigation_blindness"],
                             row_data["definitional_conflation"], row_data["sensationalism"],
                             row_data["distortion_reasoning"], row_data["epoch"])
                        )
                        imported += 1
                    except sqlite3.IntegrityError as e:
                        if "UNIQUE constraint failed" in str(e):
                            skipped += 1
                        else:
                            errors.append(f"Insert error for post_id {post_id}: {e}")

                except Exception as e:
                    errors.append(f"Error processing result: {e}")

        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in {json_file}: {e}")
        except Exception as e:
            errors.append(f"Error reading {json_file}: {e}")

    conn.commit()
    conn.close()
    return imported, skipped, errors


def main():
    parser = argparse.ArgumentParser(description="Import V4 coding results.")
    parser.add_argument("--file", type=Path, help="Path to JSON file")
    parser.add_argument("--dir", type=Path, help="Path to directory of JSON files")
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.error("Must specify either --file or --dir")
    if args.file and args.dir:
        parser.error("Cannot specify both --file and --dir")

    path = args.file or args.dir
    imported, skipped, errors = import_results(path)

    print(f"V4 Import Summary:")
    print(f"  Imported: {imported}")
    print(f"  Skipped: {skipped}")
    if errors:
        print(f"  Errors: {len(errors)}")
        for error in errors[:10]:  # Show first 10 errors
            print(f"    - {error}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more errors")


if __name__ == "__main__":
    main()
