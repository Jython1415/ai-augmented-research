# Verification Instructions (v4)

## RULES — READ FIRST

**You have exactly TWO steps**: Read your batch file, then Write your results file. That's it.

**FORBIDDEN** (violation = task failure):
- Do NOT use the Bash tool at all — not for any reason
- Do NOT write Python scripts, shell scripts, or ANY code
- Do NOT use jq, cat, head, sqlite3, wc, or any command-line tools

**REQUIRED TOOLS** (use ONLY these):
- **Read** tool: to read your batch file
- **Write** tool: to create your results file

---

## Context

You are VERIFYING posts that were previously classified as "relevant" to Shumailov et al. (2024) "AI models collapse when trained on recursively generated data" (Nature 631, 755-759).

Your job: check whether each post actually has a **traceable citation signal** — a specific URL, author name, DOI, paper title, or reference to a specific news article about THIS paper.

The previous classifier sometimes marked posts as relevant when they only *described* the concept of model collapse without actually citing the paper. Your job is to catch these false positives.

---

## Decision Checklist

For each post, check the `text` field. Answer: does this post contain at least ONE of the following?

### TRUE citation signals (mark `verified: true`):
1. **URL to the paper**: nature.com/articles/s41586-024-07566-y, arxiv.org/abs/2305.17493
2. **URL to Nature News**: nature.com/articles/d41586-024-02420-7 or nature.com/articles/d41586-024-03023-y
3. **Any nature.com URL** about model collapse (nature.com/articles/...)
4. **URL to verified news coverage** about model collapse from AI training on AI data. Verified domains: techcrunch.com, theregister.com, gizmodo.com, scientificamerican.com, theconversation.com, bigthink.com, heise.de, bloomberg.com, technologyreview.com, venturebeat.com, popsci.com, nytimes.com, axios.com, arstechnica.com, futurism.com, popularmechanics.com, ibm.com/think, euronews.com, theglobeandmail.com, abc.net.au, cosmosmagazine.com, gigazine.net, singularityhub.com, cacm.acm.org, freethink.com, techxplore.com, noemamag.com, mindmatters.ai, zdnet.com, wired.com
   - IMPORTANT: The URL must be to an article specifically about model collapse / AI training on AI data. A zdnet.com article about iPhone specs is NOT relevant.
5. **URL to platformer.news** about model collapse (topical coverage)
6. **Author name**: "Shumailov" or "Shumaylov"
7. **DOI**: 10.1038/s41586-024-07566-y
8. **Paper title**: "AI models collapse when trained on recursively generated data" or "The Curse of Recursion"
9. **Specific Nature paper reference**: "the Nature paper on model collapse", "the Nature study", "published in Nature" (about model collapse), "a paper in Nature"
10. **Verified news headline**: "AI models fed AI-generated data quickly spew nonsense", "Model collapse: scientists warn...", "AI-Generated Data Can Poison Future AI Models", "When A.I.'s Output Is a Threat to A.I. Itself", "AI could choke on its own exhaust"
11. **Wikipedia link**: en.wikipedia.org/wiki/Model_collapse
12. **arxiv.org URL** for the specific paper (abs/2305.17493) — NOT a different arxiv paper
13. **Reply context**: If `is_reply` is true and the classification_rationale mentions parent/quote context, mark as `verified: true, signal: "reply context (not independently verifiable)"` — we can't see parent text in this pass

### FALSE citation signals (mark `verified: false`):
- "Discusses model collapse" / "describes model collapse phenomenon" — concept description, not citation
- "About AI training on AI data" — topic description, not citation
- "Explicit definition of model collapse" — concept, not citation
- Uses metaphors like "Habsburg AI", "ouroboros", "AI eating itself" without any URL/author/paper reference
- Links to a DIFFERENT arxiv paper (not 2305.17493) — e.g., arxiv.org/abs/2601.02631, arxiv.org/abs/2505.13947
- Links to a DIFFERENT topic article (Apple reasoning collapse, AI funding, copyright)
- Says "model collapse" without any of the above signals
- Classification rationale says something like "Links to article about model collapse" but no actual URL is visible in the text

### EDGE CASES:
- **Truncated URLs** (e.g., "nature.com/articles/s41..." or "techcrunch.com/2024/07/..."): Mark `verified: true` if the truncated URL plausibly points to the paper/coverage
- **Multiple URLs**: If one URL is about model collapse and another isn't, still `verified: true`
- **Non-English posts** with a relevant URL: `verified: true` (URL is the signal, not the language)

---

## Output Format

Use the **Write tool** to create your results file at:
`/private/tmp/claude/relevance/v4/verify/results_BATCHID.json`

```json
{
  "batch_id": "verify_NNN",
  "total": 50,
  "verified_true": 45,
  "verified_false": 5,
  "verifications": [
    {"id": 123, "verified": true, "signal": "nature.com URL in text"},
    {"id": 456, "verified": false, "reason": "No URL/author/DOI in text; rationale says 'discusses model collapse' which is concept description only"},
    {"id": 789, "verified": true, "signal": "reply context (not independently verifiable)"}
  ]
}
```

- Include ALL posts from the input — do not skip any
- Use the exact post IDs from the input
- Keep signal/reason to one sentence

## What to Report Back

When done, report:
- Batch ID
- Verified true count
- Verified false count
- List of false positive IDs with brief reasons
