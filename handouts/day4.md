# Day 4: Operating the platform and architecture decisions

**Modules:** 7 (Running the platform) and 8 (Architecture decisions and roadmap)
**Labs:** 13, 14, 15 (worksheet), 16 (worksheet)  **Assignment:** A3 (for your capstone, due Day 5 morning)

## By the end of today you can
* Describe what a production deployment of an AI assistant adds beyond a prototype
* Read a trace, find where latency and cost go, and forecast a monthly bill
* Write an Architecture Decision Record (ADR) for an AI choice
* Critique a reference architecture and outline a phased adoption roadmap

---

## Module 7.1: Deployment patterns

**From notebook to service**
```
users --> SSO / identity --> API gateway (auth, rate limits, quotas per tenant)
      --> AI application service (stateless; serverless or containers)
            |--> model gateway --> model providers (with fallback)
            |--> vector database (filters from the user's identity)
            |--> tools / MCP servers (least privilege)
            |--> cache (frequent questions, embeddings)
      --> logs, traces, metrics, cost --> dashboards and alerts
ingestion pipeline: document sources --> extract --> chunk --> embed --> vector DB (on change)
```

**Hosting choices:** serverless functions or edge workers (simple, scale to zero, short requests), containers on a
managed platform (Cloud Run, App Runner, Azure Container Apps, Kubernetes) for longer or heavier work. AI requests are
slow (seconds) and spiky, so design for timeouts, streaming and retries.

**Serving many teams (multi-tenancy):** one platform, many applications. Each gets its own API key or identity, quota,
budget, prompt and index namespace, and its own cost line.

**Caching:** exact-match cache for repeated questions; embedding cache for unchanged documents; provider prompt caching
for long, repeated system prompts.

### Lab 13: Web UI and a shareable link (notebook `lab13_deploy_ui`)
Wrap the assistant in a Gradio chat UI and share a link. Your trainer will demo the same assistant deployed on a
serverless edge platform with its own domain name.

---

## Module 7.2: Monitoring and cost

**Trace:** one request broken into timed steps (spans): embed, search, prompt build, LLM call, guards. Standard:
OpenTelemetry (with GenAI semantic conventions); AI-specific tools include Langfuse, Arize Phoenix and cloud tracing.

**What to watch**
| Signal | Why |
|---|---|
| latency p50 and p95 per step | users feel p95; the LLM call usually dominates |
| tokens in and out per request | the cost driver; input dominates in RAG |
| cost per request, per tenant, per day | budgets, showback and chargeback |
| error and rate-limit rates per provider | trigger fallback |
| refusal rate and user feedback | quality drift |
| guard events | attacks, data leaks |

**Cost levers:** smaller model for easy requests; fewer or shorter passages (k, chunk size); caching; batch processing
for offline jobs; prompt caching; output length limits.

### Lab 14: Traces and cost (notebook `lab14_monitoring_cost`)

---

## Module 8.1: Decision records

An **Architecture Decision Record (ADR)** captures one significant decision: context, options, decision, consequences.
AI platforms produce many such decisions (model, vector store, hosting, guardrail approach, build or buy) and they need
revisiting as the market changes quickly. ADRs make the reasoning reviewable.

**AI non-functional requirements to state explicitly:** quality bar (test set and pass rate), latency target, cost
ceiling, data residency, retention, explainability (citations), human oversight, availability and fallback,
**vendor exit plan** (how you would switch model or vector database within weeks).

### Lab 15: Write an ADR (worksheet, 30 minutes, individual)
Using [adr_template.md](adr_template.md), write an ADR for: **"Which model (or models) does the Meridian employee
assistant use?"** Use your Lab 3 matrix and Lab 14 numbers. Peer review in pairs: does the ADR state the trade-off it
accepts?

---

## Module 8.2: Reference architectures and roadmap

**Common enterprise patterns**
* **Knowledge assistant** (RAG over internal documents): HR, IT, policy, product knowledge
* **Customer support copilot:** suggested replies to agents, with human approval, before any customer-facing bot
* **Document processing:** extraction and classification of forms, invoices, KYC (workflow, not agent)
* **Analyst assistant:** natural language over governed data (text-to-SQL with strict controls)

**Phased adoption roadmap (example)**
| Phase | Duration | Focus |
|---|---|---|
| 0. Foundations | 0 to 3 months | identity, model gateway, approved providers, logging, policy, first test sets |
| 1. Internal assistants | 3 to 6 months | low-risk internal RAG use cases; measure value and quality |
| 2. Copilots | 6 to 12 months | human-in-the-loop tools for employees serving customers |
| 3. Selective automation | 12 months and later | agents with narrow tools and approvals, where the data proves it |

### Lab 16: Review a reference architecture (worksheet, 30 minutes, groups)
Your trainer shows a reference architecture for a customer support copilot. In groups, answer:
1. Where does identity flow, and is retrieval filtered by it?
2. Where are the guardrails? What is missing?
3. What happens when the model provider is down or slow?
4. How is quality measured before and after release?
5. Name three changes you would make, and outline a 90-day plan to reach a pilot.

---

## Assignment A3 (about 45 minutes, due tomorrow morning)
Write **one ADR for your capstone design** (your team's capstone case is announced today). Choose the decision your
team finds hardest.

## Key terms
API gateway, model gateway, multi-tenancy, trace, span, p95, showback, chargeback, prompt caching, ADR,
non-functional requirement, vendor exit plan. See [glossary.md](glossary.md).

## Further reading
* OpenTelemetry semantic conventions for GenAI: https://opentelemetry.io/docs/specs/semconv/gen-ai/
* Langfuse (open-source LLM tracing): https://langfuse.com/docs
* ADR templates and practice: https://adr.github.io
* Cloudflare Workers AI and Vectorize: https://developers.cloudflare.com/workers-ai/ and https://developers.cloudflare.com/vectorize/
