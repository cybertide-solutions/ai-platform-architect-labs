# Decision and evidence workbook

Use this template for each session. Keep observed results separate from assumptions and design proposals.

## Architecture decision record

- Decision ID, date, owner and requirement:
- Options considered, including a simpler/non-AI option:
- Chosen option and why it fits the constraints:
- Evidence: test/case, input, version, actual result and location:
- Cost, data, operational and failure tradeoffs:
- What remains untested:
- Reversal trigger and migration path:

## Evidence register

| ID | Requirement | Method | Version / configuration | Actual outcome | Provenance | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| E01 | | | | | live model / actual local software / injected fixture / hypothetical calculation / proposed design | |

## Semantic answer review

For each answer, compare with the source and expected behavior. Mark each separately: correct facts, supported claims, complete response (including explicit gaps), authorised evidence, appropriate refusal. Record a reason for any failure. Do not award a generated-answer score to an evidence-only search result. A valid quote does not prove the answer follows from it.

## Data lifecycle checklist

Who owns the source? How are metadata/ACLs verified? What is the section/chunk strategy? Which model creates embeddings? How is a new version published? How do revocation, deletion, index migration and cache invalidation work? What evidence proves a user cannot retrieve another tenant's source?

## Release manifest

Code revision or ZIP hash; prompt version; exact model ID; adapter/options; index version/digest; embedding model/dimensions; data/permission version; evaluation case version; review owner/date; deployment artifact; release decision; rollback target.

## Operating design

Define service catalogue entry, onboarding request, application owner, platform owner, data owner, security approver, incident owner and financial owner. For each recurring decision identify one accountable owner. Explain support escalation and model/data change approval.

## Incident runbook

Signal → classification → impact → containment → user communication → recovery test → release/rollback owner → post-incident action. Include provider timeout, stale data, suspected unauthorised retrieval and repeated invalid model output. Avoid exposing prompts/credentials in routine telemetry.
