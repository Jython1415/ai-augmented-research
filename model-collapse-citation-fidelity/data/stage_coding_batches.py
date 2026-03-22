# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stage production coding batches for citation fidelity study.
Pass 1: Post text only.
Pass 2: Post + context (parent text, quoted text, thread context).
"""

import sqlite3
import json
import argparse
from pathlib import Path

DB_PATH = Path("/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db")


def get_uncoded_units(pass_num: str, batch_size: int = 10):
    """Query all citation_units that haven't been coded for the specified pass.

    Pass 1: Code based on post text only (no context).
    Pass 2: Code based on post + context (parent posts, quoted posts, thread context).
    Pass "v4": Code based on post text only (for V4 scheme).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if pass_num == 1 or pass_num == "v4":
        # Find all citation units that don't have results in the respective table yet
        table_name = "coding_pass1" if pass_num == 1 else "coding_v4"
        query = f"""
            SELECT
                cu.id as cu_id,
                p.id as post_id,
                cu.epoch,
                cu.citation_type,
                cu.created_at,
                p.text
            FROM citation_units cu
            JOIN posts p ON p.uri = cu.anchor_post_uri
            WHERE cu.id NOT IN (SELECT citation_unit_id FROM {table_name})
            ORDER BY cu.epoch, cu.created_at
        """
        rows = conn.execute(query).fetchall()

        batches = []
        for i in range(0, len(rows), batch_size):
            batch = []
            for row in rows[i : i + batch_size]:
                batch.append({
                    "post_id": row["post_id"],
                    "cu_id": row["cu_id"],
                    "epoch": row["epoch"],
                    "citation_type": row["citation_type"],
                    "created_at": row["created_at"],
                    "text": row["text"],
                })
            batches.append(batch)

    elif pass_num == 2:
        # Find all citation units that don't have results in coding_pass2 table yet
        # (but do have results in coding_pass1, since pass 2 requires pass 1 to be complete)
        query = """
            SELECT
                cu.id as cu_id,
                p.id as post_id,
                cu.epoch,
                cu.citation_type,
                cu.created_at,
                p.text,
                pc.parent_text,
                pc.quoted_text,
                (SELECT GROUP_CONCAT(tc.post_text, '|||')
                 FROM thread_context tc
                 WHERE tc.citation_unit_id = cu.id AND tc.relationship = 'parent'
                 ORDER BY tc.depth) as parent_chain,
                (SELECT GROUP_CONCAT(tc.post_text, '|||')
                 FROM thread_context tc
                 WHERE tc.citation_unit_id = cu.id AND tc.relationship = 'self_reply'
                 ORDER BY tc.depth) as self_replies
            FROM citation_units cu
            JOIN posts p ON p.uri = cu.anchor_post_uri
            LEFT JOIN post_context pc ON p.id = pc.post_id
            WHERE cu.id NOT IN (SELECT citation_unit_id FROM coding_pass2)
            ORDER BY cu.epoch, cu.created_at
        """
        rows = conn.execute(query).fetchall()

        batches = []
        for i in range(0, len(rows), batch_size):
            batch = []
            for row in rows[i : i + batch_size]:
                unit = {
                    "post_id": row["post_id"],
                    "cu_id": row["cu_id"],
                    "epoch": row["epoch"],
                    "citation_type": row["citation_type"],
                    "created_at": row["created_at"],
                    "text": row["text"],
                }
                if row["parent_text"]:
                    unit["parent_text"] = row["parent_text"]
                if row["quoted_text"]:
                    unit["quoted_text"] = row["quoted_text"]
                if row["parent_chain"]:
                    unit["parent_chain"] = row["parent_chain"]
                if row["self_replies"]:
                    unit["self_replies"] = row["self_replies"]
                batch.append(unit)
            batches.append(batch)

    else:
        raise ValueError(f"Invalid pass: {pass_num}. Must be 1, 2, or v4.")

    conn.close()
    return batches, len(rows)


def main():
    parser = argparse.ArgumentParser(description="Stage production coding batches.")
    parser.add_argument("--pass", required=True, dest="pass_num",
                        help="Coding pass: 1, 2, or v4")
    parser.add_argument("--batch-size", type=int, default=10,
                        help="Batch size (default 10)")
    args = parser.parse_args()

    pass_num = args.pass_num

    # Validate and normalize pass_num
    try:
        if pass_num in ["1", "2"]:
            pass_num = int(pass_num)
        elif pass_num != "v4":
            # Try to parse as int
            pass_num = int(pass_num)
            if pass_num not in [1, 2]:
                raise ValueError()
    except ValueError:
        parser.error("--pass must be 1, 2, or v4")

    batch_size = args.batch_size

    # Query and create batches
    batches, total_cus = get_uncoded_units(pass_num, batch_size)

    if not batches:
        print(f"No uncoded units for pass {pass_num}")
        return

    # Create output directory (handle both int and string pass_nums)
    pass_str = f"pass{pass_num}" if isinstance(pass_num, int) else pass_num
    batch_dir = Path(f"/private/tmp/claude/coding/production/{pass_str}")
    batch_dir.mkdir(parents=True, exist_ok=True)

    # Write batches
    for batch_idx, batch in enumerate(batches, start=1):
        batch_file = batch_dir / f"batch_{batch_idx:03d}.json"
        with open(batch_file, 'w') as f:
            json.dump(batch, f, indent=2)

    # Summary
    num_batches = len(batches)
    print(f"Pass {pass_num} coding batches:")
    print(f"  Total CUs to code: {total_cus}")
    print(f"  Number of batches: {num_batches}")
    print(f"  Batch size: {batch_size}")
    if batches:
        print(f"  Last batch size: {len(batches[-1])}")
    print(f"  Output directory: {batch_dir}")


if __name__ == "__main__":
    main()
