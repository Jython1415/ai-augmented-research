# Relevance Classification Instructions (v4 — Decision Tree + Chain-of-Thought)

## RULES — READ FIRST

**You have exactly TWO steps**: Read your batch file, then Write your results file. That's it.

**FORBIDDEN** (violation = task failure):
- Do NOT use the Bash tool at all — not for any reason
- Do NOT write Python scripts, shell scripts, or ANY code
- Do NOT use jq, cat, head, sqlite3, wc, or any command-line tools

WHY THIS MATTERS: In previous runs, agents that used Bash wrote Python scripts with regex-based domain matching to classify posts programmatically. These scripts produced incorrect results (missed 8x more relevant posts than LLM judgment). You MUST classify each post using your own reading comprehension, not code.

**REQUIRED TOOLS** (use ONLY these):
- **Read** tool: to read your batch file
- **Write** tool: to create your results file

You are the classifier. Read each post. Apply your judgment using the decision tree below. Write JSON results. Do NOT import — the main agent handles that.

---

## Context

You are classifying Bluesky posts for a research study about how people cite the paper "AI models collapse when trained on recursively generated data" by Shumailov et al. (2024), published in Nature (vol. 631, pp. 755-759).

This study has a NARROW scope: a post is relevant ONLY if it contains a **traceable citation signal** pointing to this specific paper. Describing the concept of model collapse is NOT enough.

---

## Decision Tree — Follow This Sequence For Every Post

For each post, check the post text, parent_text, AND quoted_text. Go through these steps in order. Stop at the first match:

**Step 1: Check for direct links to the paper**
Does the text contain a URL to the actual paper?
- nature.com/articles/s41586-024-07566-y (the Nature article)
- nature.com/articles/d41586 (Nature News coverage)
- arxiv.org/abs/2305.17493 (the arXiv preprint)
→ If YES: **RELEVANT**. Stop here.

**Step 1b: Check for links to verified news coverage**
Does the text contain a URL to a news article specifically about model collapse from training on AI-generated data? The URL must be about this topic — not just from a listed domain.

IMPORTANT: Many news domains (theguardian.com, mashable.com, venturebeat.com) publish articles about many AI topics. A Guardian article about Apple's reasoning model, or a VentureBeat article about AI funding, is NOT relevant just because it's from a listed domain. The article itself must be about model collapse (AI training on synthetic/AI-generated data causing degradation).

Known verified article domains: techcrunch.com, theregister.com, scientificamerican.com, theconversation.com, bigthink.com, heise.de, bloomberg.com, technologyreview.com, venturebeat.com, popsci.com, gizmodo.com, nytimes.com, axios.com, arstechnica.com, futurism.com, popularmechanics.com, ibm.com/think, euronews.com

→ If the URL links to an article specifically about model collapse (AI training on AI data): **RELEVANT**. Stop here.
→ If the URL is about a different topic (Apple reasoning, AI funding, climate, politics): **NOT RELEVANT** on this step — continue to Step 2.

**Step 2: Check for author/DOI/title**
Does the text contain "Shumailov", "Shumaylov", the DOI "10.1038/s41586-024-07566-y", or the paper title "AI models collapse when trained on recursively generated data" or "The Curse of Recursion"?
→ If YES: **RELEVANT**. Stop here.

**Step 3: Check for specific paper reference**
Does the text say "the Nature paper on model collapse", "the Nature study", "published in Nature", "a paper in Nature about model collapse", or similar phrasing that specifically identifies THIS paper (not just "a study" or "research")?
→ If YES: **RELEVANT**. Stop here.

**Step 4: Check for verified news article references**
Does the text reference a specific news headline or article about this paper? Known headlines include:
- "AI models fed AI-generated data quickly spew nonsense"
- "Model collapse: scientists warn against letting AI eat its own tail"
- "AI-Generated Data Can Poison Future AI Models"
- "What is model collapse? An expert explains"
- "Could machine learning models cause their own collapse?"
- "When A.I.'s Output Is a Threat to A.I. Itself"
- "AI could choke on its own exhaust"
→ If YES: **RELEVANT**. Stop here.

**Step 5: None of the above**
If you reached this step, the post has NO traceable citation signal.
→ **NOT RELEVANT**. Even if the post perfectly describes model collapse.

---

## Few-Shot Examples

Study these carefully. They represent the hardest classification decisions.

<examples>

<example>
<post_text>For anyone reading unfamiliar with model collapse: www.nature.com/articles/s41... AI models can't continue useful "learning" if most of their training content is AI-produced.</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: Contains nature.com URL about model collapse. Stop.</reasoning>
<classification>RELEVANT</classification>
</example>

<example>
<post_text>This is good. Model collapse in AI and how to prevent it. theconversation.com/what-is-mode...</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: Contains theconversation.com URL about model collapse. Stop.</reasoning>
<classification>RELEVANT</classification>
</example>

<example>
<post_text>these ai models are going to collapse and theyre going to be left stranded cause they forgot how to do anything without a billion monkeys at a billion typewriters telling them what to do</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: No URL. Step 2: No author/DOI/title. Step 3: No specific paper reference. Step 4: No news headline. Step 5: Reached — this describes a general concern about AI without any citation signal.</reasoning>
<classification>NOT RELEVANT</classification>
</example>

<example>
<post_text>AI trained on itself develops MAD Model Autophagy Disorder, becomes Habsburg inbred AI.</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: No URL. Step 2: No author/DOI/title. Step 3: No specific paper reference. Step 4: No news headline. Step 5: Reached — uses metaphors ("Habsburg AI", "MAD") but provides no traceable citation to the paper.</reasoning>
<classification>NOT RELEVANT</classification>
</example>

<example>
<post_text>My daughter has an interesting theory. It's an ouroboros. The more people use AI, the less actual new data will be available, and it will run out of things to train itself on and eventually eat itself.</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: No URL. Step 2: No author/DOI/title. Step 3: No specific paper reference. Step 4: No news headline. Step 5: Reached — describes the concept of recursive AI degradation but cites no paper, author, or article.</reasoning>
<classification>NOT RELEVANT</classification>
</example>

<example>
<post_text>Can AI Eat Itself? The Real Risk of Model Collapse. What happens when artificial intelligence starts learning mostly from itself? Picture a photocopy of a photocopy—edges blur, colors wash out, and detail drains away. That image underpins a growing concern in AI research known as model collapse.</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: No URL. Step 2: No author/DOI/title. Step 3: Mentions "AI research" but doesn't reference "the Nature paper" or any specific publication. Step 4: No news headline. Step 5: Reached — eloquent concept description but no traceable citation.</reasoning>
<classification>NOT RELEVANT</classification>
</example>

<example>
<post_text>And I say this after researching model collapse extensively. The next model that collapses is our ability to balance powerful technology with using it responsibly.</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1: No URL. Step 2: No author/DOI/title. Step 3: Says "researching model collapse" but doesn't reference a specific paper or publication. Step 4: No news headline. Step 5: Reached — claims to have researched the topic but provides no citation.</reasoning>
<classification>NOT RELEVANT</classification>
</example>

<example>
<post_text>This is what is known as model collapse</post_text>
<parent_text>Interesting article on the phrase plaguing research papers theconversation.com/what-is-mode...</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1b: parent_text contains theconversation.com URL about model collapse (AI training on AI data). This is verified coverage of the topic. Stop.</reasoning>
<classification>RELEVANT</classification>
</example>

<example>
<post_text>Apple's own research shows AI models get WORSE at reasoning over time. The accuracy collapse is real. theguardian.com/technology/2025...</post_text>
<parent_text>null</parent_text>
<quoted_text>null</quoted_text>
<reasoning>Step 1b: Contains theguardian.com URL but this article is about Apple's reasoning model accuracy, NOT about model collapse from training on AI-generated data. Continue to Step 2. Step 2: No author/DOI/title. Step 3: No specific Nature paper reference. Step 4: No verified headline. Step 5: NOT RELEVANT — the Guardian article is about a different AI topic.</reasoning>
<classification>NOT RELEVANT</classification>
</example>

</examples>

---

## Input Format

Each post in the batch file has these fields:
- **text**: The post's own text
- **search_term**: The search term that matched this post
- **parent_text**: The text of the post this is replying to (null if not a reply)
- **quoted_text**: The text of a post this quotes/embeds (null if no quote)

Check ALL three text fields (text, parent_text, quoted_text) when running through the decision tree.

---

## Output Format

Use the **Write tool** (not Bash) to create your results file. Format:

```json
{
  "batch_id": "THE_BATCH_ID_FROM_INPUT",
  "classifications": [
    {
      "id": 123,
      "citation_signal": "nature.com URL in post text",
      "relevant": true,
      "rationale": "Links to Nature article on model collapse"
    },
    {
      "id": 456,
      "citation_signal": "none",
      "relevant": false,
      "rationale": "Describes model collapse concept without any URL, author, or paper reference"
    }
  ]
}
```

**CRITICAL**: The `citation_signal` field must be filled in BEFORE you decide `relevant`. Write what specific signal you found (or "none"). Then set `relevant` based on that signal.

**What counts as a citation_signal value**: A specific URL (e.g. "nature.com URL in post text"), author name ("Shumailov mentioned"), DOI, or paper title.
**What does NOT count**: "discusses model collapse", "describes synthetic data issue", "mentions AI training degradation", "explicit definition of model collapse". These are concept descriptions, not citations. If you cannot point to a literal URL or author name in the text, the signal is "none".

- Include ALL posts from the input file — do not skip any
- Use the exact post IDs from the input
- Keep rationales to one sentence

## What to Report Back

When done, report:
- How many posts classified as relevant
- How many posts classified as not relevant
