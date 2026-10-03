# Setup guide

Complete this **before Day 1**. It takes about 15 minutes. You need:

1. A free **Groq API key** (the LLM used in the labs). A free **Gemini API key** as a backup is recommended.
2. **One** way to run the notebooks:
   * **Option A: Google Colab** (recommended). Nothing to install. You need a Google account and a browser.
   * **Option B: Your own laptop** with Python and VS Code. Choose this if you prefer working locally, or want to
     use an AI coding assistant (Claude Code, GitHub Copilot) next to the labs.
3. Run the notebook **`00_setup_check`** and confirm it ends with **ALL CHECKS PASSED**.

If anything fails, send a screenshot of the output to your trainer **before** the course starts.

---

## 1. API keys

### Groq (required)
1. Open https://console.groq.com and sign in (Google, GitHub or email). No credit card is needed.
2. In the left menu click **API Keys**, then **Create API Key**. Name it `ai-architect-course`.
3. Copy the key (it starts with `gsk_`). **It is shown only once.** Keep it in a password manager or a private note.

The free tier allows roughly 30 requests a minute and 1,000 requests a day per model, which is more than the labs need.
Each participant must use **their own** key: limits are per account.

### Gemini (recommended backup)
1. Open https://aistudio.google.com and sign in with a Google account.
2. Click **Get API key** (left menu), then **Create API key**. Copy it.

If Groq is unavailable during the course, your trainer will ask you to switch to Gemini (see section 5).

### Keep keys secret
Never paste a key into a notebook cell, a chat or a screenshot. The steps below store it safely.

---

## 2. Option A: Google Colab

1. Open the course page on GitHub (link from your trainer) and click **00_setup_check** in the table, on the
   **Open in Colab** badge. Or open https://colab.research.google.com, choose **File > Open notebook > GitHub**
   and paste the course repository address.
2. **Add your key as a Colab secret:**
   * Click the **key icon** in the left sidebar (*Secrets*).
   * Click **+ Add new secret**. Name: `GROQ_API_KEY`. Value: your key.
   * Switch on **Notebook access** for that secret.
   * Optional: add `GEMINI_API_KEY` the same way.
   * Secrets are stored in your Google account, so you add them once and every course notebook can use them.
     Each new notebook may ask you once to allow access: click **Grant access**.
3. Run the first cell (the play button, or **Shift+Enter**). The first run in each notebook downloads the course files
   and installs packages: about 30 to 60 seconds.
4. Run the remaining cells. The last line should read **ALL CHECKS PASSED**.

**Colab tips**
* Each notebook has its own runtime. Always run the **setup cell first** in every notebook.
* If Colab shows *"Runtime disconnected"*, click **Reconnect** and run the setup cell again.
* Save your own changes with **File > Save a copy in Drive**.

---

## 3. Option B: your laptop with VS Code

Supported: Windows 10/11, macOS 13 or later, Linux. About 1 GB free disk space.

### 3.1 Install Python 3.12
* **Windows:** download Python 3.12 from https://www.python.org/downloads/windows/ (Windows installer, 64-bit).
  On the first installer screen **tick "Add python.exe to PATH"**, then click *Install Now*.
* **macOS:** download the macOS 64-bit universal installer for Python 3.12 from https://www.python.org/downloads/macos/
  and run it.
* **Linux:** use your package manager, for example `sudo apt install python3.12 python3.12-venv`.

Check it in a new terminal: `python --version` (Windows) or `python3.12 --version` (macOS/Linux).
Python 3.10, 3.11 and 3.13 also work.

### 3.2 Install VS Code and two extensions
1. Install VS Code from https://code.visualstudio.com
2. Open VS Code, click the **Extensions** icon in the left bar (four squares), and install:
   * **Python** (publisher: Microsoft)
   * **Jupyter** (publisher: Microsoft)

### 3.3 Get the course files
* With Git: `git clone <course repository address>`
* Without Git: on the GitHub page click the green **Code** button, then **Download ZIP**, and unzip it.

### 3.4 Create a virtual environment and install packages
Open a terminal **in the course folder** (in VS Code: **File > Open Folder**, choose the course folder, then
**Terminal > New Terminal**) and run:

**Windows (PowerShell)**
```
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If PowerShell refuses to run the activate script, run this once and try again:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**macOS / Linux**
```
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
The install takes 1 to 3 minutes.

### 3.5 Add your key
In the course folder, copy the file `.env.example` to a new file named `.env` and put your key in it:
```
GROQ_API_KEY=gsk_your_key_here
GEMINI_API_KEY=your_gemini_key_here
```
`.env` is listed in `.gitignore`, so it is never committed to Git.

### 3.6 Run the setup check
1. In VS Code open `notebooks/00_setup_check.ipynb`.
2. Click **Select Kernel** (top right of the notebook), then **Python Environments**, then the one marked `.venv`.
3. Click **Run All**. The output should end with **ALL CHECKS PASSED**.

### Optional: uv instead of pip
If you use `uv`: `uv venv -p 3.12` then `uv pip install -r requirements.txt`. The notebooks work with uv environments
(the optional labs install extra packages with uv automatically when pip is not present).

---

## 4. Optional labs 8b (CrewAI) and 8c (Google ADK)

These install extra packages from inside the notebook. **Run them in Colab** if you can: CrewAI is large (about 750 MB
including its dependencies) and on some laptops its dependency `onnxruntime` has no installable version
(for example Intel Macs and macOS older than 14).

To run them locally, use a **separate** virtual environment so the main labs stay clean:
```
py -3.12 -m venv .venv-agents            (macOS/Linux: python3.12 -m venv .venv-agents)
.venv-agents\Scripts\Activate.ps1         (macOS/Linux: source .venv-agents/bin/activate)
pip install -r requirements.txt crewai google-adk litellm
```
Then select `.venv-agents` as the kernel for labs 8b and 8c.

---

## 5. Switching the LLM provider

The labs pick a provider automatically: Groq if `GROQ_API_KEY` is found, else Gemini if `GEMINI_API_KEY` is found.
To switch, run this in a new cell right after the setup cell (works in Colab and locally):
```
lk.setup("gemini")      # or lk.setup("groq")
```
Locally you can also make it permanent with a line `LLM_PROVIDER=gemini` in `.env`.
To force a specific model: `LLM_MODEL=...` (big model) and `LLM_MODEL_SMALL=...` (small model) in `.env`, or
`import os; os.environ["LLM_MODEL"] = "..."` followed by `lk.setup()`.

**Offline backup (local only):** install Ollama from https://ollama.com, run `ollama pull llama3.2:3b`, and set
`LLM_PROVIDER=ollama` in `.env`. It is slower and less accurate, but needs no internet once the model is downloaded.

---

## 6. Troubleshooting

| Message | What it means | Fix |
|---|---|---|
| `No LLM provider available` | No key found | Colab: add the secret and switch on *Notebook access*. Local: check `.env` is in the course folder (not in `notebooks/`) and the line starts with `GROQ_API_KEY=` with no spaces or quotes |
| `LLM request rejected (401)` | Key wrong or revoked | Create a new key and replace it |
| `RateLimitError ... waiting` | Too many requests per minute | Nothing: the labs wait and retry automatically |
| `ConnectError`, `ProxyError`, `SSL: CERTIFICATE_VERIFY_FAILED` | Office network or proxy blocks the API | Try a mobile hotspot to confirm. Then use Colab, or ask your IT team to allow `api.groq.com` and `generativelanguage.googleapis.com` |
| `pip install` fails behind a proxy | Proxy blocks package downloads | `pip install --proxy http://<proxy-host>:<port> -r requirements.txt`, or use Colab |
| `embedding model could not load ... using offline fallback` | The embedding model (from huggingface.co) is blocked | The labs still work with a simpler built-in embedder. Search quality is lower. Ask IT to allow `huggingface.co` or use Colab |
| `ModuleNotFoundError: labkit` | The setup cell was not run | Run the first cell of the notebook |
| VS Code does not show `.venv` as a kernel | The environment was created after VS Code opened | **Ctrl+Shift+P** (macOS **Cmd+Shift+P**), run *Developer: Reload Window*, then Select Kernel again |
| Colab: `git clone` failed | Repository address is wrong or private | Tell your trainer |
