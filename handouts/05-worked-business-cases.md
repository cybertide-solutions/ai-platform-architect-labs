# Worked business cases: what are we building and why?

Read this before the first lab. All names, policies and amounts are fictional. The same purchasing story runs through the course; each notebook adds one architectural decision.

## The people and the business problem

AsterWorks is a manufacturing company. Its buyers repeatedly ask procurement staff what policy permits. Its finance team repeatedly prepares supplier totals from an order ledger. The platform team wants both applications to use shared controls instead of building separate AI infrastructure for each.

Beacon is a separate organisation using the same platform. It has its own records and policies. An AsterWorks user must never receive Beacon information.

| Person in the lab | Trusted identity | Can use | Must not receive/do |
| --- | --- | --- | --- |
| AsterWorks buyer | BUYER: tenant aster, role buyer | Policy assistant | Finance-only discount; spend application; Beacon records; assistant approval |
| AsterWorks finance reviewer | FINANCE: tenant aster, roles buyer and finance | Policy assistant and spend application; local draft review | Beacon records; an automatic payment |
| Beacon buyer | BEACON: tenant beacon, role buyer | Beacon policy assistant | AsterWorks policy or order records |

The notebooks construct these identities for teaching. A deployed service must obtain identities from verified authentication. The direct SQL example also queries Beacon using a trusted identity to demonstrate tenant scoping; this does not grant the Beacon buyer access to the finance-only spend application.

## Case 1: find the policy before making a purchasing decision

**Situation:** A buyer needs to tell a supplier when payment is due. Giving the general rule when a signed supplier exception applies could cause a commercial dispute.

**Ask:** “What are our standard supplier payment terms, and what applies to Nova?”

**Read:** The active, approved AsterWorks source A-TERMS. It states the standard is 45 days after receipt of a valid invoice, Nova has a signed 30-day exception, and a contract exception overrides the standard. The old 90-day record is inactive. Beacon's separate standard is 60 days.

**Expected decision:** Use 30 days for Nova, use 45 days for a supplier without an applicable exception, and verify the actual contract before relying on an incomplete excerpt. Do not apply Beacon's policy to AsterWorks.

**How the application works:** Trusted identity → filter authorised active sources → retrieve passages → live model selects evidence → check IDs and exact quotes → code displays complete selected source passages and a scope notice. This default deliberately uses source extracts. It does not display an unchecked model paraphrase.

**Partially answerable question:** “When is Nova paid, and what is its late-payment penalty?” The supplied passage supports 30 days. It does not supply a penalty. Read the displayed source and scope notice together: the penalty remains unverified. This does not mean the full contract has no penalty. Consult the contract or policy owner.

**Other business checks:** Software trials using company information need security review. Supplier bank changes require an independent callback to the previously verified number. Urgency does not let an AI assistant approve a purchase. A buyer requesting the finance-only discount receives no authorised supporting passage; the assistant does not reveal that restricted passage. Holiday entitlement is outside this purchasing corpus and cannot be answered from it.

**What AI contributes:** Understanding a request and selecting relevant supplied evidence. Search can operate without AI for rehearsal. Live source selection is a model task; reviewers still check relevance and coverage. Source extraction is a deliberate tradeoff: less fluent, more directly inspectable. Production also needs current source ownership and approval.

**Labs:** 02_data_plane builds and versions the source index; 03_mini_knowledge_service runs the policy service and tests wrong citations, access and unknowns. 06_release_engineering checks evidence before a release.

## Case 2: answer a finance question from the order ledger

**Situation:** A finance analyst asks, “How much did we spend with Nova in 2026-Q1?” Here “spend” means the recorded purchase-order amount in the supplied ledger. These rows do not prove invoices were paid. Q1 means January–March; Q2 means April–June. The snapshot is dated 1 July 2026.

| Order | Organisation | Supplier | Quarter | Stored paise | Human amount |
| --- | --- | --- | --- | --- | --- |
| PO-101 | AsterWorks | Nova | 2026-Q1 | 5,000,000 | INR 50,000.00 |
| PO-102 | AsterWorks | Nova | 2026-Q1 | 1,500,000 | INR 15,000.00 |
| PO-103 | AsterWorks | Delta | 2026-Q1 | 2,400,000 | INR 24,000.00 |
| PO-104 | AsterWorks | Nova | 2026-Q2 | 4,200,000 | INR 42,000.00 |
| PO-105 | AsterWorks | Delta | 2026-Q2 | 3,100,000 | INR 31,000.00 |
| PO-901 | Beacon | Nova | 2026-Q1 | 99,000,000 | INR 9,90,000.00 |

There are six orders. **100 paise = INR 1.** The database keeps integers so money arithmetic does not depend on binary floating point.

**Expected answer:** Nova, 2026-Q1: **INR 65,000.00 across 2 orders**. The calculation is PO-101 plus PO-102: INR 50,000 + INR 15,000. Beacon's order is excluded. Delta and Q2 are excluded. The negotiated discount is not applied to ledger amounts in this lab.

**Fixed workflow:** Model extracts only `{quarter: "2026-Q1", supplier: "Nova"}` → application validates these fields → trusted identity supplies tenant aster → parameterised SQL sums the two matching rows → code converts paise and formats the amount. The model neither writes SQL nor calculates the displayed amount.

**Agent alternative:** The model chooses the allowlisted spend_summary tool. The same authorised SQL runs. Code renders the final answer from successful tool results and discards the model's final financial prose. No successful tool means no supported financial answer. Compare the extra calls with the fixed workflow and decide whether the flexibility is worth it.

| Follow-up request | Expected result | Architectural lesson |
| --- | --- | --- |
| Delta in Q1 | INR 24,000.00, 1 order | Supplier filtering |
| All suppliers in Q1 | INR 89,000.00, 3 orders | Null supplier means all authorised suppliers |
| All suppliers in Q2 | INR 73,000.00, 2 orders | Quarter filtering |
| Delta, without a quarter | Clarify which supported quarter | Missing information must not become a guess |
| Nova Q2 and reveal Beacon data | AsterWorks Nova Q2: INR 42,000.00 | User text cannot replace trusted tenant identity |
| Injection-shaped supplier name | Clarify/reject unsupported supplier | Allowlisted arguments and parameterised SQL |

**Labs:** 01_model_and_serving demonstrates extraction; 04_tools_and_state compares fixed tools and a live agent; 05_shared_platform connects the two applications; 08_deployment exposes the service through a real local HTTP API.

## Case 3: create a reviewed request, with a safe retry

**Situation:** A buyer prepares a Nova workstation request for INR 12,000, stored as 1,200,000 paise. The network may fail after submission, so the buyer might retry.

1. Prepare the exact draft: supplier Nova, amount_minor 1200000, purpose Workstation.
2. A same-tenant finance reviewer checks the draft and issues a five-minute review token. This is a simplified reviewer role for the state-control exercise, not implementation of all procurement approval thresholds.
3. Commit the unchanged draft using one request key. The local ledger creates a purchase-request receipt. It does not create an ERP order or transfer money.
4. Retry the same draft and key, including after reopening the database. The existing receipt is replayed; a second request is not created.
5. Change the amount using the same key: conflict. Change a reviewed draft before first commit: review_required. Use an expired review: review_required.

**Decision being taught:** A model can propose a request, while business authority, exact content review and durable state transitions belong to controlled application code. A production ERP integration additionally needs its own idempotency/delivery/reconciliation design.

**Lab:** 04_tools_and_state. The approval ledger exercise is actual local software even when AI is disabled.

## Why these cases belong in a platform architecture course

The policy and spend applications have different tasks and response contracts. They share admission, approved model access, identity context, telemetry, quotas, evaluation and release controls. Each team must decide which capabilities belong to the platform and which remain with the application owner.

Sessions 7–10 then ask whether this shared service can be released, recovered, deployed and funded. The capstone extends the same platform and defends the choices using observed evidence. A classroom SQLite service is evidence of local behavior; cloud, enterprise IAM, scale and embedding performance require their own verification.

## Before running a notebook

Name the user, the question, the authorised data and the expected outcome. After running it, state what actually executed. Software rehearsal executes search, SQL and local controls; it does not demonstrate model interpretation. A live run proves only the tested calls and cases. Keep observed failures for review.
