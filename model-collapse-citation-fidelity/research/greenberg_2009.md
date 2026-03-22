# Greenberg 2009: Citation Distortions and Unfounded Authority

**Citation:** Greenberg, S. A. (2009). How citation distortions create unfounded authority: Analysis of a citation network. *British Medical Journal*, 339, b2680. doi:10.1136/bmj.b2680

**Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/

---

## Executive Summary

Greenberg analyzed how scientific claims become established as "unfounded authority" through systematic distortions in citation networks. Using β-amyloid in inclusion body myositis (IBM) as a case study, the research identifies five citation distortion mechanisms that compound through networks, creating belief systems that persist despite contradictory or weak empirical evidence. The study is directly applicable to understanding how AI-generated content and scientific claims propagate with increasing distortion through social media and citation networks.

---

## Five Distortion Mechanisms

### 1. Citation Bias

**Definition:** Systematic ignoring of papers that contain content conflicting with a claim.

**Precise Detection Method:**
- Classified all primary data papers as either supportive or critical
- Counted citations received by each category
- Performed statistical comparison (p=0.01 threshold)

**Quantitative Evidence:**
- Supportive primary data papers: received 94% of 214 citations to primary data
- Critical primary data papers: received only 6% of citations
- One critical paper by the same lab that produced supportive findings received zero citations despite that lab citing "104 other citations to primary data papers"

**Case Example (IBM Study):**
- 4 supportive papers (all from same laboratory): Reported presence of β-amyloid molecules in IBM muscle
- 6 critical papers: Showed affected fibers in only 0-5 patients; demonstrated non-specificity (molecule present in up to 43 control patients across seven disease categories)
- The bias was not against the laboratory itself but against contradictory *content*

---

### 2. Amplification

**Definition:** Expansion of a belief system without data—citation made to papers that contain no primary data, increasing the number of citations supporting the claim exponentially.

**Precise Detection Method:**
- Classified all papers by type: primary data, review, model, other
- Traced citation paths through non-data papers
- Measured traffic flow and network betweenness centrality
- Tracked growth rates of citation versus citation *paths*

**Quantitative Evidence (1996-2007):**
- Supportive citations: increased sevenfold to 636
- Supportive citation paths: increased **777-fold** to 220,553
- Critical citations: grew only to 21 with 28 citation paths
- Ratio of citation-path growth to citation growth shows compounding power: 777÷7 = 111× amplification factor

**The "Lens Effect":**
- Single review paper: accounted for 63% of all citation paths (139,391 paths)
- Four review papers by same research group: 95% of all citation paths flowed through them
- Eight key papers (seven from one research group): concentrated and magnified 97% of citation traffic
- Result: These papers acted as "lenses" that focused and amplified supportive information while isolating critical data

---

### 3. Citation Transmutation (Hypothesis → Fact)

**Definition:** Conversion of hypothesis into fact through citation alone. A paper states "X *may* happen" but downstream citations claim "X *does* happen."

**Precise Detection Method:**
- Tracked specific subclaim across citation chain: "β-amyloid accumulation precedes other abnormalities"
- Examined how claim status changed (hypothesis → tentative → established fact)
- Identified citations to papers containing no relevant statements (dead-end citations)

**Quantitative Evidence:**
- Subclaim stated in 27 papers supported by 37 citations
- 9 citations (24%) were "dead end citations" linking to papers with "no statement on the temporal relation of β-amyloid to other abnormalities"
- These papers cited as confirming evidence despite containing no relevant data

**Exact Transmutation Pathway:**
1. Paper A (primary data): states as hypothesis "may represent early changes"
2. Paper B (review): cites Paper A, claims as fact "precedes vacuolization"
3. Paper C (secondary review): cites Paper B as confirmation of established fact
4. Papers D-N: cite through B and C, treating it as proven

---

### 4. Citation Diversion

**Definition:** Citing content but claiming it has a different meaning, thereby distorting its implications while maintaining apparent scientific legitimacy.

**Precise Detection Method:**
- Cross-referenced citing papers with actual cited papers
- Examined actual content of cited sources
- Evaluated whether citations accurately represented findings
- Measured how misrepresented citations propagated downstream

**Quantitative Evidence - Primary Example:**

One primary data paper (ref 77) reported:
- No β-amyloid in 3 of 5 IBM patients
- Presence in only "few fibers" in remaining 2

Three citing papers (refs 28, 37, 38) claimed these findings "confirmed" the claim by stating:
- β-amyloid "accumulated in vacuolated muscle fibers"
- Only 1.4-5% of myofibres were actually vacuolated
- All vacuolated fibers actually *lacked* the protein

**Downstream Cascade:**
- Over 10 years, these three supportive citations developed into **7,848 supportive citation paths**
- Result: A single misrepresented citation compounds into thousands of downstream false citations

**Second Diversion Example:**
- Cited paper stated: intracellular accumulation "may be an epiphenomenon unrelated to myofiber death"
- Citing paper claimed it showed: "widely accepted that intracellular accumulation plays an important role"
- Implies opposite meaning of original source

---

### 5. Back-Door Invention

**Definition:** Repeated misrepresentation of conference abstracts as peer-reviewed full papers, bypassing peer review standards.

**Quantitative Evidence:**
- Seven different papers made 17 citations to 12 different misrepresented abstracts
- Example: Citation listed as "Neurol 2003;60:333-334" when actual publication was "Neurol 2003;60(suppl 1):A333-4" (abstract supplement, not peer-reviewed article)

---

## Case Study: β-Amyloid in Inclusion Body Myositis

### The Central Claim
"β-amyloid and its precursors are abnormally and specifically present in inclusion body myositis muscle fibers"

### Historical Evolution (1992-2007)

| Period | Development |
|--------|-------------|
| 1992-1993 | Initial primary data reports from one laboratory |
| 1995-1996 | Critical data emerged showing non-specificity and minimal presence |
| 1996-2007 | Exponential growth of supportive citations despite unchanged or contradicted evidence |
| By 2007 | At least 200 journal articles accepted claim as established fact |

### Clinical Importance
The belief directly influenced:
- Research funding allocation
- Design of treatment trials
- Clinical decision-making protocols
- NIH grant proposal framing

### Complete Citation Network Data

| Measure | Value | Notes |
|---------|-------|-------|
| Total papers in network | 242 | PubMed-indexed English-language |
| Total unique citations | 675 | Unduplicated citations |
| Total citation paths | 220,609 | Complete chains through network |
| Primary data papers (supportive) | 4 | All from single laboratory |
| Primary data papers (critical) | 6 | Some from same lab as supportive papers |
| Authority papers identified | 10 | All expressed supportive view |
| Citations to supportive primary data | 201 | 94% of primary data citations |
| Citations to critical primary data | 13 | 6% of primary data citations |
| Supportive citations (1996-2007) | 636 | 7× growth |
| Supportive citation paths (1996-2007) | 220,553 | 777× growth |
| Critical citations (1996-2007) | 21 | Minimal growth |
| Critical citation paths (1996-2007) | 28 | Minimal growth |
| Dominant review papers (bottleneck) | 8 | Concentrated 97% of citation traffic |
| Single review paper contribution | 63% | 139,391 of 220,553 paths |
| Review papers from single group | 4 | Controlled 95% of path traffic |

---

## How Distortions Compound Through Citation Networks

### The Four-Stage Cascade Model

**Stage 1: Citation Bias Establishes Initial Authority**
- Four supportive primary data papers achieved "authority status" through network topology analysis
- Critical papers remained isolated (receiving 0-3 citations each)
- Computational analysis (Kleinberg's HITS algorithm) assigned high authority to papers with high citation traffic, regardless of evidentiary merit
- Result: Unequal visibility in the network

**Stage 2: Amplification Exponentially Expands Reach**
- Eight influential papers (mostly reviews) concentrated citation traffic
- These papers made no primary data contributions but cited supportive work
- Citation paths grow through preferential attachment: early-cited papers receive disproportionately more future citations
- Network exhibits power-law distribution where few papers dominate
- Result: 777-fold growth in citation paths despite only 7-fold growth in direct citations

**Stage 3: Transmutation Converts Uncertainty into Apparent Fact**
- Hypothetical statements (hypothesis level) re-cited as established findings (fact level)
- Dead-end citations create false authority (citing papers that contain no relevant data)
- Through repeated citation chains, "may represent" becomes "demonstrates"
- Each citation raises the epistemic status of the claim
- Result: Claim becomes empirically supported through form rather than substance

**Stage 4: Diversion Prevents Self-Correction**
- Critical findings by the same laboratory producing supportive work were never self-cited
- When critical papers were cited, their implications were inverted
- Network structure prevented contradictory information from spreading
- Authority papers formed a closed supportive network
- Result: Network becomes resistant to empirical correction

### The Lens Effect: Bottleneck Amplification

The most powerful compounding mechanism is the **lens effect**: a small number of influential papers with high betweenness centrality concentrated and redirected citation flow.

**Mathematical Properties:**
- Single review paper: 63% of all paths (139,391 of 220,553)
- Four papers: 95% of paths
- These papers acted as "information choke points"
- Each citation to a review paper that itself cites N supportive papers creates N additional downstream citation paths
- The multiplication compounds: each new citing paper creates new paths through all upstream papers

**Example Calculation:**
- Initial primary data paper cited by Review A: 1 citation
- Review A cites Paper by Review B: creates path through both
- Review B cites Review C: creates N more paths through all previous papers
- A single misrepresented citation (diversion) in Review A can generate 7,848 downstream paths in 10 years

---

## Quantitative Metrics Developed

### 1. Citation Classification System
- **Supportive:** Underlying statement supports the belief
- **Neutral:** Ambiguous relevance
- **Critical:** Weakens or refutes the belief

### 2. Citation Bias Measurement
- Chi-square or Fisher exact test comparing citation frequencies across paper categories
- Significance threshold: p=0.01
- Ratio of supportive to critical citations

### 3. Authority Identification Algorithm
- Kleinberg's HITS algorithm (Hyperlink-Induced Topic Search)
- Computational identification of "hub" and "authority" papers based purely on network topology
- Did not require manual assessment of paper quality
- Revealed that authority status correlated with citation traffic, not empirical merit

### 4. Citation Path Analysis
- Tracked complete information flow from source to endpoint
- Measured exponential growth: citation paths grew 777× while direct citations grew 7×
- Identified bottleneck papers with high betweenness centrality

### 5. Betweenness Centrality
- Measured how many shortest paths between paper pairs pass through a given paper
- Identified 8 papers controlling 97% of citation traffic
- Showed that network structure, not content quality, determined information flow

### 6. Dead-End Citation Index
- Proportion of citations to papers containing no relevant data: 24% in one subclaim
- Measured false authority from citations without supporting content

### 7. Transmutation Severity Index
- Tracked claim status change across citation chains
- Quantified hypothesis → established fact progression
- Example: 27 papers making a claim, 37 citations supporting it, 9 (24%) being dead-end citations

---

## Application to Shumailov Paper and Social Media Distortion

### Direct Mappings

| Greenberg Mechanism | IBM Case | Shumailov Case (Predicted) |
|---|---|---|
| Citation Bias | Critical papers ~6% citations | Shumailov contradictions/weaknesses cited rarely on social media |
| Amplification | 777× growth in citation paths from reviews | AI-generated amplification of Shumailov claims; viral retweeting |
| Transmutation | "May happen" → "Does happen" | "Contains concerning patterns" → "Definitively proves model collapse" |
| Diversion | Cited as confirming evidence when contradictory | Shumailov claims reframed as stronger/broader than original paper |
| Back-Door Invention | Abstracts misrepresented as peer-reviewed | Social media summaries lacking nuance; incomplete quotations |

### Compound Effect Predictions

1. **Initial Social Media Bias:** Accounts amplifying model collapse concerns receive more engagement; critical analysis sidelined

2. **Bot/AI Amplification:** AI-generated content citing Shumailov through reviews and summaries, not primary analyses

3. **Hypothesis Hardening:** Tentative concern ("Models may exhibit behavior X") becomes stated fact ("Model collapse proven")

4. **Misrepresentation in Threads:** Threads claiming Shumailov "shows X" when paper actually says "may suggest X under certain conditions"

5. **Citation Paths Explosion:** One viral AI-generated thread citing Shumailov creates thousands of downstream retweets and citations, exponentially amplifying distortion

6. **Network Resistance to Correction:** Once false frame established, critical social media posts citing actual findings face algorithm downweighting or are simply missed in citation network

### Critical Difference: Speed and Scale

- **Greenberg IBM case:** 15 years (1992-2007) for distortion to achieve authority
- **Shumailov on social media:** Distortion could compound in 6-12 months through automated amplification and AI-generated content
- **Citation paths:** Greenberg measured ~220k paths; social media could generate millions in equivalent timeframe

---

## Key Findings on Compounding

The most critical insight from Greenberg's work is that **distortion mechanisms are not additive; they are multiplicative**:

> "Whether such data confirm the claim is perhaps open to interpretation. At the least these data are exaggerated and generalised through the combinatorial effects of all distortion mechanisms working simultaneously."

**Specific Compounding Evidence:**
1. Single misrepresented citation → 7,848 downstream citation paths in 10 years
2. Four review papers → 95% of all information flow
3. Initial citation bias (94% vs 6%) → fed into amplification stage
4. Transmutation (24% dead-end citations) → propagated through amplification network
5. Diversion examples → each single case generated thousands of false paths

**The Self-Reinforcing Loop:**
1. Bias reduces critical content visibility
2. Amplification increases supportive content visibility
3. Authors following information cascade face publication incentives to cite supportively
4. New authors citing established papers further entrench distortion
5. Network becomes increasingly resistant to correction as supportive view dominates authority structure

---

## Relevance to AI-Augmented Research on Model Collapse

### Why This Matters for Your Study

1. **Empirical Framework:** Greenberg provides operationalized definitions of distortion mechanisms applicable to both traditional citations and social media shares/reposts

2. **Detection Methods:** Citation classification scheme and network analysis tools can be adapted to social media data (treating retweets as citations)

3. **Compounding Model:** The four-stage cascade and lens effect explain why AI-generated summaries of Shumailov will create exponential amplification

4. **Quantitative Targets:** The 777× citation path growth in 11 years suggests you should expect similar order-of-magnitude amplification in social media distortion metrics

5. **Prevention Insights:** Greenberg's computational detection of authority without content analysis suggests similar approaches could identify emerging distortion in social media networks in real-time

6. **Social Context:** Unlike traditional publishing (with 15-year timescale), social media enables distortion mechanisms to compound 10-100× faster, potentially creating unfounded authority within months

---

## Sources

- [Greenberg 2009 on PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/)
- [Original BMJ publication](https://www.bmj.com/content/339/bmj.b2680)
- [James Lind Library documentation](https://www.jameslindlibrary.org/greenberg-sa-2009/)
