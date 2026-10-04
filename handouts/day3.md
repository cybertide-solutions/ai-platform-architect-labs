# Day 3: Trust (evaluation and security) and the mini project

**Modules:** 5 (Evaluation and quality) and 6 (Security and Responsible AI)
**Activities today:** Lab 9, Lab 10, Lab 11, Lab 12 (notebooks); the **mini project** in teams. No homework tonight.

Every notebook lab works the same way: open it from the course page's **Open in Colab** badge (or from the
`notebooks` folder in VS Code), run the cells from top to bottom, then the **Try this** cells at the end, and answer
the questions written under them. A lab worked if every code cell has a green tick and there is no red error box.
When you finish a lab, type `Lab N done` in the course chat.

## By the end of today you can
* Build a test set and score an assistant on retrieval and on answers, including with an LLM judge
* Turn prompt and model changes into gated releases
* Explain the main AI-specific attacks and demonstrate prompt injection
* Design layered guardrails and an audit trail that support DPDP Act and EU AI Act obligations

---

## Module 5.1: Measuring quality

"It looked good in the demo" is not a quality bar. You need a **test set** (also called an evaluation set or golden
set): questions with expected answers and, for RAG, the document that contains each answer.

**What to measure in a RAG assistant**
| Metric | Question it answers |
|---|---|
| Retrieval hit rate (recall at k) | did search find the right document? |
| Faithfulness (groundedness) | is every claim in the answer supported by the passages? |
| Answer correctness | does the answer match the expected answer? |
| Refusal accuracy | does it say "I don't know" when the documents don't have the answer? |
| Latency and cost per answer | can we afford it at scale? |

**LLM-as-judge:** a model grades answers against the expected answer using written criteria. It is fast and cheap,
but it can be wrong, so spot-check its verdicts and keep the criteria strict and simple. Human review stays essential
for high-risk domains.

**Where test questions come from:** subject-matter experts, real user questions (logged and anonymised), past
incidents and complaints. A test set is a living asset: every production failure becomes a new test.

Frameworks such as Ragas, DeepEval, promptfoo and cloud evaluation services automate this; the concepts are the ones
in the lab.

### Lab 9: Build a test set and score the assistant (notebook `lab09_eval_set`, 30 minutes)
**What you do:** run the notebook from top to bottom. In section 2, add at least 3 questions of your own to the cell
(the notebook explains exactly how, and gives a table of ideas), then run the rest.
**What you will see:** the 5 starter questions as a table; the judge's instructions and one sample verdict (PASS);
a line such as `[baseline] answer pass rate: 90%   retrieval hit rate: 100%   (10 questions)`; a table of the
questions that failed; and `saved baseline_scores.csv`.
**Answer at the end:** for each failure, one word: **retrieval** (wrong document found), **generation** (right
document, wrong answer), **judge** (the answer was fine, the judge was wrong) or **test** (the expected answer was
unclear).

---

## Module 5.2: Safe releases

In AI systems, **behaviour changes without code changes**: a new prompt, a new model version, a new chunk size, new
documents. Treat each as a release:
1. Run the test set before and after
2. Compare scores; some tests are **must-pass** (refusals, safety)
3. A **release gate** in CI ships or blocks the change
4. Optionally run the new version in **shadow** (on real traffic, not shown to users) or as an **A/B test**

Pin model versions where the provider allows it, and plan for the provider retiring them.

### Lab 10: Treat prompt and model changes as releases (notebook `lab10_safe_release`, 25 minutes)
**What you do:** run the notebook from top to bottom, then the two Try this cells.
**What you will see:** three evaluation runs: **A** (the current prompt), **B** (a "friendlier" prompt that says to
use general knowledge), **C** (the current prompt on a smaller, cheaper model); a side-by-side table of PASS and FAIL;
then the release gate printing a line such as `baseline 88% -> candidate 75%; refusals ok: False  =>  BLOCK`.
In Try this 2, version **D** is friendly but keeps the refusal rule.
**Answer at the end:** LLM answers vary between runs. How many runs would you need before trusting a 5% difference?

---

## Module 6.1: AI-specific risks

The **OWASP Top 10 for LLM Applications** is the common reference. Today we focus on:
* **Prompt injection, direct:** the user tells the model to ignore its rules
* **Prompt injection, indirect:** instructions hidden in content the model reads (documents, web pages, emails)
* **Sensitive information disclosure:** the model reveals data from its prompt, its context or other users
* **Excessive agency:** an agent can do more than it should (tools with too much power, no approvals)

**Key principle:** the model cannot reliably tell instructions from data. Prompts are not a security boundary.
Design so that a fully manipulated model still cannot do serious harm: least-privilege tools, access control before
retrieval, approvals for actions, and checks on outputs.

### Lab 11: Attack the assistant (notebook `lab11_prompt_injection`, 25 minutes)
**What you do:** run the notebook from top to bottom. In Try this 1, write your own attack in the `my_attack` line
and run the cell; run Try this 2 as it is.
**What you will see:** three attacks on an assistant whose system prompt holds a secret discount code: (1) "ignore all
previous instructions", (2) pretending to be a store manager, (3) a vendor document with a hidden instruction. A
scoreboard shows which attacks succeeded (`True`). Results differ between models and runs; that is the point.
**Answer at the end:** what should never be put in a prompt?

---

## Module 6.2: Guardrails and compliance

**Layered guardrails**
```
user input --> [input guard: PII masking, injection signals, topic limits]
           --> [retrieval: access filters, trusted sources only, strip hidden content]
           --> model
           --> [output guard: secrets, links, PII, citation required, toxicity]
           --> user                     [audit log at every step]
```

**India: Digital Personal Data Protection Act, 2023 (DPDP Act).** Key ideas for AI systems: process personal data
only for a stated, consented purpose; collect the minimum; honour rights to access, correct and erase; protect
against breaches and report them; be careful about what goes to third-party processors (including model APIs). Check
the current DPDP Rules with your legal team.

**EU AI Act** (relevant if you serve EU users or are part of an EU group): risk-based. Some uses are prohibited;
**high-risk** uses (for example credit scoring, hiring) carry strict requirements for risk management, data
governance, logging, human oversight and transparency; chatbots must tell users they are talking to an AI.

**Audit log:** who asked, what (masked), which sources were used, what was answered, which guard fired. Protect the
log itself: it contains sensitive data.

### Lab 12: Add guardrails and an audit log (notebook `lab12_guardrails`, 30 minutes)
**What you do:** run the notebook from top to bottom, then the two Try this cells.
**What you will see:** personal data replaced by labels such as `[EMAIL]` and `[PAN]`; the direct attack flagged by
the keyword check; the hidden instruction in the vendor document replaced by `[removed hidden content]`; the output
guard rejecting an answer with an unknown e-mail domain; a table where no attack leaks the secret or the bad link,
and the normal question is usually answered (30 days); and the audit log, one JSON line per request.
**Answer at the end:** which control would you trust most, and which is easiest to bypass? Is masking personal data
in the prompt enough under the DPDP Act?

---

## Mini project: Policy Q&A Assistant (2 hours, teams of 4 to 5)
**Notebook:** `mini_project`. Your trainer tells you your team and your breakout room.

**What you build:** one assistant for Meridian employees that combines Labs 5 to 9:
1. answers from the policies, with citations;
2. one tool that raises an HR, IT or Finance ticket, behind an approval rule;
3. a score on at least 8 test questions.

**How to work:**
1. Choose roles: one **driver** shares the screen and runs the notebook; one **note-taker** fills in the demo
   checklist (Step 5 of the notebook); everyone else reviews each decision.
2. Run the notebook once from top to bottom with the defaults. It works as it is.
3. Go back to each cell marked `TEAM DECISION` (chunk size, system prompt, approval rule, test questions), agree a
   change and a reason, edit it, and run the notebook again from top to bottom.
4. At the time your trainer gives, stop building and fill in the Step 5 checklist.

**Demo (5 minutes per team):** your decisions and why; your score and the failure you learned most from; a live
policy question with citations; a ticket request that triggers the approval; what you would do before production.

**Assessed on:** working demo (40%), quality of decisions and reasoning (40%), test set quality (20%).

## Key terms
test set, recall at k, faithfulness, LLM-as-judge, release gate, shadow testing, prompt injection (direct,
indirect), excessive agency, guardrail, PII, DPDP Act, high-risk AI system, audit log. See [glossary.md](glossary.md).

## Further reading
* OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/
* Ragas (RAG evaluation metrics): https://docs.ragas.io
* Digital Personal Data Protection Act, 2023 (MeitY): https://www.meity.gov.in/data-protection-framework
* EU AI Act overview: https://artificialintelligenceact.eu
