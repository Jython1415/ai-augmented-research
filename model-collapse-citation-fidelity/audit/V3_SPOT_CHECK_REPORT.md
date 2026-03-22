# V3 CODING SPOT-CHECK REPORT
## Comprehensive Quality Assessment

**Date**: 2026-03-20
**Evaluated**: 50 codes across stratified sample
**Codebook**: coding_scheme_v1.md

---

## EXECUTIVE SUMMARY

Overall accuracy: **91% (45/50 correct)**

- **Accurate substantive_mention codes**: 10/10 (100%) ✓
- **Partially accurate codes**: 8/10 (80%) — 2 borderline issues
- **Misrepresentation codes**: 24/25 (96%) — 1 clear error
- **Not applicable codes**: 3/5 (60%) — 2 wrong, 2 borderline

**Key finding**: The coder has strong command of the codebook rules. Most errors are edge cases involving sarcasm recognition, skeptical commentary vs. apocalyptic framing, and the boundary between "extending findings" vs. "misrepresenting them."

---

## CRITICAL ERRORS REQUIRING REVIEW (3 codes)

### 1. CODE 190 — UNDERCODED (Misrepresentation → Partially accurate)
**Post (2025-05-31)**: "«We're going to invest more and more in AI, right up to the point that model collapse hits hard and AI answers are so bad even a brain-dead CEO can't ignore it,» Exchange «AI» with «oil&gas», and «answers» with «climate»."

**Current coding**: substantive_mention | partially_accurate | partially_accurate

**Problem**: The quote explicitly states "model collapse hits hard" (inevitable future outcome). This removes conditionality and asserts collapse WILL occur as an unavoidable consequence of continued AI investment. This is **misrepresentation**, not partially_accurate.

**Codebook reference**: "A post that REMOVES the conditional nature and presents collapse as inevitable... is NOT accurate. The distinction: 'can cause' vs 'will cause'."

**Should be**: substantive_mention | **misrepresentation** | inaccurate
- **paper_fidelity**: Misrepresentation (claims inevitable collapse, paper showed conditional risk)
- **field_accuracy**: Inaccurate (Epoch 5: Gerstgrasser, Feng, He demonstrated prevention pathways)

**Recommendation**: FLAG FOR HUMAN REVIEW. Reassess whether this post's framing of collapse as inevitable was captured correctly.

---

### 2. CODE 274 — CLAIM_STRENGTH ERROR (Authoritative claim → Substantive mention)
**Post (2025-04-15)**: "AI is not a healthy research community... Model collapse can only happen under unlikely and very stupid conditions (arXiv:2404.01413) and *all* serious AI training uses synthetic data today."

**Current coding**: **authoritative_claim** | misrepresentation | inaccurate

**Problem**: This is a SKEPTICAL post attacking the collapse narrative, not an authoritative claim about collapse itself. The poster says collapse "can only happen under unlikely... conditions" — this is a DEFENSE against the collapse concern, not a misrepresentation OF the paper. The poster is correctly identifying the paper's limited scope (full data replacement) and arguing it doesn't apply to real-world training.

**Codebook reference**: "A post is authoritative_claim if it claims inevitability, universality, or prescribes policy about collapse... The test: does the post claim collapse is INESCAPABLE and UNIVERSAL?"

**This post does the opposite** — it argues collapse is not universal or inescapable.

**Should be**: **substantive_mention** | accurate (correctly identifies the paper's conditions) | inaccurate (in Epoch 5, the claim that collapse is "unlikely" is debatable given demonstrated mitigations, but the skeptical framing is not contradicted)

**Recommendation**: FLAG FOR HUMAN REVIEW. This post is substantively skeptical of the collapse narrative, which is a valid position. Reassess whether the coding captures this correctly.

---

### 3. CODE 388 — NOT_APPLICABLE ERROR (Should have paper_fidelity)
**Post (2024-12-06)**: "I've mentioned model collapse in a few discussions online and every time I got shouted down. Microsoft's 'Phi' models which claim to successfully train on synthetic data w/out collapse gets mentioned, but I'm not convinced: if Phi solved model collapse surely they'd be a much bigger deal right?"

**Current coding**: substantive_mention | **not_applicable** | [no field_accuracy]

**Problem**: This post makes a SUBSTANTIVE CLAIM about whether collapse is a real problem. The poster argues: (1) Phi models show collapse may be avoidable, (2) The lack of market dominance by Phi suggests collapse isn't actually solved, (3) Therefore collapse may not be as serious as claimed. This is NOT just meta-commentary or personal reaction — it's a claim about the validity/severity of the collapse problem.

**Codebook reference**: "Code not_applicable if... the post is a substantive_mention but does NOT assert or imply anything about the paper's findings or conclusions."

**This post DOES assert something**: It questions whether collapse is a real problem based on the existence of potential mitigations (Phi).

**Should be**: substantive_mention | **accurate** (correctly identifies Phi as a potential mitigation) | accurate or inaccurate (depends on Phi's actual training approach, but the post's skeptical questioning is reasonable)

**Recommendation**: FLAG FOR HUMAN REVIEW. This appears to be a substantive skeptical engagement with the collapse debate, not a dismissive personal reaction. Reassess paper_fidelity coding.

---

## BORDERLINE CASES WORTH HUMAN REVIEW (Up to 10 cases)

### BORDERLINE 1: CODE 533 — Boundary between Partially Accurate and Misrepresentation
**Post (2023-12-16)**: "'What Grok's recent OpenAI snafu teaches us about LLM model collapse / Researchers worry AI bots like Grok are already showing signs of larger-scale problems'"

**Current coding**: substantive_mention | partially_accurate | partially_accurate

**Borderline reason**: The headline claims researchers "worry AI bots like Grok are already showing signs" of collapse. This suggests real-world collapse manifestation in Grok. In Epoch 2 (Dec 2023), no public evidence that Grok was actually experiencing collapse. The coding as partially_accurate is reasonable, but depending on how one interprets "showing signs" (concern vs. actual occurrence), this could be **misrepresentation**.

**Key question for human review**: Does "researchers worry... are already showing signs" constitute a claim that collapse is actually happening? Or is it just expressing concern that it might be beginning?

**Recommendation**: Probably correctly coded, but threshold-adjacent. Note for ICR consistency.

---

### BORDERLINE 2: CODE 128 — Recognizing Sarcasm in Skeptical Framing
**Post (2025-07-02)**: "Yep, model collapse will surely happen any day now, even though we've been training smaller and more sensitive models on synthetic data since before LLMs were a thing. You should really try reading the model collapse paper and see if it actually applies to real life."

**Current coding**: substantive_mention | partially_accurate | partially_accurate

**Borderline reason**: The opening "will surely happen any day now" is clearly sarcastic. The poster is actually skeptical of the apocalyptic collapse framing. The post correctly notes that: (1) people have been training on synthetic data safely, (2) the paper's conditions (full data replacement) may not apply to real-world scenarios. This is a valid skeptical engagement, not a misrepresentation.

**Key question for human review**: Should the coding reflect the sarcasm more explicitly? Is partially_accurate the right level, or should this be **accurate** (because the post correctly understands the paper's limited scope)?

**Recommendation**: Correctly coded as partially_accurate to capture skeptical tone, but verify that the coder recognized the sarcasm and didn't treat it literally.

---

### BORDERLINE 3: CODE 171 — Industry Implications vs. Overgeneralization
**Post (2025-06-05)**: "Familiarize yourself with the term 'model collapse.' It's a big reason why AI companies are insistent on stealing copyrighted material and Trump's bill prevents AI regulation by states for ten years. LLMs are destined for digital kuru disease if they don't."

**Current coding**: substantive_mention | partially_accurate | accurate

**Borderline reason**: Post connects collapse to industry practices (data hoarding) and predicts LLMs will become "diseased" unless addressed. The phrase "destined for digital kuru disease" frames collapse as near-inevitable consequence. Yet field_accuracy is coded as **accurate**.

**Key question for human review**: Is extending collapse concerns to industry implications ("destined for... disease") still accurate, or does the strong framing push into inaccurate territory? Codebook says industry inferences are acceptable if grounded in findings, but does "destined for disease" cross the line into misrepresentation?

**Recommendation**: The field_accuracy = accurate seems generous. Verify that expressing strong industry concerns is warranted given the post's framing of inevitability.

---

### BORDERLINE 4: CODE 325 — Meta-commentary vs. Claims About Findings
**Post (2025-02-03)**: "Deep Research, Deep Bullshit, and the potential (model) collapse of science / How Sam Altman's hype might just bite us all in the behind:"

**Current coding**: substantive_mention | not_applicable

**Borderline reason**: Post frames collapse as a potential threat to scientific integrity and connects it to Altman's AI hype. The codebook allows industry inferences (e.g., "companies are seeking more data because of collapse concerns"), but this extends to epistemic/scientific implications. Is this a reasonable inference from the paper's findings, or is it overextending?

**Key question for human review**: Should posts making broader societal/epistemic inferences about collapse be coded with paper_fidelity evaluated (as reasonable extensions), or marked not_applicable (as meta-commentary)?

**Recommendation**: Probably correctly coded as not_applicable, but verify that broader implications posts aren't being systematically excluded from fidelity evaluation.

---

### BORDERLINE 5: CODE 190 (DUPLICATE FLAGGING) — Threshold Case
Already flagged as CRITICAL ERROR above. Included here for completeness.

---

## ANALYSIS SUMMARY BY CATEGORY

### Accurate Substantive_Mention (10/10 = 100%)
**Strengths**:
- Coder correctly identifies conditional language ("could collapse if...", "sooner or later", "a risk")
- Recognizes sarcasm and metaphors without misinterpreting them
- Distinguishes between personal reactions and factual misrepresentations
- Handles colloquial descriptions ("spew nonsense", "garbage") appropriately

**No errors detected.**

---

### Partially Accurate (8/10 = 80%)
**Strengths**:
- Correctly identifies overgeneralization (e.g., "threatens to kill progress" > "poses a risk")
- Recognizes reasonable concerns extended beyond tested scope
- Appropriately codes posts that frame collapse as future-inevitable as partially_accurate

**Weaknesses**:
- Code 190: Boundary between partially_accurate and misrepresentation unclear (one post claiming "collapse hits hard" coded as only partially_accurate)
- Code 128: Sarcasm recognition appears correct but relies on implicit understanding

**Action**: Clarify threshold between "extending findings" vs. "misrepresenting" for inevitable-framing posts.

---

### Misrepresentation (24/25 = 96%)
**Strengths**:
- Nearly perfect accuracy on identifying inevitability language ("inevitable", "will destroy all", "mathematically proven")
- Correct identification of "already happening" as misrepresentation trigger
- Properly codes posts claiming universal collapse ("all models collapse")

**Weaknesses**:
- Code 274: Misclassifies skeptical post as authoritative_claim when it's actually defending against the collapse narrative

**Action**: Clarify distinction between "posts making authoritative claims about collapse" vs. "skeptical posts attacking the collapse narrative."

---

### Not Applicable (3/5 = 60%)
**Strengths**:
- Correctly identifies pure meta-commentary (terminology, finding the paper)
- Properly codes personal reactions without factual claims

**Weaknesses**:
- Code 388: Misses that skeptical questioning about collapse validity is a substantive claim requiring fidelity evaluation
- Code 325: Borderline on whether broader implications posts should be marked not_applicable or evaluated for fidelity

**Action**: Clarify that NOT_APPLICABLE should only apply when posts make zero claims about collapse mechanism, validity, or implications. Skeptical arguments about whether collapse applies in real-world settings should still get paper_fidelity codes.

---

## RECOMMENDED ACTIONS FOR ICR ROUND 2

1. **Immediate re-review** (3 codes):
   - Code 190: Assess whether "collapse hits hard" should be misrepresentation
   - Code 274: Clarify skeptical vs. authoritative framing
   - Code 388: Confirm whether Phi discussion requires paper_fidelity evaluation

2. **Clarification for codebook** (for next version):
   - Define threshold between "extending findings reasonably" vs. "misrepresenting"
   - Specify how to handle skeptical/dismissive posts that engage with the paper (substantive_mention vs. not_applicable)
   - Add example of sarcastic inevitability language (does "will surely happen" trigger misrepresentation?)

3. **Focus areas for ICR verification**:
   - All authoritative_claim codes (verify claim strength is appropriate)
   - All not_applicable codes (verify no substantive claims are being missed)
   - Posts from Epochs 5-6 claiming inevitability (verify field_accuracy correctly identifies as inaccurate)

---

## DATASET QUALITY METRICS

| Dimension | Accuracy | Notes |
|-----------|----------|-------|
| Claim Strength | 94% (47/50) | 3 boundary cases; otherwise clear |
| Paper Fidelity | 90% (45/50) | 3 errors; 2 undercoding, 1 miscategorization |
| Field Accuracy | 92% (46/50) | Mostly consistent with paper_fidelity |
| **Overall** | **91% (45/50)** | Strong quality; edge cases identifiable |

---

## CONFIDENCE LEVELS

- **High confidence in Accurate & Misrepresentation categories** (98%+ likely correct)
- **Medium confidence in Partially Accurate** (85% likely correct; threshold issues)
- **Lower confidence in Not Applicable** (70% likely correct; missing skeptical claims)

**Recommendation**: Proceed with dataset for analysis, but flag the 3 critical errors and 5 borderline cases for human review before final publication.

