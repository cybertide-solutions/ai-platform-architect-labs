# Independent curriculum rationale and validation

Prepared 4 October 2026 for Kamlendra Chauhan. This revision derives its scope, duration, case study and assessment from the Radiant brief and primary-source research. The supplied Claude curriculum/code was not used as the design specification for this revision. The brief remains the business requirement; portfolio facts follow Kamlendra's supplied status/URLs.

## Recommendation and interpretation

Propose Enterprise AI Platform Architecture: from a solution to a shared service. The target is solution architects designing and operating shared enterprise AI capabilities. “AI Operating System Architect” is an ambiguous label, so this is an explicit interpretation to confirm with the client, not a claimed industry-standard job definition. The practical emphasis is generative AI. Broader predictive-ML platforms, advanced GPU engineering or a named vendor platform require a scope adjustment.

36 live hours across twelve three-hour weekday sessions gives room for architecture decisions, meaningful experiments, a three-hour mini project and six-hour capstone. The duration is a reasoned proposal, not something required by a cited framework or by the hiring email. Two individual assignments add approximately 2–3 hours outside class. A six-day, six-contact-hour alternative preserves the same outcomes if preferred by the client.

## Why these design choices

| Choice | Reason | Evidence learners produce |
| --- | --- | --- |
| Start with workload and non-AI baseline | An architect must justify investment and scope before choosing infrastructure. | Investment brief, success criteria, boundaries. |
| Two applications share one platform | Reuse, policy and ownership become observable across consumers. | Policy service plus exact spend service, separate permissions and attribution. |
| Model interprets; SQL calculates money | The probabilistic component has a bounded contribution. | Typed extraction, validation, exact totals and clarification. |
| One coherent purchasing case | Learners spend time on new architecture decisions rather than learning a new business story for every lab. | Cumulative decisions and a capstone change. |
| Inspectable Python core | Avoid setup/framework overhead while exposing control flow. | Readable engine, actual HTTP/SQLite behavior, original changes. |
| Real embeddings and live tools are explicit | A credible AI course needs actual model behavior and measured uncertainty. | Provider preflight, saved vectors, model/tool results and human review. |
| Separate software and semantic evidence | Provenance formatting cannot guarantee a correct answer. | Deliberately misleading citation, independent semantic review and pending gates. |
| Production operations included | Platform architecture includes release, cost and ownership after the demo. | Manifest, rollback, failure runbook, deployment design, TCO and RACI. |

## Primary-source research and what it informed

These sources informed coverage and tradeoffs, not the fictional dataset or a copied curriculum. Research consulted 4 October 2026. Vendor documentation can change; exact provider/model capabilities must be preflighted.

- AWS, [Generative AI lifecycle](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lifecycle.html): supports covering business scoping, model/customisation choices, integration, deployment and ongoing improvement. Applied across sessions 1–10.
- Microsoft, [Gateway in front of model deployments](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/azure-openai-gateway-multi-backend): supports evaluating central routing/control, client attribution and quota/reliability needs rather than assuming every workload needs a gateway. Applied in sessions 6, 8 and 10.
- Google Cloud, [Enterprise generative AI and ML blueprint](https://docs.cloud.google.com/architecture/blueprints/genai-mlops-blueprint): supports environment separation, controlled deployment artifacts/pipelines and platform operating responsibilities. Applied in sessions 7, 9 and 10.
- NIST, [AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence): informs lifecycle risk ownership and evaluation. This voluntary framework is not presented as a certification or legal-compliance guarantee.
- OWASP, [Top 10 for LLM applications](https://genai.owasp.org/llm-top-10/): informs source, output, tool-authority and retrieval threat discussions. Applied in sessions 3, 5 and 9.
- Anthropic engineering, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): informs the workflow-versus-agent distinction and preference for justified complexity. This public engineering reference is independent of the user's supplied Claude-generated materials.
- Model Context Protocol, [Architecture](https://modelcontextprotocol.io/docs/learn/architecture): informs host/client/server and protocol responsibilities. MCP is conceptual coverage; no MCP server is deployed in this course.
- Groq, [OpenAI-compatible API](https://console.groq.com/docs/openai) and [structured outputs](https://console.groq.com/docs/structured-outputs): examples of why provider/model compatibility must be checked explicitly. No particular provider or free quota is guaranteed.
- Google AI, [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings): confirms embedding use as a real model operation. The supplied adapter requires a compatible embeddings REST endpoint; it does not automatically support every provider's native API format.
