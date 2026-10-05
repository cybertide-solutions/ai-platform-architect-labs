# Enterprise AI Platform Architecture labs

A fresh 36-hour programme for solution architects: twelve three-hour weekday sessions. Build two applications on a shared platform and use evidence to defend architecture decisions.

## Start in Google Colab

1. Click **Open in Colab** beside the required lab below. Start with **Preflight**.
2. Connect to a runtime if prompted, then run the notebook's **first code cell**. It downloads the course code and data automatically. Use a standard CPU runtime; these labs do not require a GPU.
3. Continue through the cells in order. You do not need to upload a ZIP, install Python locally or paste setup code.

The default software rehearsal needs no API key. For live AI, configure the private provider secrets described below. Opening Colab may require signing into your Google account; if it asks permission to run a GitHub notebook, review the notebook and confirm to proceed.

| When | Lab | Launch |
| --- | --- | --- |
| Before class | [Preflight](notebooks/00_preflight.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/00_preflight.ipynb) |
| Session 2 | [Models and serving](notebooks/01_model_and_serving.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/01_model_and_serving.ipynb) |
| Session 3 | [Data plane](notebooks/02_data_plane.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/02_data_plane.ipynb) |
| Session 4 | [Mini project](notebooks/03_mini_knowledge_service.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/03_mini_knowledge_service.ipynb) |
| Session 5 | [Tools and state](notebooks/04_tools_and_state.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/04_tools_and_state.ipynb) |
| Session 6 | [Shared platform](notebooks/05_shared_platform.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/05_shared_platform.ipynb) |
| Session 7 | [Release engineering](notebooks/06_release_engineering.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/06_release_engineering.ipynb) |
| Session 8 | [Reliability](notebooks/07_reliability.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/07_reliability.ipynb) |
| Session 9 | [Deployment](notebooks/08_deployment.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/08_deployment.ipynb) |
| Session 10 | [Economics](notebooks/09_economics.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/notebooks/09_economics.ipynb) |
| Live readiness | [Groq verification](verification/groq_live_check.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cybertide-solutions/ai-platform-architect-labs/blob/main/verification/groq_live_check.ipynb) |

Read [the worked business cases](handouts/05-worked-business-cases.md) before the labs. It explains the users, source records, exact amounts and expected decisions.

Session 1 uses [the client brief](handouts/01-client-brief.md). Sessions 11–12 use [the capstone workbook](handouts/04-projects-and-assessment.md). The [learning journey](handouts/02-learning-journey.md) maps all sessions to outcomes.

Save a copy of your notebook to Drive if you want to retain edits. Download evidence from `outputs/` before discarding a runtime: runtime files are temporary. Running setup again reuses existing course files and does not overwrite your work. For a fresh course download, save your work first, then disconnect/delete the runtime and reopen the notebook.

## Local setup

Use Python 3.11 or later. The engine and software checks use the standard library. A notebook UI is optional:

```sh
python -m venv .venv
```

Activate `.venv` using your operating system's usual command, then:

```sh
python -m pip install -r requirements.txt
python scripts/start_jupyter.py
```

The launcher asks privately for live configuration and passes it to all notebook kernels in that Jupyter session. It writes no credential file. Choose N for software rehearsal. If you launch Jupyter another way, set the environment before launching it; values set inside one notebook kernel do not automatically reach another.

Open a notebook from `notebooks/`. Run from the beginning. Each notebook creates its own small dataset/index; shared review artifacts are saved explicitly. Rerunning may overwrite those review artifacts, so copy reviewed results before regenerating them.

Run software verification from the repository root:

```sh
python -m unittest discover -s tests -v
python scripts/check_notebooks.py
```

The second command executes code cells in isolated Python processes without a notebook UI. It is a rehearsal check, not a test of Colab/Jupyter rendering or live APIs.

## Colab secrets for live AI

Software rehearsal needs no secrets. For the **Groq verification** notebook, add `GROQ_API_KEY` in Colab's Secrets panel (key icon), enable notebook access, set `RUN_LIVE=True` and choose **Runtime → Run all**. Its first cell fetches the course files automatically; the final cell downloads a report without the key.

For the **core live labs**, use the trainer-approved CHAT_URL, CHAT_MODEL and CHAT_KEY, plus the separate EMBED_URL, EMBED_MODEL and EMBED_KEY. Save those six names in Colab Secrets, grant access, and set USE_COLAB_SECRETS=True in the notebook's setup cell. The main preflight requires both chat and embedding capabilities. Never put credentials in a code cell or GitHub. Secret access and runtime variables do not automatically carry across unrelated runtimes.

## Live AI configuration

Set `LIVE_MODE=1` only after account and budget approval. Privately provide:

| Variable | Meaning |
| --- | --- |
| CHAT_URL | HTTPS base URL for a compatible Chat Completions endpoint, without `/chat/completions` |
| CHAT_MODEL | Exact approved model ID supporting JSON object output and native tools |
| CHAT_KEY | Secret provider credential |
| CHAT_MODEL_B | Optional second model at the same endpoint for comparison |
| EMBED_URL / EMBED_MODEL / EMBED_KEY | Approved real embeddings endpoint and model |
| CHAT_OPTIONS | Optional JSON object of tested provider-specific options; no model/messages/tools/response_format overrides |

The adapter uses actual HTTPS requests. Compatibility must be tested for the exact provider/model; no universal provider support is claimed. Select a JSON/tool-capable chat model and preflight embeddings. Set token/output controls in tested provider options and enforce an account budget. The per-client 60-request allowance is a local guard, not a dollar cap and not a cross-process limit. A second model needs a new client and may incur additional cost.

Without live credentials, search, SQL, access controls, HTTP, SQLite actions and software failure experiments still execute. They do not produce simulated AI answers. Live interpretation, native model tool use, real embeddings and semantic answer quality remain unverified until exercised. Authored fixtures are labelled. The full course requires approved live access; rehearsal is not a substitute for that learning outcome.

## What is supplied

- Ten notebooks including preflight; readable Python modules; fictional policies and orders.
- Participant worksheets, mini project, two assignments, capstone, assessment criteria and architecture handouts.
- Software checks, local HTTP deployment and an optional Dockerfile.
- No cloud provisioning, external payment/action, hosted vector database, enterprise IAM or GPU benchmark is hidden in the package.

All purchasing policies and records are fictional classroom data. The prototype is intentionally small and inspectable. Production deployment requires the additional controls and evidence discussed in the course.

## Groq-only readiness check

Use `verification/groq_live_check.ipynb` to load `GROQ_API_KEY` from Colab Secrets and export a credential-free live report. It needs only the chat key; course files download automatically. Embeddings remain a separate check. This extra notebook is a readiness utility in addition to the ten core notebooks.

## Answer display controls

Purchase-order totals are stored as integer paise and displayed by code: 6,500,000 paise = INR 65,000.00. The spend tool returns both total_minor and total_display. The agent uses authorised tool facts for its displayed answer, discarding model-generated financial prose. The policy service displays complete selected approved source excerpts with a scope_note. Missing excerpt information does not prove that the full contract lacks a term. Review source relevance, coverage and freshness independently.

The revised Groq report identifies itself as live-readiness-v2 and checks the tool amount and displayed amount separately. Embeddings and human policy review remain separate requirements.
