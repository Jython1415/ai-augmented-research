# Publication Plan — Model Collapse Study

## Status: VDD Review ✓ → Data Cleanup ✓ → ANALYSIS.md Rewrite ✓ → LaTeX + Viz Next

## What's Done

### VDD Adversarial Review (3 agents)
- Methodology critic, statistical verifier, overclaims critic
- Found: numerical discrepancies, circular operationalization, causal language, generalizability overclaims
- All addressed in ANALYSIS.md rewrite

### Data Cleanup
- DB cleaned: 99 posts with invalid/missing coding values NULLed out
- 2,736 of 2,835 relevant posts (96.5%) have complete valid coding
- All tables in ANALYSIS.md now match fresh DB queries

### ANALYSIS.md Rewrite
- Title: "Model Collapse on Bluesky: How Discourse Diverged from the Science"
- Narrowed from "public discourse" → "Bluesky discourse" throughout
- Causal language softened ("predicts" → "correlates with")
- New limitations: circularity caveat, validation sample size, consensus drift
- Section headings neutralized
- Numbers corrected across all 8 result tables + appendix
- README.md updated to match

## What's Next: LaTeX Paper + Visualizations

### LaTeX Paper
- **Template**: arXiv preprint style (single-column, wide margins)
- **Output**: `paper/paper.tex` → compile to `paper/paper.pdf`
- **Content source**: ANALYSIS.md (already complete and reviewed)

### 4 Visualizations (Saloni Dattani's principles)

**Principles**: label directly on charts, all text horizontal, colorblind-accessible palette, no 3D/pie/rotated text, charts work standalone, reproducible code.

**Viz 1: Accuracy by Epoch (grouped bar)**
- Data: Appendix A1. X=E1-E4, bars=accurate/oversimplified/wrong/unfalsifiable

**Viz 2: Literature Awareness × Accuracy (heatmap)**
- Data: Table 2.4. 3 rows × 4 cols, color=percentage

**Viz 3: Accuracy by Source Type (horizontal bar)**
- Data: Table 2.5. 5 sources ordered by accuracy rate

**Viz 4: Monthly Volume Timeline (line)**
- Data: Appendix A2. Annotate Nature pub (Jul 2024) and Schaeffer (Mar 2025)

### Implementation
- Python (matplotlib/seaborn) → PDF figures in `paper/figures/`
- LaTeX includes via \includegraphics
- Compile with pdflatex/latexmk
- All in `paper/` directory

## Corrected Data (for LaTeX tables)

### Table 2.1: Accuracy Distribution
| Accuracy | n | % |
|----------|---|---|
| Oversimplified | 1,272 | 45.7% |
| Accurate | 715 | 25.7% |
| Unfalsifiable | 639 | 23.0% |
| Wrong | 155 | 5.6% |

### Table 2.2: Accuracy by Epoch
| Epoch | Period | Coded Posts | % Accurate | % Oversimplified |
|-------|--------|-------------|------------|------------------|
| E1 | Pre-Jul 2024 | 336 | 21.7% | 47.0% |
| E2 | Jul-Sep 2024 | 226 | 34.1% | 48.2% |
| E3 | Oct 2024-Feb 2025 | 554 | 26.7% | 42.6% |
| E4 | Mar 2025+ | 1,665 | 25.0% | 46.2% |

### Table 2.4: Literature Awareness × Accuracy
| | Accurate | Oversimplified | Wrong | Unfalsifiable |
|---|---|---|---|---|
| Cites post-2024 (n=486) | 89.9% (437) | 7.8% (38) | 0.2% (1) | 2.1% (10) |
| Only original (n=870) | 17.5% (152) | 69.4% (604) | 6.0% (52) | 7.1% (62) |
| No citations (n=1,425) | 8.8% (126) | 44.2% (630) | 7.2% (102) | 39.8% (567) |

### Table 2.5: Source × Accuracy
| Source | Total | % Accurate | % Oversimplified | % Wrong |
|--------|-------|-----------|-----------------|---------|
| Other paper | 270 | 76.7% | 14.4% | 1.1% |
| Nature paper | 132 | 57.6% | 36.4% | 3.0% |
| Quote post | 55 | 30.9% | 40.0% | 5.5% |
| News article | 390 | 19.5% | 60.8% | 2.8% |
| None | 1,934 | 17.5% | 47.9% | 6.9% |

### Table 2.6: Claim Type × Accuracy
| Claim Type | Total | % Accurate | % Oversimplified | % Wrong |
|-----------|-------|-----------|-----------------|---------|
| Empirical | 1,091 | 48.3% | 43.3% | 5.1% |
| Meta-commentary | 686 | 16.3% | 23.5% | 1.5% |
| Normative | 340 | 13.5% | 46.2% | 7.4% |
| Predictive | 619 | 3.7% | 75.9% | 10.3% |

### Table 2.7: Caveating Distribution
| Caveating | n | % |
|-----------|---|---|
| None | 1,927 | 68.9% |
| Weak hedge | 553 | 19.8% |
| Strong hedge | 315 | 11.3% |

### Table 2.8: Literature Awareness by Epoch
| Epoch | % Citing Post-2024 Nuance |
|-------|--------------------------|
| E1 | 8.3% |
| E2 | 19.0% |
| E3 | 17.8% |
| E4 | 19.0% |

## After LaTeX
- Git commit all files
- User handles Bluesky post
