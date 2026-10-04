# Day 2: Knowledge, tools and agents

**Modules:** 3 (Knowledge layer: RAG) and 4 (Tools and agents)
**Activities today:** Lab 5, Lab 6, Lab 7, Lab 8 (notebooks); optional Lab 8b (CrewAI) and Lab 8c (Google ADK);
Assignment A2 (homework)

Every notebook lab works the same way: open it from the course page's **Open in Colab** badge (or from the
`notebooks` folder in VS Code), run the cells from top to bottom, then the **Try this** cells at the end, and answer
the questions written under them. A lab worked if every code cell has a green tick and there is no red error box.
When you finish a lab, type `Lab N done` in the course chat.

## By the end of today you can
* Explain how retrieval-augmented generation (RAG) works and where each design choice sits
* Build a searchable knowledge index and get answers with citations
* Enforce access control when searching documents
* Explain tool calling, what MCP standardises, and when to use an agent instead of a fixed workflow
* Put a human approval step in front of a risky action

---

## Module 3.1: RAG fundamentals

Language models know nothing about your company's documents, and their knowledge stops at a training date. **RAG**
fixes this at the moment of each question: find the relevant passages, put them in the prompt, and ask the model to
answer only from them.

```
INGESTION (runs when documents change)
  documents --> extract text --> split into chunks --> embed --> store vectors + metadata
                                                                in a vector database

QUERY (runs for every question)
  question --> embed --> vector search (top k, filtered by access) --> prompt with passages
           --> model --> answer with citations --> checks --> user
```

| Building block | What it does | Design choices |
|---|---|---|
| **Text extraction** | turns PDF, Word or HTML into text | tables and scanned pages need special handling (OCR, layout-aware parsers) |
| **Chunking** | splits text into passages | chunk size, overlap, splitting at headings or sentences |
| **Embedding model** | turns text into a vector; similar meaning gives similar vectors | language support (Hindi?), vector size, cost, where it runs |
| **Vector database** | stores vectors and finds the nearest ones quickly | managed or self-hosted, metadata filters, scale, hybrid search |
| **Metadata** | document, page, department, date, access groups | enables filters and citations |

**Vector database options (examples):** Qdrant, Weaviate, Milvus, Chroma, pgvector (inside PostgreSQL), OpenSearch,
Elasticsearch, and cloud services such as Vertex AI Vector Search, Azure AI Search and Cloudflare Vectorize. For most
enterprises the deciding factors are operational: what your teams already run, filtering, security and cost.
In the labs we use **Qdrant in local mode**: it runs inside Python with no server, and the same code connects to a
Qdrant server or Qdrant Cloud by changing one line.

### Lab 5: Build the knowledge layer (notebook `lab05_rag_ingest`, 30 minutes)
**What you do:** run the notebook from top to bottom, then the two Try this cells.
**What you will see:** 20 pages loaded from 10 policy documents; 38 chunks; a vector of 512 numbers for one sentence;
a similarity table where the question about holidays is closest to the sentence about annual leave; search results
that find the right policy without matching words; and different results for the same question when the search is
limited to one department.
**Answer at the end:** where should access-control information come from in your company, and what happens when a
document's permissions change after it was indexed?

---

## Module 3.2: RAG design choices

* **Grounding prompt:** "answer only from the passages, cite them, say you don't know otherwise."
* **The "I don't know" path:** a production assistant must refuse rather than invent. Test it explicitly.
* **Citations:** let users check answers, and let you audit them.
* **Access control:** filter the search by department or group before anything reaches the model. The model cannot leak
  what it never receives. Permissions must be kept in step with the source system.
* **Chunk size and k (number of passages):** small chunks are precise but lose context; large chunks carry context but
  cost more tokens. Decide by measuring, not by opinion.
* **Hybrid search and reranking:** combine keyword and vector search, then reorder the top results with a reranker.
  Helps with product codes, names and exact terms.
* **Freshness:** re-index when documents change; delete the vectors of removed documents.

**RAG or fine-tuning?** RAG adds knowledge that changes; fine-tuning changes behaviour or style. Most enterprise
knowledge assistants need RAG first.

### Lab 6: Answers with citations (notebook `lab06_rag_answers`, 30 minutes)
**What you do:** run the notebook from top to bottom, then the two Try this cells.
**What you will see:** an answer about hotel limits that cites the travel policy; the exact passages the model
received; "I don't know based on the policies." for questions the documents do not cover; a different answer for an
HR user and a Customer Service user asking the same question; and a table comparing three chunk sizes.
**Answer at the end:** how many test questions would you need before choosing a chunk size, and who should write them?

---

## Module 4.1: Tool calling and MCP

**Tool calling:** you describe functions to the model (name, description, parameters). The model replies with a request
to call one, with arguments. **Your code** decides whether to run it, runs it, and sends the result back. The model
never runs anything itself.

```
user  --> model : "Where is ORD-1001?"
model --> app   : please call order_status(order_id="ORD-1001")
app   --> order system --> result
app   --> model : the result
model --> user  : "Shipped, arriving 5 Oct"
```

**MCP (Model Context Protocol)** is an open standard for offering tools and data to AI applications. Instead of every
assistant integrating every API differently, a system publishes an **MCP server** once and any MCP-capable assistant or
agent framework can use it. The architecture questions become: which MCP servers are approved, which identity calls
them, and how calls are logged.

**Tool design rules:** clear names and descriptions; narrow, typed parameters; read-only tools by default; actions that
change data behind permission checks and approvals; safe to repeat where possible; every call logged.

### Lab 7: Give the assistant a tool (notebook `lab07_tool_calling`, 25 minutes)
**What you do:** run the notebook from top to bottom, then the two Try this cells.
**What you will see:** the model replies with no text, only a request to call `order_status`; your code runs it; the
second call gives the final answer (shipped, arriving 5 Oct); a question about support hours makes no tool call.
**Answer at the end:** did a vague tool description still work, and what does that tell you about writing tool
descriptions?

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

**Guidance:** start with a workflow; add agent steps only where requests really vary. Put limits on every agent:
allowed tools, maximum steps, budget, and **human approval** for actions that move money, change records or contact
customers. Enforce approvals in code, not in the prompt.

**Frameworks** (CrewAI, LangGraph, Google ADK, OpenAI Agents SDK and others) wrap the same loop and add structure:
roles, memory, state, tracing. Keep your tools and business rules independent of the framework so you can switch.

### Lab 8: An agent with a human approval step (notebook `lab08_agent_approval`, 30 minutes)
**What you do:** run the notebook from top to bottom. In section 4 the notebook stops and asks you to approve a refund:
type `yes` or `no` and press Enter (Colab: a box under the cell; VS Code: a box at the top of the window).
**What you will see:** a step-by-step trace (`[step 1] MODEL WANTS: ...`, `RESULT: ...`); without the gate the agent may
issue a full INR 7,999 refund; with the gate it stops for your approval because the amount is above INR 5,000; then
the same job done as a fixed workflow.
**Answer at the end:** where else in your organisation does an AI action need a human approval, and who approves?

**Optional, Labs 8b and 8c:** the same agent built with **CrewAI** (`lab08b_crewai`) and **Google ADK**
(`lab08c_google_adk`). Run them in Colab; each installs its framework first (1 to 2 minutes).

---

## Assignment A2: RAG risks for your own use case (about 45 minutes, due before 09:15 tomorrow)
**Write one page with these three headings:**
1. **Use case:** a knowledge assistant from your own work, in two sentences (who uses it, which documents).
2. **Five risks and controls:** a table with five rows: the risk, and one concrete control for it. Example risks:
   outdated documents, permission leaks, scanned tables, ambiguous questions, Hindi or mixed-language questions,
   answers that need two documents.
3. **First test:** the one risk you would test first, and exactly how (what question you would ask, what result
   would worry you).

**Submit** it the same way as Assignment A1.

## Key terms
RAG, chunk, overlap, embedding, vector database, metadata filter, top-k, hybrid search, reranker, grounding, tool
calling, MCP, agent, workflow, human-in-the-loop. See [glossary.md](glossary.md).

## Further reading
* Qdrant documentation (local mode, filtering): https://qdrant.tech/documentation/
* Model Context Protocol: https://modelcontextprotocol.io
* CrewAI documentation: https://docs.crewai.com
* Google Agent Development Kit: https://google.github.io/adk-docs/
* Anthropic, "Building effective agents" (workflows and agents): https://www.anthropic.com/engineering/building-effective-agents
