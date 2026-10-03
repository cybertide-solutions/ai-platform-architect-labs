# AI Platform: Solution Architect Programme (labs and handouts)

Five days, hands-on. You will build, measure, secure and operate a small AI assistant for a fictional company,
**Meridian Retail**, and use it to learn the architecture decisions behind enterprise AI platforms.

**Start here:** follow [SETUP.md](SETUP.md), then run `00_setup_check`. It must end with **ALL CHECKS PASSED**.

Every notebook runs unchanged in **Google Colab** and in **VS Code** on your laptop.

## Daily handouts
| Day | Theme | Handout |
|---|---|---|
| 1 | Foundations: the AI platform, LLM basics, model choices, prompts | [handouts/day1.md](handouts/day1.md) |
| 2 | Knowledge: RAG, tools and agents | [handouts/day2.md](handouts/day2.md) |
| 3 | Trust: evaluation, security, mini project | [handouts/day3.md](handouts/day3.md) |
| 4 | Operate: deployment, monitoring, cost, architecture decisions | [handouts/day4.md](handouts/day4.md) |
| 5 | Capstone | [handouts/day5_capstone.md](handouts/day5_capstone.md) |

Also: [assignments](handouts/assignments.md), [ADR template](handouts/adr_template.md), [glossary](handouts/glossary.md).

## Labs
Click a badge to open the notebook in Google Colab.

| Lab | Topic | Open |
|---|---|---|
| 00 | Setup check | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/00_setup_check.ipynb) |
| 1 | Sketch the AI platform layers (worksheet in Day 1 handout) | n/a |
| 2 | First LLM calls: tokens, JSON, streaming, two models | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab02_first_llm_call.ipynb) |
| 3 | Model decision matrix | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab03_model_decision_matrix.ipynb) |
| 4 | Prompt design, measured on 20 tickets | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab04_prompt_design.ipynb) |
| 5 | RAG ingestion into Qdrant | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab05_rag_ingest.ipynb) |
| 6 | Grounded answers, refusals, access control, chunk size | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab06_rag_answers.ipynb) |
| 7 | Tool calling (and what MCP standardises) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab07_tool_calling.ipynb) |
| 8 | Agent loop with a human approval gate | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab08_agent_approval.ipynb) |
| 8b | Optional: the same agent in CrewAI | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab08b_crewai.ipynb) |
| 8c | Optional: the same agent in Google ADK | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab08c_google_adk.ipynb) |
| MP | Mini project: Policy Q&A Assistant (Day 3) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/mini_project.ipynb) |
| 9 | Build a test set; LLM-as-judge | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab09_eval_set.ipynb) |
| 10 | Release gate for prompt and model changes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab10_safe_release.ipynb) |
| 11 | Prompt injection attacks | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab11_prompt_injection.ipynb) |
| 12 | Guardrails, PII masking, audit log | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab12_guardrails.ipynb) |
| 13 | Web UI and a shareable link | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab13_deploy_ui.ipynb) |
| 14 | Traces, latency, cost forecast | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/lab14_monitoring_cost.ipynb) |
| 15 | Write an ADR (worksheet in Day 4 handout) | n/a |
| 16 | Review a reference architecture (worksheet in Day 4 handout) | n/a |

## What is in this folder
```
labkit.py            shared helpers used by every lab (read it: it is short and commented)
requirements.txt     Python packages for the labs
data/policies/       10 policy PDFs of the fictional company Meridian Retail
data/tickets.csv     20 labelled support tickets (Lab 4)
data/eval_starter.csv  5 test questions (Labs 6, 9, 10)
data/extra/          a poisoned document used in the security labs
notebooks/           the labs
handouts/            daily notes, worksheets, templates
```

## Technology used
| Layer | Choice in the labs | Why |
|---|---|---|
| LLM | Groq free tier (Llama models), Gemini as backup | free, fast, OpenAI-compatible API |
| LLM client | `openai` Python package | the de facto standard interface; works with most providers |
| Embeddings | `model2vec` small open model | runs on any CPU, no GPU or heavy dependencies |
| Vector database | Qdrant (local mode) | no account or server needed; the same code points at a Qdrant server in production |
| UI | Gradio | a chat UI and a shareable link in a few lines |

All company data in this course is fictional.
