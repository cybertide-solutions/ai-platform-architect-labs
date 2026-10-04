# Enterprise AI Platform Architecture labs

A fresh 36-hour programme for solution architects: twelve three-hour weekday sessions. Build two applications on a shared platform and use evidence to defend architecture decisions.

## Start here

1. Read `handouts/01-client-brief.md` and `handouts/02-learning-journey.md`.
2. Complete `notebooks/00_preflight.ipynb` 3–5 working days before class.
3. Work through notebooks 01–09 in session order. Session 1 is a workshop; sessions 11–12 use the capstone workbook.
4. Keep your decisions, measurements and changes in `outputs/`. Never commit keys or sensitive customer data.

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

## Colab setup

Upload this ZIP to a new Colab session. Extract it with Python's `zipfile.ZipFile(...).extractall('/content')`; the ZIP contains a top-level `ai-platform-architect-labs` directory. Upload/open the desired notebook in Colab. Its setup cell locates `/content/ai-platform-architect-labs`. For repeatable Colab use, save CHAT_URL, CHAT_MODEL, CHAT_KEY, EMBED_URL, EMBED_MODEL and EMBED_KEY in Colab Secrets, grant notebook access, and set USE_COLAB_SECRETS=True in each notebook setup cell. Alternatively, use the private preflight prompt in each runtime; values do not automatically persist across separate runtimes. Alternatively, after this version is published, clone `https://github.com/cybertide-solutions/ai-platform-architect-labs` into `/content/ai-platform-architect-labs`. The existing repository is not assumed to have these files yet. Colab itself has not been exercised in the supplied verification.

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

Use `verification/groq_live_check.ipynb` to load `GROQ_API_KEY` from Colab Secrets and export a credential-free live report. It needs only the chat key and the matching student ZIP. Embeddings remain a separate check. This extra notebook is a readiness utility in addition to the ten core notebooks.
