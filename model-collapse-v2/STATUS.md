# Study Status

## Current State

**Phase F (Paper Writing) — COMPLETE. All phases finished.**

V2 coding is complete and archived. V3 codebook revision (stricter, preserving conditional nature of findings) underwent 3 ICR calibration rounds and achieved final consensus: α = 0.917 (claim) / 0.757 (fidelity) / 0.779 (field). Full re-code of both passes complete: 539/539 CUs in Pass 1, 539/539 in Pass 2. V3 codes normalize enum values and address V2 systematic leniency in paper_fidelity. All analyses re-run with V3 data; paper updated with all V3 statistics, revised results section, and methodology caveat on V2→V3 audit.

**Current phase**: Phase F (Paper Writing) — COMPLETE.
**Next immediate step**: Project complete. Paper ready for review.

## Immediate Next Steps

Project complete. Paper ready for review.

## Phase Progress

### Phase 1: Design & Alignment — COMPLETE
- Research question: How faithfully do Bluesky users represent Shumailov et al. (2024) when citing it, and does this change as the field evolves?
- Unit of analysis: Citation event (same person citing in 3 threads = 3 units); thread-level for self-reply threads
- Citation signals: Links (Nature/arXiv/DOI), author names, title phrases, indirect attributions, news coverage
- Accuracy dimensions: (1) Faithful to paper's claims? (2) Accurate to broader field state at time of posting?
- Two-pass coding design: Post-only (pass 1) vs. with-context (pass 2) to measure how context changes interpretation

### Phase 2-2.5: Search Term Discovery — COMPLETE
- Initial 9 search terms (3 tiers), then expanded to 16 terms with 7 metaphorical/informal terms
- Verified 35+ news coverage URLs as citation signals
- Corpus: 7,503 posts from Bluesky (May 2023 onward)

### Phase 4: Literature Timeline — COMPLETE
- 15 verified papers across 6 knowledge epochs (1960s to 2024)
- All entries verified against arXiv abstracts (11 factual corrections applied)
- Coded as "coding-reference.md" for subagent prompts

### Phase 3: Data Collection & Classification — COMPLETE

#### Collection & Relevance Filtering
- v4 classification (decision tree + citation_signal chain-of-thought + hard negatives)
- 581 posts classified as relevant (7.7% of 7,503)
- Verification pass on 446 non-auto-accepted relevant posts (9 batches)
- 29 confirmed false positives after manual reconciliation (4.8% FP rate)
- **Final: 581 relevant posts** (later cleaned to 539 CUs after Shumailov false positive removal)

#### Citation Units & Thread Context
- 539 citation units extracted (36 link, 60 author_name, 152 title_phrase, 333 indirect)
- 691 context posts fetched for 263/539 units (318 units standalone)
  - 377 parent posts, 232 reply children, 82 self-replies
- Thread context fetching complete

#### Author Profiles
- 445/445 unique authors fetched from Bluesky API (complete)

### Phase 5: Coding — V3 COMPLETE

#### V3 Results (Post-only & With-Context)
- **Pass 1 (post-only)**: 539/539 CUs coded
  - claim_strength: 22 authoritative_claim, 107 neutral_share, 410 substantive_mention
  - paper_fidelity: 288 accurate, 99 partially_accurate, 25 misrepresentation, 127 N/A
  - field_accuracy: 319 accurate, 65 partially_accurate, 28 inaccurate, 127 N/A
- **Pass 2 (with-context)**: 539/539 CUs coded
  - claim_strength: 8 authoritative_claim, 116 neutral_share, 415 substantive_mention
  - paper_fidelity: 306 accurate, 89 partially_accurate, 14 misrepresentation, 130 N/A
  - field_accuracy: 332 accurate, 59 partially_accurate, 18 inaccurate, 130 N/A

#### V3 Codebook Revision (2026-03-20)
- **Issue found**: V2 audit revealed 38% of pass 1 "accurate" should be "partially_accurate"; 33% of "partially_accurate" should be "misrepresentation"
- **Root cause**: V1-V2 codebook too permissive on "reasonable interpretive extensions" of paper claims
- **V3 fix**: paper_fidelity now requires preserving CONDITIONAL nature of findings
  - "AI trained on AI can degrade" → accurate (conditional)
  - "Collapse threatens all AI" → partially_accurate (overgeneralizes scope)
  - "Collapse is inevitable" → misrepresentation (removes conditionality)
- **Calibration examples**: Increased from 4 to 12 examples, added cross-dimension consistency rules
- **V3 ICR calibration**: 3 rounds completed
  - Round 1: α = 0.775 (claim) / 0.685 (fidelity) / 0.729 (field)
  - Round 2-3: Refined codebook boundaries and cross-dimension rules
  - Final: α = 0.917 (claim) / 0.757 (fidelity) / 0.779 (field) — all acceptable
- **Data integrity**: Enum values normalized across all 1,078 coded rows (both passes)

### Phase E: Analysis — COMPLETE

#### Analysis Status (V3 Data)
- V3 re-code complete with 539/539 CUs in both passes
- All summary statistics, epoch trends, and two-pass comparison re-run with V3 codes
- Outputs: Updated figures, summary statistics file (`analysis_output_v3.txt`), epoch trend analysis
- Key finding: Epoch fidelity decline from 88% (Pass 1, Epoch 1-4) to 62% (Pass 1, Epoch 6); no reach-accuracy correlation

### Phase F: Paper Writing — COMPLETE

#### Paper Draft (Updated with V3 Results)
- `paper/paper.tex` — Conference paper revised with V3 statistics and methodology section
- `paper/references.bib` — 19 BibTeX references
- **Status**: All V3 results integrated; paper ready for review
- All figures updated to reflect V3 analysis (in `paper/` directory)

## Data Architecture

### Database Tables
- `posts` — 7,503 posts (581 relevant, 6,922 not relevant, 0 unclassified)
- `citation_units` — 539 CUs with coding results from pass 1 (coding_pass=1 column)
- `coding_pass2` — 539 CUs with coding results from pass 2 (separate table for two-pass comparison)
- `post_context` — 691 context posts (parent_text, quoted_text, thread structure)
- `author_profiles` — 445 unique authors (follower counts, bio, names)

### Key Files
- **Codebooks**: `prompts/coding_scheme_v1.md` (V3, stricter), `prompts/coding_scheme_pass2.md` (V3, stricter)
- **Classification**: `prompts/classification_instructions_v*.md` (v2 final, narrow scope)
- **Literature**: `lit-timeline/timeline.md`, `lit-timeline/coding-reference.md`, `lit-timeline/news-coverage-urls.md`
- **Audit**: `audit/verification/` (v4 verification results), `audit/icr/` (ICR samples and coder results)
- **Analysis**: `data/analyze_all.py`, `data/analyze_epoch_trends.py`, `data/analyze_twopass.py`, `data/analyze_authors.py`
- **Paper**: `paper/paper.tex`, `paper/references.bib`, figures in `paper/`

## V3 Codebook Design

### Core Change
Paper_fidelity `accurate` now requires preserving the CONDITIONAL nature of the paper's finding.

### Dimensions
1. **claim_strength** (3 levels): authoritative_claim, neutral_share, substantive_mention
2. **paper_fidelity** (4 levels): accurate, partially_accurate, misrepresentation, not_applicable
   - Accurate: Finds and presents the finding with its conditional assumptions intact
   - Partially_accurate: Extends, generalizes, or adds caveats (reasonable but not direct)
   - Misrepresentation: Removes conditionality, overstates inevitability, or contradicts the paper
   - Not_applicable: For neutral_share posts (no fidelity assessment)
3. **field_accuracy** (4 levels): accurate, partially_accurate, inaccurate, not_applicable
   - Accurate: Reflects current field knowledge at time of posting
   - Partially_accurate: Missing new findings but not contradicting them
   - Inaccurate: Contradicts established field knowledge
   - Not_applicable: For neutral_share posts

### 12 Calibration Examples (Key Boundary Cases)
- Conditional language ("can cause") vs. deterministic ("will cause") vs. inevitable ("must cause")
- Scope preservation ("model collapse under these conditions") vs. overgeneralization ("model collapse will doom AI")
- Timing awareness (2023 vs. 2024 field context)
- Causal claims (the paper shows correlation, not proof)

### Cross-Dimension Consistency Rules
- If paper_fidelity=misrepresentation, claim_strength cannot be authoritative_claim (inconsistent)
- If claim_strength=neutral_share, paper_fidelity and field_accuracy should be N/A
- If field_accuracy=inaccurate (contradicts field), paper_fidelity likely partially_accurate+ or misrepresentation

## V3 Calibration Status
- **Round 1 complete** (2026-03-20): α = 0.775/0.685/0.729
  - claim_strength: Stricter boundaries, down from 0.888 (expected)
  - paper_fidelity: Main revision axis, C1 over-corrects, C2 too generous on scope
  - field_accuracy: Down from 0.816 (expected)
- **Round 2-3 complete** (2026-03-20): Refined codebook boundaries and cross-dimension rules
  - claim_strength: α = 0.917 (all 3 coders converged on stricter authoritative_claim)
  - paper_fidelity: α = 0.757 (main revision axis resolved, boundary agreement improved)
  - field_accuracy: α = 0.779 (expected convergence)
- **Status**: All dimensions acceptable (α ≥ 0.75); proceeding to full re-code
- **Calibration data**: `/private/tmp/claude/coding/calibration/` (50-post stratified sample)

## Key Learnings

### Fleet Operations
- Haiku agents use Bash ~75% of the time even with prompt bans; explicit tool restrictions required (no Bash in spawn prompt + instruction file)
- Positive framing ("X IS accurate") outperforms negative ("don't code X as") by ~8%
- Multi-batch agents: 3-4 batches before context limits; dispatch 4-5 per iteration for ~16/iteration
- Import verification critical: Always check DB unclassified count after each wave; run reconciliation at session boundaries
- Test-before-scale: Always run 2-3 agents and audit JSONL logs before full fleet (avoided 50K+ tokens wasted)

### Classification & Coding
- v4 decision tree + citation_signal chain-of-thought + hard negatives: 4.8% FP rate (vs v3's 32%)
- Context-first design: 28% of hard cases change classification when parent/quote context available
- Verification with full context: Include parent_text/quoted_text in verification batches (verification agents need same context as classifiers)
- VDD-style audits catch systematic bias that ICR alone misses (discovered V2 paper_fidelity leniency via 50-post audit)

### Dataset Properties
- 7,503 posts, 539 final citation units, 445 unique authors
- 27% of units from 53 repeat citers (1 super-citer with 18)
- 45% have thread context, 55% standalone
- 5.5% authoritative claims, 19% neutral shares, 76% substantive mentions (pass 1)
- Epoch 6 (2024) shows decline in fidelity + rise in authoritative claims (potential recency bias — Epoch 6 is 3.6x larger)

## Project Files

### Data Scripts
- `data/init_db.py` — Database initialization (7 tables)
- `data/collect_posts.py` — Bluesky post collection
- `data/stage_relevance_batches.py` — Stages classification batches with context
- `data/import_relevance_results.py` — Idempotent import (WAL, --file flag, skip-classified)
- `data/build_citation_units.py` — Creates citation_units from relevant posts
- `data/fetch_thread_context.py` — Fetches full thread context (parent + descendants)
- `data/fetch_author_profiles.py` — Fetches author profiles from Bluesky API
- `data/stage_coding_batches.py` — Stages coding batches (supports pass 1 and 2)
- `data/import_coding_results.py` — Idempotent import for coding results
- `data/analyze_all.py` — Summary statistics and epoch trends
- `data/analyze_epoch_trends.py` — Epoch fidelity decline analysis
- `data/analyze_twopass.py` — Two-pass comparison (κ computation)
- `data/analyze_authors.py` — Author demographics and repeat citer analysis

### Artifacts
- `data/posts.db` — SQLite database (ground truth)
- `.env` — Bluesky credentials (gitignored)
- `.gitignore` — Excludes sensitive files and database
- `lit-timeline/` — Literature timeline, coding reference, news URLs
- `papers/` — Downloaded PDFs of 15 referenced papers
- `prompts/` — All instruction files (classification v2, codebooks v1-v3)
- `audit/` — Audit reports, verification results, ICR samples
- `paper/` — Paper draft (LaTeX) and figures

## Subagent Fleet Status

V3 re-code fleet complete. No active fleet dispatches. Awaiting analysis phase.

## Coordination Notes for Future Phases

- **All subagents are Haiku**. Scope tasks to 1 focused item per agent. Pre-stage inputs locally.
- **Compact between phases**. Check in with user at each phase transition.
- **For foundational artifacts**: Match verification rigor to construction rigor (VDD review, per-item verification).
- **Coding-reference.md is key**. Any changes to accuracy standards flow through it.
- **Import verification**: Always check DB unclassified count after each wave. Run reconciliation at session boundaries.
- **Pre-flight checklist**: Test ALL evaluation criteria on 2-3 agents before scaling any fleet operation.
- **No important files in /tmp**. All methodology artifacts live in project directory; /tmp is for ephemeral batch I/O only.
