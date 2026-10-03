"""labkit: small helper library shared by all labs.

Works the same in Google Colab and in a local Python / VS Code setup.
Everything here is plain Python so participants can read it.

Main functions
  setup()                 find API keys, pick a provider and models, print a summary
  chat(...)               one call to the LLM, returns text (logs tokens, latency, cost)
  chat_json(...)          same, but returns a Python dict
  embed(texts)            turn texts into vectors (numpy array)
  load_pdfs(), chunk_pages()           read and split the policy documents
  new_store(), index_chunks(), search() Qdrant vector store helpers
  build_policy_index()    all of the above in one call
  rag_answer(...)         retrieval-augmented answer with citations
  run_agent(...)          simple tool-calling agent loop with optional approval
  mask_pii(text)          redact common personal data patterns
  calls_df()              table of every LLM call made in this session
  check()                 end-to-end smoke test of the whole setup
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import uuid
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

# ----------------------------------------------------------------- environment

IN_COLAB = "google.colab" in sys.modules

try:  # local runs: read keys from a .env file next to this module
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except Exception:
    pass


def get_secret(name: str) -> str | None:
    """Look for a secret in: environment variables, Colab secrets, .env file."""
    val = os.environ.get(name)
    if val:
        return val.strip()
    if IN_COLAB:
        try:
            from google.colab import userdata
            val = userdata.get(name)
            if val:
                os.environ[name] = val.strip()
                return val.strip()
        except Exception:
            pass
    return None


def pip_install(*packages: str, module: str | None = None) -> None:
    """Install packages into the running Python if `module` is not importable yet.
    Uses pip, or uv when the environment was created by uv (uv venvs have no pip)."""
    import importlib.util
    import shutil
    import subprocess
    if module and importlib.util.find_spec(module) is not None:
        return
    print(f"Installing {' '.join(packages)} (one time, may take a minute)...")
    if importlib.util.find_spec("pip") is not None:
        cmd = [sys.executable, "-m", "pip", "install", "-q", *packages]
    elif shutil.which("uv"):
        cmd = ["uv", "pip", "install", "-q", "--python", sys.executable, *packages]
    else:
        raise RuntimeError(f"Neither pip nor uv found. Install manually: pip install {' '.join(packages)}")
    subprocess.run(cmd, check=True)


# ----------------------------------------------------------------- providers

PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key": "GROQ_API_KEY",
        "big": ["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "meta-llama/llama-4-scout-17b-16e-instruct"],
        "small": ["llama-3.1-8b-instant", "openai/gpt-oss-20b"],
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key": "GEMINI_API_KEY",
        "big": ["gemini-2.5-flash", "gemini-3-flash", "gemini-flash-latest"],
        "small": ["gemini-2.5-flash-lite", "gemini-flash-lite-latest", "gemini-2.0-flash-lite"],
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key": None,
        "big": ["llama3.2:3b", "qwen2.5:3b", "llama3.1:8b"],
        "small": ["llama3.2:3b", "qwen2.5:3b", "llama3.2:1b"],
    },
    "mock": {  # offline rehearsal only: a local fake server
        "base_url": os.environ.get("MOCK_BASE_URL", "http://127.0.0.1:8787/v1"),
        "key": None,
        "big": ["mock-model"],
        "small": ["mock-model"],
    },
}

# Illustrative paid prices in USD per 1M tokens (input, output), used only to show
# what the free-tier calls WOULD cost. Check the provider's pricing page for current prices.
PRICE_PER_M = {
    "llama-3.3-70b-versatile": (0.59, 0.79),
    "llama-3.1-8b-instant": (0.05, 0.08),
    "openai/gpt-oss-120b": (0.15, 0.60),
    "openai/gpt-oss-20b": (0.075, 0.30),
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.5-flash-lite": (0.10, 0.40),
}

CONFIG: dict = {}
CALLS: list[dict] = []
_client = None


def _ollama_running() -> bool:
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        return True
    except Exception:
        return False


def _choose_provider() -> str | None:
    forced = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if forced:
        return forced
    for name in ("groq", "gemini"):
        if get_secret(PROVIDERS[name]["key"]):
            return name
    if not IN_COLAB and _ollama_running():
        return "ollama"
    return None


def _ask_for_key() -> str | None:
    """Last resort: ask the participant to paste a Groq key (input is hidden)."""
    try:
        from getpass import getpass
        print("No API key found. Paste your Groq API key (starts with gsk_), or press Enter to skip.")
        k = getpass("GROQ_API_KEY: ").strip()
    except Exception:
        return None
    if k:
        os.environ["GROQ_API_KEY"] = k
        return "groq"
    return None


def _pick(available: list[str], prefs: list[str]) -> str:
    for p in prefs:
        if p in available:
            return p
    return prefs[0]


def setup(provider: str | None = None, quiet: bool = False) -> dict:
    """Find keys, choose provider and models. Safe to call many times."""
    global _client
    from openai import OpenAI

    if provider:
        os.environ["LLM_PROVIDER"] = provider
    name = _choose_provider() or _ask_for_key()
    if not name:
        raise RuntimeError(
            "No LLM provider available.\n"
            "  Colab: add GROQ_API_KEY under the key icon (Secrets) and switch on 'Notebook access'.\n"
            "  Local: put GROQ_API_KEY=... in the .env file in the course folder.\n"
            "  See SETUP.md, section 'API keys'.")
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider '{name}'. Use one of: {', '.join(PROVIDERS)}")
    p = PROVIDERS[name]
    key = get_secret(p["key"]) if p["key"] else "not-needed"
    if not key:
        raise RuntimeError(f"Provider '{name}' needs {p['key']}. See SETUP.md, section 'API keys'.")
    _client = OpenAI(base_url=p["base_url"], api_key=key, timeout=60, max_retries=0)

    available: list[str] = []
    try:
        available = [m.id.replace("models/", "") for m in _client.models.list().data]
    except Exception as e:  # listing is optional; the chat call will tell us more
        if not quiet:
            print(f"(could not list models: {type(e).__name__}; using defaults)")
    big = os.environ.get("LLM_MODEL") or _pick(available, p["big"])
    small = os.environ.get("LLM_MODEL_SMALL") or _pick(available, p["small"])
    CONFIG.clear()
    CONFIG.update(provider=name, base_url=p["base_url"], big=big, small=small, available=available)
    if not quiet:
        where = "Google Colab" if IN_COLAB else "local Python"
        print(f"Running in {where}, Python {sys.version.split()[0]}")
        print(f"LLM provider: {name}   big model: {big}   small model: {small}")
    return dict(CONFIG)


def client():
    if _client is None:
        setup(quiet=True)
    return _client


def model_name(model: str = "big") -> str:
    if not CONFIG:
        setup(quiet=True)
    return CONFIG.get(model, model)


# ----------------------------------------------------------------- LLM calls

def _cost(model: str, pin: int, pout: int) -> float:
    a, b = PRICE_PER_M.get(model, (0.0, 0.0))
    return (pin * a + pout * b) / 1_000_000


def _call(kwargs: dict, tag: str | None):
    """Call the API with polite retries on rate limits and server errors."""
    from openai import RateLimitError, APIStatusError, APIConnectionError, APITimeoutError
    delays = [3, 6, 12, 24, 40]
    for attempt in range(len(delays) + 1):
        t0 = time.time()
        try:
            resp = client().chat.completions.create(**kwargs)
            dt = time.time() - t0
            u = getattr(resp, "usage", None)
            pin = getattr(u, "prompt_tokens", 0) or 0
            pout = getattr(u, "completion_tokens", 0) or 0
            CALLS.append({"time": time.strftime("%H:%M:%S"), "tag": tag or "", "provider": CONFIG.get("provider"),
                          "model": kwargs["model"], "latency_s": round(dt, 2), "prompt_tokens": pin,
                          "completion_tokens": pout, "est_cost_usd": round(_cost(kwargs["model"], pin, pout), 6)})
            return resp
        except (RateLimitError, APIConnectionError, APITimeoutError) as e:
            err = e
        except APIStatusError as e:
            # Groq sometimes returns 400 "tool_use_failed" when a model writes a malformed tool call.
            # A retry usually succeeds, so treat it like a temporary error (at most twice).
            if e.status_code == 400 and "tool_use_failed" in str(e) and attempt < 2:
                err = e
            elif e.status_code < 500:
                raise RuntimeError(f"LLM request rejected ({e.status_code}): {e.message}") from None
            else:
                err = e
        if attempt < len(delays):
            print(f"  ({type(err).__name__}; waiting {delays[attempt]}s and retrying)")
            time.sleep(delays[attempt])
    raise RuntimeError(f"LLM call failed after retries: {err}")


def chat(prompt=None, *, system: str | None = None, messages: list | None = None, model: str = "big",
         temperature: float = 0.0, max_tokens: int = 800, json_mode: bool = False, tools: list | None = None,
         tag: str | None = None, raw: bool = False):
    """Send one request. Pass a prompt string, or a full messages list.
    Returns the reply text, or the full message object if tools are given or raw=True."""
    msgs = list(messages or [])
    if system:
        msgs.insert(0, {"role": "system", "content": system})
    if prompt is not None:
        msgs.append({"role": "user", "content": prompt})
    kwargs = {"model": model_name(model), "messages": msgs, "temperature": temperature, "max_tokens": max_tokens}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    if tools:
        kwargs["tools"] = tools
    resp = _call(kwargs, tag)
    msg = resp.choices[0].message
    if tools or raw:
        return msg
    return (msg.content or "").strip()


def parse_json(text: str) -> dict:
    """Parse JSON from a model reply, tolerating ```json fences and extra text."""
    t = (text or "").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            return json.loads(m.group(0))
        raise


def chat_json(prompt, *, system: str | None = None, model: str = "big", tag: str | None = None, **kw) -> dict:
    sys_msg = (system or "") + "\nReply with a single valid JSON object only."
    return parse_json(chat(prompt, system=sys_msg.strip(), model=model, json_mode=True, tag=tag, **kw))


def stream(prompt: str, *, system: str | None = None, model: str = "big") -> str:
    """Print the reply token by token, as a chat UI would."""
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    out = []
    for ev in client().chat.completions.create(model=model_name(model), messages=msgs, stream=True, temperature=0):
        if ev.choices and ev.choices[0].delta and ev.choices[0].delta.content:
            piece = ev.choices[0].delta.content
            out.append(piece)
            print(piece, end="", flush=True)
    print()
    return "".join(out)


def calls_df():
    import pandas as pd
    return pd.DataFrame(CALLS)


def reset_calls():
    CALLS.clear()


# ----------------------------------------------------------------- embeddings

EMBED_MODEL_NAME = os.environ.get("EMBED_MODEL", "minishlab/potion-retrieval-32M")
_embedder = None
EMBED_INFO = {}


class HashEmbedder:
    """Offline fallback: hashed word and word-pair counts. Lower quality, never fails."""
    dim = 1024

    def encode(self, texts):
        import numpy as np
        out = np.zeros((len(texts), self.dim), dtype="float32")
        for i, t in enumerate(texts):
            words = re.findall(r"[a-z0-9]+", t.lower())
            feats = words + [a + "_" + b for a, b in zip(words, words[1:])]
            for f in feats:
                h = int(hashlib.md5(f.encode()).hexdigest(), 16)
                out[i, h % self.dim] += 1.0 if (h >> 20) % 2 else -1.0
        return out


def _load_embedder():
    global _embedder
    if _embedder is not None:
        return _embedder
    if os.environ.get("EMBED_BACKEND", "").lower() != "hash":
        try:
            from model2vec import StaticModel
            _embedder = StaticModel.from_pretrained(EMBED_MODEL_NAME)
            EMBED_INFO.update(backend="model2vec", model=EMBED_MODEL_NAME)
            return _embedder
        except Exception as e:
            print(f"(embedding model could not load: {type(e).__name__}; using offline fallback embedder)")
    _embedder = HashEmbedder()
    EMBED_INFO.update(backend="hash", model="HashEmbedder(1024)")
    return _embedder


def embed(texts) -> "np.ndarray":
    """Return one L2-normalised vector per text."""
    import numpy as np
    if isinstance(texts, str):
        texts = [texts]
    v = np.asarray(_load_embedder().encode(list(texts)), dtype="float32")
    n = np.linalg.norm(v, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return v / n


# ----------------------------------------------------------------- documents

def load_pdfs(folder: str | Path = DATA / "policies") -> list[dict]:
    """Read every PDF in a folder. Returns one record per page."""
    from pypdf import PdfReader
    pages = []
    for f in sorted(Path(folder).glob("*.pdf")):
        reader = PdfReader(str(f))
        for i, pg in enumerate(reader.pages, start=1):
            text = pg.extract_text() or ""
            first = text.splitlines()[0] if text else ""
            parts = [x.strip() for x in first.split("|")]
            dept = parts[1] if len(parts) > 2 else "Unknown"
            pages.append({"doc": f.name, "page": i, "dept": dept, "text": text})
    return pages


def chunk_text(text: str, size: int = 600, overlap: int = 100) -> list[str]:
    """Split text into pieces of about `size` characters, cutting at whitespace,
    with `overlap` characters repeated between neighbours."""
    text = re.sub(r"[ \t]+", " ", text).strip()
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = text.rfind(" ", start + size // 2, end)
            end = cut if cut > 0 else end
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return [c for c in chunks if c]


def chunk_pages(pages: list[dict], size: int = 600, overlap: int = 100) -> list[dict]:
    out = []
    for p in pages:
        for j, c in enumerate(chunk_text(p["text"], size, overlap)):
            out.append({"id": len(out), "doc": p["doc"], "page": p["page"], "dept": p["dept"], "chunk": j, "text": c})
    return out


# ----------------------------------------------------------------- vector store (Qdrant local mode)

def new_store(collection: str = "policies", dim: int | None = None, location: str = ":memory:"):
    """Create an in-process Qdrant instance. In production you would pass
    url="https://..." and api_key=... instead of location; the rest is the same."""
    from qdrant_client import QdrantClient, models
    if dim is None:
        dim = embed(["dimension probe"]).shape[1]
    qc = QdrantClient(location=location)
    if qc.collection_exists(collection):
        qc.delete_collection(collection)
    qc.create_collection(collection, vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE))
    return qc


def index_chunks(qc, chunks: list[dict], collection: str = "policies", batch: int = 128) -> int:
    from qdrant_client import models
    for i in range(0, len(chunks), batch):
        part = chunks[i:i + batch]
        vecs = embed([c["text"] for c in part])
        qc.upsert(collection, points=[
            models.PointStruct(id=c["id"], vector=v.tolist(), payload={k: c[k] for k in c if k != "id"})
            for c, v in zip(part, vecs)])
    return qc.count(collection).count


def search(qc, query: str, k: int = 4, collection: str = "policies", dept=None) -> list[dict]:
    """Semantic search. `dept` can be a department name or a list of names (access control)."""
    from qdrant_client import models
    flt = None
    if dept:
        match = models.MatchAny(any=list(dept)) if isinstance(dept, (list, tuple, set)) else models.MatchValue(value=dept)
        flt = models.Filter(must=[models.FieldCondition(key="dept", match=match)])
    res = qc.query_points(collection, query=embed([query])[0].tolist(), limit=k, query_filter=flt, with_payload=True)
    return [{"score": round(p.score, 3), **p.payload} for p in res.points]


def build_policy_index(size: int = 600, overlap: int = 100, extra_docs: list[dict] | None = None):
    """Load, chunk, embed and index the policy PDFs. Returns (store, chunks)."""
    chunks = chunk_pages(load_pdfs(), size, overlap)
    for d in extra_docs or []:
        for j, c in enumerate(chunk_text(d["text"], size, overlap)):
            chunks.append({"id": len(chunks), "doc": d["doc"], "page": 1, "dept": d.get("dept", "External"), "chunk": j, "text": c})
    qc = new_store()
    index_chunks(qc, chunks)
    return qc, chunks


# ----------------------------------------------------------------- RAG

RAG_SYSTEM = """You are the policy assistant for Meridian Retail employees.
Answer ONLY from the numbered context passages. Cite passages like [1] or [2].
If the context does not contain the answer, reply exactly: "I don't know based on the policies."
Keep answers short and factual."""


def format_context(hits: list[dict]) -> str:
    return "\n\n".join(f"[{i}] ({h['doc']}, page {h['page']})\n{h['text']}" for i, h in enumerate(hits, start=1))


def rag_answer(question: str, qc, k: int = 4, dept=None, min_score: float | None = None,
               system: str = RAG_SYSTEM, model: str = "big", tag: str = "rag") -> dict:
    hits = search(qc, question, k=k, dept=dept)
    if min_score is not None:
        hits = [h for h in hits if h["score"] >= min_score]
    if not hits:
        return {"answer": "I don't know based on the policies.", "sources": [], "hits": []}
    prompt = f"Context:\n{format_context(hits)}\n\nQuestion: {question}"
    ans = chat(prompt, system=system, model=model, tag=tag)
    cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", ans) if 0 < int(n) <= len(hits)})
    sources = [f"{hits[i-1]['doc']} p.{hits[i-1]['page']}" for i in cited]
    return {"answer": ans, "sources": sources, "hits": hits}


# ----------------------------------------------------------------- evaluation

JUDGE_SYSTEM = """You grade answers from a policy assistant.
Compare the ASSISTANT ANSWER with the EXPECTED ANSWER for the QUESTION.
PASS if the assistant answer states the same key fact (wording may differ).
If the expected answer says NOT IN DOCUMENTS, PASS only if the assistant says it does not know.
FAIL otherwise. Return JSON: {"verdict": "PASS" or "FAIL", "reason": "<one short sentence>"}"""


def judge(question: str, expected: str, answer: str, model: str = "big") -> dict:
    """LLM-as-judge: does the answer match the expected answer?"""
    try:
        r = chat_json(f"QUESTION: {question}\nEXPECTED ANSWER: {expected}\nASSISTANT ANSWER: {answer}",
                      system=JUDGE_SYSTEM, model=model, tag="judge")
        v = str(r.get("verdict", "FAIL")).upper()
        return {"verdict": "PASS" if v.startswith("PASS") else "FAIL", "reason": r.get("reason", "")}
    except Exception as e:
        return {"verdict": "FAIL", "reason": f"judge error: {e}"}


def evaluate(qc, rows: list[dict], *, system: str = RAG_SYSTEM, model: str = "big", k: int = 4,
             label: str = "run", answer_fn=None):
    """Run every test question through the assistant and grade it.
    rows: dicts with question, expected_answer, source_doc. Returns a pandas DataFrame."""
    import pandas as pd
    out = []
    for r in rows:
        if answer_fn:
            res = answer_fn(r["question"])
        else:
            res = rag_answer(r["question"], qc, k=k, system=system, model=model, tag=f"eval:{label}")
        docs = [h["doc"] for h in res.get("hits", [])]
        hit = (r["source_doc"] == "none") or (r["source_doc"] in docs)
        g = judge(r["question"], r["expected_answer"], res["answer"])
        out.append({"question": r["question"], "retrieval_hit": hit, "verdict": g["verdict"],
                    "answer": res["answer"][:160], "judge_reason": g["reason"]})
    df = pd.DataFrame(out)
    print(f"[{label}] answer pass rate: {(df.verdict == 'PASS').mean():.0%}   "
          f"retrieval hit rate: {df.retrieval_hit.mean():.0%}   ({len(df)} questions)")
    return df


def load_csv(path: str | Path) -> list[dict]:
    import csv
    with open(ROOT / path if not Path(path).is_absolute() else path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ----------------------------------------------------------------- agents

def tool_spec(fn, description: str, params: dict, required: list | None = None) -> dict:
    """Describe a Python function as an OpenAI-style tool."""
    return {"type": "function", "function": {"name": fn.__name__, "description": description,
            "parameters": {"type": "object", "properties": params, "required": required or list(params)}}}


def console_approver(name: str, args: dict) -> bool:
    if os.environ.get("AUTO_APPROVE"):
        return os.environ["AUTO_APPROVE"].lower() in ("1", "yes", "true")
    ans = input(f"APPROVAL NEEDED: run {name}({args})? Type yes or no: ")
    return ans.strip().lower() in ("y", "yes")


def run_agent(user_msg: str, tools: dict, *, system: str = "You are a helpful assistant. Use tools when needed.",
              needs_approval: set | None = None, approver=console_approver, max_steps: int = 6,
              model: str = "big", verbose: bool = True) -> str:
    """tools: {name: (python_function, tool_spec_dict)}. Prints a readable trace."""
    needs_approval = needs_approval or set()
    specs = [spec for _, spec in tools.values()]
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user_msg}]
    for step in range(1, max_steps + 1):
        msg = chat(messages=msgs, tools=specs, model=model, tag="agent")
        calls = msg.tool_calls or []
        if not calls:
            if verbose:
                print(f"[step {step}] FINAL ANSWER: {msg.content}")
            return msg.content or ""
        msgs.append({"role": "assistant", "content": msg.content or "", "tool_calls": [
            {"id": c.id, "type": "function", "function": {"name": c.function.name, "arguments": c.function.arguments}} for c in calls]})
        for c in calls:
            name = c.function.name
            try:
                args = json.loads(c.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            if verbose:
                print(f"[step {step}] MODEL WANTS TOOL: {name} {args}")
            if name not in tools:
                result = {"error": f"unknown tool {name}"}
            elif name in needs_approval and not approver(name, args):
                result = {"error": "A human reviewer rejected this action. Tell the user it needs manual handling."}
                if verbose:
                    print(f"[step {step}] HUMAN REJECTED {name}")
            else:
                try:
                    result = tools[name][0](**args)
                except Exception as e:
                    result = {"error": f"{type(e).__name__}: {e}"}
            if verbose:
                print(f"[step {step}] TOOL RESULT: {result}")
            msgs.append({"role": "tool", "tool_call_id": c.id, "content": json.dumps(result, default=str)})
    return "Stopped: step limit reached."


# ----------------------------------------------------------------- guardrails

PII_PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "CARD": r"\b(?:\d[ -]?){13,16}\b",
    "AADHAAR": r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b",
    "PAN": r"\b[A-Z]{5}\d{4}[A-Z]\b",
    "PHONE": r"(?:\+91[ -]?)?\b[6-9]\d{9}\b",
}


def mask_pii(text: str) -> tuple[str, list[str]]:
    """Replace personal data with labels. Returns (masked_text, list_of_labels_found)."""
    found = []
    for label, pat in PII_PATTERNS.items():
        if re.search(pat, text):
            found.append(label)
            text = re.sub(pat, f"[{label}]", text)
    return text, found


# ----------------------------------------------------------------- smoke test

def check(full: bool = True) -> bool:
    """Run before the course: verifies packages, key, LLM, JSON, tools, embeddings, Qdrant."""
    ok = True

    def line(name, passed, detail=""):
        nonlocal ok
        ok = ok and passed
        print(f"{'PASS' if passed else 'FAIL'}  {name}  {detail}")

    line("Python version", sys.version_info >= (3, 10), sys.version.split()[0])
    for mod in ("openai", "qdrant_client", "model2vec", "pypdf", "pandas"):
        try:
            __import__(mod)
            line(f"package {mod}", True)
        except Exception as e:
            line(f"package {mod}", False, str(e))
    try:
        cfg = setup(quiet=True)
        line("LLM provider found", True, f"{cfg['provider']} ({len(cfg['available'])} models listed)")
        t = chat("Reply with the single word: ready", max_tokens=10, tag="check")
        line("LLM reply", bool(t), repr(t[:40]))
        line("big model", True, cfg["big"])
        if full:
            j = chat_json('Return {"ok": true}', tag="check")
            line("JSON mode", isinstance(j, dict))
            spec = {"type": "function", "function": {"name": "get_time", "description": "Get the time in a city",
                    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}
            m = chat("What time is it in Delhi? Use the tool.", tools=[spec], tag="check")
            line("tool calling", bool(m.tool_calls), m.tool_calls[0].function.name if m.tool_calls else "no tool call")
    except Exception as e:
        line("LLM", False, str(e)[:200])
    try:
        v = embed(["hello world"])
        line("embeddings", v.shape[0] == 1, f"{EMBED_INFO.get('backend')} {EMBED_INFO.get('model')} dim={v.shape[1]}")
        if EMBED_INFO.get("backend") == "hash":
            print("      NOTE: the real embedding model did not download. Labs still run, with lower search quality.")
        qc, chunks = build_policy_index()
        hits = search(qc, "How many days of annual leave do I get?", k=1)
        line("vector search (Qdrant)", bool(hits), f"{len(chunks)} chunks; top hit: {hits[0]['doc']}")
    except Exception as e:
        line("embeddings / Qdrant", False, str(e)[:200])
    print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED: see SETUP.md, section 'Troubleshooting'")
    return ok
