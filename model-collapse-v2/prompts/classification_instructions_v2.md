# Relevance Classification Instructions (v2 — Narrow Citation Scope)

## RULES — READ FIRST

**You have exactly TWO steps**: Read your batch file, then Write your results file. That's it.

**FORBIDDEN** (violation = task failure):
- Do NOT use the Bash tool at all — not for any reason
- Do NOT write Python scripts, shell scripts, or ANY code
- Do NOT use jq, cat, head, sqlite3, or any command-line tools

**REQUIRED TOOLS** (use ONLY these):
- **Read** tool: to read your batch file
- **Write** tool: to create your results file

You are the classifier. Read each post. Apply your judgment. Write JSON results. Do NOT import — the main agent handles that.

---

## Context

You are classifying Bluesky posts for a research study about how people cite the paper "AI models collapse when trained on recursively generated data" by Shumailov et al. (2024), published in Nature (vol. 631, pp. 755-759).

**IMPORTANT**: This study uses a NARROW scope. A post is only relevant if it contains a **traceable citation** to this specific paper, or is part of a conversation thread that cites the paper. General discussion of "model collapse" or AI degradation is NOT sufficient.

**THE MOST COMMON MISTAKE**: Classifying a post as relevant because it *describes* model collapse (AI training on AI data causes degradation). Describing the concept is NOT a citation. You must find a specific link, author name, paper title, or verified news article reference. If a post just says "model collapse happens when AI trains on AI output" with no URL, no author, no paper reference — it is NOT RELEVANT, no matter how accurately it describes the concept.

## Your Task (3 steps)

1. Read this instruction file (you're doing that now)
2. Read your assigned batch file using the **Read** tool
3. Classify each post and write results using the **Write** tool

Do NOT import results — the main agent handles that after you finish.

## Input Format

Each post in the batch file has these fields:
- **text**: The post's own text
- **search_term**: The search term that matched this post
- **parent_text**: The text of the post this is replying to (null if not a reply)
- **quoted_text**: The text of a post this quotes/embeds (null if no quote)

Use ALL available fields when classifying. For short or empty posts, the parent_text and quoted_text often reveal what the post is about.

## Classification Criteria

### What counts as a CITATION (post is RELEVANT)

A post is relevant if **the post itself, its parent_text, or its quoted_text** contains at least one of these citation signals:

**Direct paper references:**
- Links to the Nature article (nature.com/articles/s41586-024-07566-y)
- Links to the arXiv preprint (arxiv.org/abs/2305.17493)
- The DOI (10.1038/s41586-024-07566-y)
- The author name "Shumailov" or "Shumaylov"
- The paper title or close paraphrase ("AI models collapse when trained on recursively generated data", "The Curse of Recursion")

**Identifiable references to THIS paper:**
- "the Nature paper on model collapse" or "the Nature study on model collapse"
- "that Nature paper about AI eating itself" or similar
- "the model collapse paper" when clearly referring to this specific paper (not the concept generally)

**News coverage of THIS paper** (sharing or discussing these verified articles):
- Nature News: "AI models fed AI-generated data quickly spew nonsense"
- TechCrunch: "Model collapse: scientists warn against letting AI eat its own tail"
- The Register: "AI models face collapse if they overdose on their own output"
- Euronews: "New study warns of model collapse as AI tools train on AI-generated content"
- Scientific American: "AI-Generated Data Can Poison Future AI Models"
- The Conversation: "What is model collapse? An expert explains..."
- Big Think / Freethink: "Model collapse threatens to kill progress on generative AIs"
- Globe and Mail: "AI models collapse and spout gibberish over time"
- heise online: "Model collapse - how synthetic data can kill AI"
- Harvard JOLT: "Model Collapse and the Right to Uncontaminated Human-Generated Data"
- CACM: "The Collapse of GPT"
- NOEMA: "The AI-Powered Web Is Eating Itself"
- Oxford press release: "Could machine learning models cause their own collapse?"
- Bloomberg: "AI 'Model Collapse': Why Researchers Are Raising Alarms"
- MIT Technology Review: "AI trained on AI garbage spits out AI garbage"
- VentureBeat: "The AI feedback loop: Researchers warn of 'model collapse'"
- TechTarget: "Model collapse explained: How synthetic training data breaks AI"
- Popular Science: "AI trained on AI churns out gibberish"
- Gizmodo: "AI Learning From Its Own Nonsense Might Just Self-Destruct"
- NYT: "When A.I.'s Output Is a Threat to A.I. Itself"
- ABC Australia: "What is model collapse?"
- Axios: "AI could choke on its own exhaust" / "This is AI's brain on AI"
- SAS Blog, Gigazine, Mind Matters, TechXplore, SingularityHub, Cosmos Magazine — all verified as about this paper
- Any article that clearly identifies Shumailov et al. or the Nature publication as its subject
- Look for URLs containing: nature.com, techcrunch.com, theregister.com, scientificamerican.com, theconversation.com, bigthink.com, heise.de, bloomberg.com, technologyreview.com, venturebeat.com, popsci.com, gizmodo.com, nytimes.com, axios.com, noemamag.com when discussing model collapse

**Citation chain (depth 1):**
- The post is a direct reply to a post that contains any citation signal above (check parent_text)
- The post quotes/embeds a post that contains any citation signal above (check quoted_text)

### What does NOT count (post is NOT RELEVANT)

- **Describes the model collapse concept without citing the paper** — even a perfect description of "AI training on AI data causes degradation" is NOT relevant without a link, DOI, author name, or news article reference
- Uses "model collapse" without any traceable citation signal — even if discussing AI training on AI data
- Uses metaphors like "Habsburg AI", "AI ouroboros", "AI eating itself" WITHOUT also citing the paper — these terms predate the paper and are used independently
- Discusses model collapse in a non-AI context (economics, healthcare, GAN mode collapse, neural collapse)
- General AI pessimism or criticism using collapse language
- Discusses a DIFFERENT paper about model collapse (e.g., Alemohammad et al. "Self-Consuming Models Go MAD") without also referencing Shumailov
- Is written primarily in a non-English language
- Has parent/quoted context that shows the conversation is about an unrelated topic

### Edge cases

- A post says "model collapse" and its parent_text contains a link to the Nature article → **RELEVANT** (citation chain)
- A post says "Habsburg AI" but nothing in post/parent/quoted references the paper → **NOT RELEVANT**
- A post says "that model collapse paper from Nature" → **RELEVANT** (identifiable reference)
- A post discusses model collapse with technical detail but no citation signal → **NOT RELEVANT** (no traceable citation)
- A post says "AI models collapse when trained on their own output" with no URL or author → **NOT RELEVANT** (describing the concept is not citing the paper)
- A post says "model collapse is when AI trains on AI data and degrades" → **NOT RELEVANT** (no citation signal, just concept description)
- A post quotes someone who linked to the arXiv preprint → **RELEVANT** (citation chain via quoted_text)

## Step 3: Write Results

Use the **Write tool** (not Bash) to create your results file. Format:

```json
{
  "batch_id": "THE_BATCH_ID_FROM_INPUT",
  "classifications": [
    {"id": 123, "relevant": true, "rationale": "One sentence why"},
    {"id": 456, "relevant": false, "rationale": "One sentence why"}
  ]
}
```

- Include ALL posts from the input file — do not skip any
- Use the exact post IDs from the input
- Keep rationales to one sentence

## What to Report Back

When done, report:
- How many posts classified as relevant
- How many posts classified as not relevant
- Whether the import succeeded or failed (and any error message if it failed)
