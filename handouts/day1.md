# Day 1: Foundations

**Modules:** 1 (AI platform foundations) and 2 (Models and platform choices)
**Labs:** 1 (worksheet), 2, 3, 4  **Assignment:** A1 (due Day 2 morning)

## By the end of today you can
* Describe an enterprise AI platform as layers, and place an existing application on them
* Explain tokens, context windows, temperature and structured output, and what each means for cost and design
* Compare models on quality, latency, cost, data residency and lock-in, and record the decision
* Improve a prompt and prove the improvement with a measurement

---

## Module 1.1: What an AI platform (an "AI OS") is

An **AI platform** is the shared set of capabilities that lets many teams build AI features safely and cheaply,
instead of each team wiring models, data and controls on its own. Think of it the way an operating system serves
applications: common services, common rules, one place to observe and govern.

```
+------------------------------------------------------------------------+
|  Applications      chat assistants, copilots, document processing, agents
+------------------------------------------------------------------------+
|  Orchestration     prompts, workflows, agents, routing between models   |
+--------------------+----------------------+----------------------------+
|  Knowledge         |  Tools and actions   |  Guardrails                 |
|  RAG, vector DBs,  |  APIs, MCP servers,  |  input/output checks, PII,  |
|  document pipelines|  approvals           |  policy, access control     |
+--------------------+----------------------+----------------------------+
|  Model layer       hosted APIs, cloud model services, self-hosted models,
|                    a gateway that routes, caches, limits and meters      |
+------------------------------------------------------------------------+
|  Operations        evaluation, tracing, cost, release management, audit |
+------------------------------------------------------------------------+
|  Foundations       identity, network, secrets, data platform, cloud     |
+------------------------------------------------------------------------+
```

**Why architects care:** without a platform, every team picks its own model, stores its own embeddings, writes its
own guardrails and has no shared view of cost or risk. The platform is where reuse, security and cost control live.

**Build, buy or compose?** Few enterprises build every layer. A typical pattern: buy the model layer (cloud model
service or API), use managed services for vector search and tracing, and build the thin layers that encode your
own rules (guardrails, access control, evaluation sets, approval flows).

### Lab 1 (worksheet, 30 minutes, in groups)
Pick an application your group knows well (for example: a customer service portal, an HR helpdesk, a claims system).
On the whiteboard or Miro board:
1. Draw the layers above.
2. Place the AI feature you would add (for example "answer customer questions from policy documents").
3. For each layer write: **what exists today**, **what is missing**, **who would own it**.
4. Circle the one gap that would block a production launch.

Be ready to present in 3 minutes.

---

## Module 1.2: LLM basics for architects

| Concept | What it is | Why it matters to an architect |
|---|---|---|
| **Token** | a piece of a word; about 4 characters of English on average | pricing, rate limits and context size are all in tokens |
| **Context window** | the maximum tokens per request (prompt + answer) | limits how much document text you can send; bigger is slower and costlier |
| **System prompt** | instructions that frame every request | where behaviour and rules are set; it is **not** a security boundary |
| **Temperature** | randomness of the output (0 = most repeatable) | use 0 for extraction, classification and RAG; higher for creative text |
| **Structured output** | asking for JSON, optionally with a schema | applications need data, not prose; always validate it |
| **Streaming** | sending tokens as they are generated | better perceived speed for chat; same cost |
| **Latency** | time to first token plus generation time | grows with output length and model size |

**Rule of thumb for cost:** `cost = input_tokens x input_price + output_tokens x output_price`. In RAG systems the
input (retrieved passages) is usually far larger than the output, so retrieval design drives cost.

### Lab 2: Your first LLM calls (notebook `lab02_first_llm_call`)
You will make a call, read its token counts, compare with and without a system prompt, extract JSON from an email,
stream an answer and compare a big and a small model on latency and estimated cost.

**Look for:** how much the system prompt changes the answer; what happens to JSON when information is missing.

---

## Module 2.1: Choosing models

### The four ways to consume a model
| Option | Examples | Strengths | Watch out for |
|---|---|---|---|
| Hosted API from a model lab or inference provider | OpenAI, Anthropic, Groq, Together | best models, no infrastructure | data leaves your network; check region, retention and contract terms |
| Cloud provider model service | Google Vertex AI, AWS Bedrock, Azure AI Foundry | runs in your cloud tenancy, enterprise controls, many models in one place | regional availability of specific models; cloud lock-in |
| Self-hosted open-weight model | Llama, Qwen, Mistral, Gemma on your GPUs (e.g. with vLLM) | full data control, fixed cost at high volume | GPU capacity, operations skills, usually lower quality than top hosted models |
| Small model on device or edge | in-browser or mobile models | privacy, offline, zero per-call cost | limited capability |

### Selection criteria
Quality on **your** tasks (measured, not from leaderboards), latency, cost per request and per month, context window,
data residency and privacy terms, availability and rate limits, ecosystem and lock-in risk, licence (for open models).

**Start small:** use the smallest model that passes your test set; route only hard requests to a big model.
A **model gateway** (a thin service or product between apps and providers) makes this routing, fallback, caching and
metering a platform capability instead of per-app code.

### Lab 3: Decision matrix (notebook `lab03_model_decision_matrix`)
Measure two models on four tasks, then score four deployment options with weights you choose for a use case.

---

## Module 2.2: Prompt design

A good production prompt usually has:
1. **Role and context:** who the model is acting as, for whom
2. **Task and rules:** what to do, what never to do
3. **Definitions:** for every label or category, what it means
4. **Output format:** JSON with fixed keys, or a fixed structure
5. **Examples (few-shot):** 2 to 5 short input and output pairs, including a tricky one

**Prompts are code.** Keep them in version control or a prompt registry, give them version ids, review changes,
and test every change against a fixed set of examples (Module 5 makes this a release gate).

### Lab 4: Prompt design (notebook `lab04_prompt_design`)
Classify 20 labelled support tickets with a naive prompt (v1) and a structured prompt (v2). Compare accuracy and
look at the errors.

---

## Assignment A1 (about 45 minutes, due tomorrow morning)
Write a **one-page model choice note** for this use case: *an internal assistant that answers HR policy questions
for 8,000 employees of an Indian bank; HR data must stay in India.* Include: the options you considered, your
weighted criteria, your choice, and the one risk you would watch. Use your Lab 3 matrix.

## Key terms
AI platform, model gateway, token, context window, temperature, structured output, few-shot, prompt registry,
data residency, open-weight model. See [glossary.md](glossary.md).

## Further reading
* Groq API documentation: https://console.groq.com/docs
* OpenAI-compatible APIs (Gemini): https://ai.google.dev/gemini-api/docs/openai
* Google Cloud, "Choose a model": https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
* AWS Bedrock model choice: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
