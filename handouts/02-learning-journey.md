# Learning journey and module-wise coverage

36 contact hours, twelve sessions of three hours. Breaks are additional. Example virtual slot: 09:30–12:45 with a 15-minute break. Five teams of four or five; rotate architect, driver, reviewer and evidence-recorder roles.

## Session 01: Frame the platform mandate | 3 hours

**Outcome:** An AI investment brief, measurable success criteria, and a platform capability map.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Business fit and non-AI baseline | 0.75 | Classify assistive, analytical and transactional workloads; identify a non-AI baseline; define value and exclusion criteria. |
| NFRs, risks and platform/app boundaries | 0.75 | Translate business constraints into latency, availability, data location, cost and quality targets; separate application, platform and infrastructure responsibilities. |
| Architecture discovery workshop | 1.17 | Map the AsterWorks brief to two applications and shared services; write an AI investment brief, measurable acceptance criteria and two ADR questions. |
| Decision review | 0.33 | Defend one build-versus-buy decision; state the assumption most likely to change it. |

**Practical reference:** `Requirements workshop`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 02: Select models and serving strategy | 3 hours

**Outcome:** A task-specific model evidence sheet and hosting/customisation ADR.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Tokens, modalities and task capability | 0.75 | Tokens, context, outputs, multimodal and embedding models; sampling and task fit; distinguish model reasoning from authoritative records. |
| Prompting, RAG, tuning and hosted/self-hosted choices | 0.75 | Prompt engineering, retrieval augmentation, fine-tuning and pretraining boundaries; model licence and data constraints; hosted APIs, managed endpoints and self-hosting. |
| Model experiment and serving calculation | 1.17 | Run typed request extraction against labelled development/holdout cases; inspect SQL totals, token/latency telemetry and weights-memory arithmetic; write a serving ADR. |
| Evidence review | 0.33 | Defend the model choice, uncertainty and the next benchmark required. |

**Practical reference:** `01_model_and_serving.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 03: Engineer the knowledge and data plane | 3 hours

**Outcome:** A versioned searchable corpus with source/permission evidence and retrieval measurements.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Sources, document structure and lifecycle | 0.75 | Trusted ingestion, source ownership, structured sections, chunking, metadata, versioning, revocation and deletion. |
| Lexical/vector/hybrid retrieval and SQL boundaries | 0.75 | Lexical relevance, embeddings/cosine, hybrid search and reranking tradeoffs; retrieval recall versus answer quality; SQL for exact structured facts. |
| Versioned retrieval experiment | 1.17 | Compare authorised search cases; publish an immutable changed policy; investigate broken chunks; execute persistent real embeddings when the endpoint is ready. |
| Evidence review | 0.33 | Choose retrieval strategy and document data lifecycle and remaining scale requirements. |

**Practical reference:** `02_data_plane.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 04: Mini project: a verifiable knowledge service | 3 hours

**Outcome:** A policy service, source inspection, unknown-answer cases and a semantic review sheet.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Acceptance contract and team scope | 0.33 | Define supported/unknown/partial-answer contracts and allocate team roles. |
| Build and investigate evidence failures | 1.50 | Build the policy service; inspect source evidence; expose a semantically wrong but structurally valid answer; add two cases and one improvement. |
| Five team demonstrations | 0.67 | Five teams demonstrate behavior, failure evidence and design reasoning in eight minutes each. |
| Review and assignment 1 | 0.50 | Review semantic labels, provide rubric feedback and set individual assignment 1. |

**Practical reference:** `03_mini_knowledge_service.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 05: Integrate tools, workflows and agents | 3 hours

**Outcome:** Exact business data, bounded tool use and durable reviewed-action evidence.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Typed tools, APIs and MCP responsibilities | 0.75 | Typed tools, function calling, API schemas, tool discovery and MCP host/client/server responsibilities; permission checks remain application responsibilities. |
| Workflow vs agent; state and human authority | 0.75 | Deterministic workflows versus model-selected agents; bounded steps, durable state, review binding, idempotency and external-system reconciliation. |
| Read-only SQL tools and transactional approval lab | 1.17 | Execute parameterised spend queries, native model tool calls and a SQLite reviewed purchase-request transaction; test tampering, expiry, replay and identity mismatch. |
| Evidence review | 0.33 | Defend the least complex workflow that meets the need. |

**Practical reference:** `04_tools_and_state.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 06: Build shared platform capabilities | 3 hours

**Outcome:** Two applications using the same platform with separate permissions, quotas and attribution.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Gateway placement and application onboarding | 0.75 | Gateway placement, common versus application-specific logic, model access and onboarding contracts. |
| Identity, tenancy, entitlements and consumption policy | 0.75 | Trusted identity, tenant/role boundaries, entitlement changes, cache keys, per-consumer quotas, usage attribution and noisy-neighbour control. |
| Two-application platform lab | 1.17 | Run policy and spend through Platform; test denied application, cross-tenant cache isolation and call quotas; implement one per-application policy extension. |
| Evidence review | 0.33 | Present a third-application onboarding contract and justify service boundaries. |

**Practical reference:** `05_shared_platform.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 07: Evaluate, version and release | 3 hours

**Outcome:** A release evidence pack that distinguishes software gates from semantic model acceptance.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Task metrics, labels, human review and judge calibration | 0.75 | Labelled tasks, retrieval versus semantic metrics, failure slices, human calibration, judge-model limits and representative evaluation sets. |
| Version manifests, regression, canary and rollback | 0.75 | Release manifests, immutable artifacts, regression gates, staged exposure, rollback and change ownership. |
| Release decision experiment | 1.17 | Reject a missing-source candidate against frozen cases; switch to a known version; require complete semantic review before an AI release decision. |
| Evidence review | 0.33 | Defend gate thresholds and identify evidence still missing for production. |

**Practical reference:** `06_release_engineering.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 08: Operate for reliability and performance | 3 hours

**Outcome:** An incident runbook, observed failure responses and capacity assumptions.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| SLIs/SLOs, traces and failure classification | 0.75 | User/task SLIs, availability, supported-answer rate, latency distributions, traces and service-versus-input failure classification. |
| Timeouts, queues, circuit breaking, cache and concurrency | 0.75 | Deadlines, retry budgets, queues/backpressure, concurrency, circuit boundaries, cache policy and recovery testing. |
| Failure and capacity experiment | 1.17 | Inject dependency failures, observe circuit opening, recover explicitly to evidence-only mode; reason about capacity and implement circuit isolation. |
| Evidence review | 0.33 | Produce an incident runbook with owners and recovery evidence. |

**Practical reference:** `07_reliability.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 09: Design deployment and security boundaries | 3 hours

**Outcome:** A running authenticated local API and a client-stack deployment/security design.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Landing zones, network, secrets and runtime patterns | 0.75 | Runtime choices, environment separation, immutable artifacts, CI/CD, network boundaries, private connectivity, workload identity and secret management. |
| Threat model, source/tool authority and governance | 0.75 | Threat modelling across source, prompt, tool and data boundaries; audit/retention ownership and risk review using NIST/OWASP guidance. |
| Local API deployment and architecture review | 1.17 | Run an authenticated loopback HTTP server; test wrong credential and tenant override; map the same flow to the client cloud/landing zone. |
| Evidence review | 0.33 | Review trust boundaries and separate tested behavior from proposed infrastructure. |

**Practical reference:** `08_deployment.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 10: Fund and run the platform as a service | 3 hours

**Outcome:** A cost sensitivity model, service catalogue, RACI and 90-day adoption plan.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| TCO, utilisation, token economics and showback | 0.75 | Token and embedding usage, request mix, cache/retry effects, fixed infrastructure/support, utilisation, showback and hosted/self-hosted TCO. |
| Ownership, self-service, onboarding and vendor exit | 0.75 | Platform/app/data/security ownership, service catalogue, support, approved model onboarding, procurement/licensing and vendor exit. |
| Economics and operating-model workshop | 1.17 | Calculate hypothetical cost sensitivity; design a third multimodal application intake; write RACI and a 90-day adoption plan. |
| Evidence review and assignment 2 | 0.33 | Review assumptions, define evidence needed and set individual assignment 2. |

**Practical reference:** `09_economics.ipynb`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 11: Capstone build and architecture review | 3 hours

**Outcome:** A shared AI platform design and prototype evidence under new client constraints.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Requirements and architecture | 1.00 | Read the new capstone brief, prioritise requirements, assign responsibilities and draw a deployment/trust-boundary design. |
| Integration and acceptance evidence | 1.25 | Integrate both applications; add a new acceptance case and one working change; assemble quality, access, action, recovery and cost evidence. |
| Peer design review and corrections | 0.75 | Swap evidence packs, challenge claims, correct design and rehearse the architecture defence. |

**Practical reference:** `Capstone workbook`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.

## Session 12: Capstone completion and defence | 3 hours

**Outcome:** Team architecture defence, individual reasoning and an assessed delivery roadmap.

| Topic | Hours | Subtopics / aligned activity |
| --- | ---: | --- |
| Final evidence and rehearsal | 0.75 | Complete evidence checks and rehearse a concise architecture defence. |
| Five architecture panels | 1.67 | Five 20-minute panels: eight-minute demo, seven-minute challenge, five-minute feedback/scoring. |
| Individual exit assessment | 0.42 | Individual 25-minute exit assessment on an unseen scenario. |
| Feedback and closure | 0.17 | Share feedback, remediation steps and next professional application. |

**Practical reference:** `Capstone panel`. Minute allocations in the trainer guide are authoritative; displayed decimal hours are rounded.
