# Model Collapse Citation Coding Reference

> Designed for inclusion in Haiku subagent prompts. Target reading time: under 2 minutes.

## Section 1: What Shumailov et al. (2024) Actually Claims

**Citation**: Shumailov et al. "AI models collapse when trained on recursively generated data." Nature 631, 755-759 (2024). arXiv:2305.17493 (May 2023).

**Core Findings:**
- Training models on recursively generated data causes irreversible defects
- Tails of the original content distribution disappear ("model collapse")
- Demonstrated across VAEs, GMMs, and LLMs (OPT-125M)

**Experimental Setup:**
- Data replacement: each generation trained only on previous generation's output
- No mitigation strategies applied (no data mixing, no filtering)
- This is a methodological choice, not a stated universal condition

**NOT Claimed:**
- Collapse happens regardless of data management strategy
- Collapse is inevitable in all real-world scenarios
- All synthetic data is harmful
- Accumulation-based training would also collapse (not tested)

---

## Section 2: Field Accuracy by Time Period

This study codes the *accuracy of information conveyed*. A citation can be inaccurate but understandable given information access.

| Period | Key Development | Accurate Claim | Inaccurate Claim |
|--------|----------------|----------------|------------------|
| **May 2023 – Mar 2024** | Preprint + supporting studies; no counterevidence | "Collapse is a serious concern under recursive training" | "Collapse is a universal law of AI" |
| **Apr – Jun 2024** | Gerstgrasser preprint: accumulation prevents collapse | "Collapse depends on data management strategy" | "Collapse is inevitable" |
| **Jul – Sep 2024** | Nature publication + media amplification | "Nature documented collapse under specific conditions" | "Nature proved collapse is inevitable" |
| **Oct 2024 – Feb 2025** | Multiple competing results; mitigations demonstrated | "It depends on the scenario" | Either "solved" or "inevitable" |
| **Mar 2025+** | 8 conflicting definitions (Schaeffer et al.) | Acknowledges complexity | Treats collapse as single settled phenomenon |

**Note**: Citing Nature without awareness of the Gerstgrasser preprint is understandable for general audiences but represents an incomplete picture. The coding captures accuracy, not blame.

---

## Section 3: Common Claims → Accuracy Rating

| Claim | Rating | Reasoning |
|-------|--------|-----------|
| "Model collapse is inevitable" | **Inaccurate** | Contradicted by accumulation evidence (Apr 2024+) |
| "AI training on AI output will destroy AI" | **Inaccurate** | Ignores multiple mitigation strategies |
| "Shumailov et al. proved AI will eat itself" | **Misrepresentation** | Paper showed specific conditions, not inevitability |
| "This study shows collapse can happen under certain conditions" | **Accurate** | Matches paper scope |
| "We need to keep human data in training" | **Partially supported** | Evidence supports retaining *original training data*; hasn't isolated human-generated data as uniquely necessary |
| "Model collapse has been debunked" | **Misrepresentation** | Real under specific conditions; caveated, not debunked |
| "The Nature paper on model collapse" | **Neutral reference** | Accuracy depends on what claim follows |
| "Model collapse only happens with data replacement" | **Partially accurate** | Captures key finding but oversimplifies the full picture |

---

## Section 4: Classification Workflow

1. **Extract posting date** → determines which time period applies
2. **Identify claim(s)** → what is being said about the paper or phenomenon?
3. **Check Paper Fidelity** → does it match what Shumailov et al. actually found? (Section 1)
4. **Check Field Accuracy** → does it reflect the knowledge state of that period? (Section 2)
5. **Note context** → thread nuance, claim strength (casual concern vs. authoritative assertion)

**Coding values:**
- **Paper Fidelity**: accurate / partially accurate / misrepresentation
- **Field Accuracy**: accurate / partially accurate / oversimplified / inaccurate

The standard scales with claim strength: casual "model collapse is concerning" is judged differently than authoritative "model collapse has been proven inevitable."

---

## Quick Reference

**Model Collapse**: Degradation when training on recursively generated synthetic data with data replacement (Shumailov et al. definition).

**Data Replacement**: Old training data discarded; only latest synthetic outputs used. The setup in Shumailov et al.

**Accumulation**: Retaining original + synthetic data across generations. Prevents collapse (Gerstgrasser et al., Apr 2024).

**Key dates**: Apr 2024 (accumulation prevents collapse), Jul 2024 (Nature publication), Mar 2025 (8 conflicting definitions).
