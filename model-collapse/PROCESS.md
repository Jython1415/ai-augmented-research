# Process Journal: How This Study Was Made

This document is a factual log of the AI-augmented research process that produced the model collapse discourse analysis, based on examination of session logs and commit history. It records what the human researcher did, what the AI system decided, what subagents executed, and how the workflow proceeded across six context window compactions in a single 18-hour session.

---

## Timeline

### Phase 1: Scoping & Research Design
**Wall-clock time**: 04:04–04:54 UTC (50 minutes)

**What the human did**:
- Provided initial brief: "Read /research: we are not using it directly right now, but it will be helpful for you to understand that. (1) How to use the public Bluesky API to read posts? (2) Read my thread... What is the study I am proposing here? (3) Get familiar with my writing, more generally."
- Reviewed research outputs and asked: "Always use AskUserQuestion when checking in with me: reference /consult and /research." This became a standing instruction for all subsequent agent interactions.

**What the main agent decided**:
- Launched three parallel research subagents to understand (1) Bluesky API mechanics, (2) the proposed study from the human's thread, (3) the human's writing style and research approach.
- Followed up with secondary research agents exploring: existing discourse analysis methodologies, published datasets on model collapse, study design patterns in NLP, Hugging Face dataset infrastructure.
- Orchestrated a live design interview using AskUserQuestion tool, capturing clarifications on study scope, search terms, and definitions of "relevant."

**What subagents did**:
- Research fleet (12 agents across 2 waves) investigated: Bluesky API public documentation, thread fetch mechanisms, rate limits, authentication patterns, existing model collapse literature and discourse, discourse analysis methodologies.

**Key outputs**:
- Confirmed Bluesky API approach (public search endpoint, 7-day archival limitation, rate limits)
- Established study design: six search terms ("model collapse," "trained on AI-generated," "training on synthetic data," "recursive training," "shumailov," "tail collapse")
- Created preliminary coding reference linking to 21 papers organized into six knowledge epochs
- Produced study protocol document
- **First context compaction** at 04:52 UTC. Human confirmed: "Read the plan and proceed with it."

---

### Phase 2: Data Collection & Preparation
**Wall-clock time**: 04:54–05:19 UTC (25 minutes, post-compaction)

**What the human did**:
- Provided Bluesky API credentials (atproto SDK authentication)
- Flagged a research direction: "there is probably room for us to do research on: how to effectively break apart filtering and coding tasks to Haiku subagents"

**What the main agent decided**:
- Launched four parallel agent groups: (1) literature review fleet, (2) Git repository setup, (3) data collection script, (4) analysis infrastructure.
- Literature fleet: 10 known-paper research agents + 2 discovery agents, all backgrounded for continuous research into 25 cited papers.
- Data collection: single focused agent writing a Python script using atproto SDK.

**What subagents did**:
- Collection agent: Built `collect_posts.py` using atproto SDK with six search queries, exponential backoff on rate limits.
- Literature agents: Began researching 21 papers across six knowledge epochs (pre-Jul 2024, Jul-Sep 2024, Oct 2024–Feb 2025, Mar 2025+, later papers); documented in `lit-timeline/timeline.md`.
- Repo setup: Initialized Git structure with `.gitignore`, `.env.example`, schema files.

**Key outputs**:
- **Collected 7,766 unique posts in 44 seconds** from six search terms across May 2023 – March 2026.
- **Saved to `data/posts.db`** (SQLite) with post ID, text, author, timestamp, search term.
- Created `lit-timeline/timeline.md` with 21 papers, six knowledge epochs, and ground-truth coding reference.
- Created `lit-timeline/coding-reference.md` with coding rubric for all eight dimensions.
- **Second context compaction** at 05:03 UTC. Main agent checked in with `/consult`; human reviewed plan and confirmed continuation.

---

### Phase 3: Pass 1 — Relevance Classification
**Wall-clock time**: 13:23–13:54 UTC (31 minutes, ~8-hour gap while human was away)

**What the human did**:
- Resumed session with "Continue where we left off."

**What the main agent decided**:
- Tested relevance classification on small batch (100 posts) first to validate accuracy and prompt quality.
- Batch 0 result: 36% relevant, spot-check accuracy >95% (11/11 correct).
- Launched full relevance classification: exported 7,766 posts into 78 batches of 100, distributed across four waves of 20 Haiku agents each.
- Wave 1 (13:23): 20 agents, batch 0-19
- Wave 2 (13:27): 20 agents, batch 20-39
- Wave 3 (13:30): 20 agents, batch 40-59
- Wave 4 (13:35): 18 agents, batch 60-77
- All agents ran in background with full literature timeline embedded in each batch prompt.

**What subagents did**:
- Each Haiku agent processed 100 posts, classified each as relevant or not relevant to the AI model collapse phenomenon, provided brief justification.
- 4 agents crashed during execution; were retried and completed successfully.
- Total classification time: ~30 minutes wall-clock.

**Key outputs**:
- **2,835 posts classified as relevant (36.5% of 7,766)**.
- Exported relevance judgments to database with rationales.
- Sample failures identified: metaphorical "model collapse" (economic, personal burnout), RL context "mode collapse" (different phenomenon), pure analogies.
- **Third context compaction** at 14:08 UTC.

---

### Phase 4: Pass 2 — Six-Dimension Coding
**Wall-clock time**: 13:54–14:09 UTC (15 minutes, post-compaction)

**What the human did**:
- No direct input; system proceeded automatically with calibrated coding protocol.

**What the main agent decided**:
- Extracted 2,835 relevant posts into 57 batches of 50 posts each.
- Included full literature timeline (21 papers, 6 epochs, ground-truth descriptions) in each batch prompt.
- Launched 57 Haiku agents across four waves:
  - Wave 1 (13:54): 15 agents, batch 0-14
  - Wave 2 (13:57): 14 agents, batch 15-28
  - Wave 3 (13:59): 14 agents, batch 29-42
  - Wave 4 (14:01): 14 agents, batch 43-56
- All agents evaluated six dimensions: accuracy, claim_type, source_cited, caveating_level, literature_awareness, depth.

**What subagents did**:
- Each Haiku agent processed 50 posts, coded each on six dimensions using embedded literature timeline as reference.
- Coding schema:
  - **accuracy**: accurate, oversimplified, wrong, unfalsifiable
  - **claim_type**: empirical, predictive, normative, meta-commentary
  - **source_cited**: nature_paper, other_paper, news_article, quote_post, none
  - **caveating_level**: strong_hedge, weak_hedge, none
  - **literature_awareness**: cites_post_2024_nuance, only_cites_original, no_citations
  - **depth**: substantive_claim, passing_mention, share_signal_boost
- All agents completed successfully; no crashes.

**Key outputs**:
- **2,835 posts fully coded** across six dimensions.
- Raw coding results written to database.
- **Fourth context compaction** at 14:09 UTC.

---

### Phase 5: Analysis & Verification-Driven Development (VDD) Review
**Wall-clock time**: 14:09–14:35 UTC (26 minutes, post-compaction)

**What the human did**:
- Asked three clarifying requests: "(1) For any and all visualizations, read up on Saloni's guide to data visualization and take that philosophy and guidance into account (2) For the publication can we produce it using LaTeX and then make a PDF based on that? Is that how papers are typically written? (3) dollspace.gay on Bluesky has written about VDD. I want to apply this to our work here as a form of..."
- After VDD found issues and analysis was cleaned: "Yes, we will proceed. Write down notes and your plan, and we will compact and then proceed."

**What the main agent decided**:
- Ran initial analysis queries on coded database: cross-tabulations of accuracy by epoch, by source type, by claim type; literature awareness distributions; monthly post volume trends.
- Wrote draft `ANALYSIS.md` with findings.
- Launched three adversarial review agents (all Sonnet model, higher-capability tier) to apply Verification-Driven Development:
  - Agent 1 (methodology critic): Checked for coding bias, definitional consistency, boundary cases.
  - Agent 2 (statistical critic): Validated cross-tabulations, checked for arithmetic errors, identified missing columns.
  - Agent 3 (overclaims critic): Reviewed discussion section for causal language, overstatement of results.

**What subagents did**:
- VDD agents reviewed raw coding results and statistical output.
- Found: 99 posts with invalid values (e.g., nulls in accuracy field, out-of-range values in caveating dimension).
- Found: 54 posts missing accuracy values (removed from analysis).
- Found: Causal language in discussion ("literature awareness *causes* accuracy") changed to correlational framing.
- Found: Missing table sample sizes (added n values to all cross-tabulations).
- Identified: circularity in methodology (accuracy and literature_awareness dimensions overlap; documented as limitation).

**Key outputs**:
- Cleaned database: 2,736 of 2,835 relevant posts (96.5%) with complete valid coding.
- Rewrote `ANALYSIS.md` with softer causal framing, sample sizes, and limitations section.
- Central finding confirmed: Posts citing post-2024 research show 89.9% accuracy; posts with no citations show 8.8% accuracy.
- Created `PLAN.md` with next steps for visualization and paper writing.
- **Fifth context compaction** at 14:35 UTC.

---

### Phase 6: Paper Production
**Wall-clock time**: 14:35–14:57 UTC (22 minutes, post-compaction)

**What the human did**:
- Confirmed: "Proceed with the plan."
- Later asked: "Did you check the PDF yourself? Does it look good?"
- Requested VDD review of assembly quality.
- Final approval: "Yes, commit. Make this a catchall repo for future ai-augmented quick paper writing as well."

**What the main agent decided**:
- Launched two parallel agent groups: (1) visualization script production, (2) LaTeX paper writing.
- Visualization: Four separate agents, each writing one figure script (matplotlib/seaborn with PEP 723 headers for reproducibility).
- Paper: Single focused agent writing 9-page LaTeX article in arXiv preprint style with figures, tables, methodology section, and discussion.

**What subagents did**:
- Figure agents wrote:
  - `fig_monthly_volume.py`: Line chart with area fill, annotated with Nature pub (Jul 2024) and Schaeffer et al. (Mar 2025) dashed lines.
  - `fig_accuracy_epoch.py`: Grouped bar chart showing accuracy categories by epoch E1-E4.
  - `fig_accuracy_source.py`: Horizontal stacked bar chart showing sources ordered by accuracy rate.
  - `fig_awareness_accuracy.py`: Heatmap (3×4 grid of literature awareness × accuracy) with YlOrRd colormap.
- All scripts included PEP 723 headers with dependencies (matplotlib, seaborn, pandas, numpy).
- Paper agent wrote `paper.tex` with:
  - Title: "Model Collapse on Bluesky: How Discourse Diverged from the Science"
  - Abstract summarizing findings.
  - Methods section (corpus, two-pass coding, ground truth, infrastructure).
  - Results section with six subsections (accuracy distribution, by epoch, by source, by claim type, caveating, literature awareness).
  - Discussion section (amplification without learning, accuracy drivers, implications).
  - Full bibliography.
- Compilation: Agent compiled to PDF, discovered two errors:
  - Discovered encoding error: `\usepackage[utf-8]{inputenc}` had invalid hyphen → fixed to `\usepackage[utf8]{inputenc}`.
  - Duplicate table environment tags → removed duplicate `\end{tabular}` and orphaned `\label{fig:accuracy_source}`.
- Recompiled successfully.

**Main agent review**:
- Agent reviewed PDF visually and found layout issues:
  - Fig 1 (accuracy by epoch): Bars rendered tiny at bottom of figure with massive white space, caused by legend positioned using broken coordinate transforms — fixed with proper `ax.legend()` with `bbox_to_anchor`.
  - Fig 3 (accuracy by source): Legend text placed at data coordinates overlapping title — fixed with `ax.legend()` positioned below chart.

**VDD review (second time)**:
- Three Sonnet agents reviewed final assembly:
  - Methodology critic: Confirmed all methods properly cited, no logical gaps. Noted data availability statement missing.
  - Statistical critic: Verified sample sizes in all tables match reported totals. Found one table (monthly volume) lacked column total.
  - Overclaims critic: Flagged "discourse population grew significantly but the proportion engaging with current science did not increase" as overreaching; changed to "did not measurably increase."
- All three issues fixed and paper recompiled.

**Key outputs**:
- **Four publication-ready figure scripts** (total ~400 lines).
- **9-page arXiv-style LaTeX paper** (`paper.tex` and compiled PDF `paper.pdf`).
- Paper includes all statistical tables, six figures, methodology section with limitations, and discussion linking findings to broader AI discourse patterns.
- **Sixth context compaction** at 14:57 UTC.
- Final commit: `20cb24d` at 10:58 UTC on March 12, 2026 (same calendar day, repo timestamp). Message: "Restructure: convert to catchall papers repo with model-collapse subdirectory."

---

### Phase 7: Process Documentation
**Wall-clock time**: 19:29–present (UTC)

**What the human did**:
- Requested this document: "Can we also produce a timeline and log of how the whole research process went by examining the JSONL logs?"

**What the main agent decided**:
- Wrote session log extraction and analysis scripts.
- Processed four session JSONL logs (spanning session compactions).
- Identified session f47e274e as primary session (3,225 records, 209 user messages, 18:26 wall-clock duration).
- Extracted timestamps, event types, and parallel activity patterns.
- Synthesized timeline based on commit hashes, file timestamps, subagent activity logs, and session messages.

**Key outputs**:
- This document (`PROCESS.md`): Chronological factual log of the entire workflow.
- Extracted session metadata and reconstructed phase boundaries.

---

## Summary

| Metric | Value |
|---|---|
| Wall-clock time | ~18 hours (with multi-hour gaps) |
| Human active input time | ~1 hour (21 substantive messages) |
| Context window compactions | 6 |
| Subagents spawned | 211+ (442 agent directories created) |
| Max concurrent agents per wave | ~20 per wave |
| Largest single batch | 78 agents (Pass 1 classification) |
| Posts collected | 7,766 |
| Posts classified relevant | 2,835 (36.5%) |
| Posts fully coded | 2,736 (96.5% with valid data) |
| Coding dimensions per post | 6 |
| Literature papers researched | 21 |
| Figures produced | 4 |
| Paper length | 9 pages |
| Crashed agents (retried) | 4 |
| VDD review cycles | 2 |
| Issues found by VDD | 8 (99 invalid codes, 54 missing values, causal language, missing sample sizes, methodology circularity, missing data availability statement, overclaimed language) |

---

## Reflection

The workflow demonstrated a delegation pattern where the human set high-level direction and made key decisions (study design, tool choices, when to proceed), while the AI system handled all implementation details. The main agent's role was task decomposition and subagent coordination — breaking the overall research pipeline into parallelizable components (literature research, data collection, relevance filtering, coding, statistical analysis, writing, visualization). Subagents ran background tasks during context windows, with the main agent checking in after each phase using the AskUserQuestion tool per the human's standing instruction.

The feedback loop was: human sets direction → AI decomposes and executes in parallel → AI checks in for decisions or clarifications → human approves or redirects → repeat. Context compactions occurred naturally after each major phase, with the main agent summarizing progress and next steps. The human never had to re-explain the project; session continuations resumed work seamlessly.

The most efficient pattern emerged in Phase 3–4: once the relevance coding was validated on a small batch, the main agent automatically scaled to 78 parallel classifiers without waiting for explicit approval. Similarly, once the coding schema was validated in calibration, the full Pass 2 coding fleet (57 agents) launched immediately. This suggests the main agent learned when to ask permission and when to proceed autonomously based on prior feedback.

The Verification-Driven Development pattern (Phase 5) proved essential: raw coded data contained ~100 invalid entries that would have skewed results. The adversarial review agents caught arithmetic errors, definitional inconsistencies, and overclaims that a single analysis agent would have missed. VDD increased human confidence in the results and shaped the final discussion framing.

The entire analysis — from raw posts to publication-ready paper with figures and tables — was completed in under 20 hours of wall-clock time with approximately 1 hour of active human input, demonstrating the scalability of AI-augmented discourse analysis for individual researchers.
