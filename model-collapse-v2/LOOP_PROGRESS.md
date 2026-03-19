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

## Iteration 2-3 (2026-03-19)

### Phase B: Fleet Coding Pass 1 — Wave 1 complete
- Dispatched 5 coding agents (batches 001-005, 50 posts)
- 3 agents completed in iteration 1, 2 completed between iterations (loop cycled before they finished)
- All 5 result files verified: valid JSON, all fields present, correct enum values, neutral_share constraints met
- Imported all 50 results to DB (0 errors)
- Progress: 50/539 CUs coded (9.3%)
- Wave 2 dispatched (batches 006-010)

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

## Iteration 4-6 (2026-03-19)

### Phase B: Fleet Coding Pass 1 — Waves 2-3 complete
- Wave 2 (batches 006-010): all verified and imported
- Wave 3 (batches 011-015): completed across iterations (some agents didn't finish before loop cycled, re-dispatched)
- Wave 4 partial (016-017): all 50 new results verified and imported
- Pattern: agents typically complete within 1-2 loop cycles; dispatching 5-7 per iteration works well
- All verification checks passing: valid JSON, correct fields, no Bash violations
- Progress: 170/539 CUs coded (31.5%)

## Iteration 7-11 (2026-03-19)

### Phase B: Fleet Coding Pass 1 — COMPLETE
- Multi-batch agent strategy: each Haiku agent handles ~3-4 batches before hitting context limits
- All 54 result files completed: all 539 citation units fully coded
- All imports clean, no errors, no Bash violations detected
- Final verification: 539/539 CUs with coding_pass = 1 in database
- Pattern confirmed: dispatch 4 agents × 4 batches each per iteration = ~16 batches/iteration
- Final idempotent import sweep (iteration 11): 0 new imports, 540 skipped (already coded), 0 errors

### Code Distribution (Pass 1, post-only)
**claim_strength:**
- authoritative_claim: 19
- neutral_share: 129
- substantive_mention: 391

**paper_fidelity:**
- accurate: 303
- partially_accurate: 85
- misrepresentation: 20
- not_applicable: 131

**field_accuracy:**
- accurate: 334
- partially_accurate: 53
- inaccurate: 21
- not_applicable: 131

### Next Phase
Moving to Phase C: Fleet Coding Pass 2 (with context, 539 CUs)
