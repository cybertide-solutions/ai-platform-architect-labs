# Day 3: Trust (evaluation and security) and the mini project

**Modules:** 5 (Evaluation and quality) and 6 (Security and Responsible AI)
**Labs:** 9, 10, 11, 12 and the **mini project**

## By the end of today you can
* Build a test set and score an assistant on retrieval and on answers, including with an LLM judge
* Turn prompt and model changes into gated releases
* Explain the main AI-specific attacks and demonstrate prompt injection
* Design layered guardrails and an audit trail that support DPDP Act and EU AI Act obligations

---

## Module 5.1: Measuring quality

"It looked good in the demo" is not a quality bar. You need a **test set** (also called an evaluation set or golden set):
questions with expected answers and, for RAG, the source that contains them.

**What to measure in a RAG assistant**
| Metric | Question it answers |
|---|---|
| Retrieval hit rate (recall at k) | did search find the right document? |
| Faithfulness (groundedness) | is every claim in the answer supported by the passages? |
| Answer correctness | does the answer match the expected answer? |
| Refusal accuracy | does it say "I don't know" when the documents don't have the answer? |
| Latency and cost per answer | can we afford it at scale? |

**LLM-as-judge:** a model grades answers against the expected answer using written criteria. It is fast and cheap,
but it can be wrong, so spot-check its verdicts and keep the criteria strict and simple. Human review stays essential for
high-risk domains.

**Where test questions come from:** subject-matter experts, real user questions (logged and anonymised), past incidents
and complaints. A test set is a living asset: every production failure becomes a new test.

Frameworks such as Ragas, DeepEval, promptfoo and cloud evaluation services automate this; the concepts are the ones in
the lab.

### Lab 9: Build a test set (notebook `lab09_eval_set`)
Extend the 5 starter questions to 15, score the assistant, and classify each failure as retrieval, generation, judge or test.

---

## Module 5.2: Safe releases

In AI systems, **behaviour changes without code changes**: a new prompt, a new model version, a new chunk size, new
documents. Treat each as a release:
1. Run the test set before and after
2. Compare scores; some tests are **must-pass** (refusals, safety)
3. A **release gate** in CI ships or blocks the change
4. Optionally run the new version in **shadow** (on real traffic, not shown to users) or as an **A/B test**

Pin model versions where the provider allows it, and plan for the provider retiring them.

### Lab 10: Release gate (notebook `lab10_safe_release`)

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

### Lab 11: Attack the assistant (notebook `lab11_prompt_injection`)

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

**India: Digital Personal Data Protection Act, 2023 (DPDP Act).** Key ideas for AI systems: process personal data only
for a stated, consented purpose; collect the minimum; honour rights to access, correct and erase; protect against
breaches and report them; be careful about what goes to third-party processors (including model APIs). Check the current
DPDP Rules with your legal team.

**EU AI Act** (relevant if you serve EU users or are part of an EU group): risk-based. Some uses are prohibited;
**high-risk** uses (for example credit scoring, hiring) carry strict requirements for risk management, data governance,
logging, human oversight and transparency; chatbots must tell users they are talking to an AI.

**Audit log:** who asked, what (masked), which sources were used, what was answered, which guard fired. Protect the log
itself: it contains sensitive data.

### Lab 12: Guardrails (notebook `lab12_guardrails`)

---

## Mini project: Policy Q&A Assistant (2 hours, teams of 4 to 5)
Notebook `mini_project`. Combine Labs 5 to 9: answers with citations, one ticket tool behind an approval rule, and a
score on at least 8 test questions. Every step works with defaults; your team makes and defends the decisions marked
`TEAM DECISION`.

**Demo (5 minutes per team):** your design decisions and why; your score and the most instructive failure; a live
policy question with citations; a ticket request that triggers approval; what you would do before production.

**Assessed on:** working demo (40%), quality of decisions and reasoning (40%), test set quality (20%).

## Key terms
test set, recall at k, faithfulness, LLM-as-judge, release gate, shadow testing, prompt injection (direct, indirect),
excessive agency, guardrail, PII, DPDP Act, high-risk AI system, audit log. See [glossary.md](glossary.md).

## Further reading
* OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/
* Ragas (RAG evaluation metrics): https://docs.ragas.io
* Digital Personal Data Protection Act, 2023 (MeitY): https://www.meity.gov.in/data-protection-framework
* EU AI Act overview: https://artificialintelligenceact.eu
