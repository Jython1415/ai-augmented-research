# Model Collapse Discourse Study

**How Bluesky discourse about AI model collapse diverged from the science**

A discourse analysis of 2,835 Bluesky posts about model collapse against a 21-paper literature timeline.

## Primary Document

See **[paper/paper.pdf](paper/paper.pdf)** for the complete analysis with findings, methodology, and discussion.

For details on the research process and data collection pipeline, see **[PROCESS.md](PROCESS.md)**.

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
PROCESS.md                 # Research process and methodology documentation
```

## Database Schema

The `posts` table contains:
- `id`, `text`, `created_at`, `author_did`, `uri` — post metadata
- `search_term_matched` — which search term found this post
- `is_relevant` — Pass 1 binary classification
- `relevance_confidence` — Pass 1 confidence score
- `claim_type`, `source_cited`, `caveating_level`, `accuracy`, `literature_awareness`, `depth` — Pass 2 coding dimensions
- `minimal_content` — flag for posts too brief to meaningfully code
- `coding_rationale` — free-text justification for coding decisions
