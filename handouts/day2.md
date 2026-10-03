# Day 2: Knowledge, tools and agents

**Modules:** 3 (Knowledge layer: RAG) and 4 (Tools and agents)
**Labs:** 5, 6, 7, 8 (optional 8b CrewAI, 8c Google ADK)  **Assignment:** A2 (due Day 3 morning)

## By the end of today you can
* Explain how retrieval-augmented generation (RAG) works and where each design choice sits
* Build a searchable knowledge index and get grounded answers with citations
* Enforce access control at retrieval time
* Explain tool calling, what MCP standardises, and when to use an agent versus a fixed workflow
* Put a human approval step in front of a risky action

---

## Module 3.1: RAG fundamentals

LLMs know nothing about your company's documents, and they are out of date. **RAG** fixes this at request time:
find the relevant passages, put them in the prompt, and ask the model to answer only from them.

```
INGESTION (offline, when documents change)
  documents --> extract text --> chunk --> embed --> store vectors + metadata
                                                      in a vector database

QUERY (online, every question)
  question --> embed --> vector search (top k, filtered by access) --> prompt with passages
           --> LLM --> answer with citations --> checks --> user
```

| Building block | What it does | Design choices |
|---|---|---|
| **Text extraction** | turns PDFs, Word, HTML into text | tables and scanned pages need special handling (OCR, layout models) |
| **Chunking** | splits text into passages | size, overlap, splitting at headings or sentences |
| **Embedding model** | turns text into a vector; similar meaning gives similar vectors | language support (Hindi?), dimension, cost, where it runs |
| **Vector database** | stores vectors and finds nearest neighbours fast | managed or self-hosted, metadata filters, scale, hybrid search |
| **Metadata** | document, page, department, date, access groups | enables filters and citations |

**Vector database options (examples):** Qdrant, Weaviate, Milvus, Chroma, pgvector (in PostgreSQL), OpenSearch,
Elasticsearch, cloud services such as Vertex AI Vector Search, Azure AI Search and Cloudflare Vectorize. For many
enterprises the deciding factors are operational: what your teams already run, filtering, security and cost.
In the labs we use **Qdrant in local mode**: it runs inside Python with no server, and the same code connects to a
Qdrant server or Qdrant Cloud by changing one line.

### Lab 5: Build the knowledge layer (notebook `lab05_rag_ingest`)
Load 10 policy PDFs, chunk them, embed, store in Qdrant, search by meaning, and filter by department.

---

## Module 3.2: RAG design choices

* **Grounding prompt:** "answer only from the passages, cite them, say you don't know otherwise."
* **The "I don't know" path:** a production assistant must refuse rather than invent. Test it explicitly.
* **Citations:** let users verify answers and let you audit them.
* **Access control:** filter at retrieval time using metadata (department, groups). The model cannot leak what it
  never receives. Permissions must be synced when they change in the source system.
* **Chunk size and k (number of passages):** small chunks are precise but lose context; large chunks carry context but
  cost more tokens and dilute relevance. Decide with measurements, not opinions.
* **Hybrid search and reranking:** combine keyword and vector search, then reorder the top results with a reranker.
  Helps with product codes, names and exact terms.
* **Freshness:** re-index when documents change; delete vectors of removed documents.

**RAG or fine-tuning?** RAG adds knowledge that changes; fine-tuning changes behaviour or style. Most enterprise
knowledge assistants need RAG first; fine-tuning is a later optimisation.

### Lab 6: Grounded answers (notebook `lab06_rag_answers`)
Answer with citations, refuse out-of-scope questions, apply department access control, and measure retrieval hit
rate for three chunk sizes.

---

## Module 4.1: Tool calling and MCP

**Tool calling:** you describe functions (name, description, parameters). The model replies with a request to call one,
with arguments. **Your code** decides whether to run it, runs it, and sends the result back. The model never executes
anything itself.

```
user --> model: "where is ORD-1001?"
model --> app: call order_status(order_id="ORD-1001")
app --> order system --> result
app --> model: result
model --> user: "Shipped, arriving 5 Oct"
```

**MCP (Model Context Protocol)** is an open standard for exposing tools, data and prompts to AI applications. Instead of
every assistant integrating every API differently, a system publishes an **MCP server** once and any MCP-capable client
(assistants, IDEs, agent frameworks) can use it. Architecture questions move to: which MCP servers are approved,
which identity calls them, and how calls are logged.

**Tool design rules:** clear names and descriptions; narrow, typed parameters; read-only tools by default; write
actions behind permission checks and approvals; idempotent where possible; every call logged.

### Lab 7: Tool calling (notebook `lab07_tool_calling`)

---

## Module 4.2: Agent patterns

An **agent** is a loop: the model chooses a tool, code runs it, the result goes back, and this repeats until the model
answers. A **workflow** is a fixed sequence written in code, with the model used only for specific steps.

| | Workflow | Agent |
|---|---|---|
| Predictability | high | lower |
| Testing | easy | harder |
| Cost and latency | lower, fixed | higher, variable |
| Handles messy, open-ended requests | poorly | well |

**Guidance:** start with a workflow; add agentic steps only where the variability of requests needs it. Put limits on
every agent: allowed tools, maximum steps, budget, and **human approval** for actions that move money, change records or
contact customers. Enforce approvals in code, not in the prompt.

**Frameworks** (CrewAI, LangGraph, Google ADK, OpenAI Agents SDK and others) wrap the same loop and add structure:
multi-agent roles, memory, state, tracing and deployment helpers. Choose on fit with your stack and team skills, and keep
your tools and business rules independent of the framework so you can switch.

### Lab 8: Agent with approval (notebook `lab08_agent_approval`)
Read an agent's trace step by step, add an approval gate for refunds above the agent limit, and compare with a fixed
workflow. Optional: the same agent in **CrewAI** (`lab08b_crewai`) and **Google ADK** (`lab08c_google_adk`).

---

## Assignment A2 (about 45 minutes, due tomorrow morning)
Choose a knowledge-assistant use case **from your own work**. List the **five biggest RAG risks** for it (for example:
stale documents, permission leaks, scanned tables, ambiguous questions, multilingual users) and for each a control.

## Key terms
RAG, chunk, overlap, embedding, vector database, metadata filter, top-k, hybrid search, reranker, grounding,
tool calling, MCP, agent, workflow, human-in-the-loop. See [glossary.md](glossary.md).

## Further reading
* Qdrant documentation (local mode, filtering): https://qdrant.tech/documentation/
* Model Context Protocol: https://modelcontextprotocol.io
* CrewAI documentation: https://docs.crewai.com
* Google Agent Development Kit: https://google.github.io/adk-docs/
* Anthropic, "Building effective agents" (workflows vs agents): https://www.anthropic.com/engineering/building-effective-agents
