# v4 Classification Fleet Protocol

## Pre-Flight Checklist (verify on 2-3 test agents)

All criteria must pass before scaling:

- [ ] **Output completeness**: All 100 posts classified, no skips
- [ ] **Output structure**: `citation_signal` field present, valid JSON, correct batch_id
- [ ] **Classification quality**: Relevant posts have actual URLs/author/DOI; hard negatives rejected
- [ ] **Tool compliance**: Zero Bash violations (no `wc`, no `cat`, no Python scripts)
- [ ] **No script classification**: Agent used LLM judgment, not Python regex/domain matching

## Wave Execution Protocol

1. Launch 5 agents per wave
2. After wave completes, run `audit_agents.py` on all agent IDs
3. Classify violations:
   - **Script violations** (Python classification code): Re-run batch immediately
   - **Minor violations** (wc -l only): Accept if results pass quality check
4. Import results only from compliant + quality-verified agents
5. First 3 waves: audit every agent. After that: spot-check 1-2 per wave.

## Quality Spot-Check Protocol

For each wave, pick 1-2 batches and verify:
- All "relevant" posts have a real citation signal in their `citation_signal` field
- No Guardian/Mashable/unrelated-domain false positives
- Hard negatives (concept-only posts) are correctly marked NOT RELEVANT

## Known Failure Modes

1. **Haiku writes Python scripts** despite prompt ban (24% in v2, ~33% in v4 test)
   - Root cause: Haiku ignores prompt-level tool restrictions
   - Mitigation: Audit after every wave, re-run violations
2. **Domain over-matching** in Step 1b (fixed in v4 prompt revision)
3. **Incomplete batches** from Haiku context limits (monitor post counts)
