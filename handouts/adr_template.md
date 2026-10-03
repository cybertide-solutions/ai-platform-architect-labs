# ADR-NNN: <short decision title>

**Status:** proposed | accepted | superseded by ADR-NNN
**Date:** YYYY-MM-DD   **Deciders:** names and roles

## Context
What problem are we solving? What constraints apply (data residency, budget, latency, skills, existing contracts,
regulation)? What evidence do we have (test results, cost estimates)?

## Options considered
| Option | Pros | Cons |
|---|---|---|
| 1. | | |
| 2. | | |
| 3. | | |

## Decision
We will ... because ...

## Consequences
* **Good:** ...
* **Bad (accepted trade-offs):** ...
* **Risks and mitigations:** ...

## How we will know this was wrong
The metric or event that would make us revisit this decision, and when we will review it.

## Exit plan
If we must reverse this decision, what changes and roughly how long it takes.

---

### Example (short)
**ADR-001: Use a vector database in managed mode for the employee assistant**
*Context:* 40,000 policy chunks today, 400,000 expected; ops team has no experience running search clusters; data must
stay in India. *Options:* managed Qdrant in an Indian region; pgvector in our existing PostgreSQL; cloud provider vector
search. *Decision:* pgvector for the pilot, because the DBA team already runs PostgreSQL in Mumbai with backups and access
control, and pilot volume is small. *Bad:* weaker filtering and scaling than a dedicated engine. *Wrong if:* p95 search
latency above 300 ms or index above 2 million vectors. *Exit:* the retrieval interface in our code hides the database;
migration estimated at 3 weeks.
