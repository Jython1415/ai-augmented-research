# Model Collapse Literature Timeline: Ground-Truth Citation Standards

**Purpose**: At time T, what would an accurate citation of Shumailov et al. (2024) "AI models collapse when trained on recursively generated data" look like, given the state of the field?

---

## EPOCH 1: Pre-Discovery (Before May 2023)

### Papers Published
- **Hataya et al.** "Will Large-scale Generative Models Corrupt Future Datasets?" arXiv:2211.08095 (Nov 2022); published ICCV 2023 (Oct 2023). Empirical evidence that generated images negatively affect downstream model performance, with effects varying by task and contamination level.

### State of Knowledge
- Intuitive concern about synthetic data quality and downstream effects existed
- No formal theory or terminology for the phenomenon
- Generative models viewed primarily as tools for data augmentation
- Recursive training scenarios not yet systematized

### Accurate Citation at This Time
- "Empirical work (Hataya et al.) has shown that generated data can degrade downstream model performance, suggesting potential risks in feedback loops."
- Appropriately tentative; no established framework

### Oversimplification/Misrepresentation
- "Model collapse is inevitable" — no collapse framework existed yet
- Treating concerns as isolated, localized problems rather than systemic

---

## EPOCH 2: Discovery & Naming (May–Dec 2023)

### Papers Published
- **Shumailov et al.** "The Curse of Recursion: Training on Generated Data Makes Models Forget." arXiv:2305.17493 (May 27, 2023); later published *Nature* 631, 755–759 (Jul 25, 2024). DOI: 10.1038/s41586-024-07566-y. Demonstrates model collapse across VAEs, GMMs, and LLMs: tails of the original content distribution disappear irreversibly. The experimental design uses data replacement (each generation trained on previous generation's output only), though this methodological choice is not stated as a universal condition.

- **Alemohammad et al.** "Self-Consuming Generative Models Go MAD." arXiv:2307.01850 (Jul 4, 2023); published ICLR 2024. Introduces "Model Autophagy Disorder" (MAD); quality or diversity progressively decreases without sufficient fresh real data in each generation.

- **Bohacek & Farid** "Nepotistically Trained Generative-AI Models Collapse." arXiv:2311.12202 (Nov 20, 2023). Shows even 3% self-generated image contamination causes persistent model collapse.

- **Briesch et al.** "Large Language Models Suffer From Their Own Output." arXiv:2311.16822 (Nov 28, 2023). Documents LLM-specific collapse mechanisms; fresh real data slows but does not prevent collapse under certain configurations.

### State of Knowledge
- "AI is eating itself" narrative dominant in media and research
- Collapse understood as a serious concern under the tested conditions
- KEY EXPERIMENTAL SETUP: all studies used data replacement (old data discarded each generation). The alternative (accumulation) was not tested during this period
- Framed as an existential concern for synthetic data scaling

### Accurate Citation at This Time
- "Model collapse has been demonstrated across multiple architectures when models train recursively on their own output (Shumailov et al., 2023; Alemohammad et al., 2023)."
- Emphasizing collapse as a demonstrated concern under data replacement is appropriate
- Since no counterevidence existed yet, framing collapse as a serious concern (not a settled inevitability) is reasonable

### Oversimplification/Misrepresentation
- "All AI will inevitably collapse" — extrapolates beyond the tested conditions
- Claiming collapse applies to all data management strategies — the studies tested data replacement; alternatives were not examined
- Note: these oversimplifications were common in media coverage and are understandable given the alarming findings, but they go beyond what the papers actually demonstrated

---

## EPOCH 3: Theoretical Depth & First Counterarguments (Jan–Jun 2024)

### Papers Published
- **Dohmatob et al.** "Model Collapse Demystified: The Case of Regression." arXiv:2402.07712 (Feb 12, 2024); published NeurIPS 2024. Provides rigorous mathematical analysis with analytic formulae; identifies crossover phenomena from fast to slow collapse rates. Also proposes adaptive regularization as a mitigation strategy.

- **Dohmatob et al.** "A Tale of Tails: Model Collapse as a Change of Scaling Laws." arXiv:2402.07043 (Feb 10, 2024); published ICML 2024. Develops theoretical framework for collapse through scaling laws; discovers loss of scaling, shifted scaling, skill 'un-learning,' and grokking when mixing human and synthesized data. Validated on transformers and Llama2.

- **Gerstgrasser et al.** "Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data." arXiv:2404.01413 (Apr 1, 2024). **CRITICAL PIVOT**: Demonstrates that collapse is **NOT inevitable** under data **accumulation**; only under **replacement**. Test error converges to finite bound when real data is retained. Validated across language models, diffusion models, and VAEs.

- **Seddik et al.** "How Bad is Training on Synthetic Data?" arXiv:2404.05090 (Apr 7, 2024); published ICLR 2025. Demonstrates collapse is unavoidable with pure synthetic data; provides theoretical bounds on a maximal synthetic data fraction below which collapse can be avoided.

- **Peterson** "AI and the Problem of Knowledge Collapse." arXiv:2404.03502 (Apr 4, 2024); published in AI & Society (Springer). Introduces "knowledge collapse" — LLMs generating output toward the distribution center, neglecting long-tail knowledge. Conceptually related but distinct from statistical model collapse.

- **Feng et al.** "Beyond Model Collapse: Scaling Up with Synthesized Data Requires Verification." arXiv:2406.07515 (Jun 11, 2024); published ICLR 2025. Demonstrates that verification-based filtering of synthetic data prevents collapse; even imperfect verifiers provide protection.

### State of Knowledge
- **MAJOR SHIFT**: Collapse is **NOT inevitable under all conditions**
- The replacement vs. accumulation distinction is the critical differentiator
- Mitigation strategies exist: data accumulation, filtering, mixing ratio optimization
- Collapse is reversible if real data is reintroduced
- Mathematical foundations now rigorous; empirical findings no longer depend solely on specific setups

### Accurate Citation After Apr 2024
- "While Shumailov et al. demonstrated model collapse under data replacement, Gerstgrasser et al. (2024) showed that data accumulation prevents collapse, making the outcome dependent on data management strategy."
- The accumulation finding is a significant qualification of the original claim
- Collapse is real but conditional, not inevitable

### Note on Awareness
- Gerstgrasser et al. was an arXiv preprint (Apr 2024), not yet peer-reviewed. Researchers actively tracking the field would be aware; general audiences likely would not until later.
- This study codes accuracy against publicly available evidence, not expected awareness. A citation may be inaccurate relative to evidence while being understandable given information access.

### Oversimplification/Misrepresentation
- "Model collapse is inevitable" — contradicted by publicly available evidence as of April 2024
- Citing Shumailov et al. as the sole word on collapse without acknowledging the accumulation caveat
- The degree to which we expect awareness of a preprint is a contextual judgment — our coding scheme captures the accuracy of the claim, with demographic context as a moderating factor in analysis

---

## EPOCH 4: Nature Publication & Public Amplification (Jul–Sep 2024)

### Papers Published
- **Shumailov et al.** "AI models collapse when trained on recursively generated data." *Nature* 631, 755–759 (Jul 25, 2024). DOI: 10.1038/s41586-024-07566-y. Peer-reviewed publication of the arXiv preprint; massive media coverage and mainstream amplification of "AI is eating itself" narrative.

### State of Knowledge
- Shumailov et al. Nature publication receives enormous attention; becomes the canonical reference for model collapse in media and general audiences
- "AI will eat itself" narrative peaks in mainstream coverage
- **CRITICAL TIMING**: The Nature publication (Jul 2024) occurs 3 months *after* Gerstgrasser et al. (Apr 2024), yet the media narrative largely ignores the mitigation pathway
- Academic community is aware of the Gerstgrasser counterargument, but the public discussion lags

### Accurate Citation After Jul 2024
- "Shumailov et al. (2024, *Nature*) documented model collapse under recursive training with data replacement." — accurate
- Ideally also noting the accumulation caveat, though this was available only as a preprint (Gerstgrasser et al., Apr 2024)
- Citing Nature as an authoritative source is reasonable and standard academic practice

### Note on the Nature Publication
- The Nature paper presents the original findings under specific experimental conditions. It does not claim universality.
- Citing Nature without awareness of the Gerstgrasser preprint is understandable for general audiences but represents an incomplete picture relative to available evidence.

### Oversimplification/Misrepresentation
- "Nature proved model collapse is inevitable" — the paper demonstrates a mechanism under specific conditions, not a universal prophecy
- Using the Nature publication to make claims that go beyond what the paper itself states
- Using media headlines ("AI will eat itself") as grounds for technical claims about model training
- Note: citing Nature without mentioning preprint counterevidence is understandable behavior, but the claim's accuracy is assessed against the full body of publicly available evidence

---

## EPOCH 5: Refinement & Competing Results (Oct 2024–Feb 2025)

### Papers Published
- **Dohmatob et al.** "Strong Model Collapse." arXiv:2410.04840 (Oct 7, 2024); published ICLR 2025 Spotlight. Demonstrates even ~1% synthetic data can lead to model collapse where larger training sets no longer help. Finds larger models can amplify collapse, though beyond the interpolation threshold, they may partially mitigate it.

- **Kazdan et al.** "Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Generating World." arXiv:2410.16713 (Oct 22, 2024). Compares three scenarios: **replace** (collapse), **accumulate** (stable), **fixed-budget** (gradual rather than explosive degradation). Concludes collapse is avoidable through data management strategy.

- **Borji** "A Note on Shumailov et al. (2024)." arXiv:2410.12954 (Oct 16, 2024). Reanalyzes collapse through kernel density estimation (KDE); argues collapse is an inherent statistical consequence of iterative training on synthetic data.

- **He et al.** "Golden Ratio Weighting Prevents Model Collapse." arXiv:2502.18049 (Feb 25, 2025). Proves optimal weight for real data is the reciprocal of the golden ratio (≈0.618); validated experimentally.

### State of Knowledge
- Different mitigation strategies yield different safe fractions (scenario-dependent, not converging on a single number)
- Collapse is real but **mitigatable and scenario-dependent**
- Competing definitions of "collapse" become apparent (loss of tail behavior vs. memorization vs. generalization drop)
- Field is converging on: "It depends on the data strategy, contamination level, and definition of collapse"

### Accurate Citation After Oct 2024
- "Model collapse occurs under specific conditions: pure synthetic training (Shumailov et al., 2024), high contamination fractions (Dohmatob et al., 2024), and data replacement strategies (Gerstgrasser et al., 2024). Safe synthetic data fractions range from ~20% to ~33% depending on architecture and verification (Seddik et al., 2024; Feng et al., 2024; He et al., 2025)."
- Should cite multiple perspectives and emphasize scenario-dependence
- Appropriate to discuss both risks and mitigation pathways in equal detail

### Oversimplification/Misrepresentation
- "Model collapse is inevitable" — contradicted by accumulated body of evidence
- Citing Shumailov et al. alone as sufficient explanation — ignores Gerstgrasser et al., Dohmatob et al., and others that clarify necessary conditions
- Claiming a single "safe" synthetic data fraction — the evidence shows a range depending on filtering, accumulation, and verification strategies
- Treating all studies as addressing the same phenomenon — competing definitions undermine this assumption

---

## EPOCH 6: Definitional Crisis & Reconceptualization (Mar 2025+)

### Papers Published
- **Schaeffer et al.** "Position: Model Collapse Does Not Mean What You Think." arXiv:2503.03150 (Mar 5, 2025). **CRITICAL META-ANALYSIS**: Identifies eight distinct and often conflicting definitions of "model collapse" across the literature. Argues that inconsistent terminology has hindered comprehensive understanding and that many apparently contradictory results stem from different definitions. Concludes that several prominent collapse scenarios are readily avoidable, and that the threat has been 'warped from a nuanced multifaceted consideration into an oversimplified threat.'

- **Shi et al.** "A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective." arXiv:2509.16499 (Sep 2025). Identifies transition from generalization to memorization during collapse in diffusion models, driven by declining entropy of synthetic training data. Proposes entropy-based data selection to mitigate collapse.

### State of Knowledge
- The field recognizes that "model collapse" is **not a single, unified phenomenon**
- Different papers are answering different questions using different metrics
- Reproducibility issues in prior work partly attributable to definitional ambiguity
- Future work must specify which definition of collapse is being addressed
- The "AI is eating itself" narrative is now understood as collapse-in-one-specific-sense, not a universal truth

### Accurate Citation After Mar 2025
- For authoritative or technical claims: should acknowledge definitional ambiguity or specify which aspect of collapse is being discussed
- For casual discussion: "model collapse is a concern" is imprecise but not inaccurate; "model collapse has been proven inevitable" is inaccurate regardless of audience
- The field itself was conflating definitions pre-March 2025; holding casual discourse to a standard the field only recently achieved requires context
- Example: "Shumailov et al. (2024) documents the loss of tail distributions (distribution deformation collapse) when trained on pure synthetic data; this is distinct from scaling-law-based collapse (Dohmatob et al., 2024), both of which may or may not manifest as degraded test loss depending on contamination level."
- Should acknowledge that comparing results across papers requires aligning on definitions
- Acceptable to say "model collapse occurs" only in carefully scoped contexts with explicit definition

### Oversimplification/Misrepresentation
- Authoritative claims that treat "model collapse" as a single, settled phenomenon without acknowledging definitional complexity
- "Model collapse has been debunked" — equally inaccurate; the phenomenon is real under specific conditions
- Claiming one paper "contradicts" another without checking if they use the same definition
- Note: casual mentions (\"model collapse is a concern\") are imprecise but not necessarily inaccurate. The standard scales with the strength of the claim being made.

---

## Key Facts for Coding

These points are essential for accurately analyzing how Bluesky users cite the model collapse literature:

1. **The Replacement Setup is Critical (May 2023 – Apr 2024)**
   - Shumailov et al. and early work used data **replacement** (old data discarded each generation) as their experimental setup
   - Gerstgrasser et al. (Apr 2024) showed that **accumulation** prevents collapse
   - Claims of inevitability during May 2023–Apr 2024 are understandable (no counterevidence yet) but extrapolate beyond tested conditions
   - After Apr 2024, claiming inevitability is an oversimplification

2. **The Nature Publication Paradox (Jul 2024)**
   - Nature publication (Jul 2024) amplified a narrative that had already been challenged in peer review (Gerstgrasser et al., Apr 2024)
   - Media coverage peaked 3 months after scientific counterarguments
   - Citing Nature is reasonable academic practice; but "Nature proved collapse is inevitable" goes beyond what the paper claims

3. **Definitional Ambiguity Emerged Late (Mar 2025)**
   - Schaeffer et al. (Mar 2025) showed that "model collapse" is not a single thing
   - Before Mar 2025, papers were talking past each other without knowing it
   - After Mar 2025, authoritative claims should acknowledge definitional complexity; casual mentions are judged by claim strength, not academic precision

4. **Three Scenarios, Three Outcomes**
   - **Replacement** (old data discarded): collapse occurs (Shumailov et al., confirmed by Dohmatob et al.)
   - **Accumulation** (real data retained): stable or improving performance (Gerstgrasser et al., validated across architectures)
   - **Filtering/Verification** (low-quality synthetic data removed): collapse prevented (Feng et al., Seddik et al.)

5. **Safe Synthetic Data Fractions (Empirically Converging)**
   - Different studies report different safe thresholds depending on setup and mitigation strategy (Oct 2024 – Feb 2025)
   - Higher fractions risky without verification (Bohacek & Farid: 3% contamination causes distortion)
   - Optimal ratio ≈0.618 (golden ratio) proposed (He et al., Feb 2025)

6. **What Oversimplification Looks Like**
   - "AI will eat itself" (ignores accumulation, filtering, verification)
   - "Model collapse is inevitable" (contradicted after Apr 2024)
   - "Shumailov et al. proves model collapse is a problem" (true), "...and therefore we must stop using synthetic data" (non sequitur; ignores mitigation)
   - Citing Shumailov et al. without mentioning Gerstgrasser et al. (missing >50% of the evidence)

7. **Timeline for Accuracy Judgments**
   - **May 2023 – Mar 2024**: "Collapse is a serious concern" = accurate. "Collapse is inevitable" = extrapolation beyond tested conditions, but understandable given no counterevidence.
   - **Apr 2024 – Jun 2024**: "Collapse is inevitable" = inaccurate given available evidence (Gerstgrasser preprint). Awareness lag is a contextual factor.
   - **Jul 2024 – Feb 2025**: "Collapse is real under specific conditions, mitigable under others" = accurate. Citing Nature without caveats is understandable but incomplete.
   - **Mar 2025+**: Authoritative claims should acknowledge definitional complexity. Casual concern is not inaccurate.

8. **Paper Priority for Understanding the Field**
   - **Essential**: Shumailov et al. (2023/2024), Gerstgrasser et al. (2024), Schaeffer et al. (2025)
   - **Important for nuance**: Dohmatob et al. (Feb & Oct 2024), Seddik et al. (2024), Feng et al. (2024)
   - **Context**: Hataya et al. (2022), Alemohammad et al. (2023), Bohacek & Farid (2023), Briesch et al. (2023)

