# Day 4: Operating the platform and architecture decisions

**Modules:** 7 (Running the platform) and 8 (Architecture decisions and roadmap)
**Activities today:** Lab 13 and Lab 14 (notebooks); Lab 15 (write an ADR, individual); Lab 16 (review a reference
architecture, groups); capstone briefing; Assignment A3 (homework)

Every notebook lab works the same way: open it from the course page's **Open in Colab** badge (or from the
`notebooks` folder in VS Code), run the cells from top to bottom, then the **Try this** cells at the end, and answer
the questions written under them. A lab worked if every code cell has a green tick and there is no red error box.
When you finish a lab, type `Lab N done` in the course chat.

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
managed platform (Cloud Run, App Runner, Azure Container Apps, Kubernetes) for longer or heavier work. AI requests
are slow (seconds) and spiky, so design for timeouts, streaming and retries.

**Serving many teams (multi-tenancy):** one platform, many applications. Each gets its own API key or identity,
quota, budget, prompt and index namespace, and its own cost line.

**Caching:** exact-match cache for repeated questions; embedding cache for unchanged documents; provider prompt
caching for long, repeated system prompts.

### Lab 13: Put the assistant behind a web UI (notebook `lab13_deploy_ui`, 25 minutes)
**What you do:** run the notebook from top to bottom. Section 2 starts the app; ask it the three questions listed in
the notebook, share the link with your neighbour, then press the cell's **stop** button.
**What you will see:** one test answer about carrying forward leave (up to 10 days); then a chat app with the title
"Meridian Policy Assistant". In Colab the cell prints a `https://....gradio.live` link that anyone can open while the
cell runs. **The cell keeps running while the app is live; that is expected.**
**Answer at the end:** which three rows of the production table in section 3 would you insist on before letting 5,000
employees use it?

After the lab your trainer demos the same assistant running on a serverless edge platform with its own web address.

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

**Cost levers:** smaller model for easy requests; fewer or shorter passages (k, chunk size); caching; batch
processing for offline jobs; prompt caching; output length limits.

### Lab 14: Traces, latency and cost (notebook `lab14_monitoring_cost`, 25 minutes)
**What you do:** run the notebook from top to bottom, then the two Try this cells. In section 3 you may change the
four numbers (employees, questions per day, working days, exchange rate) to fit your organisation.
**What you will see:** a trace table where the `llm call` span takes almost all the time; a table of 8 requests
where input tokens are many times the output tokens; a summary with p50 and p95 latency and cost per request; a bar
chart; a monthly forecast line such as `330,000 requests/month -> about USD ...`; and a budget check printing `OK`.
**Answer at the end:** who pays? How would you charge each business unit for its use?

---

## Module 8.1: Decision records

An **Architecture Decision Record (ADR)** captures one significant decision: context, options, decision,
consequences. AI platforms produce many such decisions (model, vector store, hosting, guardrail approach, build or
buy), and they need revisiting as the market changes quickly. ADRs make the reasoning reviewable.

**AI non-functional requirements to state explicitly:** quality bar (test set and pass rate), latency target, cost
ceiling, data residency, retention, explainability (citations), human oversight, availability and fallback,
**vendor exit plan** (how you would switch model or vector database within weeks).

### Lab 15: Write an ADR (30 minutes: 20 minutes alone, 10 minutes in pairs)
**The decision:** "Which model (or models) does the Meridian employee assistant use?" Assume 5,000 employees, the
policies from this week, employee data that must stay in India, and a budget of INR 50,000 a month for model use.

**Steps:**
1. Open [adr_template.md](adr_template.md). Copy the headings into a new document (Word, Google Docs or the course
   Miro board, as your trainer says).
2. **Title:** `ADR-001: Model choice for the Meridian employee assistant`.
3. **Context:** 3 to 5 lines: the users, the constraints above, and your evidence (your Lab 3 matrix result and your
   Lab 14 cost per request).
4. **Options considered:** at least 3 options in the table, each with one pro and one con. Example options: a hosted
   large model; a hosted small model; a cloud model service in an Indian region; a self-hosted open model; a small
   model with a large model only for hard questions.
5. **Decision:** one sentence starting "We will ... because ...".
6. **Consequences:** one good point, one accepted downside, one risk with its mitigation.
7. **How we will know this was wrong:** one metric with a number (for example "pass rate below 85% on the test set").
8. **Exit plan:** what changes if you reverse the decision, and how long it takes.
9. **Pair review (10 minutes):** swap with your neighbour. Check two things and tell them: does the ADR name the
   downside it accepts? Is the "wrong if" a number someone could actually measure?

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

### Lab 16: Review a reference architecture (30 minutes in groups, then 3 minutes per group)
A retailer's team proposes this design for a **customer support copilot**. It has problems. Find them.

```
Customer --> website chat --> Support Copilot API (one shared service account)
   Support Copilot API --> LLM provider (one provider, no fallback, no timeout)
   Support Copilot API --> Vector DB (all documents, no filters; full rebuild every night)
   Support Copilot API --> CRM API (read and write, including issuing refunds)
   Agent desktop shows suggested replies; the agent clicks "Send"
   Logs: application logs only, kept for 7 days
```

**Steps:**
1. Copy the diagram into your group's Miro frame.
2. Answer the five questions below in your frame, one sticky note per answer.
3. Choose one person to present in 3 minutes.

**Questions:**
1. Where does the user's identity flow? Is retrieval filtered by it?
2. Where are the guardrails? What is missing?
3. What happens when the model provider is down or slow?
4. How is quality measured before and after a release?
5. Name your three most important changes, and outline a 90-day plan to a pilot (what happens in weeks 1 to 4, 5 to 8
   and 9 to 12).

---

## Capstone briefing (end of today)
Your trainer presents tomorrow's capstone from [day5_capstone.md](day5_capstone.md): the cases, deliverables,
schedule and scoring. Your team chooses its case before leaving today.

## Assignment A3: One ADR for your capstone (about 45 minutes, due before 09:15 tomorrow)
Write one ADR for the decision your team finds hardest in its capstone case (for example: model choice, vector
database, hosting, agent or workflow). Use the same headings as Lab 15, from [adr_template.md](adr_template.md).
Each team member writes their own; your team may use the best one as one of its two capstone ADRs.
**Submit** it the same way as Assignments A1 and A2.

## Key terms
API gateway, model gateway, multi-tenancy, trace, span, p95, showback, chargeback, prompt caching, ADR,
non-functional requirement, vendor exit plan. See [glossary.md](glossary.md).

## Further reading
* OpenTelemetry semantic conventions for GenAI: https://opentelemetry.io/docs/specs/semconv/gen-ai/
* Langfuse (open-source LLM tracing): https://langfuse.com/docs
* ADR templates and practice: https://adr.github.io
* Cloudflare Workers AI and Vectorize: https://developers.cloudflare.com/workers-ai/ and https://developers.cloudflare.com/vectorize/
