# AsterWorks: two applications, one shared AI platform

A fictional manufacturing group wants buyers to understand purchasing rules and finance staff to inspect supplier spend. A separate Beacon tenant uses different payment terms and must remain isolated. The platform team expects additional applications later.

## Business outcomes

1. Buyers find current authorised policy with supporting source sections and explicit unknowns.
2. Finance obtains exact quarter/supplier spend from the order ledger. Models interpret requests; SQL calculates money.
3. A reviewed purchase draft becomes a durable local purchase request with a receipt and safe replay. No assistant approves a purchase or executes a payment.
4. Application owners can adopt shared identity, model access, evaluation, telemetry and cost controls.

## Starting facts

There are 11 source records, including an inactive old policy, one unapproved malicious vendor note and a finance-only discount. Six fictional purchase orders span two tenants. Amounts are integer minor currency units. The source manifest is a trusted ingestion artifact in this lab; a production system must validate ownership, provenance and permissions upstream.

## Classroom assumptions, to challenge

The organisation prefers managed services unless constraints justify operating infrastructure. Team members know APIs and basic Python. No actual customer data may be sent to the model provider. The initial scope is text-based; session 10 adds a multimodal intake design. Availability, latency, quality targets and cost ceilings must be proposed by participants, labelled assumptions and justified. The hiring email does not supply these values.

## Session 1 worksheet

- User and decision supported:
- Non-AI baseline and why AI might add value:
- One failure that would make the solution unacceptable:
- Task-quality measure, latency measure, availability measure and cost measure:
- Data owner and permission boundary:
- Shared capability versus application responsibility:
- Build/buy decision, alternative and evidence needed:
- Explicitly out of scope:

Produce a one-page investment brief and a trust-boundary diagram. Defend one decision in the final review.
