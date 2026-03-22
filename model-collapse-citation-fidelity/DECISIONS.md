# Decision Log

Append-only record of study design decisions and user input. Prevents re-asking settled questions across compaction events.

---

## 2026-03-13: Study Scope

**Decision**: New paper focused specifically on Bluesky posts that cite Shumailov et al. (2024) "AI models collapse when trained on recursively generated data" (Nature 631, 755-759).

**Rationale (user)**: "Pointing to it, at any point, and saying 'model collapse is inevitable' would be overstating the case because, if you read the paper, there are very specific assumptions behind the analysis. And similar to the previous run, the further along you get in time, more research comes out that supports this position — what meaningful citation and reference to this paper would be reflective of the fact that the central claim of this paper has been caveated by further research."

---

## 2026-03-13: Unit of Analysis

**Decision**: Unit of analysis is a single person's usage of the paper, not individual posts.

**Context fetch strategy**: Get preceding context (from anyone, establishes what author is responding to) + author's own follow-up replies/quotes. Bulk replies from others are not particularly helpful. Need to explore what prior reference studies have done and what's computationally feasible.

**Rationale (user)**: "If it is part of a thread (series of self-replies) then we want to fetch the surrounding context. If it is part of a discussion back and forth with people, then we want to grab that context as well."

**API capability**: Bluesky getPostThread supports parentHeight (up to 1000 ancestors) and depth (up to 1000 descendants). At 500-2000 posts, fetching full context takes ~2-10 minutes.

---

## 2026-03-13: Citation Identification

**Decision**: All four signal types count as "citing" the paper:
1. Links to the paper (Nature URL, arXiv URL, DOI)
2. Author name mentions ("Shumailov" etc.)
3. Title/phrase references ("Curse of Recursion", paper title)
4. Indirect attributions ("that Nature study on model collapse")

---

## 2026-03-13: Time Range

**Decision**: May 2023+ (preprint onward through present)

---

## 2026-03-13: Accuracy Ground Truth — Two Dimensions

**Decision**: Code both dimensions independently:
1. **Faithful to paper's claims?** — Does the citation accurately represent what Shumailov et al. actually found/claimed?
2. **Accurate to broader field state?** — Does the citation reflect the current state of knowledge at the time of posting? (e.g., uncritically citing only this study is less defensible in 2026)

**Rationale (user)**: "Two dimensions: accurate representation of paper's claims?, accurate to the broader state of the field? (uncritically citing only this study is less defensible now in 2026, for example)."

---

## 2026-03-13: Search Term Strategy

**Decision**: Iterative expansion approach:
1. Start with obvious terms
2. Run mini-experiment
3. Analyze found posts for language patterns
4. Extract new candidate terms from actual discourse
5. Repeat

**Validation before full collection**: All three checks required:
- Signal-to-noise ratios per search term
- Coverage estimate (not missing large pockets)
- End-to-end pipeline test on small sample

**User note**: "LLMs are not necessarily the best at this sort of expansive creative style of thinking by default (neither are humans tbh), so we'll need to be thoughtful with how we approach the search terms and find the non-obvious ones too."

---

## 2026-03-13: Literature Review

**Decision**: Fresh from scratch. Do not extend round 1's 21-paper timeline.

**Rationale (user)**: "Explore the exact process used to create the first time, try to come up with a better strategy ourselves from the lessons of the first one, and then build up a new one from scratch."

**Lessons from round 1**:
- Epoch-based narrative structure worked well (captures shifting understanding)
- Timeline frozen at build time was a limitation
- No validation pass before deployment to subagents
- coding-reference.md condensed version for subagent prompts was effective
- Two arXiv dates were wrong ("verify" notes never resolved)

---

## 2026-03-13: Coding Dimensions

**Decision**: Design after literature review, but leaning toward a much tighter coding scheme than round 1's 6 dimensions.

---

## 2026-03-13: User Involvement

**Decision**: More hands-on, front-loaded. Heavy involvement during design/validation, with frequent AskUserQuestion check-ins at major decision points. Also need to establish coordination patterns for long execution phases.

**User note**: "You should also check-in with me about the coordination (with me) and orchestration (of subagents) patterns to use this time around, based on work the previous time. Also like, how to keep yourself and your agents on track during long sessions and across compaction events."

---

## 2026-03-13: Session State Management

**Decision**: Three-file system (merged to two):
- STATUS.md — current phase + plan + progress (updated at phase transitions)
- DECISIONS.md — this file (append-only)
- Database as ground truth coordination layer

Round 1 used PLAN.md as inter-phase checkpoint (114 lines). This time we separate mutable state (STATUS) from immutable decisions (this file).

---

## 2026-03-13: Paper Relationship

**Decision**: Independent study. Stands alone — does not require reading the round 1 paper.

---

## 2026-03-13: Coding Scheme Design

**Decision**: Fewer dimensions (2-3) with more structured decision-making guidance and examples for Haiku agents.

**Rationale (user)**: "Fewer dimensions, + probably more guidance, because we are asking Haiku to do the coding, it benefits from structured decision-making guidelines and examples."

**Design timing**: After literature timeline is built. The two accuracy dimensions are confirmed:
1. Faithful to paper's actual claims?
2. Accurate to the broader state of the field at time of posting?

---

## 2026-03-13: Inter-Coder Reliability

**Decision**: Formal Krippendorff's alpha + human validation.

**Implementation**:
1. Random sample 50-75 posts from corpus
2. 3 independent Haiku agents code all posts
3. Compute Krippendorff's α per dimension
4. If α < 0.667 → revise codebook, re-test
5. Human reviews 15-20 posts for correctness validation
6. Report both metrics in paper

**Thresholds**: α ≥ 0.800 = strong; 0.667–0.799 = tentative (report with caveats); < 0.667 = unacceptable, revise codebook.

---

## 2026-03-13: Haiku Prompt Structure

**Decision**: XML-tagged sections: rubric → examples → content → output directive.

**Key constraints for Haiku**:
- Feed complete rubric as single block (not pointwise) — +14% correlation
- Use XML tags: `<rubric>`, `<examples>`, `<input_data>`
- Keep rubric under ~30 criteria (Haiku shows instruction density cliff)
- Haiku tends toward complete instruction abandonment over graceful degradation

**Examples**: Build iteratively. Start with 3, run calibration, add examples targeting disagreement patterns. May end up with 5-8.

---

## 2026-03-13: Context Format for Coding Agents

**Decision**: Raw thread context, structured for Haiku readability.

**Rationale (user)**: "Raw thread context, but we should definitely structure the data in such a way that it is easy for a Haiku agent to understand."

**Implementation**: Store full thread context in database. Present to coding agents in structured XML format with clear delineation of: parent posts (preceding context), the citing post itself, and author follow-ups.

---

## 2026-03-13: Execution Coordination

**Decision**: Front-load decisions, then execute with minimal check-ins at specific high-value points.

**Check-in points identified**:
- Coding and context inclusion review (after calibration)
- Paper output format and framing (before writing)

**Rationale (user)**: "Once we nail down the plan it would only be at specific points when coordinate with the human in the loop is the most helpful. Best to execute, and then we can fix issues later."

---

## 2026-03-13: Sequencing

**Decision**: Timeline first, then search term experiments.

**Rationale**: Need to know what "accurate" means before looking at the data.

---

## 2026-03-13: Research Question

**Decision**: How faithfully do Bluesky users represent the claims of Shumailov et al. (2024) when citing it, and does this change as the scientific field evolves?

**Secondary analysis**: Demographic characterization of the citing population using:
- Bio text analysis (self-identified role: researcher, journalist, developer, etc.)
- Follower/reach metrics (does reach correlate with citation accuracy?)
- Repeat citers (do individuals become more accurate over time?)

**Approach**: Exploratory. No formal hypotheses.

**User's expectation**: "Often misrepresentation at the start, and then not keeping up with the state of the field as more papers following up on the original paper, or refuting it, get published."

---

## 2026-03-13: Unit of Analysis (REVISED)

**Decision**: Each citation event is a unit. Same person citing in 3 threads = 3 units. Thread-level: if any post in a self-reply thread cites the paper, the entire thread is the unit.

---

## 2026-03-13: Two-Pass Coding Design

**Decision**: Code each citation unit twice:
- **Pass 1 (post-only)**: Code based on the citing post(s) alone, no thread context
- **Pass 2 (with context)**: Code with full thread context included

**Purpose**: Compare results to measure how much context changes citation interpretation. This is a methodological contribution.

**Context rules for pass 2**:
- All self-replies by the citing author (no limit)
- Author's ancestor chain up to 5 levels
- Non-author parent chain up to 3 levels
- All quoted posts resolved (fetch quoted post text)

---

## 2026-03-13: Second-Order Citations

**Decision**: Collect posts that quote a post that cites the paper (second-order citations). Validate during search term experiments whether these are actually about the paper or meta-critique.

**Rationale (user)**: "Are they commenting on the paper, or is it meta-critique that is not really about the paper and its claims?"

---

## 2026-03-13: Demographics

**Decision**: Characterize the citing population using:
1. Bio text analysis (categorize by self-identified role)
2. Follower/reach metrics
3. Repeat citer analysis

Not: domain/affiliation analysis (not selected).

---

## 2026-03-13: Phase 2.5 — Deeper Search Term Discovery

**Decision**: Add Phase 2.5 (post-compact) for more thorough search term discovery before full data collection.

**Rationale (user)**: "We should do another round of this, post compact, where we try to identify more fruitful search terms. I think we have underexplored this area, and it is important for the quality of this paper that we are thorough in this work."

**Coverage analysis findings**:
- Bluesky search API cannot match URLs (Nature link searches return 0)
- Informal terms ("Habsburg AI", "eating itself") return 0 from search but exist in data via other terms
- 12 "Habsburg" posts, 12 "ouroboros" posts, 11 "mad cow/kuru" posts, 4 "eating itself" posts found via broad "model collapse" term
- 9 Nature URL posts captured via "trained on recursively generated" rather than URL search
- Current estimated relevance rate: ~57% across all terms

**Phase 2.5 scope**:
- Analyze language patterns in already-collected relevant posts to discover non-obvious search terms
- Test whether there are entire vocabularies/communities we're missing
- Consider media coverage terms, quote post chains, and cross-language search
- May add new search terms and re-collect before proceeding to Phase 3

---

## 2026-03-13: Bluesky Search API Limitations

**Decision**: Document as methods limitation in paper. Bluesky's search API cannot match URLs, handles phrase matching inconsistently, and some multi-word queries return 0 despite posts existing with those words.

**Impact**: Posts sharing the Nature link without keyword phrases are only captured if they also use terms like "model collapse" or "trained on recursively generated". This is a systematic gap in our collection that favors posts with explicit discussion over link-only shares.

---

## 2026-03-13: Phase 2.5 Search Term Expansion Results

**Decision**: Added 7 new search terms capturing metaphorical/informal model collapse discourse. Corpus expanded from 5,649 to 7,481 posts (+32%).

**New terms added (Tier 2b)**:
- "Habsburg AI" (225 posts, high signal — dynastic inbreeding metaphor)
- "digital inbreeding" (34 posts, high signal)
- "self-consuming generative" (18 posts, high signal — academic term)
- "synthetic data collapse" (27 posts, high signal)
- "AI eating itself" (489 posts, medium signal — popular framing)
- "AI ouroboros" (916 posts, medium signal — mythological metaphor)
- "AI feeding on itself" (120 posts, medium signal)

**Terms tested and rejected** (low signal-to-noise):
- "model autophagy" — mostly biological autophagy research
- "curse of recursion" — gaming/poetry, not about the paper
- "AI cannibalism" — random noise (politics, Epstein)
- "trained on AI data" / "AI trained on AI" — too broad
- "data collapse AI" — financial/climate collapse, not AI

**Key findings**:
- 140 authors overlap between old and new term sets (discourse community continuity)
- 5,460 unique authors total (up from ~3,964)
- New terms capture genuinely different vocabulary — metaphorical discourse vs. technical/academic
- Medium-signal terms will require relevance filtering in Phase 3

---

## 2026-03-13: Phase 3 Design Decisions

**Relevance filtering scope**: Paper-referencing only. Keep posts that explicitly or implicitly reference Shumailov et al. (2024) / the Nature paper. Posts discussing model collapse generally without paper reference are excluded. This gives a tighter corpus directly answering the research question.

**Batching strategy**: 10 posts per Haiku call for relevance classification. ~750 calls total. Binary classification (relevant/not) with one-line rationale.

**Schema reconciliation**: Reconcile init_db.py with the live posts table before Phase 3 begins. Add relevance columns to posts table.

---

## 2026-03-13: Non-English Post Handling

**Decision**: English-only study. Non-English posts classified as not relevant by Haiku during relevance filtering.

**Implementation**: Added to classification instructions rather than language detection library. Haiku trivially detects language while reading each post. ~2% of corpus is non-English (mostly German, some Japanese/French/Scandinavian).

**Rationale**: Simplest approach. No new dependencies. Handles mixed-language edge cases naturally. Document as methods limitation in paper.

---

## 2026-03-13: Embed/Quote Data Gap

**Decision**: Extract embed data during thread context fetching (Step 5 of Phase 3). No separate collection pass needed.

**Rationale**: The atproto API returns embed data as part of thread responses. When fetch_thread_context.py runs for relevant posts, we can extract and store embed_type at that point — zero additional API calls. Enhancement to fetch_thread_context.py to be implemented before running Step 5.

---

## 2026-03-13: Subagent Fleet Pattern (Validated)

**Decision**: Self-import pattern for relevance classification fleet.

**Pattern**:
- Instructions in a shared file (read by each subagent)
- Batches staged as JSON files (100 posts each)
- Each subagent: Read instructions → Read batch → Write results (Write tool) → Self-import with --file flag
- 5 parallel subagents per wave, ~15 waves
- Import script is idempotent (WAL mode, UPDATE WHERE relevant IS NULL, try/except on rename)

**Validation results**:
- 96% classification agreement across batch sizes (5, 25, 100)
- Perfect run-to-run consistency
- 80% per-wave success rate (transient failures leave no partial state)
- Self-import with --file eliminates race conditions
- Clean re-run: failed batches picked up by WHERE relevant IS NULL

**Per-subagent prompt (~50 tokens)**:
"Read instructions at [path]. Follow all 4 steps. Your batch file: [path]. Your results file: [path]."

---

## 2026-03-13: Context-First Classification Design

**Decision**: Fetch parent and quoted post context for ALL posts before relevance classification. Classify with full context rather than post-only.

**Rationale**: Empirical testing showed 28% of hard cases (short/empty reply posts) changed classification when parent context was available. Good study design requires filtering and coding on the same context basis.

**Implementation**:
- fetch_post_context.py fetches parent text and quoted text for all 7,481 posts (~20 min, Bluesky API)
- Stored in post_context table (post_id, parent_text, parent_author, quoted_text, quoted_author)
- Staging script includes parent_text and quoted_text in batch files
- Classification instructions updated to tell subagents to use all available context

**Token budget**: 100 posts with parent+quote context ≈ 17K tokens, well under the 25K Read tool limit.

---

## 2026-03-13: Read Tool Token Limit (25K)

**Decision**: Document and design around the 25K token per-read-call limit in Claude Code.

**Constraint discovered empirically**:
- Read tool caps at 25,000 tokens per call (error at 25,023 tokens)
- Secondary limit: 256 KB file size
- Files >10KB return persisted output with 2KB preview

**Impact on batch sizing**:
- 100 posts with parent+quote context: ~17K tokens (safe, 68% utilization)
- 100 posts with parent+quote+grandparent: ~21K tokens (tight, 84%)
- 50 posts with full context: ~11K tokens (comfortable, 44%)

**Decision**: Keep batch size at 100 with parent+quote context. Do not include grandparent context in classification batches.

---

## 2026-03-13: Claude Code Subagents for Classification (Not API)

**Decision**: Use Claude Code Haiku subagents for relevance classification, NOT direct Anthropic API calls.

**Rationale (user)**: "I can't pay for the Anthropic API on top of my Claude Code plan."

**Pattern**: Instruction file + staged batch files + Write tool output + self-import with --file flag. Tested and validated.

---

## 2026-03-13: ICR for Relevance Filtering

**Decision**: Apply the same inter-coder reliability protocol to relevance classification that was designed for Phase 5 coding.

**Protocol**:
1. Sample 50 posts (stratified across search terms)
2. 3 independent Haiku agents classify each post
3. Compute Krippendorff's alpha
4. If α < 0.667 → revise classification prompt, re-test
5. Only run full fleet after calibration passes

**Rationale**: Relevance filtering determines which posts enter the study. If the classifier is unreliable, the entire corpus is compromised. Same rigor as coding.

---

## 2026-03-13: Rollback Strategy

**Decision**: Reset and re-run if classifications are systematically wrong.

**Implementation**: SET relevant=NULL for affected posts (by search_term, batch, or all), fix the prompt, re-stage, re-classify. The idempotent import and WHERE relevant IS NULL design supports clean re-runs.

---

## 2026-03-13: No Expected Relevance Rate Threshold

**Decision**: No preset expected relevance rate. Run classification and evaluate results empirically. Flag anomalies manually rather than setting arbitrary thresholds.

---

## 2026-03-13: Short/Empty Post Handling

**Decision**: Keep all posts in classification pipeline, including empty and very short posts. Do not auto-reject based on length.

**Rationale**: Investigation showed 58% of empty posts and 59% of short posts are replies — they're reactions to substantive parent posts. Context (parent_text, quoted_text) reveals their meaning. The two-pass coding design in Phase 5 handles these naturally.

**Data**: 44 empty posts (<5 chars), 469 short posts (<50 chars), 307 of which are replies.

---

## 2026-03-14: Narrow Scope — Direct Citations Only

**Decision**: Restrict relevance to posts with a traceable citation chain to Shumailov et al. (2024). No longer classify based on topic matching alone.

**What counts as relevant**:
- Direct link to Nature article, arXiv preprint, DOI, or identifiable news coverage
- Naming the authors (Shumailov, Shumaylov)
- Quoting the paper title
- Replying to or quoting a post that does any of the above (depth 0-1)
- Sharing identifiable news coverage of the paper

**What is NOT relevant under this scope**:
- General "model collapse" discourse without traceable citation
- Metaphorical terms (Habsburg AI, AI ouroboros, etc.) unless in a citation chain
- Posts about mode collapse (GANs), catastrophic forgetting, data poisoning, etc.
- General AI pessimism using collapse language

**Rationale (user)**: "There is so much confusion around this term that it is probably hard to identify which form of model collapse someone is referring to, unless there is a direct citation in the post, in the quoted post, or in the context surrounding the post."

**Research supporting this**:
- "Habsburg AI" coined Feb 2023 by Jathan Sadowski — predates Shumailov's preprint
- "AI ouroboros" also Feb 2023 — independent metaphor
- Schaeffer et al. (2025) identifies 8 competing definitions of "model collapse"
- Empirical analysis of our corpus: only ~13% of "model collapse" posts clearly reference the recursive training mechanism
- Methodological literature supports narrow primary samples for faithfulness analysis

---

## 2026-03-14: Metaphorical Terms Same Standard as All Others

**Decision**: Terms like "Habsburg AI" and "AI ouroboros" are NOT treated as implicit citations. They require the same traceable citation chain as any other post.

**Rationale (user)**: "How do we differentiate between the tail collapse claim vs. broader model collapse in the case of these metaphors? How do we know that they were coined specifically in response to this finding vs. tail collapse, or other forms of model collapse?"

**Research confirming this**: Habsburg AI and AI ouroboros both predate Shumailov's preprint (May 2023). They were coined independently and are used for multiple AI concerns beyond the specific paper.

---

## 2026-03-14: Corpus Size Acceptable at 500-800

**Decision**: Narrow scope expected to yield ~500-800 posts with direct citations. This is acceptable.

**Rationale (user)**: "500-800 is fine, but narrower scope means we do need to make sure that our search strategy will successfully find all link-based or text-based citations of this paper. Including quoting a post that links to this, or maybe even considering second-level chains."

---

## 2026-03-14: Literature Artifacts — Timeline + Terminology Landscape

**Decision**: Maintain two separate literature artifacts:
1. **timeline.md** — Papers in the Shumailov et al. lineage (directly responding to or building on the Nature paper). Used as context during classification.
2. **terminology-landscape.md** — Broader terminology space: related concepts, competing definitions, metaphor origins. Used as "what this study is NOT about" reference.

**Requirement**: All referenced papers downloaded as PDFs in `papers/` directory.

---

## 2026-03-14: Supplementary Search Strategy Needed

**Decision**: Current keyword-based search is insufficient for narrow scope. Need supplementary searches using:
- Bluesky `domain:` search operators for paper URLs and news coverage URLs
- Co-author name variations (Shumaylov spelling)
- Major news coverage URLs (TechCrunch, Nature News, etc.)

**To be designed**: After literature update is complete.

---

## 2026-03-14: Citation Chain Depth 0-1

**Decision**: Depth 0 (direct citation) and depth 1 (reply/quote of a citing post) are included. Depth 2+ excluded — research shows reframing effects and signal degradation become problematic beyond depth 1.

**Source**: Twitter/X citation chain research shows 5x higher reframing rate in quote posts (28.9% vs 8.3% for replies). Exponential decay in chain participation at each successive level.

---

## 2026-03-14: English-Only Confirmed for Narrow Scope

**Decision**: Non-English posts excluded even if they contain direct citation signals. Document as methods limitation.

**Rationale (user)**: Confirmed English-only. Non-English posts with citations exist (e.g., Spanish post citing Shumailov + Nature link in ICR sample) but are excluded for consistency.

---

## 2026-03-14: News Coverage as Citation Signals

**Decision**: Sharing identifiable news coverage of the Shumailov paper counts as a citation signal.

**Process**: 3 research agents from different angles (Google, citation trails, social sharing), then 5 verification agents fetching 25 URLs, then 2 more targeted agents for missing outlets. Result: ~20 verified URLs confirmed about Shumailov specifically. 3 URLs excluded (wrong paper or no specific citation). Multiple major outlets confirmed NO coverage (Ars Technica, Wired, The Verge, BBC, Guardian, WaPo).

**Verified coverage list**: lit-timeline/news-coverage-urls.md

**User feedback**: Single-agent research is insufficient for foundational artifacts. Must use multiple agents from different angles + verification pass.

---

## 2026-03-14: ICR v2 Results (Narrow Scope)

**Decision**: Classification instructions v2 (narrow citation-chain scope) passed ICR with α = 0.943 (STRONG).

**Details**:
- v1 (topic-based): α = 0.766 on random sample (acceptable but ambiguous)
- v2 random sample: α = 0.000 (statistical artifact — almost no positives in random sample)
- v2 balanced sample (25 likely positive + 25 likely negative): α = 0.943, 96% agreement, 2 disagreements
- Disagreements: 1 non-English post with citation (resolved: exclude), 1 truncated news URL (edge case)

**Instructions location**: /private/tmp/claude/relevance/classification_instructions_v2.md

---

## 2026-03-14: Supplementary Bluesky Searches Required

**Decision**: Must run supplementary Bluesky searches using domain: operators before fleet classification. Keyword-only search misses link-only shares.

**Rationale (user)**: "100%: we need to update our search strategy to find these second-level citations and discussions of the paper."

**Search strategy**: Use Bluesky domain: operators for ALL ~20 verified news coverage URL domains (not just paper URLs). Full list in lit-timeline/news-coverage-urls.md.

---

## 2026-03-14: Expanded Auto-Accept for Narrow Scope

**Decision**: Auto-accept posts matching: shumailov, arXiv URL, DOI, title fragment, AND posts containing verified news coverage URLs. Reduces Haiku classification workload.

**Rationale**: Under narrow scope, these ARE the core relevant posts. Auto-accepting them is both faster and more reliable than sending them through Haiku.

---

## 2026-03-14: Coding Reference Update Timing

**Decision**: Update coding-reference.md AFTER classification, not before. Focus on finalizing the corpus first.

**Rationale (user)**: Get the corpus finalized first. The 8-definitions research and terminology landscape will inform Phase 5 coding design.

---

## 2026-03-14: Second-Order Citations Terminology

**Decision**: Use "second-order citations" (Alperin et al. 2024) as terminology for news-mediated mentions of the paper.

**Key reference**: Alperin et al. (2024) "Second-order citations in altmetrics: A case study analyzing the audiences of COVID-19 research in the news and on social media" (*Quantitative Science Studies*, MIT Press). Direct precedent for our study design.

**Finding**: News from just 5 outlets was shared 2x as much as the papers themselves in the COVID study. First-order (direct paper) and second-order (news-about-paper) citations reached "largely distinct" audiences.

---

## 2026-03-14: News Coverage Research Methodology

**Decision**: Use three-source strategy for comprehensive news coverage identification:
1. **Crossref Event Data API** (programmatic, DOI-based) — most reliable
2. **Mining our own Bluesky data** (SQL extraction of URLs from posts) — most directly relevant
3. **Web search agents** (multiple angles) — fills gaps

**Results**: ~25 verified news coverage URLs. Key finds from Crossref (Popular Science, Vox) that web searches missed entirely. Key finds from our own data (Cosmos Magazine) that no external source captured.

**Lesson**: Single-agent web searches are insufficient. Programmatic APIs + empirical data mining + web searches together are needed for comprehensive coverage.

---

## 2026-03-15: News Coverage Verification Complete

**Decision**: News coverage list finalized with ~35 verified URLs. Key additions this session:
- Bloomberg, MIT Technology Review, VentureBeat, TechTarget all CONFIRMED about Shumailov via web search
- PopSci VERIFIED (explicit Nature study reference in article text)
- ABC.net.au, Axios (2 articles), Cosmos Magazine assessed as LIKELY/CONFIRMED
- Mashable, Gadgets360, Fast Company, 404 Media, Slate, Tom's Hardware confirmed NOT about Shumailov (different topics)

**Artifacts updated**: news-coverage-urls.md, classification_instructions_v2.md, stage_relevance_batches.py (auto-accept expanded to ~40 URL fragments)

---

## 2026-03-15: Supplementary Bluesky Search Strategy

**Decision**: Domain-based Bluesky searches don't work well (search only matches post text, not embedded link URLs). Used news article title/phrase searches instead. Found 22 new posts sharing Scientific American, MIT Tech Review, and Nature News articles that our keyword searches missed. Corpus expanded from 7,481 to 7,503 posts.

---

## 2026-03-15: Fleet Classification Architecture — No Bash for Subagents

**Decision**: Classification subagents must NOT have access to Bash. Agents only Read batch file + Write results file. Main agent handles all imports after each wave.

**Root cause**: Audited subagent JSONL logs from first fleet run. 75% of Haiku agents wrote Python heredoc scripts to classify posts via regex instead of LLM judgment, despite explicit "FORBIDDEN" instructions. The delegation-guard plugin suppresses the block-heredoc hook during subagent execution, so there's no safety net.

**Impact of first run**: All 5,250 fleet classifications RESET. The regex-based classifications produced high false positive rates (some batches 20-45% relevant vs expected 5-10%).

---

## 2026-03-15: Strengthened Classification Criteria (v3)

**Decision**: Added explicit "MOST COMMON MISTAKE" section to instructions: describing the model collapse concept is NOT a citation. Must find specific URL, author name, paper title, or verified news article reference.

**Evidence**: Test run showed batch 002 going from 23 relevant (v2) → 7 relevant (v3) with the strengthened instructions. False positives like "AI trains on AI data and degrades" (no URL) correctly excluded.

---

## 2026-03-15: Test-Before-Scale Protocol for Fleet Operations

**Decision**: Always test 2-3 agents and audit their JSONL logs before running full fleet waves. Verify: (1) correct tool usage (no forbidden Bash), (2) output quality (spot-check relevant rationales), (3) completeness (all 100 posts classified).

**Rationale**: First fleet run wasted ~50K tokens and hours before discovering 75% of agents were non-compliant. A 2-agent test wave would have caught this immediately.

---

## 2026-03-17: No Important Files in /tmp

**Decision**: All methodology artifacts, prompts, audit trails, and scripts must live in the project directory — never only in `/tmp`. Temp dirs are for ephemeral batch I/O only.

**New project structure:**
- `prompts/` — Classification and verification instruction files (all versions)
- `audit/` — Audit reports, classification agent audits
- `audit/verification/` — Verification batch results + apply script
- `audit/icr/` — ICR scripts, samples, and coder results

**What stays in /tmp**: Input batch files (generated from DB, ephemeral) and result files pre-import (copied to DB, then disposable). These are working artifacts, not methodology records.

**Rationale**: `/tmp` is cleared on reboot. Previous sessions had 402 files / 11MB of irreplaceable methodology artifacts sitting only in `/tmp`. Moved all important files to project directory.

---

## 2026-03-17: Verification Policy Decisions

**Decisions made during v4 verification pass:**
1. Articles from unlisted domains (FT, Forbes, NPR, Guardian, etc.) ARE relevant if about model collapse from AI training on AI data — the verified domain list is a helper, not exhaustive
2. Link card posts (headline without visible URL) count as citation signals — the shared article IS the signal
3. YouTube videos about model collapse (e.g., "Curse of Recursion") count as citation signals
4. Posts sharing articles from our "Excluded" list (fastcompany Grok article, tomshardware ChatGPT article) ARE false positives — confirmed not about Shumailov
5. Vague references like "the first paper about the technology" without identifying Nature/Shumailov are NOT citation signals

**Rationale**: Needed consistent rules for reconciling 128 verification flags. Three-category triage (confirmed FP / reinstate / manual review) was efficient. 29 confirmed false positives out of 610 = 4.8% FP rate.

---

## 2026-03-20: V4 Coding Scheme Redesign

**Decision**: Replace ordinal paper_fidelity and field_accuracy scales with binary distortion tags.

**Rationale (user + Opus)**:
- V3 spot-check revealed the accurate/partially_accurate/inaccurate scale conflates fundamentally different error types
- "Partially accurate" was used for certainty inflation, scope inflation, temporal overclaims, AND causal conflation — these are distinct problems with distinct implications
- Binary tags produce higher ICR than ordinal scales (literature-supported)
- Tag-based scheme enables richer analysis: which distortions dominate? How do they evolve across epochs?
- Inspired by Wright et al. (2024) fine-grained distortion framework, Sumner et al. (2014) exaggeration typology

**What's preserved**: claim_strength (3 levels, α=0.917)
**What's replaced**: paper_fidelity + field_accuracy → ~8 binary distortion tags
**What this enables**: Distortion co-occurrence analysis, per-tag epoch trajectories, distortion typology as methodological contribution

**Candidate tags** (to be refined after deep research):
- certainty_inflation, scope_inflation, temporal_overclaim, causal_conflation
- mechanism_omission, mitigation_blindness, definitional_conflation, sensationalism

---

## 2026-03-22: V4 Calibration Complete — Accept and Proceed

**Decision**: Accept V4 calibration results (α=0.796 for "any distortion", 94-96% pairwise agreement) and proceed to production coding.

**Rationale**:
- Per-tag α values are low for some tags due to low prevalence (1-4 TRUE per coder out of 50), not boundary confusion
- Agreement percentages are excellent (94-99% per tag)
- "Any distortion" α=0.796 is nearly strong threshold
- Further calibration rounds show diminishing returns
- certainty_inflation boundary (α=0.530) is acceptable given the aggregate signal

**Production plan**: Single-pass coding of 539 CUs. No two-pass design needed — binary tags are objective enough that context shouldn't change judgment (verify post-coding).
