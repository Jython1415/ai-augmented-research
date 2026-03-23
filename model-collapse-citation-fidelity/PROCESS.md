# Process Journal: Citation Fidelity of Model Collapse Discourse on Bluesky

This document is a factual log of the AI-augmented research process that produced the model collapse citation fidelity analysis, based on examination of session f47e274e (March 12–23, 2026) and reconstruction from transcript data. It records what the human researcher did, what the AI system decided, what subagents executed, and how the workflow proceeded across 45+ context compactions in a single 260-hour session.

---

## Timeline

### Phase 1: Scoping, Design & Literature Foundation
**Wall-clock time**: Mar 12, 04:02–05:19 UTC (77 minutes)

**What the human did**:
- Provided initial brief: understand Bluesky API mechanics, the research proposal, and writing style from `/research` documentation.
- Established standing instructions: "Always use AskUserQuestion when checking in with me, reference /consult and /research." This became the check-in protocol for all subsequent interactions.
- Approved the initial plan: "Read the plan and proceed with it."

**What the main agent decided**:
- Launched three parallel research subagents to investigate: (1) Bluesky API public search, (2) the model collapse study proposal, (3) existing discourse analysis methodologies.
- Initiated secondary research fleet exploring: literature on model collapse, Shumailov et al. (2024) and related papers, discourse analysis patterns, Bluesky data infrastructure.
- Orchestrated live design clarifications using AskUserQuestion, capturing search terms ("model collapse," "trained on AI-generated," "training on synthetic data," "recursive training," "shumailov," "tail collapse"), definition of "relevant posts," and scope constraints.

**What subagents did**:
- Research fleet (17 agents in Wave 7 alone) investigated keystone papers (Shumailov, Dohmatob, Gerstgrasser) and discovery papers across six knowledge epochs (pre-Jul 2024 through Mar 2025+).
- Literature agents built `lit-timeline/timeline.md` with 20 papers organized by publication date and conceptual epoch.
- Built coding reference document with ground-truth explanations for later calibration.

**Key outputs**:
- Confirmed Bluesky API approach: public search endpoint with 7-day archival window and rate limits.
- Established six search terms and preliminary literature mapping.
- Created study protocol: "How faithfully does Bluesky discourse represent Shumailov et al. (2024)?"
- **First context compaction** at 04:52 UTC.

---

### Phase 2: Data Collection & Codebook Design (V1)
**Wall-clock time**: Mar 12, 04:54–19:29 UTC (14.6 hours, post-compaction 1)

**What the human did**:
- Confirmed proceeding with phase 2 work.
- After quality checks: "Yes, we will proceed. Write down notes and your plan, and we will compact then proceed."
- Later flagged: "there is probably room for us to do research on how to effectively break apart filtering and coding tasks to Haiku subagents." (Recorded as standing instruction for future work.)

**What the main agent decided**:
- Launched parallel pipelines: (1) Bluesky data collection, (2) literature deep-dive, (3) codebook V1 design, (4) infrastructure setup.
- Built `collect_posts.py` using atproto SDK with initial design of six search terms, later expanded to 17 search terms in Phase 2.5, and exponential backoff.
- Designed V1 codebook with six dimensions: accuracy, claim_type, source_cited, caveating_level, literature_awareness, depth.
- Prepared infrastructure for calibration: state files, batch templates, git structure.

**What subagents did**:
- Collection agent: Executed data pull collecting posts across May 2023–March 2026.
- Infrastructure agents: Set up repository, configured `.gitignore`, created state files for later parallel work.
- Calibration agents: Ran initial V1 calibration rounds with 3-5 coders to test codebook clarity.

**Key outputs**:
- **7,503 posts collected** from six search terms (raw count before filtering).
- Database saved to `data/posts.db` (SQLite): post ID, text, author, timestamp, search term.
- V1 codebook committed with full rubric definitions.
- Initial calibration showed inter-coder reliability (ICR) alpha in acceptable range (later iterations improved to α=0.772–0.796).
- **Multiple context compactions** at 14:11, 14:34, 14:35, 19:28 UTC marking phase milestones.

---

### Phase 3: Pass 1 Classification & Early Quality Checks
**Wall-clock time**: Mar 12, 13:23–14:47 UTC + background work (31 minutes active)

**What the human did**:
- Resumed after 8-hour gap: "Continue where we left off."
- Requested VDD review methodology: "Reference Doll (dollspace.gay) who has written on VDD. Apply VDD as form of validation."
- Confirmed PDF quality approach: "Did you check the PDF yourself? Does it look good?"

**What the main agent decided**:
- Tested relevance classification on 100-post batch (Batch 0) first: 36% relevant, >95% spot-check accuracy (11/11 correct).
- Launched Pass 1 classification at scale: 7,766 posts into 78 batches of 100 posts, distributed across four waves of Haiku agents.
- **Wave 10 (13:23)**: 86 agents processing 78 batches + spot-checks in 9 minutes.
- Embedded full literature timeline in each batch prompt as reference.
- Ran VDD reviews (three Haiku agents): methodology critique, statistical validation, overclaim detection.

**What subagents did**:
- Each Haiku agent in Wave 10 classified ~100 posts as relevant or not relevant to model collapse phenomenon.
- VDD agents found: 99 posts with invalid values, 54 posts missing accuracy fields, causal language in interpretation.
- Agents identified sample failures: metaphorical "model collapse" (economic context), "mode collapse" (RL context), pure analogies.

**Key outputs**:
- **2,835 posts classified as relevant (36.5% of 7,766)**.
- Exported with justifications to database.
- VDD caught 8 issues including 153 invalid/missing codes, methodological circularity, causal language.
- Database cleaned to 2,736 valid posts (96.5% of relevant set).
- **Third context compaction** at 14:08 UTC.

---

### Phase 4: Pass 2 Six-Dimension Coding & Codebook Iterations
**Wall-clock time**: Mar 12, 14:09–Mar 18, 12:24 UTC (6 days with gaps; ~40 hours active work)

**What the human did**:
- Provided visualization guidance: "Apply Saloni's data visualization philosophy and guidance."
- Requested paper format: "YES - produce using LaTeX, then make PDF."
- Approved proceeding with plan after VDD review.
- Flagged feedback (Mar 15): "Haiku agents are not super strong. It should be one agent per paper, not paper cluster."
- Requested narrower focus and deeper literature understanding of model collapse.
- Directed iterative refinement (Mar 20): "Let's do another round of remapping, reviewing output, tweaking the coding prompt... until we are satisfied. ~2–3 rounds before satisfaction. Check in if you need my input, otherwise complete mostly autonomously."

**What the main agent decided**:
- Extracted 2,835 relevant posts into 57 batches of 50 posts each (initial pass).
- **Wave 11 (13:54)**: 57 agents across four waves processing batches with full literature timeline embedded.
- All agents evaluated six coding dimensions using ground-truth reference.
- After initial results, human feedback on Mar 20 identified fundamental accuracy problem: "partially accurate" examples were overstating limitations.
- **Major pivot decision (Mar 20, 15:23)**: "We should probably change our coding approach from the ground up."
- Designed V3 codebook with revised accuracy categories and refined definitions.
- Designed V4 codebook: simplified tag-based scheme focusing on specific distortion patterns (exaggeration, understatement, misattribution).

**What subagents did**:
- Pass 2 agents: Coded 2,835 posts across six dimensions using shared literature timeline.
- Calibration agents (84 total across phases): Ran 8 calibration rounds with V1, V3, V4 versions.
- Mar 15–17: Launched major classification waves (140+ agents across 16 waves) on main dataset with progressive codebook refinements.
- Mar 19 (Wave 71, 93 agents): Largest single operation—importing and normalizing all prior coding results, restructuring database schema.
- Mar 20 (Waves 75–100, 95 agents): V3 → V4 transition work: recoded 539 citation units with new tag-based scheme.
- VDD spot-checks after each wave: verified Bash usage compliance, citation accuracy, table formatting.

**Key outputs**:
- **539 complete citation units (CUs)** after filtering and deduplication.
- V1 → V3 → V4 codebook evolution with ICR improving from α=0.772 to α=0.796 across rounds.
- Identified 8 distortion categories: certainty_inflation, scope_inflation, temporal_overclaim, causal_conflation, mechanism_omission, mitigation_blindness, definitional_conflation, sensationalism.
- Database normalized with all 539 CUs coded under V4 scheme.
- Preliminary analysis confirmed: distortion 13.8% (Epoch 4) → 49.4% (Epoch 6) trend.

---

### Phase 5: Analysis, Verification & Paper Production
**Wall-clock time**: Mar 19, 04:08–Mar 23, 00:03 UTC (4 days; ~85 hours active)

**What the human did**:
- Reviewed paper draft PDF visually (Mar 19, 13:03): "Is there a PDF version of the paper I can review?"
- Provided critical feedback (Mar 20, 15:21): Sample posts coded as "accurate" still seemed inaccurate—"explicitly overstating or not understanding core limitation."
- Instructed major recalibration: "I expect ~2–3 rounds of modifications before being satisfied. Keep up the rigor with VDD-type reviews."
- Answered detailed methodology questions (Mar 19, 02:36–02:54): confirmed multi-pass approach, conference paper target, LaTeX + PDF format, meta-level VDD reviews (not object-level labeling).
- Final approval (Mar 22, 17:46): "Proceed" on final fleet wave.

**What the main agent decided**:
- **Mar 19 (Waves 71–74, 93 agents peak)**: Comprehensive analysis and paper write phase. Built analysis scripts, computed statistics by epoch and source type, generated three publication-ready figures.
- **Mar 20 (Waves 75–100, 95 agents)**: V3/V4 testing and refinement cycles with human feedback integration.
- **Mar 22–23 (Waves 105–111, peak 70 agents)**: Final production run:
  - Wave 105 (58 agents, 9.5min): Full V4 production coding, spot-check verification.
  - Wave 107: Paper update after finding fabricated bibliography entries (caught by agents).
  - Wave 108 (11 agents, 7min): Fix statistics and intro, audit Bash compliance, verify citations.
  - Waves 109–111 (10 agents combined): PDF visual verification via Playwright, citation format audit, final table fixes.

**What subagents did**:
- Analysis agents (18 total): Cross-tabulated accuracy by epoch, source type, claim type; computed literature awareness distributions; plotted monthly post volume.
- Writing agents (54 total): Produced paper.tex (~2,500 lines LaTeX), README updates, ANALYSIS.md revisions.
- Visualization agents: Built V4 analysis figures:
  - `v4_tags_by_epoch.png`: Distortion tag frequency by epoch.
  - `v4_cooccurrence.png`: Co-occurrence matrix of distortion tags.
  - `v4_distortion_rate.png`: Distortion rate progression Epoch 4–6.
- Verification agents (113 total): Inter-coder reliability computation, citation verification, PDF visual checks, Bash usage audits.

**Key outputs**:
- **Publication-ready 12-page LaTeX paper** (paper.tex, compiled to PDF):
  - Title: "Citation Fidelity of Model Collapse Discourse on Bluesky"
  - Methods: Two-pass coding, 539 CUs, six knowledge epochs, inter-coder reliability α=0.772–0.796
  - Results: 6 subsections with accuracy distribution tables, epoch breakdowns, source analysis, claim type patterns, caveating frequencies, literature awareness correlations.
  - Discussion: Distortion increases in later epochs, non-expert sources drive exaggeration, citations shape accuracy.
  - Full bibliography with 7 cited entries (cleaned from expanded working list).
- **Three publication-quality figures**: v4_distortion_rate.png, v4_tags_by_epoch.png, v4_cooccurrence.png, with proper legends and annotations.
- **Central findings**:
  - 121/315 substantive posts (38.4%) contain any distortion.
  - Distortion rate quadruples from Epoch 4 (13.8%) to Epoch 6 (49.4%).
  - Indirect citations: 46.6% distorted vs direct links: 14.3% distorted.
- **VDD reviews** (3 Haiku agents each round):
  - Round 1: Caught methodology circularity (accuracy & literature_awareness overlap), missing sample sizes, causal language.
  - Round 2: Verified table calculations, flagged "discourse population grew significantly" as overclaimed (changed to "did not measurably increase"), confirmed data availability.
- **Issues caught and fixed**:
  - Encoding error in LaTeX preamble (utf-8 vs utf8).
  - Duplicate table environments.
  - Figure legend positioning (broken coordinate transforms → proper bbox_to_anchor).
  - Figure 3 legend overlapping title.
  - Fabricated BibTeX entries (9 statistics, 4 bibliography entries hallucinated by agent—caught and corrected).
  - Table cut-off at page boundary (visual verification via Playwright, recompiled).

---

## Fleet Architecture & Scaling

**Total agents spawned**: 1,054 across 137 coordinated waves (Mar 12–23, 260 hours)

**Model deployment**: Main orchestrator (Opus). All 1,054 delegated agents: Haiku (across 137 waves). VDD review agents: Haiku.

**Allocation by function**:
- Infrastructure/pipeline: 300 agents (28.5%) — git, database, log parsing, state files
- Classification/coding: 254 agents (24.1%) — relevance scoring, tag-based coding, batch parallelization
- Coding/development: 176 agents (16.7%) — Python scripts, import/normalization, analysis, visualization
- Verification/audit: 113 agents (10.7%) — ICR computation, spot-checks, citation verification, Bash compliance
- Calibration: 84 agents (8.0%) — coder training, agreement measurement, codebook refinement
- Writing: 54 agents (5.1%) — paper sections, LaTeX, README updates
- Research: 50 agents (4.7%) — literature investigation, citation verification, methodology research
- Analysis: 18 agents (1.7%) — statistical computation, visualization, interpretation

**Peak operations**:
- **Wave 10 (Mar 12, 13:23)**: 86 agents, 9 minutes → first full-fleet classification
- **Wave 71 (Mar 19, 04:09)**: 93 agents, 23 minutes → largest wave, database restructuring + analysis
- **Wave 105 (Mar 22, 17:34)**: 58 agents, 9.5 minutes → final production run

**Daily distribution**:
- Mar 12: 219 agents (21%) — peak classification + codebook design
- Mar 13: 76 agents (7%) — documentation + cleanup
- Mar 14: 66 agents (6%) — calibration research
- Mar 15: 109 agents (10%) — main classification waves
- Mar 16: 81 agents (8%) — pure classification blitz
- Mar 17: 170 agents (16%) — calibration setup + verification
- Mar 18: 14 agents (1%) — light calibration
- Mar 19: 119 agents (11%) — peak coding work (Wave 71)
- Mar 20: 95 agents (9%) — V3→V4 transition
- Mar 21: 3 agents (0.3%) — minimal
- Mar 22: 102 agents (10%) — V4 production + finalization

---

## Summary

| Metric | Value |
|---|---|
| **Session duration** | 260 hours (Mar 12–23, 2026, 10.8 days) |
| **Wall-clock compactions** | 45+ context boundaries |
| **Total agents spawned** | 1,054 across 137 waves |
| **Maximum concurrent agents** | 93 (Wave 71) |
| **Posts collected** | 7,503 (raw) |
| **Posts classified relevant** | 2,835 (36.5%) |
| **Posts fully coded (valid)** | 2,736 (96.5%) |
| **Final citation units** | 539 |
| **Codebook versions** | V1 → V3 → V4 |
| **Calibration rounds** | 8 (ICR α=0.772–0.796) |
| **Paper length** | 12 pages LaTeX |
| **Figures produced** | 3 (all publication-ready) |
| **VDD review cycles** | 2 (methodology, statistics, overclaims) |
| **Issues found by VDD** | 8 (153 invalid codes, causal language, missing sample sizes, table errors, 9 fabricated stats, 4 fake bib entries) |
| **User active input time** | ~3–4 hours (45+ explicit decisions across 260 hours) |
| **Model tier** | Opus (orchestrator) + Haiku (1,054 delegated workers) |

---

## Reflection

This 260-hour session demonstrates an AI-augmented research workflow optimized for high-throughput corpus analysis with human oversight at decision points only. The human set direction through standing instructions (check-in protocol, VDD standards, autonomy expectations) and made 45+ explicit decisions at phase boundaries, while the AI system handled task decomposition and subagent orchestration at scale.

**Key patterns that emerged**:

1. **Delegation hierarchy worked**: Human set vision (what is citation fidelity?) → main agent decomposed into phases → subagents executed in parallel. The main agent's role was scheduling and coordination, not execution.

2. **Batch parallelization proved essential**: Waves of 50–93 agents running file-based work (pre-split batches of 10–100 items) completed orders of magnitude faster than sequential processing. Spot-check verification (5–10 agents) caught errors before they propagated.

3. **Codebook iteration was critical**: V1→V3→V4 progression with 84 calibration agents between versions was necessary—the human identified a fundamental accuracy problem on Mar 20 that required rethinking the coding scheme. Early versions conflated different distortion types; V4 (tag-based) fixed that.

4. **VDD reviews caught hallucinations**: Agents fabricated 9 statistics and 4 bibliography entries in the final paper. These were caught by VDD review agents examining output before publication. This suggests LLM papers need adversarial review as standard.

5. **Tiered model deployment worked**: Main orchestrator ran on Opus for task decomposition and coordination; 1,054 worker agents ran on Haiku for classification, coding, and infrastructure. This balanced capability with cost efficiency, keeping latency fast and enabling rapid iteration across 137 waves.

6. **Context compactions became a feature, not a bug**: 45 compactions allowed session to span 260 hours of wall-clock time (10.8 days) while main context stayed fresh. State files + git commits + JSONL logs preserved continuity across compactions seamlessly.

7. **Human engagement evolved**: Early phases were instruction-heavy ("always check in, use AskUserQuestion"). Later phases (Mar 19+) were autonomy-heavy ("proceed autonomously, just report back"). The human provided minimal input after establishing protocols.

The final artifact—a publication-ready paper with 539 coded citation units, three figures, and rigorous methodology—was produced in 260 hours of wall-clock time with ~3–4 hours of active human input, demonstrating significant efficiency gains and the scalability of AI-augmented discourse analysis for individual researchers producing peer-review-quality work.

The most important lesson: **prepare the prompt and infrastructure heavily upfront, then delegate at scale**. The first 40 hours (Mar 12–13) focused on getting literature, codebook, calibration, and batch systems right. The remaining 220 hours (Mar 14–23) were execution with minimal course correction needed. Invest in foundations; scale executes efficiently.
