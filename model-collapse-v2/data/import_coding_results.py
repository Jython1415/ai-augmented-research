# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Import coding results into citation_units table.

Supports both pass 1 and pass 2 coding results. Idempotent: skips units
that already have coding for the specified pass.
"""

import sqlite3
import json
import argparse
from pathlib import Path
from typing import Optional

DB_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")

REQUIRED_FIELDS = {
    "post_id",
    "claim_strength",
    "claim_strength_reasoning",
    "paper_fidelity",
    "paper_fidelity_reasoning",
    "field_accuracy",
    "field_accuracy_reasoning",
    "epoch",
}


def load_result_files(source: Path) -> list[dict]:
    """Load result JSON files from file or directory.

    Args:
        source: Path to a single JSON file or directory of JSON files.

    Returns:
        List of result objects loaded from JSON.

    Raises:
        FileNotFoundError: If source doesn't exist.
        ValueError: If source is not a file or directory.
    """
    if not source.exists():
        raise FileNotFoundError(f"Path does not exist: {source}")

    results = []

    if source.is_file():
        with open(source, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
    elif source.is_dir():
        json_files = sorted(source.glob("*.json"))
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    results.extend(data)
                else:
                    results.append(data)
    else:
        raise ValueError(f"Source must be a file or directory: {source}")

    return results


def validate_result(result: dict, result_num: int) -> Optional[str]:
    """Validate result object has all required fields.

    Args:
        result: Result object to validate.
        result_num: Index for error reporting.

    Returns:
        Error message if validation fails, None if valid.
    """
    missing = REQUIRED_FIELDS - set(result.keys())
    if missing:
        return f"Result {result_num}: missing fields {missing}"
    return None


def import_results(pass_num: int, results: list[dict]) -> tuple[int, int, int]:
    """Import coding results into the appropriate coding_passN table.

    Args:
        pass_num: Coding pass (1 or 2).
        results: List of result objects to import.

    Returns:
        Tuple of (imported_count, skipped_count, error_count).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()

    imported = 0
    skipped = 0
    errors = 0

    # Determine target table based on pass number
    table_name = f"coding_pass{pass_num}"

    for result_num, result in enumerate(results, start=1):
        # Validate result
        error_msg = validate_result(result, result_num)
        if error_msg:
            print(f"ERROR: {error_msg}")
            errors += 1
            continue

        post_id = result.get("post_id")

        if post_id is None:
            print(f"ERROR: Result {result_num}: post_id is required")
            errors += 1
            continue

        try:
            # Find citation_unit by post_id -> uri -> anchor_post_uri
            cursor.execute(
                """
                SELECT cu.id FROM citation_units cu
                JOIN posts p ON p.uri = cu.anchor_post_uri
                WHERE p.id = ?
                """,
                (post_id,),
            )
            row = cursor.fetchone()

            if not row:
                print(f"WARNING: Result {result_num}: No citation_unit found for post_id {post_id}")
                errors += 1
                continue

            cu_id = row[0]

            # Check if already coded for this pass
            cursor.execute(
                f"""
                SELECT citation_unit_id FROM {table_name}
                WHERE citation_unit_id = ?
                """,
                (cu_id,),
            )
            existing = cursor.fetchone()

            if existing:
                # Already coded for this pass
                skipped += 1
                continue

            # Insert coding results into the pass-specific table
            # Note: rationale field contains all reasoning
            cursor.execute(
                f"""
                INSERT INTO {table_name}
                    (citation_unit_id, claim_strength, field_accuracy,
                     paper_fidelity, rationale, agent_id)
                VALUES (?, ?, ?, ?, ?, NULL)
                """,
                (
                    cu_id,
                    result.get("claim_strength"),
                    result.get("field_accuracy"),
                    result.get("paper_fidelity"),
                    # Combine all reasoning fields into rationale
                    f"claim_strength: {result.get('claim_strength_reasoning')}\n"
                    f"paper_fidelity: {result.get('paper_fidelity_reasoning')}\n"
                    f"field_accuracy: {result.get('field_accuracy_reasoning')}",
                ),
            )
            imported += 1

        except sqlite3.Error as e:
            print(f"ERROR: Result {result_num}: Database error: {e}")
            errors += 1
            continue

    conn.commit()
    conn.close()

    return imported, skipped, errors


def main():
    parser = argparse.ArgumentParser(
        description="Import coding results into citation_units table."
    )
    parser.add_argument(
        "--pass",
        type=int,
        required=True,
        choices=[1, 2],
        dest="pass_num",
        help="Coding pass (1 or 2)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        type=Path,
        help="Path to a single result JSON file",
    )
    group.add_argument(
        "--dir",
        type=Path,
        help="Path to directory of result JSON files",
    )

    args = parser.parse_args()

    # Determine source path
    source = args.file if args.file else args.dir

    try:
        # Load results
        results = load_result_files(source)

        if not results:
            print(f"No results found in {source}")
            return

        # Import results
        imported, skipped, errors = import_results(args.pass_num, results)

        # Print summary
        print(f"\nPass {args.pass_num} import summary:")
        print(f"  Imported: {imported}")
        print(f"  Skipped (already coded): {skipped}")
        print(f"  Errors: {errors}")
        print(f"  Total processed: {imported + skipped + errors}")

        if errors > 0:
            exit(1)

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)


if __name__ == "__main__":
    main()
