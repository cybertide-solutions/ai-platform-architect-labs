# Architecture primer

## How a policy request flows

The API establishes identity → platform checks application entitlement and quota → retrieval filters approved active sources by tenant/role → retrieval ranks eligible content → model receives the question and selected passages → structural provenance is validated → response and minimal trace are returned. Semantic acceptance is established through evaluation, not guaranteed per response by the structural checker.

## How a spend request flows

The API establishes identity → model extracts a typed quarter/supplier request → local code validates the fields → parameterised SQL applies the trusted tenant predicate and computes integer totals → exact result is returned. A model-selected tool loop is an alternative exercise; its final prose must be checked against tool facts.

## How a purchase request flows

A draft is validated → an authorised human reviewer approves that exact draft for a principal → the commit checks expiry, digest and idempotency inside a database transaction → a durable local receipt is returned. External ERP delivery needs an additional integration contract, outbox/reconciliation and failure handling. The model cannot mint authority.

## Key distinctions

| Distinction | Why it matters |
| --- | --- |
| Model / application / platform | Task intelligence, product behavior and reusable operating controls have different owners. |
| RAG / fine-tuning | Retrieved facts can change independently; tuning changes model behavior and requires a separate data/training/evaluation lifecycle. |
| Workflow / agent | Code-defined steps are easier to bound; model-selected steps add flexibility and uncertainty. |
| Source recall / answer quality | Finding the right passage does not ensure the answer uses it correctly. |
| Protocol / authority | API or MCP compatibility does not grant permission. |
| Local test / production evidence | Correct software behavior at small scale does not establish load, IAM, provider quality or operational readiness. |
| Call quota / cost budget | Requests have different token counts and prices; financial control needs attributed usage and account-level limits. |

## Production extension map

Replace trusted identity objects/static tokens with validated IdP/workload identities. Replace in-process quotas/cache/circuits with appropriately scoped shared controls. Replace the small SQLite index with a governed scalable store when workload requires it. Add ingestion validation, revocation propagation, private networking, secret rotation, deployment pipelines, audited actions, representative evaluation and operational tests. Keep the task contracts and evidence discipline.
