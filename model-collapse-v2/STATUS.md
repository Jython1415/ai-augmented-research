# Study Status

## Current Phase: Phase 5 IN PROGRESS → Ralph Loop

### Ralph Loop Configuration
- Prompt: RALPH_PROMPT.md
- Max iterations: 75
- Completion promise: RESEARCH_COMPLETE
- Scope: Full remaining project (infrastructure → coding → analysis → paper)

### v4 Re-Run (2026-03-17)

Full v4 re-run of all 7,338 non-auto-accepted posts with improved classification prompt. All 7,503 posts now classified.

**Why v4 re-run:** The v3 classification had a 32% false positive rate (207/640 flagged by verification). Root cause: Haiku treated concept descriptions ("discusses model collapse") as citation signals. v4 fixes this with 3 structural improvements:
1. **Decision tree** — sequential steps replacing declarative criteria
2. **citation_signal chain-of-thought** — must identify specific URL/author/DOI BEFORE deciding relevance
3. **Hard negative few-shot examples** — 5 posts that perfectly describe model collapse but have no citation

**v4 execution:**
- 74 batches in 15 waves (5 agents/wave) + 1 gap-fill batch (106 posts from 4 incomplete batches)
- All batches complete, all posts classified
- Found 8 batch result files from earlier waves that were never imported (discovered via reconciliation at end)
- Gap-fill pattern: re-stage unclassified posts from incomplete batches 010, 012, 032, 040

### Verification Pass (2026-03-17)

446 non-auto-accepted relevant posts verified across 9 batches (50 posts each), 2 test + 7 scaled.

**Raw verification results:** 128 posts flagged as potential false positives (28.7%)

**Reconciliation:** Many flags were verification design artifacts, not true FPs:
- Verification agents only saw post text, not parent_text/quoted_text → reply/quote context posts incorrectly flagged
- Verification used a fixed domain list → legitimate model collapse articles from unlisted domains flagged
- Manual review of all 128 flagged posts → 29 confirmed false positives

**29 confirmed false positives by category:**
- 17 linked to different arxiv papers (not Shumailov's 2305.17493)
- 6 were about different topics entirely (Tailwind business model, OpenAI pricing, brain-AI alignment, JAMA medical, Substack business, LLM bubble)
- 6 had only concept descriptions without any traceable citation signal

**Policy decisions made during verification:**
- Articles from unlisted domains (FT, Forbes, NPR, The Guardian, etc.) ARE relevant if about model collapse from AI training on AI data — the verified domain list is a helper, not exhaustive
- Link card posts (headline without visible URL) count as citation signals — the shared article IS the signal
- YouTube videos about model collapse (ShusuVq32hc "Curse of Recursion") count as citation signals
- Posts sharing articles from our "Excluded" list (fastcompany Grok article, tomshardware ChatGPT article) ARE false positives — these articles aren't about Shumailov
- Vague references like "the first paper about the technology" without identifying Nature/Shumailov are NOT citation signals

### Final Classification Results (post-verification)
| Metric | Count | % |
|--------|-------|---|
| Total | 7,503 | 100% |
| Relevant | 581 | 7.7% |
| Not relevant | 6,922 | 92.3% |
| Auto-accepted (subset of relevant) | 164 | 2.2% |
| Verified non-auto-accepted | 417 | 5.6% |
| Unclassified | 0 | 0% |

**v4 false positive rate:** 29/610 = 4.8% (dramatically improved from v3's 32%)

### Next Steps (in order)
1. ~~**Build citation units**~~ ✓ Done — 581 units
2. ~~**Fetch full thread context**~~ ✓ Done — 691 context posts
3. **Fetch author profiles** (Step 7) — script TBD, can be done in parallel with Phase 5
4. **Begin Phase 5** — Coding scheme design and calibration ← PRIMARY NEXT STEP

### Critical Learnings for Fleet Ops
- v4 decision tree + citation_signal field dramatically reduced false positives vs v3
- Haiku Bash violations: ~25-33% rate even with prompt bans. Contextual WHY explanation helps but doesn't eliminate.
- **Import verification is critical**: Always check DB unclassified count after each wave import. Run reconciliation at session boundaries.
- Gap-fill pattern: re-stage unclassified posts into single batch, run as final cleanup
- 15 waves + gap-fill = 76 agents total. Stable quality after initial prompt refinement.

**Blockers**: None

### Verification Learnings for Future Fleet Ops
- Verification agents need ALL context the classifier had — include parent_text/quoted_text in verification batches
- Domain verification lists should be treated as helpers, not exhaustive — check article topic, not just domain
- 3-category triage (confirmed FP / reinstate / manual review) is efficient for reconciling verification disagreements
- v4 FP rate of 4.8% vs v3's 32% validates the decision tree + citation_signal approach

## Plan

### Phase 1: Design & Alignment ✓ COMPLETE
- [x] Initial literature review (28 papers identified)
- [x] Research thread context strategies (Bluesky API capabilities confirmed)
- [x] Research session coordination patterns
- [x] Define research question and unit of analysis
- [x] Define context inclusion rules (two-pass design)
- [x] Define inter-coder reliability approach (Krippendorff's α + human check)
- [x] Define Haiku prompt structure (XML-tagged, rubric → examples → content)
- [x] Define session state management (STATUS.md + DECISIONS.md)
- [x] Align on coordination pattern (front-loaded, then execute)

### Phase 4: Literature Ground-Truth Timeline ✓ COMPLETE
- [x] Fresh build from scratch (15 verified papers across 6 knowledge epochs)
- [x] Temporal map: what was accurate understanding at time T?
- [x] Structure as knowledge epochs with pivot points
- [x] All 15 paper entries verified against arXiv abstracts (11 factual corrections applied)
- [x] 4 previously-unverified papers found and confirmed with arXiv IDs
- [x] VDD critical review of epoch boundaries and accuracy standards (3 critical issues resolved)
- [x] Build coding-reference.md for subagent prompts (83 lines)
- [x] Two accuracy dimensions baked in: paper fidelity + field state
- [x] Re-verification pass on corrected entries (5/5 passed)
- [x] Coding reference reviewed and 1 claim rating corrected
- Files: lit-timeline/timeline.md, lit-timeline/coding-reference.md, lit-timeline/verified-abstracts.md

### Phase 2: Search Term Discovery & Mini-Experiments ✓ COMPLETE
- [x] Start with obvious terms — tested 8 initial + 12 additional candidate terms across 3 experiment rounds
- [x] Run mini-experiments: signal-to-noise ratio per term — 9 final terms selected (3 tiers)
- [x] Analyze found posts for language patterns → extract new candidate terms — language patterns analyzed, informal terms too noisy
- [x] Test second-order citation collection (quote posts) — thread context fetching tested and working
- [x] Iterate until coverage estimate is satisfactory — 5,649 posts collected, ~57% relevance estimated
- [x] End-to-end pipeline test on small sample — 44-post sample manually assessed

### Phase 2.5: Deeper Search Term Discovery ✓ COMPLETE
- [x] Analyze language patterns in collected relevant posts for non-obvious search terms
- [x] Investigate coverage gaps: communities/vocabularies we may be missing
- [x] Test media coverage terms, quote post chains, cross-language patterns
- [x] Add any new terms and re-collect
- [x] Verify coverage improvement before proceeding to Phase 3

### Phase 3: Data Collection & Relevance Filtering — v4 CLASSIFICATION COMPLETE

#### v4 Classification ✓ COMPLETE
- [x] Researched Haiku prompt engineering (Anthropic docs, classification guides)
- [x] Built v4 prompt with decision tree + citation_signal CoT + hard negative examples
- [x] Fixed domain over-matching in Step 1b (split into Step 1 + Step 1b with topic check)
- [x] Pre-flight checklist: 5 criteria verified on test agents
- [x] Fleet run: 74 batches in 15 waves + gap-fill batch
- [x] All 7,503 posts classified (610 relevant, 6,893 not relevant)
- [x] Reconciliation: found and imported 8 batch files missed in earlier waves

#### Verification ✓ COMPLETE
- [x] Run verification agents on 446 non-auto-accepted relevant posts (9 batches)
- [x] Check: citation_signal is actual URL/author (not concept description)
- [x] Check: linked paper is Shumailov et al. (not a different paper)
- [x] Policy decision: platformer.news / Wired.com / unlisted domains → relevant if about model collapse topic
- [x] Update DB with verification results (29 false positives flipped to not relevant)
- [x] Final totals: 581 relevant (7.7%)

#### Remaining Phase 3 Steps
- [x] Build citation units (Step 5): 581 units created (36 link, 60 author_name, 152 title_phrase, 333 indirect)
- [x] Fetch full thread context (Step 6): 691 context posts for 263/581 units (45% have context; 318 standalone)
  - 377 parent posts, 232 reply children, 82 self-replies
- [ ] Fetch author profiles (Step 7): script ready, deferred pending dependency fix

### Phase 5: Coding — Pass 1 COMPLETE, Pass 2 COMPLETE
- [x] Design tight coding scheme (3 dimensions: claim_strength, paper_fidelity, field_accuracy)
- [x] Build examples iteratively (10 worked examples in codebook)
- [x] Calibration: 8 rounds with 3 independent Haiku agents on 50-post sample
- [x] Krippendorff's α achieved: claim_strength=0.888, paper_fidelity=0.762, field_accuracy=0.816
- [x] VDD review of codebook (contradictions found and fixed)
- [x] Shumailov false positive cleanup (42 removed, 539 CUs final)
- [x] Build production infrastructure (staging, import, pass 2 codebook, author profiles)
- [x] Fleet coding Pass 1 (post-only, 539 CUs) — COMPLETE
- [x] Fleet coding Pass 2 (with-context, 539 CUs) — COMPLETE (all 539 coded)
- [x] Fetch author profiles (445/445 from Bluesky API) — COMPLETE

### Phase E: Analysis ✓ COMPLETE
- [x] Statistical analysis (citation fidelity over time, epoch trends)
- [x] Demographics analysis (bio roles, reach, repeat citers)
- [x] Two-pass comparison (context effect on coding, κ=0.51-0.70)
- [x] Figure generation (3 figures: epoch trends, two-pass comparison, author followers)
- [x] VDD review of analysis (methodology sound, epoch trend caveat-worthy, missing effect sizes)

### Phase F: Paper Writing ✓ COMPLETE
- [x] Draft paper outline
- [x] Write methods section
- [x] Write results section (with figures)
- [x] Write discussion (interpret epoch trend, explain context drift)
- [x] Write conclusion
- [x] LaTeX validation (braces, citations, environments)
- [x] Content validation (spot-check statistics against data)
- [x] All figures referenced and valid

## File-Level Artifacts
- data/init_db.py — Database initialization (7 tables)
- data/collect_posts.py — Bluesky post collection (experiment + full modes)
- data/export_sample.py — Stratified sample export for testing
- data/fetch_thread_context.py — Thread context fetching from Bluesky API (deep context for coding)
- data/test_new_terms.py — Search term candidate testing script (Phase 2.5)
- data/filter_relevance.py — Haiku-powered relevance filtering (10 posts/batch, auto-accept Tier 1)
- data/build_citation_units.py — Creates citation_units from relevant posts with citation_type classification
- data/posts.db — SQLite database with 7,503 collected posts
- .env — Bluesky credentials (gitignored)
- .gitignore — Excludes .env and posts.db
- data/fetch_post_context.py — Lightweight context fetcher (parent + quote text for classification)
- data/test_batch_tokens.py — Token count validator for batch files
- data/stage_relevance_batches.py — Stages batches WITH context (parent_text and quoted_text)
- data/import_relevance_results.py — Idempotent import (WAL, --file, skip-classified)
- lit-timeline/terminology-landscape.md — Broader terminology landscape (what study is NOT about)
- lit-timeline/news-coverage-urls.md — Verified news coverage URLs (citation signals for classifiers)
- papers/ — Downloaded PDFs of all 17 referenced papers
- prompts/ — All classification/verification instruction files (v1, v2, v4) + FLEET_PROTOCOL.md
- audit/ — Audit reports, classification agent audits
- audit/verification/ — v4 verification batch results + apply script
- audit/icr/ — ICR scripts, samples, and coder results (reusable for Phase 5)

## Subagent Fleet Status
No active fleet dispatches. v4 classification and verification complete.

### DB State Summary (post-verification)
- posts: 7,503 (581 relevant, 6,922 not relevant, 0 unclassified)
- citation_units: 539 (36 link, 60 author_name, 152 title_phrase, 333 indirect)
- thread_context: 671 posts across 263 citation units (318 standalone)

## Codebook V3 Revision (2026-03-20)
- V3 codebook applied: stricter paper_fidelity boundaries
- ICR calibration round 1: α = 0.775/0.685/0.729 (all tentative)
- Need 1 more calibration round before full re-code
- After re-code: re-run all analysis scripts and update paper

## Coordination Notes for Future Phases
- All subagents are Haiku (haiku-enforce plugin). Scope tasks to 1 focused item per agent. Pre-stage inputs locally.
- Compact between phases. Check in with user at each phase transition.
- For foundational artifacts: match verification rigor to construction rigor (VDD review, per-item verification).
- The coding-reference.md is the key artifact for Phase 5 (coding). Any changes to accuracy standards must flow through it.
- Classification uses Claude Code Haiku subagents, NOT Anthropic API (user constraint: no separate API billing)
- **Import verification**: Always check DB unclassified count after each wave. Run reconciliation at session boundaries.
- **Pre-flight checklist**: Test ALL evaluation criteria on 2-3 agents before scaling any fleet operation.
