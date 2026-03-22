# Biomedical Citation Error Taxonomy (Sarol et al. 2024)

**Source**: Assessing Citation Integrity in Biomedical Publications: Corpus Annotation and NLP Models
**Authors**: M. Janina Sarol et al.
**Publication**: Bioinformatics, 2024 Jun 26;40(7):btae420
**DOI**: Available at PMC11231046
**Data & Code**: https://github.com/ScienceNLP-Lab/Citation-Integrity

---

## Executive Summary

This paper presents a comprehensive 8-category error taxonomy for classifying citation accuracy problems in biomedical publications. The taxonomy organizes errors hierarchically into major (4 categories) and minor (4 categories) with explicit priority ordering. The study annotated 3,063 citations across 100 highly-cited biomedical publications, finding 39.18% contain accuracy errors.

---

## 1. EXACT 8-CATEGORY TAXONOMY

### Major Error Categories (Higher Priority)
1. **ACCURATE** — Citation context is consistent with reference article evidence
2. **CONTRADICT** — Citation context contradicts statements in the reference article
3. **NOT_SUBSTANTIATE** — Citation is relevant to reference but fails to substantiate all citing statements
4. **IRRELEVANT** — No corresponding information exists in reference article

### Minor Error Categories (Lower Priority)
5. **INDIRECT** — Evidence contains citations to other sources; reference is not original source
6. **OVERSIMPLIFY** — Reference findings are oversimplified or overgeneralized
7. **MISQUOTE** — Numbers or percentages are inaccurately cited
8. **ETIQUETTE** — Citation style is ambiguous; unclear what's being cited (common in multi-citations)

---

## 2. PRECISE DEFINITIONS AND DECISION RULES

### ACCURATE (Correct Citation)
**Definition**: The citation context is consistent with an evidence segment in the reference article.

**Decision Rule**: No discrepancy between cited statement and supporting evidence in reference.

### CONTRADICT (Major Error #1)
**Definition**: The citation context contradicts a statement made in the reference article.

**Priority**: Highest priority error category. Takes precedence over all other categories.

**Key Distinction from NOT_SUBSTANTIATE**: Direct logical contradiction vs. incomplete support. CONTRADICT is when the reference says something opposite or incompatible with the citation; NOT_SUBSTANTIATE is when the reference simply doesn't fully support the claim.

### NOT_SUBSTANTIATE (Major Error #2)
**Definition**: The citation is relevant to the reference article content but fails to support all statements in the citing paper.

**Decision Rule**: Reference article addresses the topic but lacks complete evidence for the citation's specific claims.

**Key Distinction from OVERSIMPLIFY**: NOT_SUBSTANTIATE = missing supporting evidence; OVERSIMPLIFY = evidence exists but is reduced in scope/generalizability.

### IRRELEVANT (Major Error #3)
**Definition**: There is no information in the reference article relevant to the citation.

**Decision Rule**: Complete absence of any corresponding content in reference article. No topical overlap.

**Priority Position**: Major error category; ranks above minor errors but below CONTRADICT.

### INDIRECT (Minor Error #1 — Extended Definition)
**Definition**: The evidence segment includes citations to other articles, indicating the reference is not the original source.

**Original Scope**: Historically applied only to review articles.

**Extended Scope (Sarol et al.): Now applies to "all types of reference articles."

**Decision Rule**: When evidence sentences in the reference article cite other works, the reference is serving as intermediary, not original source.

**Example Context**: Citing a statement attributed in the reference article to another paper.

### OVERSIMPLIFY (Minor Error #2)
**Definition**: The reference article's findings are oversimplified or overgeneralized in the citation.

**Decision Rule**: Evidence exists in reference but citation reduces, generalizes, or omits important qualifications, limitations, or nuance.

**Key Distinction from NOT_SUBSTANTIATE**:
- OVERSIMPLIFY: Evidence IS present but citation strips qualifications or scope
- NOT_SUBSTANTIATE: Evidence is ABSENT or incomplete for the claim

**Key Distinction from CONTRADICT**:
- OVERSIMPLIFY: Evidence supports general direction but citation removes caveats
- CONTRADICT: Evidence contradicts the claim itself

### MISQUOTE (Minor Error #3)
**Definition**: Numbers or percentages are inaccurately cited.

**Decision Rule**: Specific quantitative data (percentages, frequencies, measurements) are cited incorrectly in the citing paper.

**Specificity**: Applies only to quantitative distortions, not qualitative misstatements.

### ETIQUETTE (Minor Error #4 — Novel Contribution)
**Definition**: Citation style is ambiguous, making it unclear what exactly is being cited, often occurring in multi-citation contexts.

**Decision Rule**: Multiple citations bundled together without clear attribution; citation format creates ambiguity about which source supports which claim.

**Priority**: Lowest priority; when ETIQUETTE overlaps with other categories, the other category takes precedence.

**Context**: "Often occurring in multi-citations" — typical pattern is citation bundles like "(Smith et al., 2010; Jones et al., 2011)" where it's unclear which statement corresponds to which source.

---

## 3. DISTINGUISHING OVERSIMPLIFY FROM CONTRADICT

This addresses the **partially_accurate vs. inaccurate problem** mentioned in your request.

### CONTRADICT
- **Nature**: Logical opposition; direct contradiction
- **Evidence exists**: Yes, but says the opposite
- **Citation direction**: Claims what reference denies
- **Example**: Citation claims "X causes Y"; reference states "X does not cause Y"
- **Severity**: Major error (highest priority)

### OVERSIMPLIFY
- **Nature**: Reduction in scope, removal of qualifications, overgeneralization
- **Evidence exists**: Yes, supporting general direction
- **Citation direction**: Claims more broadly than reference warrants; removes caveats
- **Example**: Citation claims "X causes Y"; reference states "Under conditions A and B, X may cause Y" (citation omits conditions)
- **Severity**: Minor error
- **Interpretation**: Citation is not entirely false but lacks appropriate qualification

### KEY DISTINCTION
The critical difference is **scope and qualification**:
- **CONTRADICT**: Reference and citation point in opposite directions (binary)
- **OVERSIMPLIFY**: Reference and citation point same direction but citation removes important qualifiers, scope limitations, or context

This maps directly to your **partially_accurate vs. inaccurate** distinction:
- OVERSIMPLIFY represents **partially accurate** (directionally correct, contextually incomplete)
- CONTRADICT represents **inaccurate** (directionally wrong)

---

## 4. INTER-CODER RELIABILITY (ICR) PER CATEGORY

### Agreement by Task

**Citation Context Identification**: κ = 0.96 (high agreement)
- Annotators reliably identified which sentences constitute the citation context
- This is the most straightforward task

**Evidence Sentence Identification**: κ = 0.20 (phase 1) → κ = 0.37 (phase 2)
- Low agreement, improved with detailed guidelines
- Challenging because multiple sentences could be relevant
- Different annotators selected different evidence sentences for same citation

**Citation Accuracy Labels (Overall)**: κ = 0.18 (phase 1) → κ = 0.31 (phase 2)
- Very low agreement initially; modest improvement over annotation phases
- Authors acknowledge this was "lower than desired"
- Improvement attributed to refined annotation guidelines

### Notes on Reliability
- Agreement scores reported for first 30 reference articles only (phases 1-2)
- Full 100-article corpus ICR not reported separately by category
- Authors note that evidence and accuracy annotation tasks were particularly difficult
- Evidence disagreement (κ = 0.37) likely cascaded into accuracy label disagreement (κ = 0.31)

---

## 5. ERROR DISTRIBUTION ACROSS CATEGORIES

### Absolute Frequencies (n=3,063 total citations)

| Category | Count | Percentage |
|----------|-------|-----------|
| ACCURATE | 1,863 | 60.82% |
| CONTRADICT | 92 | 3.00% |
| NOT_SUBSTANTIATE | 243 | 7.93% |
| IRRELEVANT | 217 | 7.08% |
| OVERSIMPLIFY | 111 | 3.62% |
| MISQUOTE | 38 | 1.24% |
| INDIRECT | 82 | 2.68% |
| ETIQUETTE | 417 | 13.61% |
| **Total Errors** | **1,200** | **39.18%** |

### Distribution Insights

**Most Common Errors** (in descending order):
1. ETIQUETTE: 417 (13.61%) — ambiguous citation style/multi-citation issues
2. NOT_SUBSTANTIATE: 243 (7.93%) — incomplete evidence
3. IRRELEVANT: 217 (7.08%) — no corresponding info
4. OVERSIMPLIFY: 111 (3.62%) — overgeneralization
5. CONTRADICT: 92 (3.00%) — direct contradiction
6. INDIRECT: 82 (2.68%) — non-original sources
7. MISQUOTE: 38 (1.24%) — incorrect numbers/percentages

**Severity-Weighted Observation**:
- Major errors (CONTRADICT, NOT_SUBSTANTIATE, IRRELEVANT): 552 (18.02%)
- Minor errors (OVERSIMPLIFY, MISQUOTE, INDIRECT, ETIQUETTE): 648 (21.16%)
- Total errors: 1,200 (39.18%)

**Notable Pattern**: ETIQUETTE is the single largest error category, suggesting citation formatting/ambiguity is a major practical problem in biomedical publishing.

---

## 6. HANDLING BORDERLINE CASES

### Priority Ordering System

**Explicit Rule** (from paper):
> "Error categories above are listed in order of priority...contradictory errors are more problematic than etiquette errors"

When citations fit multiple categories, annotators apply **hierarchical priority**:

**Priority Order (Highest to Lowest)**:
1. CONTRADICT
2. NOT_SUBSTANTIATE
3. IRRELEVANT
4. INDIRECT
5. OVERSIMPLIFY
6. MISQUOTE
7. ETIQUETTE

### Decision Framework

When borderline, select the **highest-priority category** that applies.

**Example Case**: A citation could be both NOT_SUBSTANTIATE and INDIRECT
- Decision: Label as NOT_SUBSTANTIATE (higher priority)

**Rationale**: "Contradictory errors are more problematic than etiquette errors" — the framework assumes some error types are more serious and should take precedence in annotation.

### Annotation Process for Ambiguous Cases

Annotators were provided:
- Citation marker and containing paragraph from citing article (highlighted)
- Full text of reference article
- Instruction to identify up to 5 evidence segments
- Instruction to select only one accuracy label

Multiple evidence segments could support the same citation (leading to disagreement on exact evidence location), but final label was always singular.

---

## 7. ANNOTATION GUIDELINES AND DECISION TREES

### Core Annotation Process

**Inputs Provided to Annotators**:
1. Citation marker (location in citing paper)
2. Paragraph containing the citation (with marker highlighted)
3. Full text of reference article
4. Up to 5 evidence segments allowed
5. Single accuracy label required

### Annotation Challenges Identified

**Problem 1: Evidence Identification**
- Challenge: Long full-text articles make locating relevant evidence difficult
- Challenge: Multiple sentences can support same citation
- Challenge: Annotators might select different relevant sentences
- Consequence: Led to low inter-annotator agreement (κ = 0.20–0.37)

**Solution Applied**:
- Provided detailed annotation guidelines
- Required annotators to read reference papers carefully
- Improved agreement from 0.20 to 0.37 (phase 2)

**Problem 2: Citation Context Identification**
- Challenge: Determining which sentences constitute the "citation context"
- Result: Actually HIGH agreement (κ = 0.96) — this task is straightforward

**Problem 3: Cross-Document Annotation Tool Support**
- Challenge: Existing tools (brat) inadequate for annotating relationships across documents
- Solution: Repurposed and post-processed brat annotations

### Annotation Guidelines Evolution

- Initial guidelines led to κ = 0.18–0.20 for accuracy labels
- Refined guidelines (post-phase 1) led to κ = 0.31 for accuracy labels (phase 2)
- Full taxonomy refined to 8 categories through iterative annotation
- ETIQUETTE added as novel category during annotation process
- INDIRECT definition extended to all reference types (not just reviews)

---

## 8. MAPPING TO YOUR USE CASE (Model Collapse Research)

### Applicability to Model Collapse Discourse Analysis

This taxonomy is highly relevant to model collapse discourse analysis, where distinguishing between accurate citations, partially accurate claims, and inaccurate claims is critical.

**Direct Mappings to Your Codebook**:

| Biomedical Category | Your Use Case | Application |
|-------------------|---------------|------------|
| ACCURATE | Accurate citation | Claims properly support evidence |
| OVERSIMPLIFY | Partially accurate | Claims remove qualifications/nuance from evidence |
| NOT_SUBSTANTIATE | Partially accurate / Unsupported | Evidence incomplete or absent |
| CONTRADICT | Inaccurate | Claim contradicts evidence |
| IRRELEVANT | Unsupported | No evidence in source for claim |
| MISQUOTE | Inaccurate | Quantitative distortion |
| INDIRECT | Evidence-chain issue | Not citing original source |
| ETIQUETTE | Ambiguous reference | Unclear what's being cited |

### Key Insights for Your Work

**1. The Partially Accurate Problem**
The biomedical paper shows this is a real, difficult annotation challenge. Their OVERSIMPLIFY category explicitly captures the scenario where:
- Evidence exists
- Citation is directionally correct
- But qualifications/scope removed
- Result: Not fully false, not fully true

**2. Low Agreement is Expected**
Your ICR challenges (κ = 0.31–0.37 for accuracy) are normal for this task. The biomedical study found similar difficulties despite being well-resourced.

**3. Priority Ordering Matters**
When categories overlap (common in real data), explicit priority rules prevent annotation chaos. Your codebook would benefit from similar hierarchical rules.

**4. ETIQUETTE/Ambiguity is Common**
The biomedical study found ETIQUETTE was the most frequent error (13.61%). This suggests citation/reference ambiguity is a major practical problem. For model collapse discourse, tracking which claims vs. which sources is equally critical.

**5. Evidence Identification is Hard**
Low agreement on evidence selection (κ = 0.20–0.37) suggests:
- Multi-sentence evidence is inherently ambiguous
- Iterative refinement helps (moved from 0.20 to 0.37)
- This may be a fundamental limit, not a guideline problem

**6. Context-Dependent Distinctions**
OVERSIMPLIFY vs. CONTRADICT distinction depends on reading the reference carefully to determine if:
- Direction is same + qualifications removed = OVERSIMPLIFY
- Direction is opposite = CONTRADICT

For model collapse claims about LLM behavior, similar careful reading is needed to distinguish overstatement from false claims.

### Recommendations for Your Codebook

1. **Adopt priority ordering**: When borderline, specify hierarchy (e.g., INACCURATE > PARTIALLY_ACCURATE > ACCURATE)
2. **Explicit decision rules**: Define what counts as "qualification" or "scope" in your domain
3. **Detailed guidelines with examples**: Invest heavily; this improves agreement more than tight rules
4. **Plan for lower ICR**: Budget for κ = 0.30–0.40 on primary accuracy labels
5. **High-agreement proxy**: Use "citation context identification" type tasks (high agreement) for initial training
6. **Evidence chains**: Track whether claims cite original evidence or filtered evidence (INDIRECT equivalent)
7. **Ambiguity category**: Include something like ETIQUETTE for when claim-source mapping is unclear

---

## References

Sarol, M. J., et al. (2024). Assessing citation integrity in biomedical publications: Corpus annotation and NLP models. *Bioinformatics*, 40(7), btae420. doi:10.1093/bioinformatics/btae420

GitHub Repository: https://github.com/ScienceNLP-Lab/Citation-Integrity

PubMed Central: https://pmc.ncbi.nlm.nih.gov/articles/PMC11231046/

---

## Document Metadata

- **Extracted**: 2026-03-20
- **Source Paper Published**: 2024-06-26
- **Total Corpus**: 100 biomedical articles, 3,063 citations
- **Error Rate**: 39.18% (1,200 citations with errors)
- **Data Availability**: Open source (GitHub)
- **Reproducibility**: Full corpus and best NLP model publicly available
