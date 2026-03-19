# Model Collapse Citation Fidelity Study — Ralph Loop Prompt

You are continuing an AI-augmented research project analyzing how Bluesky users cite Shumailov et al. (2024) "AI models collapse when trained on recursively generated data" (Nature 631, 755-759).

## First: Orient Yourself

1. Read `STATUS.md` — this is your ground truth for what's done and what's next
2. Read `DECISIONS.md` — settled design decisions, do not re-ask these
3. Check git log (`git log --oneline -20`) — see what recent iterations accomplished
4. Read `LOOP_PROGRESS.md` — iteration-by-iteration log of what you've done

Based on these, determine which phase you're in and what the next task is.

## Project Phases

### Phase A: Build Infrastructure
**Gate**: All scripts exist, tested on 2-3 posts, committed to git.

Tasks (do ONE per iteration):
- [ ] Write `data/stage_coding_batches.py` — stages 539 CUs into batches of 10 posts each, writes to `/private/tmp/claude/coding/production/`. Include post text, epoch, citation_type, cu_id, post_id. For Pass 2, also include parent_text, quoted_text, and thread context.
- [ ] Write `data/import_coding_results.py` — reads result JSON files, writes to citation_units table (claim_strength, paper_fidelity, field_accuracy + reasoning fields, epoch, coding_pass). Idempotent (skip already-coded units for that pass).
- [ ] Write pass 2 codebook variant at `prompts/coding_scheme_pass2.md` — copy of coding_scheme_v1.md with added section: "You have additional context below the post. Use parent_text and quoted_text to inform your coding — a reply that looks neutral may be substantive when you see what it's responding to. If context changes your interpretation, note this in your reasoning."
- [ ] Write `data/fetch_author_profiles.py` — fetches Bluesky profiles for all unique authors in citation_units. Store in an `author_profiles` table (did, handle, display_name, description, followers_count, follows_count, posts_count, fetched_at). Use httpx with credentials from .env.
- [ ] Test staging script on 2-3 batches, verify output format
- [ ] Test import script on mock results, verify DB writes
- [ ] Commit all infrastructure with descriptive message

### Phase B: Fleet Coding Pass 1 (Post-Only)
**Gate**: All 539 CUs coded in Pass 1, all waves verified, results imported to DB.

Structure per iteration:
1. Check how many CUs still need Pass 1 coding (query DB: `SELECT COUNT(*) FROM citation_units WHERE coding_pass IS NULL OR coding_pass < 1`)
2. If all coded → move to Phase C
3. Stage next wave (5 batches of 10 posts)
4. Dispatch 5 coding agents in parallel (use Agent tool, run_in_background):
   - Each agent: Read codebook at `prompts/coding_scheme_v1.md`, Read batch, Write results
   - Spawn prompt must include: "Do NOT use Bash for any reason. Use Read to read files and Write to write results."
5. Wait for all 5 to complete
6. Run 1 verification agent: reads all 5 result files + the 5 agent transcripts (output files). Checks:
   - Did each agent read the codebook?
   - Did each agent read the correct batch file?
   - Did each agent use only Read + Write (no Bash)?
   - Are all posts in each batch accounted for in results?
   - Is the JSON valid and all required fields present?
   - Report any failures
7. If verification passes: import results using import script
8. If any agent failed verification: re-run that specific batch
9. After 3 consecutive failures on the same batch: log to LOOP_PROGRESS.md, skip it, continue (gap-fill later)
10. Update STATUS.md with wave progress
11. Commit: "Pass 1: wave N complete (X/539 CUs coded)"

### Phase C: Fleet Coding Pass 2 (With Context)
**Gate**: All 539 CUs coded in Pass 2, results imported.

Same structure as Phase B but:
- Use `prompts/coding_scheme_pass2.md` as the codebook
- Stage batches WITH parent_text, quoted_text, and thread context
- coding_pass = 2 in DB
- Pass 2 is INDEPENDENT of Pass 1 — coders do NOT see Pass 1 codes
- Query: `SELECT COUNT(*) FROM citation_units WHERE coding_pass < 2`

### Phase D: Author Profiles
**Gate**: All unique authors in citation_units have profiles fetched.

Tasks:
- Run `data/fetch_author_profiles.py` (may need multiple iterations if API rate-limited)
- Verify: all authors have profiles or are marked as unfetchable (deleted/suspended accounts)
- Commit results

### Phase E: Analysis
**Gate**: All analyses complete, figures generated, results committed.

Tasks (one per iteration):
- [ ] Citation fidelity trends over epochs — compute distribution of claim_strength, paper_fidelity, field_accuracy per epoch. Generate figures (matplotlib/seaborn, save to `figures/`).
- [ ] Two-pass comparison — for each CU, compare Pass 1 vs Pass 2 codes. Compute: how many changed? Which dimension changed most? Which direction? Statistical test (McNemar's or similar). This is a methodological contribution.
- [ ] Author demographics — categorize bios by role (researcher, journalist, developer, student, etc.). Compute distributions.
- [ ] Repeat citer analysis — identify authors who cited multiple times. Did their accuracy change over time?
- [ ] Reach correlation — do followers/reach correlate with citation accuracy? Compute correlation, generate scatter plot.
- [ ] Summary statistics table — total CUs, by epoch, by citation_type, by claim_strength, by fidelity, by field_accuracy. Both passes.
- [ ] Meta-level VDD review — spawn a review agent that critiques the analysis: are the statistical tests appropriate? Are the figures clear? Are there obvious gaps?
- [ ] Commit all analysis outputs

### Phase F: Paper Writing
**Gate**: Complete paper draft in `paper/paper.tex`.

Tasks (one per iteration):
- [ ] Create `paper/` directory with LaTeX template (generic academic, two-column)
- [ ] Write Abstract + Introduction — research question, motivation, contribution
- [ ] Write Methods — data collection, coding scheme design, ICR calibration, two-pass design
- [ ] Write Results — findings from Phase E analyses, reference figures
- [ ] Write Discussion — implications, limitations (English-only, AI coders not human, Bluesky-only platform, narrow citation scope), future work
- [ ] Write Conclusion
- [ ] Compile references (BibTeX)
- [ ] Self-review: spawn a review agent that reads the full paper and provides critical feedback. Fix issues.
- [ ] Final compile check (if pdflatex available) or just verify LaTeX is well-formed
- [ ] Commit final paper

## Quality Controls

- **Bash ban for coding agents**: Every coding agent spawn prompt MUST include "Do NOT use Bash for any reason."
- **Verification after every wave**: 1 verifier agent checks tool compliance, not labeling quality.
- **Retry policy**: Re-run failed batches immediately. After 3 consecutive failures on the same batch, skip and gap-fill.
- **Meta-level VDD**: After completing each major phase (B, C, E, F), spawn a review agent to critique the process and output quality. Log findings in LOOP_PROGRESS.md.
- **Git commits**: Commit after each completed wave or major task with descriptive messages.

## Iteration Protocol

Every iteration, follow this pattern:
1. **Orient**: Read STATUS.md, LOOP_PROGRESS.md, git log
2. **Decide**: What is the ONE next task?
3. **Execute**: Do that task
4. **Record**: Append to LOOP_PROGRESS.md what you did, what worked, what didn't
5. **Update**: Update STATUS.md with new progress
6. **Commit**: Git commit if meaningful work was done

## Key Files

| File | Purpose |
|------|---------|
| `STATUS.md` | Current phase, progress, blockers |
| `DECISIONS.md` | Settled design decisions (append-only) |
| `LOOP_PROGRESS.md` | Per-iteration log (append-only) |
| `data/posts.db` | SQLite database (ground truth) |
| `prompts/coding_scheme_v1.md` | Pass 1 codebook |
| `prompts/coding_scheme_pass2.md` | Pass 2 codebook (with context) |
| `data/stage_coding_batches.py` | Batch staging script |
| `data/import_coding_results.py` | Result import script |
| `data/fetch_author_profiles.py` | Author profile fetcher |
| `data/compute_icr.py` | ICR computation (reference) |
| `.env` | Bluesky credentials |

## Coding Scheme Summary

3 dimensions, calibrated via 8-round ICR:
- **claim_strength**: neutral_share / substantive_mention / authoritative_claim (α=0.888 STRONG)
- **paper_fidelity**: accurate / partially_accurate / misrepresentation / not_applicable (α=0.762 TENTATIVE)
- **field_accuracy**: accurate / partially_accurate / inaccurate / not_applicable (α=0.816 STRONG)

## Completion

When ALL phases (A through F) are complete and the paper draft is committed:

<promise>RESEARCH_COMPLETE</promise>

If stuck after 10 iterations on the same task: document what's blocking in LOOP_PROGRESS.md, skip it, move to the next task. Come back to skipped tasks in a gap-fill pass before Phase F.
