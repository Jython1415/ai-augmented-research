# Coding Scheme v2 — Pass 2 (With Context)

> For Haiku subagent prompts. Read this entire document before coding any posts.

## Quick Reference — Key Rules (read these FIRST)

1. **The test for `neutral_share` vs `substantive_mention` is: does the shared text make a causal, evaluative, or predictive claim about model collapse?** If YES → `substantive_mention`. If the text is purely a paper title, formal citation, descriptive headline ("New study examines AI training"), or link with no claims → `neutral_share`. It does not matter who wrote the text — poster or headline writer.

2. **Paper fidelity `accurate` requires preserving the CONDITIONAL nature of the finding.** The paper showed collapse under SPECIFIC conditions (full data replacement, recursive training). A post is `accurate` ONLY if it describes collapse as conditional on training approach, OR describes the general mechanism without claiming inevitability/universality. A post that says "AI trained on AI output can degrade" = accurate. A post that says "AI will inevitably collapse" or "collapse is already happening" = NOT accurate.

3. **The bar for `partially_accurate` is: gets the general direction right but overgeneralizes or extends beyond tested conditions.** "Synthetic data causes problems" without specifying it's about recursive replacement = partially_accurate. "Collapse threatens all AI" = partially_accurate (overgeneralizes scope). "Collapse is inevitable" or "collapse is proven/certain" = misrepresentation (removes conditionality entirely).

4. **Field accuracy: claims must not be contradicted by available evidence at that epoch.** "Collapse is a concern" = accurate in every epoch. "Collapse is inevitable" = inaccurate after Apr 2024 (Gerstgrasser showed prevention). "Collapse is already happening in deployed systems" = inaccurate (no evidence of this).

## Your Task

You are coding Bluesky posts that cite Shumailov et al. (2024) "AI models collapse when trained on recursively generated data" (Nature 631, 755-759). For each post, you will assign values on **three dimensions** using the decision trees below.

## Context Available

In addition to the post text, you have been provided with contextual information:

- **parent_text**: The post this is replying to (if it's a reply)
- **quoted_text**: The post being quote-posted (if it's a quote post)
- **parent_chain**: The thread of parent posts leading up to this one
- **self_replies**: Follow-up posts by the same author

**How to use context**: A reply that looks like a neutral share on its own may be substantive when you see what it's responding to. A vague reference to "this paper" may become a clear citation when the parent post contains the link. Use all available context to inform your coding, but code the CITING POST's claims — not the parent's claims.

If context changes your interpretation compared to what a post-only reading would suggest, note this in your reasoning (e.g., "Context reveals this is responding to a thread about Shumailov's findings, making the vague reference a substantive mention").

---

## Dimension 1: Claim Strength

**Question**: Does this post make evaluable claims about model collapse?

**Decision tree** (only 2 decision points):

1. Does the post add ANY of its own words that characterize, describe, or react to the paper or model collapse phenomenon?
   - **NO** → `neutral_share`. The post ONLY contains: a link, the paper title, a formal citation, hashtags, or a news headline being shared — with ZERO added commentary from the poster. STOP — code Dimensions 2 and 3 as `not_applicable`.
   - **YES** → continue to step 2.

2. Does the post claim **inevitability, universality, or prescribe policy action** about model collapse?
   - **YES** — presents collapse as an inescapable universal law. Trigger phrases: "inevitable", "proven", "will destroy all", "must stop", "mathematically certain". The word "always" alone does NOT trigger authoritative_claim — "it was always going to be a problem" (predictability) is different from "collapse will always happen to every model" (universality). The key test: does the post claim collapse is INESCAPABLE and UNIVERSAL? → `authoritative_claim`
   - **Additional triggers for authoritative_claim**: Posts using universal quantifiers ("all AI", "every model", "always") combined with certainty about collapse, OR posts claiming collapse is "already happening" in real-world systems as established fact, OR posts prescribing policy based on collapse inevitability ("we must stop", "the only solution is"). The test: does the post claim CERTAINTY about collapse's occurrence or impact?
   - **NO** — everything else: questions, reactions, descriptions, hedged claims, factual statements, opinions, concerns, explanations → `substantive_mention`

**Values**: `neutral_share` | `substantive_mention` | `authoritative_claim`

**What counts as "poster's own words"?**
- Anything the poster typed themselves: reactions ("uh oh", "fascinating", "I love this term"), paraphrases, opinions, questions, descriptions
- A shared news headline IS the article's words, not the poster's — if the poster ONLY shares a headline + link with zero added text, that's `neutral_share`
- But if the poster adds ANYTHING alongside the headline (even "ugh", an emoji reaction, or "this is important"), that's `substantive_mention`
- A news headline that contains **editorial framing** (e.g., "why X helps prevent Y", "as X happens, Y follows") IS a substantive claim — even if the poster didn't write it. The test is: does the shared text make a claim about model collapse? If yes, code `substantive_mention` regardless of who wrote the text. Only code `neutral_share` for headlines that are purely descriptive titles (e.g., "New study examines AI training data").

**Boundary examples**:
- "AI models collapse when trained on recursively generated data" + link (paper title only) → `neutral_share`
- Full academic citation with no commentary → `neutral_share`
- News headline + link, zero added text from poster → `neutral_share`
- "Not sure how I missed reading this paper" + link → `substantive_mention` (personal reaction)
- "Interesting research" + link → `substantive_mention` (evaluative word)
- "I love the term Habsburg AI" → `substantive_mention` (personal reaction)
- "I was trying to get the link to the model collapse paper" → `substantive_mention` (poster's own words about the paper)
- "This study shows collapse happens under recursive training" → `substantive_mention`
- "Model collapse is inevitable and will ruin all AI" → `authoritative_claim`
- "It's mathematically proven — this will destroy AI" → `authoritative_claim`
- "Synthetic data has its limits — why human-sourced data can help prevent AI model collapse" (news headline with causal claim) → `substantive_mention`
- "As generative AI models collapse, they get existential" (news headline with editorial framing) → `substantive_mention`
- "New study: AI models collapse when trained on recursively generated data" (descriptive headline, just restates paper title) → `neutral_share`

---

## Dimension 2: Paper Fidelity

**Question**: Does the post accurately represent what Shumailov et al. actually found?

Code `not_applicable` if:
- Dimension 1 = `neutral_share`, OR
- The post is a `substantive_mention` but does NOT assert or imply anything about the paper's findings or conclusions. Examples of substantive_mention posts that get `not_applicable` for paper_fidelity:
  - Personal reactions to terminology: "I love the term Habsburg AI" (reacts to a label, not the paper's findings)
  - Seeking the paper: "I was trying to get the link to the model collapse paper" (action, not a claim about findings)
  - Questions without assertions: "Is this the same as Shumailov et al.?" (question, not a claim)
  - Meta-commentary: "Not sure how I missed reading this paper" (personal reflection, no claim about what the paper found)
  - Metaphor appreciation without mechanism claims: "The Habsburg AI metaphor is brilliant" (evaluates terminology, not findings)

The test: **Does the post assert or imply something about what the paper found, what collapse is, or how it works?** If YES → evaluate fidelity. If NO (just personal reaction, question, or meta-commentary) → `not_applicable`.

### What the paper actually found (ground truth):

- **Core finding**: Training models on **recursively generated data** causes **irreversible defects** called "model collapse"
- **Mechanism**: Each generation of model learns a slightly distorted version of the previous generation's distribution. Over iterations, the tails of the original distribution disappear — minority/rare content is progressively lost while majority content is amplified
- **Two phases**: (1) "Early model collapse" — loss of variance, distribution narrows; (2) "Late model collapse" — model converges to a single point or degenerate distribution
- **Models tested**: Gaussian Mixture Models (GMMs), Variational Autoencoders (VAEs), and a large language model (OPT-125M fine-tuned on wikitext2)
- **LLM results specifically**: After ~9 generations of recursive training, OPT-125M output became repetitive and low-quality. Perplexity degraded significantly.
- **Experimental setup**: **Full data replacement** — each generation was trained ONLY on the previous generation's output, with NO access to original human-generated data. This is a worst-case scenario, not the only possible training approach.
- **The paper's own framing**: Presented as a warning about a risk that requires careful data management, NOT as an inevitable outcome of all AI development

### What the paper did NOT claim:

- Collapse happens regardless of data management strategy
- Collapse is inevitable in all real-world scenarios
- All synthetic data is harmful
- Accumulation-based training would also collapse (not tested)

### Decision tree:

1. Identify the **claim about model collapse** the post makes (explicit or implicit).

2. Does the claim preserve the CONDITIONAL nature of the finding?
   - **YES — claim describes collapse as conditional or describes the mechanism without universalizing**: The post says collapse happens under recursive training, when AI trains on AI output, or under specific data management failures. It may describe the phenomenon in general terms ("AI trained on AI degrades") without claiming it's inevitable or universal. This is `accurate`.
   - **PARTIALLY — claim gets the mechanism right but overgeneralizes**: The post extends the finding beyond what was tested. Examples: "synthetic data causes problems" (paper tested recursive replacement, not all synthetic data), "collapse threatens all AI" (paper tested specific models under specific conditions), "collapse is already happening" (paper showed lab conditions, not deployed systems). This is `partially_accurate`.
   - **NO — claim removes conditionality entirely**: The post presents collapse as inevitable, universal, mathematically proven, or certain to occur regardless of data management. Words like "inevitable", "proven", "will destroy", "certain", "already happening everywhere" signal misrepresentation. Also: attributing unrelated phenomena (ChatGPT getting worse, hallucination, general AI failure) to model collapse without evidence. This is `misrepresentation`.

**The key test**: Does the post preserve the fact that collapse is a CONDITIONAL risk dependent on training approach? If yes → accurate. If it overgeneralizes → partially_accurate. If it removes conditionality → misrepresentation.

### Special Cases

**Metaphor and terminology posts**: If a post primarily comments on terminology (e.g., "I love the term Habsburg AI") or appreciates a metaphor rather than making a claim about collapse itself:
- If the post makes NO claim about the collapse mechanism → claim_strength = `substantive_mention` (personal reaction), paper_fidelity = `not_applicable` (no paper claim to evaluate)
- If the metaphor IMPLIES a claim about collapse (e.g., "we've reached the Habsburg stage" = collapse is happening) → evaluate that implied claim normally
- Do NOT code metaphor appreciation as `accurate` just because the metaphor is apt — evaluate only claims about the paper's findings

**Industry inference**: Reasonable inferences about how findings motivate industry practice (e.g., "companies are seeking more training data because of collapse concerns") are `accurate` if grounded in the paper's findings, even if not explicitly tested by the paper.

**Paper titles as neutral**: Paper titles shared without poster commentary count as neutral citations — code paper_fidelity as `not_applicable`, not `accurate`. The title is the paper's own description, not a claim by the poster.

**Colloquial vs. quantitative language**: Informal descriptions like "quickly," "spew nonsense," "indecipherable," or "basic" are acceptable when they characterize the OUTPUT QUALITY degradation the paper demonstrated. Only mark as `partially_accurate` if the post makes a SPECIFIC FALSE CLAIM (e.g., "degradation happens on generation 1" when paper showed later). Colloquial tone ≠ inaccuracy.

**Scope extension boundary**: A post that makes a REASONABLE INFERENCE from the paper's mechanism is `accurate` — e.g., "we should be careful about training data quality." A post that EXTENDS TO CERTAINTY about real-world occurrence is `partially_accurate` — e.g., "collapse is already happening in deployed systems." The distinction: inference about risk vs. assertion about reality.

**Values**: `accurate` | `partially_accurate` | `misrepresentation` | `not_applicable`

**Calibration examples** (apply these strictly):
- "model collapse is a thing" → `accurate` (vague but not wrong)
- "AI models can degrade when trained on their own output" → `accurate` (correctly conditional)
- "training on synthetic data carries risks of collapse" → `accurate` (correctly identifies risk without certainty)
- "AI trained on AI output degrades" → `accurate` (general description of mechanism)
- "synthetic data causes collapse" → `partially_accurate` (paper tested recursive replacement, not all synthetic data)
- "collapse threatens all AI" → `partially_accurate` (overgeneralizes from specific models/conditions)
- "collapse is already happening" → `partially_accurate` (extends lab findings to real world without evidence)
- "we need pre-2023 data or AI will collapse" → `partially_accurate` (reasonable concern but presented as certainty)
- "model collapse is inevitable" → `misrepresentation` (paper did not claim inevitability)
- "it's mathematically proven that AI will collapse" → `misrepresentation` (no such proof exists)
- "collapse will destroy/ruin all AI" → `misrepresentation` (universality + inevitability)
- "ChatGPT is getting worse because of model collapse" → `misrepresentation` (attributes unrelated phenomenon without evidence)

**Values**: `accurate` | `partially_accurate` | `misrepresentation` | `not_applicable`

---

## Dimension 3: Field Accuracy

**Question**: Does the post reflect the state of scientific knowledge at the time it was posted?

Code `not_applicable` if:
- Dimension 1 = `neutral_share`, OR
- The post is a `substantive_mention` but does NOT make a factual claim about model collapse, AI training, or the state of the field. Apply the same test as paper_fidelity: personal reactions, questions, meta-commentary, and terminology appreciation without mechanism claims get `not_applicable`.

### Knowledge epochs (use the post's date to determine which applies):

**Epoch 2: May 2023 – Mar 2024** (Discovery phase — arXiv preprint, no counterevidence yet)
- Shumailov et al. posted to arXiv (2305.17493) in May 2023
- No published counterevidence or mitigation strategies yet
- Accurate: "Collapse is a serious concern under recursive training", "training on synthetic data risks quality loss"
- Inaccurate: "Collapse is a universal law of AI" (extrapolates beyond tested conditions)

**Epoch 3: Apr – Jun 2024** (First counterevidence: Gerstgrasser et al.)
- Gerstgrasser et al. (arXiv, Apr 2024): Showed that **accumulation** (mixing synthetic data with original data, rather than replacing it) **prevents collapse entirely**. This directly demonstrated that Shumailov's result depends on the data replacement setup.
- Accurate: "Collapse depends on data management strategy", "collapse happens under recursive replacement but can be prevented"
- Inaccurate: "Collapse is inevitable" (directly contradicted by Gerstgrasser)
- Note: Gerstgrasser was an arXiv preprint; general audiences may not be aware. Code accuracy against available evidence, note awareness as contextual.

**Epoch 4: Jul – Sep 2024** (Nature publication + media amplification)
- Shumailov et al. published in Nature (Jul 2024, vol 631, pp 755-759) — massive media coverage
- Media headlines often simplified to "AI will eat itself" or "AI doom loop" without nuance
- Accurate: "Nature documented collapse under specific conditions", "recursive training causes degradation"
- Partially accurate: Presenting collapse as settled/universal when Gerstgrasser already showed prevention (understandable given media framing)
- Inaccurate: "Nature proved collapse is inevitable"

**Epoch 5: Oct 2024 – Feb 2025** (Multiple competing results, mitigations demonstrated)
- Feng et al.: Verification/filtering of synthetic data prevents collapse
- He et al.: "Golden ratio" mixing of synthetic and real data avoids collapse
- Multiple teams demonstrated practical mitigation strategies
- Accurate: "It depends on the scenario", cites multiple perspectives, "collapse is a risk that can be managed"
- Partially accurate: "There's no way around collapse" or "the only solution is X" (ignores multiple demonstrated mitigations)
- Inaccurate: Either "collapse is solved/debunked" or "collapse is inevitable"

**Epoch 6: Mar 2025+** (Definitional fragmentation; Schaeffer et al.)
- Schaeffer et al.: Identified 8 conflicting definitions of "model collapse" in the literature — the field doesn't even agree on what the term means
- Debate shifted from "does it happen?" to "what exactly are we measuring?"
- Accurate: Acknowledges complexity, specifies which aspect of collapse, expresses concern (still warranted)
- Partially accurate: Treats collapse as a single settled phenomenon with one meaning
- Inaccurate: "Collapse is inevitable" or "collapse has been debunked"

### Critical principle: Code the CLAIMS, not the completeness

Field accuracy asks: **are the specific claims in this post contradicted by available evidence at the time?** It does NOT ask whether the post cites the full literature or presents a complete picture. A post that accurately describes Shumailov's findings without mentioning Gerstgrasser is `accurate` — the claims are correct, even if incomplete. A post that says "there's no way to prevent collapse" is `partially_accurate` — that specific claim IS contradicted by evidence showing prevention is possible.

### Decision tree:

1. Identify the post's **date** → determine which epoch applies.
2. Are any of the post's claims **contradicted** by evidence available at that time?
   - **NO** — claims are consistent with available evidence → `accurate`
   - **PARTIALLY** — claims overstate, understate, or imply a more absolute picture than available evidence supports (e.g., "there's no way to prevent collapse" in Epoch 5+, or presenting collapse as settled/universal when mitigations exist) → `partially_accurate`
   - **YES** — claims are directly contradicted by available evidence (e.g., "collapse is inevitable" after Apr 2024, "collapse has been debunked") → `inaccurate`

**Calibration by claim strength**:
- `substantive_mention` in any epoch saying "model collapse is concerning" → `accurate` (concern is warranted in every epoch)
- `substantive_mention` in Epoch 5 saying "Shumailov showed models collapse under recursive training" → `accurate` (correct claim, even though mitigations exist)
- `substantive_mention` in Epoch 5 saying "models always collapse when trained on synthetic data" → `inaccurate` (contradicted by Gerstgrasser)
- `authoritative_claim` in Epoch 5 saying "model collapse is inevitable" → `inaccurate` (strong claim directly contradicted)

**Values**: `accurate` | `partially_accurate` | `inaccurate` | `not_applicable`

---

---

## CODING RULES — Apply These Consistently

**Rule 1: Paper fidelity `accurate` requires preserving conditionality.**
The paper's core finding is that recursive training on synthetic data (under full data replacement) causes collapse. A post that describes this mechanism — even in general terms like "AI trained on AI output degrades" — is `accurate`. But a post that REMOVES the conditional nature and presents collapse as inevitable, universal, or already occurring in deployed systems is NOT accurate. The distinction: "can cause" vs "will cause", "under certain conditions" vs "always", "a risk" vs "a certainty".

**Rule 2: Claims consistent with evidence ARE field-accurate, even without citing the full literature.**
"Shumailov showed collapse under recursive training" is `accurate` in every epoch — that claim is never contradicted. Code `oversimplified` only if the post implies a more absolute picture than evidence supports (e.g., "there's no way to prevent collapse"). Code `inaccurate` only when claims are directly contradicted by available evidence.

**Rule 3: Any text making a claim about model collapse IS a substantive_mention.**
`neutral_share` requires ZERO claims about model collapse — only a paper title, citation, link, or purely descriptive headline. If the shared text contains causal claims, editorial framing, value judgments, or predictions about collapse, code `substantive_mention`. The test: does the text make a claim? If yes → `substantive_mention`.

**Rule 4: Reasonable extensions must not remove conditionality.**
Connecting collapse to related concerns (data quality, training practices) is fine and `accurate`. But extending to inevitability, universality, or real-world certainty crosses the line. "We should be careful about training data quality" = accurate extension. "AI is inevitably poisoning itself" = misrepresentation (removes conditionality, adds certainty).

When evaluating paper_fidelity, consider whether the post's framing contradicts mitigations known at its epoch. A post in Epoch 5+ calling something "a very bad idea" without qualification, when mitigations are well-established, should be `partially_accurate` rather than `accurate`.

---

## Cross-Dimension Consistency

Your codes across dimensions should be logically consistent:
- If claim_strength = `authoritative_claim` (inevitability/universality), then paper_fidelity should typically be `misrepresentation` (paper didn't claim inevitability)
- If paper_fidelity = `misrepresentation`, then field_accuracy should typically be `inaccurate` (misrepresentations are contradicted by evidence in every epoch after Epoch 2)
- If paper_fidelity = `accurate`, the post should NOT contain inevitability/universality claims
- If field_accuracy = `accurate`, the specific claims should be consistent with evidence at that epoch — check that inevitability claims aren't coded accurate after Apr 2024

---

## Output Format

For each post, output a JSON object:

```json
{
  "post_id": 123,
  "claim_strength": "neutral_share",
  "claim_strength_reasoning": "Shares the paper title with no added commentary",
  "paper_fidelity": "not_applicable",
  "paper_fidelity_reasoning": "Neutral share — no claim to evaluate",
  "field_accuracy": "not_applicable",
  "field_accuracy_reasoning": "Neutral share — no claim to evaluate",
  "epoch": 4
}
```

**Substantive mention example:**
```json
{
  "post_id": 456,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "Post adds own reaction: 'fascinating' characterizes the finding",
  "paper_fidelity": "accurate",
  "paper_fidelity_reasoning": "Correctly describes the mechanism (training on synthetic data causes degradation) and preserves conditionality",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted Mar 2024 (Epoch 3); the claim is consistent with available evidence",
  "epoch": 3
}
```

**Every rating MUST include reasoning.** The reasoning field should be 1-2 sentences explaining why you chose that value. Reference specific text from the post.

---

## Worked Examples

### Example 1: Neutral share
**Post** (2024-07-25): "AI models collapse when trained on recursively generated data www.nature.com/articles/s41..."
```json
{
  "post_id": 134,
  "claim_strength": "neutral_share",
  "claim_strength_reasoning": "Shares the paper title and link with no added commentary",
  "paper_fidelity": "not_applicable",
  "paper_fidelity_reasoning": "Neutral share — no claim to evaluate",
  "field_accuracy": "not_applicable",
  "field_accuracy_reasoning": "Neutral share — no claim to evaluate",
  "epoch": 4
}
```

### Example 2: Accurate substantive mention
**Post** (2023-09-12): "I would be interested in how the targeted use and limitation to 'one generation of reuse' interacts with the study on model-collapse in the case of iterative and continuous feeding of one models output to the next generation arxiv.org/abs/2305.17493"
```json
{
  "post_id": 20,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "Describes the iterative feeding mechanism and asks a technical question — adds own words beyond just sharing the link",
  "paper_fidelity": "accurate",
  "paper_fidelity_reasoning": "Correctly identifies the recursive/iterative training mechanism and links to the specific arXiv paper",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted Sep 2023 (Epoch 2); engaging with collapse as a concern under recursive training matches the knowledge state",
  "epoch": 2
}
```

### Example 3: Misrepresentation with authoritative claim
**Post** (2024-12-18): "It's not just unethical, but this kind of feedback loop is mathematically proven to make diffusion models worse... So even as a scam, it's self-defeating & leads to model collapse (aka Habsburg AI.) Like Kessler Syndrome but for data, this will ruin all naive models."
```json
{
  "post_id": 566,
  "claim_strength": "authoritative_claim",
  "claim_strength_reasoning": "Claims 'mathematically proven' and 'will ruin all naive models' — inevitability + universality",
  "paper_fidelity": "misrepresentation",
  "paper_fidelity_reasoning": "Claims collapse is 'mathematically proven' and 'will ruin all naive models' — paper showed specific conditions, not a universal mathematical proof",
  "field_accuracy": "inaccurate",
  "field_accuracy_reasoning": "Posted Dec 2024 (Epoch 5); 'will ruin all naive models' contradicts evidence that accumulation, filtering, and verification prevent collapse",
  "epoch": 5
}
```

### Example 4: Concern is accurate even in late epochs
**Post** (2025-10-17): "Same! This paper has haunted me since I read it. I don't think we have the data lineage systems to avoid model collapse!"
**Parent context**: "This is one of my biggest fears with LLMs. They reduce the incentive to create new, non-LLM materials, so we're going to train on more and more LLM material..."
```json
{
  "post_id": 721,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "Expresses concern and makes a claim about data lineage systems — adds own words beyond sharing",
  "paper_fidelity": "accurate",
  "paper_fidelity_reasoning": "References data lineage and avoiding collapse — consistent with the paper's finding about data contamination. Does not misrepresent the scope.",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted Oct 2025 (Epoch 6); expressing concern about data lineage for model collapse is warranted — mitigations exist but require exactly the kind of data management systems the poster doubts we have. The claim is not contradicted by evidence.",
  "epoch": 6
}
```

### Example 5: Accurate description even in Epoch 5
**Post** (2024-11-16): "AI training on AI generated content leads to 'model collapse'. Access to pre-2019 content is absolutely necessary."
```json
{
  "post_id": 1292,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "States collapse mechanism and need for clean data — adds characterization beyond sharing. No inevitability/universality claim.",
  "paper_fidelity": "accurate",
  "paper_fidelity_reasoning": "Correctly describes the core mechanism (training on AI-generated content leads to collapse). The claim about pre-2019 content goes slightly beyond the paper but is consistent with its implications.",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted Nov 2024 (Epoch 5); the claim that AI-on-AI training leads to collapse is correct. While mitigations exist, the post doesn't claim collapse is inevitable — it identifies a real problem and a real need (clean training data).",
  "epoch": 5
}
```

### Example 6: Authoritative claim, inaccurate
**Post** (2025-06-06): "Can't believe the media isn't more focused on inevitable model collapse. The AI hype debt/credit bubble will implode when it becomes clear these systems have irreversibly polluted themselves with synthetic rot."
```json
{
  "post_id": 3224,
  "claim_strength": "authoritative_claim",
  "claim_strength_reasoning": "Uses 'inevitable' and 'irreversibly polluted' — claims universality and inevitability",
  "paper_fidelity": "misrepresentation",
  "paper_fidelity_reasoning": "Claims collapse is 'inevitable' and 'irreversible' in all cases — paper showed specific conditions, and later work showed mitigations",
  "field_accuracy": "inaccurate",
  "field_accuracy_reasoning": "Posted Jun 2025 (Epoch 6); 'inevitable' and 'irreversibly polluted' contradicted by Gerstgrasser (accumulation), Feng (verification), and He (golden ratio) — multiple mitigation pathways demonstrated",
  "epoch": 6
}
```

### Example 7: News headline with editorial framing = substantive_mention
**Post** (2024-08-15): "As generative AI models collapse, they get existential www.nytimes.com/..."
```json
{
  "post_id": 75,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "The headline 'As generative AI models collapse, they get existential' makes a causal claim about collapse having existential consequences — this IS a substantive claim even though it's a headline, not the poster's own words",
  "paper_fidelity": "partially_accurate",
  "paper_fidelity_reasoning": "Implies collapse is actively happening to generative AI models broadly, which overgeneralizes from the paper's specific recursive training conditions",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted Aug 2024 (Epoch 4); expressing concern about collapse during Nature publication period is consistent with available evidence",
  "epoch": 4
}
```

### Example 8: News headline with causal claim = substantive_mention
**Post** (2024-12-05): "Synthetic data has its limits — why human-sourced data can help prevent AI model collapse venturebeat.com/..."
```json
{
  "post_id": 4727,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "The headline makes a causal claim: synthetic data has limits AND human-sourced data helps prevent collapse. These ARE substantive claims about model collapse, even though the poster shared a headline rather than writing their own words",
  "paper_fidelity": "accurate",
  "paper_fidelity_reasoning": "Claims that synthetic data has limits and human data helps prevent collapse — consistent with the paper's finding that recursive synthetic training causes collapse",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted Dec 2024 (Epoch 5); the claim that human-sourced data helps prevent collapse is supported by Gerstgrasser's accumulation findings and other mitigation research",
  "epoch": 5
}
```

### Example 9: Dismissive post = substantive_mention, not authoritative_claim
**Post** (2024-05-12): "OpenAI trained an entire video generator on *exclusively* synthetic data... and people still bring up that dumb 'model collapse' paper whenever they talk about synthetic data. get with the times!"
```json
{
  "post_id": 833,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "Dismisses the paper as 'dumb' and outdated — this IS the poster's own evaluative reaction. But it does not claim inevitability or universality, so it's substantive_mention, not authoritative_claim",
  "paper_fidelity": "partially_accurate",
  "paper_fidelity_reasoning": "Implies the paper is invalidated by one counterexample (OpenAI's video generator using raytraced/game engine data), but the paper studied recursive LLM training, not curated synthetic data from external engines — different scenario",
  "field_accuracy": "partially_accurate",
  "field_accuracy_reasoning": "Posted May 2024 (Epoch 3); dismissing collapse entirely goes beyond what Gerstgrasser showed — Gerstgrasser demonstrated that accumulation prevents collapse, not that all synthetic data training is safe",
  "epoch": 3
}
```

### Example 10: "Always going to be a problem" = substantive_mention, accurate
**Post** (2025-05-10): "This is not a surprise, it was always going to be a problem: AI models collapse when trained on recursively generated data"
```json
{
  "post_id": 101,
  "claim_strength": "substantive_mention",
  "claim_strength_reasoning": "Adds personal reaction ('not a surprise', 'always going to be a problem') — these are the poster's own words characterizing the finding. Does not claim inevitability for ALL AI, just says the problem was predictable",
  "paper_fidelity": "accurate",
  "paper_fidelity_reasoning": "Correctly states the core finding: AI models collapse when trained on recursively generated data. 'Always going to be a problem' is a reasonable interpretation — recursive training on synthetic data IS a persistent risk, even if mitigations exist",
  "field_accuracy": "accurate",
  "field_accuracy_reasoning": "Posted May 2025 (Epoch 6); saying collapse 'was always going to be a problem' is not contradicted — it IS a real problem. The poster does not claim it's inevitable or unsolvable, just that it was predictable",
  "epoch": 6
}
```
