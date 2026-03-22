# Wright & Wührl et al. (2024) Paper Research
## "Understanding Fine-grained Distortions in Reports of Scientific Findings"

**Paper Citation:** Wührl, Amelie; Wright, Dustin; Klinger, Roman; Augenstein, Isabelle (2024). Understanding Fine-grained Distortions in Reports of Scientific Findings. *Findings of the Association for Computational Linguistics: ACL 2024*, Bangkok, Thailand.

**arXiv:** https://arxiv.org/abs/2402.12431
**ACL Anthology:** https://aclanthology.org/2024.findings-acl.369/

---

## 1. ANNOTATION CATEGORIES (FOUR DIMENSIONS)

Based on web search results, the paper annotates scientific findings across four characteristics:

### Confirmed Dimensions:
1. **Causality** - Whether causal claims are distorted
2. **Certainty** - Whether confidence/certainty levels are altered
3. **Generality** - Whether scope of findings is expanded or reduced
4. **Sensationalism** - Whether findings are sensationalized

**STATUS:** Exact definitions per dimension not yet extracted from full paper. Need to consult Section 2 (Annotation Scheme) of the full PDF for precise definitions and operational criteria.

---

## 2. ANNOTATION LEVELS PER DIMENSION

**STATUS:** Not yet determined from available web sources.

Likely hypotheses based on similar science communication annotation schemes:
- Binary (distorted vs. not distorted)
- Ternary (understated, accurate, overstated)
- 5-point ordinal scale (various levels of distortion)

**ACTION NEEDED:** Check full paper methodology section for the exact scale used for each dimension.

---

## 3. INTER-CODER RELIABILITY (ICR) RESULTS

**STATUS:** Not extracted from web sources.

**ACTION NEEDED:** Check paper for Cohen's kappa, Fleiss' kappa, or Krippendorff's alpha scores per dimension.

---

## 4. ANNOTATION GUIDELINES & THRESHOLDS

**STATUS:** Not yet extracted from available sources.

### Key Information Needed:
- How is "inflated certainty" operationalized?
- What constitutes a threshold for marking a distortion?
- Are there quantitative boundaries (e.g., "increase in scope >10%")?
- Examples of edge cases and how they're classified

**ACTION NEEDED:** Consult the annotation guidelines document (likely in supplementary materials) or Appendix of the full paper.

---

## 5. ANNOTATION PROCESS DETAILS

### Dataset Size
- **1,600 instances** annotated
- Each instance: scientific finding from academic paper + corresponding report in news article or tweet
- Sources: Academic papers paired with news and social media reports

### Number of Annotators
**STATUS:** Not yet extracted from web sources.

**ACTION NEEDED:** Check methodology section for annotator count and their background/expertise.

### Training Process
**STATUS:** Not yet extracted from web sources.

Typical annotation training would include:
- Initial training rounds on a subset
- Regular IAA checks
- Refinement of guidelines based on disagreements

**ACTION NEEDED:** Consult full paper for specifics.

---

## 6. WORKED EXAMPLES

**STATUS:** Not yet located in available web sources.

**ACTION NEEDED:** Check Appendix or main paper body for examples showing:
- Before/after pairs (original finding vs. reported finding)
- Annotation decisions and rationales
- Edge cases

---

## 7. STRENGTHS & WEAKNESSES FOR SOCIAL MEDIA CITATION USE CASE

### Potential Strengths for Your Use Case:
1. **Fine-grained categorization** - Four distinct dimensions allow nuanced analysis beyond binary distortion
2. **Multi-channel data** - Includes both news articles AND tweets, relevant to social media
3. **Paired comparison framework** - Original academic paper vs. report methodology could work well for single-paper citations
4. **Structured annotation scheme** - If available as clear guidelines, could be reproducible for new domains
5. **Established baseline models** - Paper includes automatic detection baselines (fine-tuned models outperform LLM prompting)

### Potential Weaknesses for Social Media Citation Use Case:
1. **Domain mismatch** - Scheme designed for formal news articles and public tweets, may not account for informal discussion dynamics
2. **Single paper limitation** - Your use case focuses on citations of ONE paper; their scheme may assume fuller context of original research
3. **Replicability concerns** - If ICR is moderate, scheme may be difficult to apply consistently to new domains/annotators
4. **LLM performance** - Paper notes few-shot LLM prompting underperforms fine-tuned models; automation may be challenging
5. **Scale questions** - Unclear if scheme generalizes beyond the 1,600 instances they annotated
6. **Context dependency** - "Sensationalism" and "certainty" may be harder to judge in short social media excerpts vs. full articles

---

## CRITICAL GAPS TO RESOLVE

To fully utilize this paper for your research, you need to:

1. [ ] **Obtain exact dimension definitions** - Get precise operational criteria for each of the four dimensions
2. [ ] **Determine scale design** - Are they binary, ordinal, or other?
3. [ ] **Extract ICR statistics** - What reliability did they achieve? Is it sufficient for your purposes?
4. [ ] **Review annotation guidelines** - Get the actual decision rules and thresholds
5. [ ] **Study worked examples** - See real instances to understand edge cases
6. [ ] **Check supplementary materials** - Dataset documentation may contain codebook
7. [ ] **Review baseline results** - Understand how well automatic detection works

---

## RECOMMENDATIONS

**For Model Collapse Research Context:**

Given that your project analyzes citations of a single paper on social media, consider:

1. **Adaptation needed** - The Wright et al. scheme was designed for comparing academic findings to news/tweets. Your use case (how a specific paper gets distorted on Twitter) may need customization.

2. **Most relevant dimension** - "Certainty" and "Generality" may be most directly applicable. "Causality" and "Sensationalism" may require reframing.

3. **Integration approach** - Rather than using their scheme wholesale, consider:
   - Using their dimension framework as starting point
   - Adapting their definitions to your domain (social media discourse about ONE paper)
   - Piloting annotation with your dataset to test reliability
   - Comparing to their ICR as a benchmark

4. **Baseline comparison** - Their paper includes automatic detection baselines; if you pursue automation, their model architectures and findings (fine-tuned > LLM prompting) provide useful guidance.

---

## SOURCE MATERIALS CONSULTED

- ACL Anthology page: https://aclanthology.org/2024.findings-acl.369/
- arXiv abstract: https://arxiv.org/abs/2402.12431
- Authors' institutional repository: https://www.uni-bamberg.de/en/nlproc/resources/sciencecommdistortion/
- Author profile: https://dustinbwright.com/publication/2024-05-05-understanding-fine-grained-distortions

**Note:** This document was compiled from web-accessible sources. Full methodological details require reading the complete paper PDF and supplementary materials from the ACL Anthology or arXiv.
