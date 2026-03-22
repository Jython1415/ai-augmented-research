# Verification Instructions

You are verifying posts that were classified as "relevant" to the Shumailov et al. (2024) Nature paper on AI model collapse. Your job is to CHECK whether each post actually has a **traceable citation signal**.

## What counts as a citation signal:
- A URL to nature.com, arxiv.org, or any news article about the paper
- DOI: 10.1038/s41586-024-07566-y
- Author name: "Shumailov" or "Shumaylov"
- Paper title: "AI models collapse when trained on recursively generated data"
- Alternate title: "The Curse of Recursion"
- Verified news source URL (theregister.com, techcrunch.com, theguardian.com, nytimes.com, scientificamerican.com, popularmechanics.com, gizmodo.com, arstechnica.com, futurism.com, theconversation.com, etc.)
- Wikipedia link about model collapse
- Reply to or quote of a post that itself has one of the above signals (check parent_text and quoted_text)
- The term "model collapse" used in a way that explicitly references "a paper", "a study", "research published in Nature", etc.

## What does NOT count:
- Describing the concept of model collapse without any of the above signals
- Saying "AI trains on AI data and degrades" with no URL, author, or paper reference
- Using terms like "Habsburg AI", "ouroboros", "AI eating itself" without citing a source
- Mentioning "model collapse" as a general term without attributing it to specific research

## Your task:
1. Read your verification batch file
2. For each post, check: does the post text, parent_text, or quoted_text contain a traceable citation signal?
3. Write a results file with this JSON format:

```json
{
  "batch_id": "verify_N",
  "verifications": [
    {"id": 123, "has_citation": true, "signal": "nature.com URL in post text"},
    {"id": 456, "has_citation": false, "reason": "concept description only, no URL/author/paper reference"}
  ]
}
```

Mark `has_citation: true` ONLY if you can identify a specific citation signal. Be strict — if in doubt, mark false.
