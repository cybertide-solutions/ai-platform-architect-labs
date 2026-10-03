# Day 5: Capstone project

**Format:** teams of 4 to 5. 5 hours of design work, then a 15-minute panel review per team, then a 1-hour final quiz.
**Weight:** 40% of the course assessment.

## The task
Design the AI platform capability for **one** case. You are the architects; the panel plays the CIO, the CISO and the
business owner.

| Case | Brief |
|---|---|
| **A. HR policy assistant** | 12,000 employees of an Indian insurance company ask HR questions in English and Hindi. Policies differ by grade and state. HR data must stay in India. Target: deflect 40% of HR tickets. |
| **B. Customer support assistant** | An online retailer gets 30,000 support chats a day. Start as a copilot that suggests replies to human agents, then move some topics to direct answers. Refunds above INR 5,000 always need a human. |
| **C. Client case** | A use case from your own organisation, agreed with the trainer by 10:00. |

## What to deliver
1. **Architecture diagram** of the AI platform layers for your case (Miro, draw.io or slides): identity, gateway,
   models, knowledge, tools, guardrails, operations. Show data flows and trust boundaries.
2. **Two ADRs** (one may be your Assignment A3): for example model choice, vector database, hosting, agent or workflow.
3. **Risk list:** top 8 risks with likelihood, impact and control. Include at least two AI-specific risks (Module 6) and
   one compliance item (DPDP Act or sector regulation).
4. **Rough cost estimate** per month at launch and at full scale, using the Lab 14 method. State your assumptions.
5. **Quality plan:** how you build the test set, your pass bar, and your release gate.
6. **90-day plan** to a pilot.

Optional: a thin working demo built from your lab code (not required, not scored extra; design quality matters most).

## Schedule
| Time | Activity |
|---|---|
| 09:15 | Recap quiz and capstone briefing; teams choose a case |
| 09:30 | Work block 1: scope, users, architecture draft |
| 11:00 | Break |
| 11:15 | Trainer check-in per team (10 minutes each); work block 2: ADRs, risks |
| 12:30 | Lunch |
| 13:15 | Work block 3: cost, quality plan, 90-day plan, rehearse |
| 14:15 | Panel reviews (15 minutes per team: 10 present, 5 questions) |
| 15:30 | Final quiz (20 multiple-choice questions, 30 minutes), answers reviewed together, course feedback |
| 16:30 | Close |

## Scoring rubric (100 points)
| Criterion | Points | What good looks like |
|---|---|---|
| Architecture | 25 | all layers covered; identity and access control explicit; clear data flows |
| Decisions (ADRs) | 20 | real options compared; trade-offs stated honestly; reversible where possible |
| Risk and compliance | 20 | AI-specific risks with concrete controls; DPDP or sector duties addressed |
| Cost and operations | 15 | reasoned numbers; monitoring and fallback described |
| Quality plan | 10 | test set source, pass bar, release gate |
| Presentation and answers | 10 | clear, within time, handles panel questions |

## Panel questions to prepare for
* What happens when the model gives a confident wrong answer to a customer? How would you find out?
* Which data leaves your network, to whom, and under what terms?
* How would you switch model providers in four weeks?
* What do you measure in the first 30 days of the pilot, and what result stops the project?
