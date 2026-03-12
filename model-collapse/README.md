# Model Collapse Discourse Study

**How Bluesky discourse about AI model collapse diverged from the science**

A discourse analysis of 2,835 Bluesky posts about model collapse (May 2023 – March 2026), coded on six dimensions against a 21-paper literature timeline.

## Key Findings

- **46% of posts oversimplify** the phenomenon; only 26% are accurate
- **Only 18% engage with post-2024 research** that established mitigations and definitional complexity
- **Accuracy rates remain similar across epochs** despite rapid scientific progress — the discourse scaled 5x without learning
- **Posts citing news articles show similar accuracy rates to unsourced posts** (19.5% vs 17.5%)
- **Posts citing academic papers show substantially higher accuracy** than posts citing news articles
- **Predictive claims are accurate only 3.7% of the time**, yet 68.9% of posts use no hedging

## Read the Full Analysis

See **[ANALYSIS.md](ANALYSIS.md)** for the complete write-up with methodology, results, and discussion.

## Repository Structure

```
data/posts.db              # SQLite database (7,766 posts, all coding results)
analysis/                  # Data collection and coding pipeline
  collect_posts.py         # Bluesky API collection
  export_batches.py        # Pass 1 batch export
  import_results.py        # Pass 1 result import
  export_pass2_batches.py  # Pass 2 batch export
  import_pass2_results.py  # Pass 2 result import
lit-timeline/
  timeline.md              # 21-paper literature timeline (ground truth)
  coding-reference.md      # Condensed coding reference for subagents
paper/                     # LaTeX paper source and figures
ANALYSIS.md                # Full analysis write-up
PLAN.md                    # Research plan and progress notes
```

## Methodology

- **Corpus**: 7,766 Bluesky posts matching 6 search terms; 2,835 coded as relevant (2,736 with complete valid coding after data cleaning)
- **Coding**: Two-pass AI-augmented coding (135 parallel subagents) validated by human calibration
- **Ground truth**: 21 papers across 6 knowledge epochs (Pre-2023 through Mar 2025+)
- **Human time**: ~1 hour total (AI-augmented hobby research)

## Database Schema

The `posts` table contains:
- `id`, `text`, `created_at`, `author_did`, `uri` — post metadata
- `search_term_matched` — which search term found this post
- `is_relevant` — Pass 1 binary classification
- `relevance_confidence` — Pass 1 confidence score
- `claim_type`, `source_cited`, `caveating_level`, `accuracy`, `literature_awareness`, `depth` — Pass 2 coding dimensions
- `minimal_content` — flag for posts too brief to meaningfully code
- `coding_rationale` — free-text justification for coding decisions
