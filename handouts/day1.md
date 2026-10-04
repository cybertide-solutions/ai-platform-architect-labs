# Day 1: Foundations

**Modules:** 1 (AI platform foundations) and 2 (Models and platform choices)
**Activities today:** Lab 1 (group worksheet), Lab 2, Lab 3, Lab 4 (notebooks), Assignment A1 (homework)

## By the end of today you can
* Describe an enterprise AI platform as six layers, and use them to find the gaps in a real application
* Explain tokens, context windows, temperature and structured output, and what each means for cost and design
* Compare models on quality, latency, cost, data residency and lock-in, and record the decision
* Improve a prompt and prove the improvement with a measurement

## How to run a notebook lab (all labs work the same way)
1. Open the course page on GitHub (link from your trainer) and click the **Open in Colab** badge next to the lab.
   If you work locally, open the same file from the `notebooks` folder in VS Code.
2. Run the cells **from top to bottom**, one at a time (**Shift+Enter**), and read the text between them.
   The first cell is always the setup cell.
3. At the end of each lab there are **Try this** cells. Run them and answer the question written under each one.
4. **The lab worked** if every code cell shows a green tick (Colab) or a check mark (VS Code) and there is no red
   error box. Answers from the AI model will differ from your neighbour's; that is expected.
5. When you have finished, type `Lab N done` in the course chat (for example `Lab 2 done`). This is how your trainer
   records lab completion, which counts towards your course score.

---

## Module 1.1: What an AI platform (an "AI OS") is

An **AI platform** is the shared set of capabilities that lets many teams build AI features safely and cheaply,
instead of each team wiring models, data and controls on its own. Think of it the way an operating system serves
applications: common services, common rules, one place to observe and govern.

**The six layers** (this diagram is used in Lab 1 and throughout the course):

```
+------------------------------------------------------------------------+
|  Applications     chat assistants, copilots, agents                    |
+------------------------------------------------------------------------+
|  Orchestration    prompts, workflows, agents, model routing            |
+----------------------+------------------------+------------------------+
|  Knowledge           |  Tools and actions     |  Guardrails            |
|  RAG, vector DBs,    |  APIs, MCP servers,    |  input and output      |
|  document pipelines  |  approvals             |  checks, PII, access   |
+----------------------+------------------------+------------------------+
|  Model layer      hosted APIs, cloud model services,                   |
|                   self-hosted models; a gateway that                   |
|                   routes, caches, limits and meters                    |
+------------------------------------------------------------------------+
|  Operations       evaluation, tracing, cost, releases,                 |
|                   audit                                                |
+------------------------------------------------------------------------+
|  Foundations      identity, network, secrets, data, cloud              |
+------------------------------------------------------------------------+
```
The middle row (Knowledge, Tools and actions, Guardrails) counts as **one layer** with three parts, which is why we say
six layers.

**Why architects care:** without a platform, every team picks its own model, stores its own embeddings, writes its
own guardrails and has no shared view of cost or risk. The platform is where reuse, security and cost control live.

**Build, buy or compose?** Few enterprises build every layer. A typical pattern: buy the model layer (a cloud model
service or an API), use managed services for vector search and tracing, and build the thin layers that encode your
own rules (guardrails, access control, evaluation sets, approval flows).

### Lab 1: Find the gaps in a real application (group worksheet, 30 minutes)
You work in a group of 4 to 5 on the group's Miro board (or a whiteboard).

1. **Choose an application** that someone in your group knows well, for example a customer service portal, an HR
   helpdesk or an insurance claims system.
2. **Choose one AI feature** you would add to it, for example "employees ask HR policy questions in chat".
3. **Write a header** at the top of your board: the application and the AI feature.
   Example: *HR helpdesk: employees ask HR policy questions in chat*
4. **Draw six empty boxes**, one per layer from the diagram above, from Applications at the top to Foundations at
   the bottom.
5. **In each box, write three short lines:**
   * **Today:** what your application already has in this layer. "Nothing" is a valid answer.
   * **Needed:** what must be built or approved for the new AI feature.
   * **Owner:** which team would be responsible. Name a team, not "IT". If nobody would own it, write "nobody".
6. **Circle the one "Needed" item** that would stop the feature going live, and note why.
7. **Present in 3 minutes:** the header, a quick walk down the six boxes, then the circled item and why it blocks
   the launch.

---

## Module 1.2: LLM basics for architects

| Concept | What it is | Why it matters to an architect |
|---|---|---|
| **Token** | a piece of a word; about 4 characters of English on average | pricing, rate limits and context size are all in tokens |
| **Context window** | the maximum tokens per request (prompt plus answer) | limits how much document text you can send; bigger is slower and costlier |
| **System prompt** | instructions that frame every request | where behaviour and rules are set; it is **not** a security boundary |
| **Temperature** | randomness of the output (0 = most repeatable) | use 0 for extraction, classification and RAG; higher for creative text |
| **Structured output** | asking for JSON, optionally with a schema | applications need data, not prose; always validate it |
| **Streaming** | sending tokens as they are generated | better perceived speed for chat; same cost |
| **Latency** | time to first token plus generation time | grows with output length and model size |
| **Reasoning model** | a model that "thinks" before answering | better on hard tasks; slower, and the thinking uses tokens you pay for |

**Rule of thumb for cost:** `cost = input_tokens x input_price + output_tokens x output_price`. In RAG systems the
input (retrieved passages) is usually far larger than the output, so retrieval design drives cost.

### Lab 2: Your first LLM calls (notebook `lab02_first_llm_call`, 25 minutes)
**What you do:** run the notebook from top to bottom, then the two **Try this** cells at the end.
**What you will see:** one answer from the model; a table of tokens, time and estimated cost for each call; the same
question answered with and without a system prompt; facts pulled out of an email as JSON; an answer appearing word by
word (streaming); the same question answered by a big and a small model.
**Answer at the end:** which of these settings belongs in application code, and which should a central platform team
control?

---

## Module 2.1: Choosing models

### The four ways to use a model
| Option | Examples | Strengths | Watch out for |
|---|---|---|---|
| Hosted API from a model company or inference provider | OpenAI, Anthropic, Groq, Together | best models, no infrastructure | data leaves your network; check region, retention and contract terms |
| Cloud provider model service | Google Vertex AI, AWS Bedrock, Azure AI Foundry | runs in your cloud account, enterprise controls, many models in one place | a specific model may not be offered in your region; cloud lock-in |
| Self-hosted open-weight model | Llama, Qwen, Mistral, Gemma on your own GPUs | full data control, fixed cost at high volume | GPU capacity, operations skills, usually lower quality than top hosted models |
| Small model on a device | in-browser or mobile models | privacy, offline, no per-call cost | limited capability |

### Selection criteria
Quality on **your** tasks (measured, not taken from public leaderboards), latency, cost per request and per month,
context window, data residency and privacy terms, availability and rate limits, lock-in risk, licence (for open models).

**Start small:** use the smallest model that passes your tests; send only hard requests to a big model.
A **model gateway** (a small service between applications and model providers) makes this routing, fallback, caching and
metering a platform capability instead of code in every application.

### Lab 3: Choose a model with a decision matrix (notebook `lab03_model_decision_matrix`, 30 minutes)
**What you do:** run the notebook. Part 1 runs four business tasks on a big and a small model. Part 2 scores four
deployment options against weighted criteria. The two **Try this** cells re-score the options for two different use
cases with weights already filled in.
**What you will see:** a results table (time, tokens, cost, answer per task and model), averages per model, a
decision matrix with a weighted score per option, and a bar chart.
**Answer at the end:** did the winning option change between the two use cases? Which weight changed it?

---

## Module 2.2: Prompt design

A good production prompt usually has five parts:
1. **Role and context:** who the model is acting as, and for whom
2. **Task and rules:** what to do, and what never to do
3. **Definitions:** for every label or category, what it means
4. **Output format:** JSON with fixed keys, or a fixed structure
5. **Examples (few-shot):** 2 to 5 short input and output pairs, including a tricky one

**Prompts are code.** Keep them in version control or a prompt registry, give them version ids, review changes,
and test every change against a fixed set of examples (Module 5 turns this into a release gate).

### Lab 4: Improve a prompt and measure it (notebook `lab04_prompt_design`, 30 minutes)
**What you do:** run the notebook. It classifies 20 labelled support tickets with a simple prompt (v1) and a structured
prompt (v2) and prints the accuracy of each. The two **Try this** cells test a v3 without examples, and show the
tickets where the model and the label disagree.
**What you will see:** an accuracy percentage for v1, v2 and v3, and a table of the tickets each version got wrong.
v1 is usually much lower than v2. Exact numbers differ between runs.
**Answer at the end:** who should own prompts in your organisation, and who approves a change?

---

## Assignment A1: Model choice note (about 45 minutes, due before 09:15 tomorrow)
**Use case:** an internal assistant that answers HR policy questions for 8,000 employees of an Indian bank.
HR data must stay in India.

**Write one page with these four headings:**
1. **Options considered:** at least three ways to use a model (see the table in Module 2.1), one line each.
2. **Criteria and weights:** your criteria with a weight for each, adding up to 100%. You can reuse your Lab 3 matrix.
3. **Choice:** the option you recommend, in two or three sentences, with the main reason.
4. **Risk to watch:** the one risk that worries you most about your choice, and how you would notice it.

**Submit** the page (Word, PDF or a photo of handwritten notes) to your trainer as announced on Day 1.

## Key terms
AI platform, model gateway, token, context window, temperature, structured output, reasoning model, few-shot,
prompt registry, data residency, open-weight model. See [glossary.md](glossary.md).

## Further reading
* Groq API documentation: https://console.groq.com/docs
* Gemini API, OpenAI compatibility: https://ai.google.dev/gemini-api/docs/openai
* Google Cloud, models on Vertex AI: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
* AWS Bedrock, supported models: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
