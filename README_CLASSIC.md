AGENTIC RAG —
=================================

Overview
--------

Adaptive Agentic RAG is an experimental Retrieval-Augmented Generation (RAG) system that demonstrates a small "agentic" orchestration layer on top of typical RAG components. The system includes:

- a persistent Chroma vectorstore built from seeded web pages or uploaded documents (TXT/MD/PDF),
- retrieval components to fetch context relevant to a user question,
- generation chains to produce answers conditioned on retrieved context,
- grading chains to assess document relevance and detect hallucinations,
- a simple workflow graph that routes queries and conditionally triggers re-queries or tool calls.

This README provides classical, step-by-step instructions to install, run, and test the repository locally.

Prerequisites
-------------

- Python 3.10 or newer
- Git
- A terminal (PowerShell recommended on Windows)
- Provider credentials (for the LLM and embedding service you plan to use). The project is configured to use Google Generative AI by default; adapt `src/models/model.py` to swap providers.

Repository contents (high level)
--------------------------------

- `main.py` — CLI entrypoint
- `streamlit_app.py` — Streamlit web demo (supports TXT/MD/PDF upload)
- `data/ingestion.py` — Vectorstore creation and `retriever` export
- `src/models/model.py` — LLM + embedding wiring
- `src/workflow/` — Chains, nodes, and the state graph
- `requirements.txt` — Python dependencies
- `tests/` — unit tests

Installation
------------

1. Clone the repository and change into the project directory:

```powershell
git clone <repository-url>
cd adaptive_rag
```

2. Create and activate a virtual environment (PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```powershell
C:/path/to/venv/Scripts/python.exe -m pip install -r requirements.txt
```

Notes:
- If `pip install -r requirements.txt` fails on one or more packages, inspect the error and install missing system-level dependencies as required (e.g., build tools or libraries needed by a package). You may also install key packages individually (for example `streamlit`, `pypdf`, `langchain`, `langchain_chroma`).

Configuration (environment variables)
-------------------------------------

1. Create a `.env` file in the project root with your provider credentials. Example keys the project may expect (adjust to your provider):

```text
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

2. Ensure any provider-specific SDKs are configured according to their documentation.

Run the CLI (quick check)
-------------------------

Run the CLI entrypoint to validate imports and basic behavior:

```powershell
python main.py
```

You will see an interactive prompt that demonstrates the retrieval and generation pipeline.

Run the Streamlit demo (recommended)
-----------------------------------

1. With the virtual environment activated, start Streamlit:

```powershell
C:/path/to/venv/Scripts/python.exe -m streamlit run streamlit_app.py
```

2. Open the URL shown by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar to create the seeded vectorstore (this downloads and indexes some web pages — one-time operation). Then upload text files or PDFs and click "Add uploaded docs to vectorstore".

4. Enter a question and click "Ask". The app will:

- route the question between vectorstore and web search,
- retrieve documents from the chosen datasource,
- generate an answer using the generation chain,
- display per-document relevance grades and a hallucination grade for the generated answer.

Testing
-------

Run the unit tests with pytest:

```powershell
C:/path/to/venv/Scripts/python.exe -m pytest tests/ -v
```

If tests fail during collection, verify that dependencies are installed and environment variables are set.

Agentic RAG vs Traditional RAG
------------------------------

This project uses an "agentic" approach. Below is a concise comparison:

Traditional RAG

- Linear pipeline: retrieve -> generate -> return.
- Assumes the vectorstore contains sufficient and reliable context.
- Simpler, easier to reason about; works well for many simple QA tasks.

Agentic RAG (this repository)

- Adds routing and small decision-making components (routers, graders).
- Can choose between vectorstore retrieval and web search for each query.
- Grades retrieved documents and may re-query or call tools based on those grades (multi-step flows).
- Provides an orchestration layer (a state graph) for conditional edges and retries to improve answer groundedness and robustness.

When to prefer Agentic RAG

- When source availability is uncertain or up-to-dateness matters.
- When you need explicit evidence checks (document grading) and re-query logic.
- When answers must be grounded and you want a system that can automatically consult external tools.

Troubleshooting
---------------

- ModuleNotFoundError: Install the missing dependency into your venv.
- ChatPromptTemplate errors: ensure keys passed into `.invoke({..})` match prompt variables (common typo: `quesion` vs `question`).
- Vectorstore creation slow: seeded creation downloads web pages and splits them; this can take time.

Extending and contributing
--------------------------

- Swap the LLM or embeddings by editing `src/models/model.py`.
- Add more document loaders (DOCX, OCR) by updating the Streamlit uploader and ingestion script.
- Improve tests and CI to cover chains and nodes.
