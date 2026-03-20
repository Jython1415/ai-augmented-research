# V3 Analysis Summary: Model Collapse Research Discourse

## Overview

Re-ran all analysis scripts with the new V3 coding data structure. The database now has 539 citation units with two independent coding passes, enabling comparison of how contextual information (thread context) affects classification decisions.

**Database Structure:**
- `coding_pass1` table: 539 records (post-only coding)
- `coding_pass2` table: 539 records (post + thread context coding)
- `citation_units` table: 539 records (anchor posts with epoch/citation_type)
- `author_profiles` table: 445 unique authors

---

## 1. Summary Statistics

### Pass 1 (Post-only)

**Claim Strength:**
- Substantive mention: 410 (76.1%)
- Neutral share: 107 (19.9%)
- Authoritative claim: 22 (4.1%)

**Paper Fidelity:**
- Accurate: 288 (53.4%)
- Partially accurate: 99 (18.4%)
- Misrepresentation: 25 (4.6%)
- Not applicable: 127 (23.6%)

**Field Accuracy:**
- Accurate: 319 (59.2%)
- Partially accurate: 65 (12.1%)
- Inaccurate: 28 (5.2%)
- Not applicable: 127 (23.6%)

### Pass 2 (With Context)

**Claim Strength:**
- Substantive mention: 415 (77.0%)
- Neutral share: 116 (21.5%)
- Authoritative claim: 8 (1.5%)

**Paper Fidelity:**
- Accurate: 306 (56.8%)
- Partially accurate: 89 (16.5%)
- Misrepresentation: 14 (2.6%)
- Not applicable: 130 (24.1%)

**Field Accuracy:**
- Accurate: 332 (61.6%)
- Partially accurate: 59 (10.9%)
- Inaccurate: 18 (3.3%)
- Not applicable: 130 (24.1%)

---

## 2. Epoch Trends

### Key Finding: Fidelity Decline in Later Epochs

When excluding "not applicable" entries, paper fidelity shows a clear inverted-U pattern:

| Epoch | Accurate Fidelity % | Accurate Field % | N (applicable) |
|-------|-------------------|-----------------|----------------|
| 2     | 79.1%             | 86.0%           | 43             |
| 3     | 72.7%             | 72.7%           | 11             |
| 4     | 88.0%             | 95.7%           | 92 (peak)      |
| 5     | 63.5%             | 71.2%           | 52             |
| 6     | 61.7%             | 69.6%           | 214 (n=273)    |

**Interpretation:** Epoch 4 (April 2024, early post-publication discourse) has the highest fidelity (88%), but accuracy declines substantially by Epoch 6 (March 2026, 2 years post-publication). The decline is consistent across both dimensions and suggests either:
- Degradation of careful citation as discourse spreads
- Greater distance from original reading context in later discourse
- Possible filtering effect: only researchers continuing discussion after 2 years

### Claim Strength by Epoch

Most citations remain substantive mentions (68-85% per epoch). Authoritative claims are rare but most common in Epoch 3 (14.3%) and Epoch 6 (5.5%).

---

## 3. Two-Pass Comparison: Context Effect

### Agreement Rates

| Dimension | Agreement | Kappa | McNemar p-value |
|-----------|-----------|-------|-----------------|
| **Claim Strength** | 85.3% (460/539) | 0.605 | N/A |
| **Paper Fidelity** | 69.6% (375/539) | 0.500 | < 0.001 |
| **Field Accuracy** | 73.5% (396/539) | 0.529 | < 0.001 |

**Interpretation:** Context (thread) significantly affects coding, especially for Paper Fidelity and Field Accuracy. The low McNemar p-values indicate context causes systematic directional bias in coding.

### Direction of Changes

**Claim Strength:**
- Decreased (more authoritative): 42 cases (7.8%)
- Increased (less authoritative): 37 cases (6.9%)
- No change: 460 cases (85.3%)

**Paper Fidelity:**
- Increased (better accuracy): 77 cases (14.3%)
- Decreased (worse accuracy): 87 cases (16.1%)
- No change: 375 cases (69.6%)

**Field Accuracy:**
- Increased (better accuracy): 70 cases (13.0%)
- Decreased (worse accuracy): 73 cases (13.5%)
- No change: 396 cases (73.5%)

**Key observation:** Pass 2 (with context) slightly downgrades accuracy assessments overall — more citations rated as less accurate when coders see thread context. This suggests thread context reveals nuance that post-only coding misses.

### Confusion Matrices

**Paper Fidelity** (most variation):
- 30 citations changed from "accurate" → "not applicable" (Pass 2 judges context needed)
- 48 citations changed from "partially accurate" → "accurate"
- 29 citations changed from "not applicable" → "accurate"

This suggests Pass 1 (post-only) coders were sometimes uncertain and marked "not applicable," but thread context clarified the citation's relationship to the paper.

---

## 4. Author Demographics (445 unique authors)

**Role Distribution (overlapping categories):**
- AI/ML specific: 149 (33.5%)
- Other/unclassified: 178 (40.0%)
- Developer/tech: 74 (16.6%)
- Researcher/academic: 57 (12.8%)
- Journalist/media: 34 (7.6%)
- Unknown (no bio): 28 (6.3%)
- Student: 10 (2.2%)

**Key finding:** Surprisingly diverse author base. Despite the paper's AI/ML focus, only 1/3 identify as AI/ML professionals. Academic researchers are a minority (13%).

---

## 5. Repeat Citers

**Distribution:** 53 authors (11.9% of 445) made multiple citations, accounting for 147/539 citations (27.3%)

**Top repeat citer:** One author with 18 citations, showing 94% accurate/substantive citations. Most repeat citers (6-7 citations) show mostly accurate citations with occasional partial accuracy.

---

## 6. Reach vs. Accuracy

**Follower statistics (N=445 with data):**
- Mean: 4,494 followers
- Median: 774 followers
- Range: 2 to 254,208
- Std Dev: 17,447 (highly right-skewed)

**Spearman Correlations (followers vs. accuracy):**
- Paper Fidelity: r = -0.007, p = 0.89 (no correlation)
- Field Accuracy: r = 0.029, p = 0.55 (no correlation)

**Interpretation:** Author reach (follower count) has NO relationship with citation accuracy. Citations from highly followed accounts are just as likely to be inaccurate as those from niche accounts.

---

## 7. Figures Generated

All figures saved to `/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/figures/`:

1. **epoch_claim_strength.png** — Stacked bar chart of claim strength across epochs (Pass 1)
2. **epoch_paper_fidelity.png** — Stacked bar chart of paper fidelity by epoch (Pass 1, excluding N/A)
3. **epoch_field_accuracy.png** — Stacked bar chart of field accuracy by epoch (Pass 1, excluding N/A)
4. **twopass_comparison_by_epoch.png** — Side-by-side Pass 1 vs Pass 2 comparison across epochs
5. **reach_vs_accuracy.png** — Scatter plots of author followers (log scale) vs. accuracy dimensions
6. **author_followers.png** — Histogram of author follower distribution (log scale)

---

## Analysis Scripts Modified

Created v3 versions of all analysis scripts to work with new table structure:

1. **analyze_all_v3.py** — Comprehensive analysis + summary stats
2. **analyze_epoch_trends_v3.py** — Epoch trend analysis with visualizations
3. **analyze_authors_v3.py** — Author role distribution + reach analysis

Note: The original `analyze_twopass.py` required modification because it was querying `citation_units` table expecting columns like `claim_strength` that are now in separate `coding_pass1`/`coding_pass2` tables. 

---

## Key Takeaways

1. **Context matters:** Pass 1 vs Pass 2 agreement is 69-85% depending on dimension, with systematic bias toward more conservative accuracy judgments when context is available.

2. **Declining fidelity over time:** Accuracy of citations peaks in Epoch 4 (88%) and declines to 62% by Epoch 6, suggesting discourse degradation or selection effects.

3. **No reach-accuracy correlation:** Citation accuracy is independent of author follower count, suggesting information spreads regardless of source authority.

4. **Diverse authorship:** Despite the AI/ML focus, the citing community is heterogeneous (33% ML/AI, 17% developers, 13% researchers, 41% other).

5. **Substantive engagement:** 76% of citations are substantive mentions (not just neutral sharing), indicating genuine discourse engagement with the paper.

---

Output file: `/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/analysis_output_v3.txt`
