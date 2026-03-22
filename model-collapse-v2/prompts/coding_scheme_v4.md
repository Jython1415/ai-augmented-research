# Coding Scheme V4 — Distortion Tag Detection

You are coding Bluesky posts that cite Shumailov et al. (2024) "AI models collapse when trained on recursively generated data" (Nature 631, 755-759).

## Quick Reference — Read First

For each post, you assign:
1. **claim_strength**: neutral_share / substantive_mention / authoritative_claim
2. **Distortion tags**: For each of 8 tags, mark TRUE or FALSE. A post with 0 true tags is a faithful representation.

## Dimension 1: Claim Strength

Same as V3. Decision tree:

1. Did the poster add ANY of their own words characterizing model collapse?
   - **NO** — only a paper title, citation, link, or purely descriptive headline → `neutral_share`. STOP. Do not evaluate distortion tags — mark all as FALSE.
   - **YES** — continue to step 2.

**Note on headlines**: A headline that makes a causal, evaluative, or predictive claim about model collapse (e.g., "why human data prevents collapse", "AI models collapse, they get existential") IS a substantive claim — code as `substantive_mention` even if the poster added no words. Only purely descriptive headlines ("New study on AI training data") are `neutral_share`.

2. Does the post present collapse as INESCAPABLE and UNIVERSAL?
   - **YES** — uses language like "inevitable", "proven", "will destroy all", "mathematically certain". Claims collapse is an inescapable universal law → `authoritative_claim`
   - **NO** — the post characterizes, reacts to, questions, or interprets the findings without claiming universality → `substantive_mention`

### Claim Strength Examples
- "AI models collapse when trained on recursively generated data [link]" → `neutral_share` (paper title + link only)
- "This is concerning — AI trained on its own output degrades" → `substantive_mention`
- "Model collapse is inevitable and will destroy all AI" → `authoritative_claim`
- "Synthetic data has its limits — why human-sourced data can help prevent AI model collapse [headline]" → `substantive_mention` (headline makes a causal claim)

---

## Dimension 2: Distortion Tags

For posts coded `substantive_mention` or `authoritative_claim`, evaluate each of the 8 distortion tags independently. Each tag is TRUE or FALSE.

A faithful representation of the paper has ALL tags FALSE.

### Tag 1: certainty_inflation
**Question**: Does the post present the paper's CONDITIONAL findings as DEFINITIVE or INEVITABLE?

**The paper says**: Model collapse CAN occur when models are trained on recursively generated data under full data replacement conditions. This is a risk that requires careful data management.

**TRUE when the post**:
- Uses "will", "inevitable", "proven", "certain", "guaranteed" about collapse
- Presents collapse as a settled fact rather than a conditional finding
- Removes hedging language (the paper's "can" becomes "does" or "will")
- Claims collapse is "already proven" or "mathematically demonstrated" as universal

**FALSE when the post**:
- Uses conditional language: "can", "may", "could", "risks", "threatens"
- Describes the phenomenon without asserting certainty
- Says "was always going to be a problem" (expressing predictability, not inevitability)
- Expresses concern without claiming certainty

**KEY DISTINCTION: Urgency or concern ≠ certainty inflation.** Posts expressing strong concern ("this is a serious problem", "we need to pay attention to this") are NOT inflating certainty — they're reacting to a real finding. Certainty inflation requires converting the paper's CONDITIONAL finding into a DEFINITIVE one. The test: does the post remove the "under these conditions" qualifier and present collapse as unconditional?

**Examples**:
- "AI models will collapse" → TRUE (conditional → definitive)
- "AI models can degrade when trained on their own output" → FALSE (preserves conditionality)
- "Model collapse is inevitable" → TRUE
- "This was always going to be a problem" → FALSE (predictability ≠ inevitability)

### Tag 2: scope_inflation
**Question**: Does the post generalize the paper's SPECIFIC findings to a broader scope than was tested?

**The paper tested**: Full data replacement on specific models (OPT-125M, VAEs, GMMs). The collapse requires recursive training where each generation trains ONLY on the previous generation's output.

**TRUE when the post**:
- Claims collapse affects "all AI" or "all models" without specifying conditions
- Extends from "recursive self-training" to "any use of synthetic data"
- Implies collapse applies to systems not tested (deployed chatbots, image generators, etc.)
- Claims "all synthetic data is dangerous" when the paper tested specific replacement scenarios

**FALSE when the post**:
- Describes the general phenomenon correctly ("training on AI output causes degradation")
- Specifies conditions or uses hedged scope
- Makes reasonable inferences about implications without claiming universality

**Implicit scope inflation via juxtaposition**: When a post places an external statistic (e.g., "57% of internet content is AI-generated") next to the paper's findings, this implies the paper's results apply at that scale — even if the post doesn't explicitly say so. If the juxtaposition would lead a reader to believe collapse applies more broadly than the paper tested, mark TRUE.

**Examples**:
- "All AI will degrade" → TRUE (scope: specific models → all AI)
- "Training models on AI output is a very bad idea" → TRUE (scope: full replacement → all synthetic data use)
- "AI models can collapse when trained on recursively generated data" → FALSE (accurate scope)

### Tag 3: temporal_overclaim
**Question**: Does the post claim collapse is CURRENTLY OCCURRING in deployed systems without evidence?

**Reality**: As of 2025, there is no peer-reviewed evidence that model collapse has occurred in commercially deployed AI systems. The paper demonstrated collapse under controlled laboratory conditions.

**TRUE when the post**:
- Claims collapse "is already happening" in production systems
- Attributes specific product degradation (ChatGPT getting worse, Grok issues) to model collapse without evidence
- Treats lab findings as confirmed real-world phenomena

**FALSE when the post**:
- Expresses concern that collapse COULD happen
- Describes the lab findings without claiming real-world occurrence
- Notes that conditions for collapse may be approaching

**Examples**:
- "Model collapse is already happening with AI-generated texts" → TRUE
- "Researchers worry AI bots like Grok are already showing signs" → TRUE (presents worry as evidence)
- "If AI companies aren't careful, this could become a real problem" → FALSE (conditional concern)

### Tag 4: causal_conflation
**Question**: Does the post attribute phenomena NOT studied in the paper to model collapse?

**The paper studied**: Distribution collapse — loss of tail distribution, convergence to repetitive/degenerate output under recursive training.

**TRUE when the post**:
- Attributes hallucinations to model collapse (different phenomenon)
- Attributes inability to count letters/do basic tasks to collapse (tokenization issues, not collapse)
- Conflates model collapse with general "AI getting worse" without specifying the mechanism
- Equates collapse with data poisoning, mode collapse (GANs), or catastrophic forgetting

**FALSE when the post**:
- Correctly identifies the mechanism (recursive training, distribution loss, quality degradation)
- Uses metaphors that capture the essence (telephone game, inbreeding) without attributing wrong effects
- Connects collapse to related but distinct phenomena while acknowledging the distinction

**Examples**:
- "Goodbye truth & accuracy. Hello hallucinations." → TRUE (conflates collapse with hallucinations)
- "Can't even count letters in 'blueberry' because of collapse" → TRUE (conflates with tokenization)
- "Like a game of telephone — each generation gets worse" → FALSE (apt metaphor for distribution loss)

### Tag 5: mechanism_omission
**Question**: Does the post describe collapse WITHOUT mentioning the key condition — recursive/self-training on model output?

**The key condition**: Collapse requires models training on their OWN output (or output of similar models) recursively. This is the core mechanism.

**TRUE when the post**:
- Says "AI degrades" or "AI collapses" without any reference to the training mechanism
- Describes collapse as a property of AI systems rather than a consequence of specific training practices
- Uses the term "model collapse" as shorthand for general AI failure

**FALSE when the post**:
- Mentions training on AI output, synthetic data, recursive data, or self-generated content
- References the feedback loop, self-training, or data contamination mechanism
- Uses metaphors that imply the recursive mechanism (eating itself, inbreeding, ouroboros)

**Examples**:
- "AI models are getting worse — model collapse!" → TRUE (no mechanism)
- "AI trained on AI output degrades over generations" → FALSE (mechanism stated)
- "The AI is eating itself" → FALSE (metaphor captures recursive mechanism)

### Tag 6: mitigation_blindness
**Question**: Does the post ignore demonstrated prevention strategies that were available at the time of posting?

**This tag is EPOCH-DEPENDENT:**
- Epoch 2 (May 2023 – Mar 2024): FALSE for all posts (no mitigations published yet)
- Epoch 3+ (Apr 2024+): Gerstgrasser et al. showed accumulation prevents collapse
- Epoch 5+ (Oct 2024+): Feng (filtering), He (golden ratio mixing) also demonstrated
- Epoch 6+ (Mar 2025+): Multiple independent mitigation strategies established

**TRUE when the post** (Epoch 3+ only):
- Claims collapse is unavoidable or has no solution
- Presents collapse as an unsolvable problem when prevention is demonstrated
- Says "there's no way around it" or "the only solution is to stop using synthetic data"
- Treats collapse as inevitable despite available mitigations

**FALSE when the post**:
- Posted before Epoch 3 (mitigations not yet available)
- Describes collapse as a concern without claiming it's unsolvable
- Acknowledges that data management strategies matter
- Doesn't make claims about solvability either way

**Examples (Epoch 5+ post)**:
- "There's no way to prevent model collapse" → TRUE
- "The models will all collapse" → TRUE (implies no prevention possible)
- "Model collapse is a concern that requires careful data management" → FALSE

### Tag 7: definitional_conflation
**Question**: Does the post treat "model collapse" as a single, settled concept when the field has identified multiple competing definitions?

**This tag is primarily relevant for Epoch 6+ (Mar 2025+)** after Schaeffer et al. identified 8 conflicting definitions of "model collapse" in the literature.

**TRUE when the post** (primarily Epoch 6+):
- Treats model collapse as having one universally agreed meaning
- Conflates tail collapse (Shumailov) with mode collapse (GANs), catastrophic forgetting, or other phenomena
- Uses "model collapse" as a catch-all term for any AI quality issue

**FALSE when the post**:
- Uses the term in a way consistent with Shumailov's definition (recursive training degradation)
- Acknowledges complexity or specifies which aspect of collapse they mean
- Posted before Epoch 6 (definitional fragmentation not yet documented)

### Tag 8: sensationalism
**Question**: Does the post use dramatic framing that goes significantly beyond what the evidence supports?

**TRUE when the post**:
- Uses apocalyptic language: "AI will eat itself", "doom loop", "the end of AI"
- Frames collapse as civilization-threatening when the paper shows a specific technical risk
- Uses emotional language designed to alarm rather than inform
- Compares to catastrophes disproportionate to the finding (kuru disease, nuclear meltdown)

**FALSE when the post**:
- Uses vivid but proportionate language ("garbage in, garbage out")
- Expresses genuine concern without dramatization
- Uses established metaphors (Habsburg AI, ouroboros) that capture the mechanism
- Describes the finding's importance without catastrophizing

**KEY DISTINCTION: Emotional tone ≠ sensationalism.** A post saying "uh oh" or "this is scary" with an accurate description is NOT sensationalist — it's a proportionate emotional reaction. Sensationalism requires DISPROPORTIONATE framing: comparing a specific technical risk to civilization-ending catastrophes, using apocalyptic language, or implying consequences far beyond what the evidence shows. The test: is the framing proportionate to the actual finding?

**Examples**:
- "LLMs are destined for digital kuru disease" → TRUE (disproportionate catastrophe framing)
- "AI companies are in serious trouble if they don't address this" → FALSE (concern without catastrophizing)
- "The AI is eating itself" → borderline — TRUE if framed as apocalyptic, FALSE if used as apt metaphor for recursive degradation
- "Uh oh, this is concerning" + accurate paper description → FALSE (emotional but proportionate)
- "As AI models collapse, they get existential" (headline) → FALSE (editorial framing, not catastrophizing)

---

## Coding Rules

**Rule 1: neutral_share posts get ALL tags FALSE.** Do not evaluate distortion tags for posts that make no claims.

**Rule 2: Tags are INDEPENDENT.** A post can have 0, 1, or multiple tags. Evaluate each separately.

**Rule 3: Epoch matters for tags 6 and 7.** Check the post's epoch before applying mitigation_blindness or definitional_conflation.

**Rule 4: When in doubt, FALSE.** Only mark TRUE when the distortion is clearly present. The threshold is: would a reader of this post form a meaningfully wrong impression?

**Rule 5: Metaphors are usually NOT distortions.** "Habsburg AI", "ouroboros", "eating itself", "telephone game" are apt metaphors for the recursive mechanism. They are not sensationalism unless combined with apocalyptic framing.

---

## Knowledge Epochs

**Epoch 2: May 2023 – Mar 2024** (Shumailov arXiv preprint, no counterevidence)
**Epoch 3: Apr – Jun 2024** (Gerstgrasser: accumulation prevents collapse)
**Epoch 4: Jul – Sep 2024** (Nature publication, media amplification)
**Epoch 5: Oct 2024 – Feb 2025** (Feng, He: multiple mitigation strategies)
**Epoch 6: Mar 2025+** (Schaeffer: 8 conflicting definitions; field fragmented)

---

## Output Format

For each post, output a JSON object:

```json
{
  "post_id": 123,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "Post adds evaluative reaction to the paper's findings",
  "certainty_inflation": false,
  "scope_inflation": true,
  "temporal_overclaim": false,
  "causal_conflation": false,
  "mechanism_omission": false,
  "mitigation_blindness": false,
  "definitional_conflation": false,
  "sensationalism": false,
  "distortion_reasoning": "Scope inflation: claims 'all AI' will degrade when paper tested specific models under full replacement conditions",
  "epoch": 4
}
```

For neutral_share posts:
```json
{
  "post_id": 456,
  "claim_strength": "neutral_share",
  "claim_strength_reasoning": "Paper title and link only, no added commentary",
  "certainty_inflation": false,
  "scope_inflation": false,
  "temporal_overclaim": false,
  "causal_conflation": false,
  "mechanism_omission": false,
  "mitigation_blindness": false,
  "definitional_conflation": false,
  "sensationalism": false,
  "distortion_reasoning": "neutral_share — no distortion evaluation",
  "epoch": 4
}
```

## Worked Examples

### Example 1: Faithful substantive mention (0 tags)
**Post** (Epoch 2): "I read a paper about how AI models can degrade when trained on their own output. Fascinating and concerning research."
- claim_strength: substantive_mention
- ALL tags FALSE
- Reasoning: Preserves conditionality ("can"), identifies mechanism ("trained on their own output"), proportionate reaction

### Example 2: Certainty inflation + scope inflation (2 tags)
**Post** (Epoch 5): "AI models will all collapse — it's been proven. Training on synthetic data is always a bad idea."
- claim_strength: authoritative_claim
- certainty_inflation: TRUE ("will", "proven")
- scope_inflation: TRUE ("all", "always", extends to all synthetic data)
- All other tags: FALSE

### Example 3: Temporal overclaim + causal conflation (2 tags)
**Post** (Epoch 6): "Model collapse is already happening — that's why ChatGPT keeps hallucinating more and more."
- claim_strength: substantive_mention
- temporal_overclaim: TRUE ("already happening" — no evidence of deployed collapse)
- causal_conflation: TRUE (attributes hallucinations to collapse)
- All other tags: FALSE

### Example 4: Mitigation blindness + certainty inflation (2 tags)
**Post** (Epoch 5): "There's absolutely no way to prevent model collapse. We're doomed."
- claim_strength: substantive_mention
- certainty_inflation: TRUE ("absolutely no way")
- mitigation_blindness: TRUE (Epoch 5: Gerstgrasser, Feng, He all demonstrated prevention)
- sensationalism: TRUE ("doomed" — catastrophizing beyond evidence)
- Other tags: FALSE

### Example 5: Mechanism omission only (1 tag)
**Post** (Epoch 4): "AI is getting worse because of model collapse. This is bad for everyone."
- claim_strength: substantive_mention
- mechanism_omission: TRUE (no mention of recursive training or data practices)
- Other tags: FALSE — the claim is vague but not inflated in certainty or scope

### Example 6: Sensationalism with accurate mechanism (1 tag)
**Post** (Epoch 4): "LLMs are destined for digital kuru disease if they keep training on their own output"
- claim_strength: substantive_mention
- sensationalism: TRUE ("digital kuru disease" — disproportionate catastrophe framing)
- certainty_inflation: TRUE ("destined" — implies inevitability)
- Other tags: FALSE (mechanism correctly identified)
