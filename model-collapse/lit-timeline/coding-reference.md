# Model Collapse Literature: Coding Reference

## How to Use This Reference

When classifying Bluesky posts about model collapse, compare the post's date to the epochs below. A post is:

- **Accurate** if its claims are consistent with what was known at the time
- **Oversimplified** if it omits important nuance available at the time
- **Wrong** if it contradicts established findings available at the time

---

## Knowledge Epochs

### 1. Pre-Jul 2024
*Before Nature publication; only known to arxiv researchers*

**What was established:**
- Gerstgrasser et al. (Apr 2024 arxiv): Accumulation prevents collapse
- Dohmatob (Feb 2024 arxiv): Tail collapse ≠ full collapse
- Shumailov et al. (Jul 2024 Nature): Collapse under replacement training

**Accurate claims:**
- "Research suggests models degrade when trained on their own output"
- "Some conditions cause model performance loss"

**Oversimplified claims:**
- "AI will collapse" (lacks specificity; depends on conditions)

**Wrong claims:**
- "This phenomenon is newly discovered" (arxiv work predates Nature)

---

### 2. Jul-Sep 2024
*Nature publication + initial media wave*

**What was established:**
- Shumailov Nature paper is anchor reference (nature.com/articles/s41586-024-07566-y)
- Collapse occurs under REPLACEMENT (not all training regimes)
- Gerstgrasser accumulation result available since Apr 2024
- Tail collapse phenomenon documented since Feb 2024

**Accurate claims:**
- "A Nature paper shows models collapse when trained recursively on synthetic data under replacement"
- "Accumulation of prior data can prevent collapse"
- "The effect varies by condition"

**Oversimplified claims:**
- "AI will inevitably collapse" (Gerstgrasser already showed accumulation prevents it)
- "All synthetic training causes collapse" (replacement-specific)

**Wrong claims:**
- "No one is studying this" (substantial arxiv body exists)
- "Everyone uses replacement training" (not industry standard)

---

### 3. Oct 2024-Feb 2025
*Refinement phase with strong collapse results*

**What was established:**
- Strong Model Collapse (Oct 2024): Even 0.1% synthetic data causes degradation
- Multiple verification methods published
- Empirical studies confirm core phenomenon
- Multiple mitigation strategies documented

**Accurate claims:**
- "The picture is complex—collapse depends on conditions"
- "Strong collapse shows degradation with minimal synthetic data"
- "Multiple factors affect whether collapse occurs"

**Oversimplified claims:**
- "Model collapse is inevitable" (multiple mitigation papers exist)
- Either extreme ("impossible" or "unavoidable")

**Wrong claims:**
- "Model collapse has been debunked" (strong collapse reconfirms it's real)
- "Only replacement causes collapse" (strong collapse shows broader conditions)

---

### 4. Mar 2025+
*Definitional crisis phase*

**What was established:**
- Position paper (Mar 2025): 8 conflicting definitions of "model collapse"
- Definitional disagreement undermines direct comparison of studies
- Core phenomenon real, but scope and conditions debated

**Accurate claims:**
- "Researchers disagree on what model collapse even means"
- "Different papers use different definitions"
- "The term needs clarification"

**Oversimplified claims:**
- Either claiming consensus or claiming total disagreement
- Claims that ignore definitional complexity

**Wrong claims:**
- "This proves model collapse isn't real" (definitional ≠ empirical)
- Claims made as if single definition exists

---

## Key Facts for Classification

Essential knowledge for a coding agent:

1. **Shumailov (Nature, Jul 2024)**: Collapse under REPLACEMENT, not all training
2. **Gerstgrasser (arxiv, Apr 2024)**: ACCUMULATION prevents collapse
3. **Dohmatob (arxiv, Feb 2024)**: "Tail collapse" ≠ "full collapse"
4. **Strong Model Collapse (Oct 2024)**: 0.1% synthetic data can degrade models
5. **Nature URL**: nature.com/articles/s41586-024-07566-y (most shared reference)
6. **"Habsburg AI"**: Metaphor coined by Jathan Sadowski, not a research finding
7. **Definitions (Mar 2025)**: 8 conflicting definitions exist in literature

---

## Common Bluesky Narratives

| Narrative | Accuracy | Why |
|-----------|----------|-----|
| "AI is eating itself" | Oversimplified | Collapse is condition-dependent |
| "Model collapse is inevitable" | Wrong (after Apr 2024) | Gerstgrasser showed accumulation prevents it |
| "The Nature paper proved AI will collapse" | Oversimplified | Proved collapse under replacement only |
| "Habsburg AI" | Metaphor, not finding | Accuracy depends on accompanying claims |
| "No one is doing anything about this" | Wrong | Multiple mitigation papers published |
| "Model collapse has been debunked" | Wrong | Real under conditions; Oct 2024 reconfirmed |
| "Only synthetic data matters" | Oversimplified | Conditions and data mix both critical |
| "Researchers all agree on what this is" | Wrong (after Mar 2025) | 8 conflicting definitions documented |

---

## Classification Workflow

1. **Extract date** from post
2. **Identify claims** being made (e.g., "collapse inevitable," "only affects X," "prevents Y")
3. **Match to epoch** above
4. **Check against accurate/oversimplified/wrong** lists for that epoch
5. **Flag definitional issues** if post uses undefined terms as if settled
6. **Note caveats** (e.g., "accurate but lacks current nuance" for pre-2025 posts)

---

## Common Pitfalls

- Conflating "tail collapse" with "full collapse"
- Treating Gerstgrasser as debunking Shumailov (they study different conditions)
- Using "Habsburg AI" without understanding it's a metaphor
- Claiming consensus after Mar 2025 when definitions diverged
- Ignoring that strong collapse (Oct 2024) is broader than Shumailov's replacement case
