# V3 Coding Spot-Check Analysis

## Sample Summary
- Accurate substantive_mention: 10 reviewed
- Partially accurate: 10 reviewed
- Misrepresentation: 25 reviewed
- Not applicable substantive_mention: 5 reviewed
- **Total: 50 codes evaluated**

---

## ACCURATE SUBSTANTIVE_MENTION CODES (n=10)

### Code 575 ✓ CORRECT
**Post (2023-06-18)**: "LLMs can't currently create new knowledge… and LLMs may influence how/whether humans choose to contribute content (e.g., stackoverflow contributions are done :( …), so I think the reliance on human labor is true at least for now, but I don't think this "model collapse" problem is inevitable?"

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Post questions whether collapse is "inevitable" - this is explicitly not claiming inevitability. Uses "model collapse" as a known phenomenon but contests inevitability. Claim is conditional ("reliance on human labor is true... for now"). Correctly coded as accurate - preserves conditionality.

---

### Code 147 ✓ CORRECT
**Post (2025-06-21)**: "It's a known issue called "model collapse". I guess one analogy would be drinking your own urine to quench your thirst. Sooner or later things will stop working."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Uses metaphor to explain the mechanism (recursive training degrades output). "Sooner or later things will stop working" expresses a conditional concern, not inevitable certainty. Correctly describes what collapse is. Accurate coding is justified.

---

### Code 404 ✓ CORRECT
**Post (2024-11-23)**: "I'd be curious to see if this phenomenon occurs with 1) larger variants of the same model teaching smaller models 2) The effect of prompting to curate high quality data than the original. It would be interesting to see how long it takes for collapse to outweigh the benefits."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Post poses technical questions about collapse conditions (larger models, data curation effects). Frames collapse as a phenomenon to study, not as inevitable. Preserves conditionality. Correctly coded.

---

### Code 520 ✓ CORRECT
**Post (2024-03-04)**: "[includes links] "don't believe either your lying eyes or the researchers, also ignore how the plagiarism image generators and spicy autocorrect companies are screaming loudly about needing to get more and more data" Faith in it. Feels religious."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Skeptical commentary on whether companies should be pushing more data collection. Implicitly acknowledges collapse as a legitimate concern without misrepresenting it. Sarcastic tone doesn't distort the paper's findings.

---

### Code 469 ✓ CORRECT
**Post (2024-07-26)**: "AI models fed AI-generated data quickly spew nonsense, and it makes perfect sense. Remember making copies on a Xerox machine? copy → copy → copy → copy → garbage."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Perfect. Uses Xerox analogy to explain the mechanism - loss of quality through repeated copying of imperfect outputs. Correctly describes the paper's finding without claiming universality or inevitability. "Quickly spew nonsense" is colloquial but accurate description of degradation.

---

### Code 509 ✓ CORRECT
**Post (2024-04-19)**: "Today's post follows up on last week's #AI and #metaphor one and goes on the trail of the model collapse metaphor (which leads to mad cow disease\!)"

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Discusses the "model collapse" metaphor itself - a meta-commentary on the terminology and its historical parallels (mad cow disease - disease transmission). Does not misrepresent the paper's findings. Correctly coded.

---

### Code 472 ✓ CORRECT
**Post (2024-07-26)**: "A study suggests that AI models, including large language models like ChatGPT, could 'collapse' if trained on data they generate themselves, leading to a 'cascading effect' of compounding errors."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: States the conditional mechanism: "could collapse if trained on..." - preserves the conditionality. Correctly identifies recursive training as the trigger. Accurate coding is justified.

---

### Code 463 ✓ CORRECT
**Post (2024-07-27)**: "TIL: AI is the Habsburg monarchy. Let's hope it's peaking now."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Uses the metaphor from the paper but adds personal commentary ("Let's hope it's peaking now"). Does not misrepresent findings - just appreciates the metaphor. Correctly coded.

---

### Code 70 ✓ CORRECT
**Post (2025-11-25)**: "(ding) Model collapse soup, order up\!"

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Dismissive/sarcastic comment. Treats collapse as a real phenomenon but with humor. Does not distort the paper's claims. Correctly coded as substantive mention (adds evaluative tone) and accurate (preserves that collapse is a genuine concern).

---

### Code 270 ✓ CORRECT
**Post (2025-04-19)**: "I wonder if this is due to model collapse."

**Assigned**: substantive_mention, accurate, accurate

**Analysis**: Poses a conditional question - "is this due to...?" Does not claim certainty. Correctly coded.

---

**VERDICT: Accurate sample 100% CORRECT (10/10)**

---

## PARTIALLY_ACCURATE CODES (n=10)

### Code 533 ⚠️ BORDERLINE
**Post (2023-12-16)**: "'What Grok's recent OpenAI snafu teaches us about LLM model collapse / Researchers worry AI bots like Grok are already showing signs of larger-scale problems'"

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: The headline uses "are already showing signs" - this suggests collapse is beginning to manifest in deployed systems (Grok). The codebook forbids claiming collapse is "already happening" without evidence of it in deployed systems. In Dec 2023 (Epoch 2), no evidence that collapse was actually occurring in Grok. This is accurately coded as partially_accurate - it extends beyond what's been demonstrated.

**Why it's correct**: The headline implies real-world occurrence without evidence. Codebook: "collapse is already happening in deployed systems" = partially_accurate. ✓

---

### Code 423 ✓ CORRECT
**Post (2024-09-09)**: '> "Model collapse" threatens to kill progress on generative AIs... Again, the kind of shit that folks in #HigherEd and #academia are oh so keen to embrace.'

**Assigned**: substantive_mention, partially_accurate, accurate

**Analysis**: The quoted headline says collapse "threatens to kill progress" (threat language = concern, not certainty). Poster adds sarcasm about academia embracing it. Coded as partially_accurate for fidelity, accurate for field. This is correct - the headline does overgeneralize slightly ("threatens to kill progress" is stronger than "poses a risk"), but field accuracy is accurate because expressing concern about collapse is warranted.

---

### Code 190 ⚠️ BORDERLINE → LIKELY WRONG
**Post (2025-05-31)**: "«We're going to invest more and more in AI, right up to the point that model collapse hits hard and AI answers are so bad even a brain-dead CEO can't ignore it,» Exchange «AI» with «oil&gas», and «answers» with «climate»."

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: The quote says "model collapse hits hard" - this is claiming collapse WILL happen ("hits" is future certainty, not conditional). The analogy to climate/oil&gas reinforces inevitability framing. This should be **misrepresentation**, not partially_accurate. The post asserts collapse will definitely occur, not that it could occur under conditions. In Epoch 5 (May 2025), this claim is directly contradicted by demonstrated mitigations (accumulation, filtering, verification).

**Issue**: Undercoded. Should be misrepresentation + inaccurate. The claim of inevitable collapse is contradicted by evidence of prevention strategies.

---

### Code 171 ✓ CORRECT
**Post (2025-06-05)**: "Familiarize yourself with the term "model collapse." It's a big reason why AI companies are insistent on stealing copyrighted material and Trump's bill prevents AI regulation by states for ten years. LLMs are destined for digital kuru disease if they don't."

**Assigned**: substantive_mention, partially_accurate, accurate

**Analysis**: Post connects collapse to industry practices (data hoarding) and predicts LLMs will become "diseased" ("digital kuru disease") if they don't address it. This extends collapse beyond the tested conditions and frames it as an inevitable industry crisis. Coded as partially_accurate for fidelity (reasonable concern but stated as certainty) and accurate for field (expressing concern is warranted even if the framing is strong). Codebook supports this - extending to industry implications can be accurate if grounded.

---

### Code 553 ✓ CORRECT
**Post (2023-08-15)**: "There's a hypothesis that as more and more of the web is written by AI, and therefore dodgy, more and more of the search results will rely on said bullshit, and everything will be increasingly terrible."

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: The post presents a "hypothesis" but frames it as "will be increasingly terrible" - extends collapse beyond what's tested (full internet replacement) to a broader claim about information quality. In Epoch 2 (Aug 2023), no evidence this is happening. Correctly coded as partially_accurate for both dimensions.

---

### Code 33 ✓ CORRECT
**Post (2026-01-25)**: "5/7 The long-term risk is called "Model Collapse." 🏗️ If AI models train on disinformation, generate more content based on it, and then new models train on that output, the internet's information quality degrades. We risk drowning in low-quality "AI slop" where truth is hard to find."

**Assigned**: substantive_mention, partially_accurate, accurate

**Analysis**: Post frames collapse as a conditional risk ("If AI models train on..."). Extends from recursive LLM training to broader internet information quality. Coded as partially_accurate for fidelity (extends beyond tested scope to internet-wide claims) but accurate for field (expressing concern about information quality degradation is warranted). This is correct.

---

### Code 175 ✓ CORRECT
**Post (2025-06-03)**: "If this is where we're headed what's it going to look like when we get to this model collapse point"

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: Questions what collapse will look like ("when we get to this... point") - frames collapse as future-inevitable rather than conditional. Partially_accurate for both dimensions correctly captures this.

---

### Code 419 ✓ CORRECT
**Post (2024-10-07)**: '"Model collapse" threatens to kill progress on generative AIs'

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: "Threatens to kill progress" is language that extends beyond conditional risk to near-certainty of harm. Partially_accurate is correct coding. The paper's finding is more "could pose a risk" than "threatens to kill progress."

---

### Code 215 ✓ CORRECT
**Post (2025-05-28)**: "Some info to round out the discussion of model collapse and enshitiffication. One estimate says in 2024 bot traffic on the internet exceeded human interaction. Time to short those AI stocks you bought."

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: Connects collapse to enshitification and bot traffic statistics, implies financial collapse ("short those stocks"). Extends beyond what Shumailov showed to broader systemic failure prediction. Correctly coded as partially_accurate - reasonable concern but overgeneralized.

---

### Code 128 ⚠️ BORDERLINE
**Post (2025-07-02)**: "Yep, model collapse will surely happen any day now, even though we've been training smaller and more sensitive models on synthetic data since before LLMs were a thing. You should really try reading the model collapse paper and see if it actually applies to real life."

**Assigned**: substantive_mention, partially_accurate, partially_accurate

**Analysis**: Post is SKEPTICAL - "will surely happen any day now" is sarcasm. The poster is arguing that collapse may NOT actually apply in real-world scenarios where synthetic data is curated, not full-replacement. This is a reasonable critique and shouldn't be marked as misrepresenting the paper. 

**Issue**: Nuance - this is actually a SKEPTICAL post that correctly interprets the paper's limited scope (full data replacement) and questions its real-world applicability. The sarcasm ("will surely happen any day now") is dismissive of apocalyptic framing, not of the paper itself. Coding as partially_accurate seems correct for capturing the skeptical tone while acknowledging the post engages seriously with the paper's conditions.

**Verdict**: CORRECT but relies on recognizing sarcasm/skepticism.

---

**VERDICT: Partially_accurate sample 8/10 CORRECT, 2 QUESTIONABLE**

**Issue Code 190**: Appears undercoded - should be misrepresentation, not partially_accurate.

**Borderline Code 128**: Correctly coded but requires recognizing skeptical/sarcastic tone.

---

## MISREPRESENTATION CODES (n=25)

I'll analyze these systematically. Misrepresentation is the key category - codes should show collapse being described as inevitable, universal, mathematically proven, or already occurring in deployed systems.

### Code 534 ✓ CORRECT
**Post (2023-12-16)**: "Model collapse is starting. Generative AI is poisoning the Internet"

**Assigned**: authoritative_claim, misrepresentation, partially_accurate

**Analysis**: Claims collapse "is starting" (asserting current-reality rather than conditional risk). In Epoch 2 (Dec 2023), no evidence collapse was actually occurring in deployed systems. Misrepresentation is correct. Field accuracy = partially_accurate is justified (expressing concern is warranted; claiming it's "happening" extends beyond evidence).

---

### Code 505 ✓ CORRECT
**Post (2024-05-24)**: "And model collapse is already happening with Aye Eye-generated texts and images btw: A New Study Says AI Is Eating Its Own Tail"

**Assigned**: authoritative_claim, misrepresentation, partially_accurate

**Analysis**: "Already happening" is the key misrepresentation trigger. Perfect example - claims real-world occurrence without evidence. Correctly coded.

---

### Code 464 ✓ CORRECT
**Post (2024-07-27)**: "I think this is a major achilles heel that'll bring the ganAI industry down... 'indiscriminately learning from data produced by other models causes 'model collapse'—a degenerative process whereby, over time, models forget the true underlying data distribution'"

**Assigned**: authoritative_claim, misrepresentation, partially_accurate

**Analysis**: Claims collapse "will bring the... industry down" - frames as inevitable industry-destroying outcome. Paper studied specific models under specific conditions, not universal industry collapse. Correctly coded as misrepresentation.

---

### Code 428 ✓ CORRECT
**Post (2024-09-04)**: "The study estimates that 57% of all Internet content is AI-generated [links to paper]"

**Assigned**: substantive_mention, misrepresentation, partially_accurate

**Analysis**: The claim "57% of internet is AI-generated" does NOT come from Shumailov - this is a stat from elsewhere. The paper is about recursive training on full-replacement data, not about internet AI saturation. Misrepresentation is correct - misattributes findings to the paper.

---

### Code 402 ✓ CORRECT
**Post (2024-11-25)**: "Eventually, the communication space will be so filled with text/images regurgitated by so-called AI that there will be model collapse. They're already researching how to protect their "AIs" from synthetic (i.e., rehashed & vomited out) material."

**Assigned**: substantive_mention, misrepresentation, inaccurate

**Analysis**: Claims collapse is inevitable ("there will be model collapse") when internet is filled with AI content. No evidence this is happening. In Epoch 5, Gerstgrasser, Feng, He all showed prevention is possible. Field accuracy = inaccurate is correct - directly contradicted by evidence.

---

### Code 399 ✓ CORRECT
**Post (2024-11-26)**: "There's a paper in Nature about inevitable model collapse when you train AI on AI. The whole house comes down around their ears. Which is one reason among a million that this stuff isn't gonna work like they want."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: Explicitly claims "inevitable model collapse" - that's the misrepresentation trigger. Paper never claimed inevitability. Correctly coded.

---

### Code 366 ✓ CORRECT
**Post (2024-12-18)**: "It's not just unethical, but this kind of feedback loop is mathematically proven to make diffusion models worse: [...] So even as a scam, it's self-defeating & leads to model collapse (aka Habsburg AI.) Like Kessler Syndrome but for data, this will ruin all naive models."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: THREE misrepresentation triggers: "mathematically proven", "will ruin all", "inevitable failure". This is a textbook misrepresentation. Correctly coded.

---

### Code 364 ✓ CORRECT
**Post (2024-12-18)**: "(2/22/24) people who actually have their hands in working with LLMs: MODEL COLLAPSE / tech companies: nah, it's fine / ChatGPT: All work and no play makes Jack a dull boy x3"

**Assigned**: substantive_mention, misrepresentation, inaccurate

**Analysis**: Implies ChatGPT is already showing collapse symptoms (repetitive output from the movie The Shining reference). Claims real-world collapse occurrence without evidence. Misrepresentation + inaccurate are correct.

---

### Code 274 ✓ CORRECT
**Post (2025-04-15)**: "AI is not a healthy research community, as the debate on X over this paper shows. Model collapse can only happen under unlikely and very stupid conditions (arXiv:2404.01413) and *all* serious AI training uses synthetic data today. But it's from Meta and got into ICLR."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: Wait - this is actually a SKEPTICAL post attacking the model collapse concern. The poster is saying collapse "can only happen under unlikely... conditions" - this is a CRITIQUE of the collapse narrative, not a misrepresentation OF the paper.

**Issue**: This post is misclassified. It should be substantive_mention (skeptical commentary, not authoritative claim about collapse). The claim_strength is wrong. This post DOES NOT misrepresent Shumailov; it argues Shumailov's conditions are unrealistic. Should be: substantive_mention, accurate (correctly identifies conditions), inaccurate (in Epoch 5, mitigations exist but the skeptical claim about "unlikely conditions" is debatable).

**Verdict: WRONG CODING - claim_strength should be substantive_mention, not authoritative_claim**

---

### Code 265 ✓ CORRECT
**Post (2025-04-24)**: "Yep - there is a paper in nature about "inevitable model collapse." If new content starts being primarily AI, LLMs become garbage quickly. So they can't succeed at what the hyper-capitalists want because they will always need real creativity to feed on."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Inevitable model collapse", "LLMs become garbage", "will always need" - all indicate certainty framing. Paper never claimed inevitability. Correctly coded.

---

### Code 241 ✓ CORRECT
**Post (2025-05-26)**: "This is 100% what is happening and will happen: 'AI models collapse when trained on recursively generated data.' Shumalov et al., Nature. 2024..."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "100% what is happening and will happen" - categorical certainty claim. Correctly coded.

---

### Code 225 ✓ CORRECT
**Post (2025-05-28)**: "AI model collapse has started / From @theregister.com"

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Has started" claims real-world occurrence. Correctly coded.

---

### Code 219 ✓ CORRECT
**Post (2025-05-28)**: '"We're going to invest more and more in AI, right up to the point that model collapse hits hard and AI answers are so bad even a brain-dead CEO can't ignore it."'

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Model collapse hits hard" - inevitable future scenario. Correctly coded.

---

### Code 216 ✓ CORRECT
**Post (2025-05-28)**: "Write this down on a sticky and put in on your monitor: "Model Collapse." You'll be glad you did. It's coming to an LLM near you, and maybe it's already here."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "It's coming... and maybe it's already here" - claims certain future occurrence. Correctly coded.

---

### Code 209 ✓ CORRECT
**Post (2025-05-28)**: "What happens when the AI models we use at work and in our personal lives give us bad, total nonsense data in replies? "AI model collapse" is almost here:"

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Is almost here" - frames as near-certain coming event. Correctly coded.

---

### Code 205 ✓ CORRECT
**Post (2025-05-29)**: "Welp, here we go... AI model collapse is becoming pervasive."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Is becoming pervasive" - claims real-world widespread occurrence. Correctly coded.

---

### Code 179 ✓ CORRECT
**Post (2025-06-02)**: 'was always a DOA "technology" / "We're going to invest more and more in AI, right up to the point that model collapse hits hard and AI answers are so bad even a brain-dead CEO can't ignore it,"'

**Assigned**: substantive_mention, misrepresentation, inaccurate

**Analysis**: Quote claims collapse "hits hard" (inevitable outcome). Poster adds "DOA technology" (dead-on-arrival). Correctly coded.

---

### Code 169 ✓ CORRECT
**Post (2025-06-05)**: "This is called "model collapse". It can only get worse. The more AI there is in the world, the more it will poison its own output..."

**Assigned**: substantive_mention, misrepresentation, inaccurate

**Analysis**: "Can only get worse", "will poison" - inevitability and universality framing. Correctly coded.

---

### Code 167 ✓ CORRECT
**Post (2025-06-06)**: "Can't believe the media isn't more focused on inevitable model collapse. The AI hype debt/credit bubble will implode when it becomes clear these systems have irreversibly polluted themselves with synthetic rot."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Inevitable model collapse", "irreversibly polluted" - classic misrepresentation language. Correctly coded.

---

### Code 127 ✓ CORRECT
**Post (2025-07-02)**: "Which paper? There are many. All models collapse when they are trained on their own output. The phenomenon is already detectable in Google's ai summaries and in Copilot's generated source code."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "ALL models collapse", "phenomenon is already detectable" - universality + real-world claim. Correctly coded.

---

### Code 115 ✓ CORRECT
**Post (2025-08-10)**: 'Researchers already coined a term for this inevitable enshittification: "model collapse"'

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Inevitable enshittification" - frames as certain outcome. Correctly coded.

---

### Code 67 ✓ CORRECT
**Post (2025-12-02)**: "I mean, we know for a fact that training generative AI on the output of generative AI simply result in the collapse of the model and nothing more."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Know for a fact", "simply result in collapse" - categorical certainty. Correctly coded.

---

### Code 18 ✓ CORRECT
**Post (2026-02-21)**: "#Emergencia Algorítmica: El fenómeno del " #Model #Collapse" amenaza con #colapsar la inteligencia artificial global en 2026 (+IA-CANIBAL)"

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: Spanish post claiming model collapse threatens to collapse all global AI in 2026. "Amenaza" (threatens) + temporal certainty. Correctly coded.

---

### Code 15 ✓ CORRECT
**Post (2026-02-24)**: "LLMs are going to model collapse anyway. Its inevitable. Their is simply not enough clean stolen real data to train on."

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: "Going to... inevitable" - textbook inevitability claim. Correctly coded.

---

### Code 11 ✓ CORRECT
**Post (2026-02-25)**: "Model Collapse Ends AI Hype"

**Assigned**: authoritative_claim, misrepresentation, inaccurate

**Analysis**: Makes a categorical claim that collapse will end AI entirely. Correctly coded.

---

**VERDICT: Misrepresentation sample 24/25 CORRECT**

**1 Issue Code 274**: Misclassified claim_strength - should be substantive_mention (skeptical commentary), not authoritative_claim.

---

## NOT_APPLICABLE SUBSTANTIVE_MENTION (n=5)

### Code 222 ⚠️ BORDERLINE
**Post (2025-05-28)**: "An article on AI model collapse. It cannot come soon enough."

**Assigned**: substantive_mention, not_applicable

**Analysis**: "It cannot come soon enough" - this is the poster's evaluative opinion. They're expressing a desire for collapse to happen. The question: does this post assert anything about the paper's findings or collapse mechanism? Or is it just a personal reaction to the concept?

The codebook says not_applicable applies when: "The post is a substantive_mention but does NOT assert or imply anything about the paper's findings or conclusions."

This post does not explain HOW collapse happens, WHEN it will happen, or even detailed claims about collapse - just expresses desire for it. **CORRECT coding as not_applicable** - no factual claims about the paper or mechanism.

---

### Code 204 ✓ CORRECT
**Post (2025-05-29)**: 'Phrase of the moment: "model collapse"'

**Assigned**: substantive_mention, not_applicable

**Analysis**: Pure meta-commentary on terminology. No claims about what collapse is or how it works. Correctly coded as not_applicable.

---

### Code 282 ✓ CORRECT
**Post (2025-03-31)**: "achei um aqui que parece interessante, depois vou ler. / arxiv.org/abs/2305.17493"

**Assigned**: substantive_mention, not_applicable

**Analysis**: Portuguese: "found one here that seems interesting, will read it later" + paper link. This is a personal note about finding the paper, not a claim about its findings. Correctly coded as not_applicable.

---

### Code 325 ⚠️ BORDERLINE
**Post (2025-02-03)**: "Deep Research, Deep Bullshit, and the potential (model) collapse of science / How Sam Altman's hype might just bite us all in the behind:"

**Assigned**: substantive_mention, not_applicable

**Analysis**: Post frames collapse as a potential threat to science and connects it to Altman's AI hype. The claim "collapse could undermine science" is an inference about collapse implications. 

**Question**: Does this assert something about the paper's findings? The post is making a CAUSAL INFERENCE (AI hype + model collapse = threat to science) but is it about the paper's findings?

The codebook allows: "Industry inference: Reasonable inferences about how findings motivate industry practice (e.g., 'companies are seeking more training data because of collapse concerns') are accurate if grounded in the paper's findings."

This post extends collapse implications to SCIENCE itself. It's not just inference about industry practice, but about broader epistemic consequences. It's borderline whether this asserts something about the paper.

**Verdict**: Probably CORRECT as not_applicable - the post is meta-commentary about implications, not direct claims about what the paper found or how collapse works.

---

### Code 388 ⚠️ BORDERLINE → LIKELY WRONG
**Post (2024-12-06)**: "I've mentioned model collapse in a few discussions online and every time I got shouted down. Microsoft's "Phi" models which claim to successfully train on synthetic data w/out collapse gets mentioned, but I'm not convinced: if Phi solved model collapse surely they'd be a much bigger deal right?"

**Assigned**: substantive_mention, not_applicable

**Analysis**: This post makes a SKEPTICAL ARGUMENT about whether the collapse problem is real. It cites a specific counterexample (Phi models) and questions its importance. 

The poster IS making claims about: (1) Whether collapse is a real problem ("I'm not convinced"), (2) Evidence for mitigation (Phi models), (3) Logical reasoning about what would happen if collapse were solved.

This is NOT just a personal reaction or meta-commentary. The poster is asserting that either collapse isn't real or isn't as serious as claimed. **This should be coded with paper_fidelity** - it's a claim about whether the collapse problem is valid/important.

**Issue**: Should be substantive_mention, accurate (correctly identifies Phi as a potential mitigation), accurate or inaccurate (depends on whether Phi actually trains on synthetic data without collapse - but the post is asking a reasonable skeptical question, not misrepresenting).

**Verdict: WRONG CODING - should have paper_fidelity evaluated, not marked not_applicable.**

---

**VERDICT: Not_applicable sample 3/5 CORRECT**

**Borderline Code 325**: Probably correct but depends on interpreting "implies claims about findings"

**Wrong Code 388**: Should be evaluated for paper_fidelity - makes skeptical claims about whether collapse is a real problem.

---

