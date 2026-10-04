# Projects, assignments and assessment

## Assessment model

Entry diagnostic is ungraded. Final score is mini project 20%, assignment 1 10%, assignment 2 10%, capstone 40%, individual exit assessment 20%. Target: 70/100 overall. An unresolved cross-tenant leak, unreviewed consequential write or misrepresented evidence in the capstone prevents signoff until corrected and retested. Missing live AI evidence is pending, never silently passed. These are proposed course criteria, not a vendor certification.

## Mini project: session 4 (20 points)

Build a policy service for buyers and finance. Demonstrate current/authorised evidence, unknown and partial-answer handling. Review nine live answers against labels, add two cases and implement one improvement. Submit diagram, review file and decision note. Score: task contract 4, source/access behavior 4, semantic review 6, improvement and evidence 4, explanation 2.

## Assignment 1: after session 4, about 60–90 minutes (10 points)

Individually produce a two-page model/data ADR. Include a model experiment result, retrieval choice, one failure, two original cases, hosted/self-hosted/customisation decision and remaining evidence. Score: requirement/options 3, observed evidence 3, justified choice/tradeoffs 3, clarity 1. Due before session 6; trainer returns feedback before session 7. If live access failed, submit architecture work with the AI evidence marked pending and complete it during remediation.

## Assignment 2: after session 10, about 60–90 minutes (10 points)

Write a two-page production-readiness memo covering deployment/IAM boundaries, release/rollback, SLO/runbook, cost sensitivity, ownership and the first 90 days. Distinguish implemented controls from proposals. Score: control/deployment design 3, operations/release 3, economics/ownership 3, evidence honesty 1. Due before session 12.

## Capstone: sessions 11–12, six contact hours (40 points)

New scenario: AsterWorks acquires a third business unit, Cedar. Cedar's purchasing policies must not leak to Aster or Beacon. Finance wants a new supplier/category report; product wants rapid onboarding. Security requires approved model endpoints and bounded tool authority. Operations requires explicit rollback and incident ownership. Procurement asks whether the platform should stay hosted or move to a private/self-hosted model. No exact throughput or budget has been supplied: ask or declare justified assumptions.

Build on the supplied two applications. Implement at least one original improvement, such as a third-tenant admission path with independent tests, per-application quotas/circuit boundaries, a new allowlisted read-only report, or stronger source lifecycle handling. Merely adding a label/configuration without behavioral evidence is insufficient.

Required deliverables:

1. One-page requirements and acceptance contract; one architecture diagram with trust boundaries.
2. Two applications on shared services, two existing tenants and a design for Cedar; implement Cedar only if it is your chosen change.
3. Model/data/serving ADR and a complete release manifest.
4. Evidence of authorised/denied requests, retrieval/semantic behavior, exact SQL data, action tampering/replay, dependency failure and rollback. Clearly label local, live, injected, hypothetical and proposed evidence.
5. At least three original acceptance cases and one implemented improvement. Include a failing case captured before the change.
6. Cost sensitivity, service ownership, incident runbook and a 90-day roadmap.
7. Outstanding production validation and remaining live evidence, if any.

Scoring: requirements/architecture 8; working integration and original change 10; evaluation/access/action/recovery evidence 10; economics/operations 6; defence and individual contribution 6. Each criterion earns full credit for justified, demonstrated choices; half for plausible but incomplete work; zero for absent or contradicted evidence. No cloud spend or public deployment is required.

Session 11: requirements/design 60 min; integration/evidence 75; peer review 45. Session 12: final evidence 45; five panels of 20 min; individual assessment 25; feedback 10. Each panel: demo 8 min, challenge 7 min, feedback 5 min. Every member must answer a question.

## Individual exit assessment (20 points, 25 minutes)

The trainer supplies an unseen short scenario. Five short-answer questions, four points each, assess model/data choice, trust boundaries, evaluation, reliability and operating economics. This checks individual competence beyond team participation. Remediation uses a revised decision note plus a targeted practical demonstration.
