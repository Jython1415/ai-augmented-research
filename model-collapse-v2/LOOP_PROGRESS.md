# Loop Progress

Iteration-by-iteration log. Append only.

## Pre-Loop (Manual Session — 2026-03-18)

### Coding Scheme Design & Calibration (Phase 5 partial)
- Designed 3-dimension coding scheme: claim_strength, paper_fidelity, field_accuracy
- Built stratified calibration sample: 50 posts across 5 epochs
- Ran 8 calibration rounds with 3 independent Haiku coders
- Iterated codebook through multiple revisions:
  - Collapsed claim_strength from 4 to 3 levels (round 3)
  - Added positive framing + worked examples targeting boundary cases (round 7)
  - Dropped oversimplified from field_accuracy (round 8)
  - VDD review found and fixed contradictions in codebook
- Final ICR: claim_strength a=0.888 (STRONG), paper_fidelity a=0.762 (TENTATIVE), field_accuracy a=0.816 (STRONG)
- Cleaned 42 Shumailov false positives (wrong papers): 581 to 539 relevant CUs
- Codebook finalized at prompts/coding_scheme_v1.md

### Infrastructure Status
- Calibration scripts exist: build_calibration_sample.py, stage_calibration_batches.py, compute_icr.py
- Production scripts needed: stage_coding_batches.py, import_coding_results.py, fetch_author_profiles.py
- Pass 2 codebook needed: prompts/coding_scheme_pass2.md
- DB schema: citation_units table has columns for coding results (claim_strength, paper_fidelity, field_accuracy + reasoning, epoch, coding_pass)

### Key Learnings
- Haiku agents use Bash ~75% of the time unless explicitly banned in BOTH spawn prompt and instruction file
- Positive framing ("X IS accurate") outperforms negative ("don't code X as partially_accurate") by ~8%
- Quick Reference section at top of codebook + worked examples = biggest ICR improvement
- Verification agents should check tool compliance, not labeling quality

## Iteration 1 (2026-03-19)

### Phase A: Build Infrastructure — COMPLETE
- Wrote data/stage_coding_batches.py (stages 539 CUs into batches of 10, supports pass 1 and 2)
- Wrote data/import_coding_results.py (idempotent import to citation_units, WAL mode, field validation)
- Wrote prompts/coding_scheme_pass2.md (pass 2 codebook with context section)
- Wrote data/fetch_author_profiles.py (Bluesky public API, 445 authors, rate limited)
- Tested end-to-end: stage → mock import → verify → rollback. Pipeline works.
- 54 batches for pass 1, DB clean and ready for fleet coding
