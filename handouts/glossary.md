# Glossary

| Term | Meaning |
|---|---|
| ADR | Architecture Decision Record: a short document capturing one decision, its options and consequences |
| Agent | a loop in which a model chooses tools, code runs them, and results go back until the model answers |
| AI platform (AI OS) | shared capabilities (models, knowledge, tools, guardrails, operations) that many AI applications use |
| API gateway | entry point that handles authentication, rate limits and routing for APIs |
| Audit log | a tamper-resistant record of who asked what, what was used and what was answered |
| Chunk | a passage of a document, the unit stored and retrieved in RAG |
| Citation | a reference from an answer to the passage that supports it |
| Context window | the maximum tokens a model accepts in one request (prompt plus answer) |
| DPDP Act | India's Digital Personal Data Protection Act, 2023 |
| Embedding | a vector of numbers representing the meaning of a text |
| EU AI Act | the European Union's risk-based regulation of AI systems |
| Excessive agency | an AI system with more power to act than it needs (an OWASP LLM risk) |
| Faithfulness | whether an answer's claims are supported by the retrieved passages |
| Few-shot prompting | including a few input and output examples in the prompt |
| Fine-tuning | further training a model on your examples to change its behaviour or style |
| Guardrail | a check on input, retrieved context or output that enforces a rule |
| Hallucination | a fluent but unsupported or false answer |
| Human-in-the-loop | a person approves or reviews before an action takes effect |
| Hybrid search | combining keyword search and vector search |
| LLM-as-judge | using a model to grade another model's output against criteria |
| MCP | Model Context Protocol: an open standard for exposing tools and data to AI applications |
| Metadata filter | restricting vector search by attributes such as department or access group |
| Model gateway | a service between applications and model providers that routes, caches, limits and meters calls |
| Multi-tenancy | one platform serving many teams with separate quotas, data and costs |
| Open-weight model | a model whose weights are published and can be self-hosted |
| p95 latency | the time within which 95% of requests complete |
| PII | personally identifiable information |
| Prompt caching | provider feature that reuses processing of a repeated prompt prefix to reduce cost and latency |
| Prompt injection | input that manipulates a model into ignoring its instructions; *indirect* when hidden in content it reads |
| RAG | retrieval-augmented generation: retrieve relevant passages and answer from them |
| Release gate | an automated check that blocks a change if test scores drop |
| Reranker | a model that reorders search results by relevance |
| Span | one timed step inside a trace |
| Structured output | model output in a fixed format such as JSON, often validated against a schema |
| Temperature | setting that controls randomness of model output |
| Test set (golden set) | questions with expected answers used to measure quality |
| Token | the unit models read and write; about 4 characters of English |
| Tool calling | a model requesting that the application run a described function |
| Top-k | the number of passages retrieved per question |
| Vector database | a database that stores embeddings and finds the nearest ones quickly |
| Workflow | a fixed sequence of steps written in code, with models used for specific steps |
