# GitHub Copilot Instructions for Agentic AI for Dummies

These instructions describe the repository as it exists today. Prefer the
small, educational, runnable-example style already used here over introducing
production-framework scaffolding that is not needed by an example. When a
requested change would alter an example's teaching purpose, preserve the simple
version and make the production concern explicit in documentation or a separate
example.

## 1. Project Overview & Architecture

This is a Python 3.12+ learning repository for agentic AI patterns. It contains
small executable demonstrations and Jupyter notebooks covering LangChain,
LangGraph, retrieval-augmented generation (RAG), MCP, guardrails, deep agents,
vectorless RAG, and LLM evaluation. It is not a web application, service, or
conventional layered backend.

The repository is a topic-oriented collection with one small reusable RAG
package:

```text
.
├── main.py                 # Minimal smoke-test entry point
├── langchains/             # LangChain basics, models, and tools
├── langgraphs/             # LangGraph chatbot and human-in-the-loop examples
├── rag/
│   ├── app.py              # RAG command-line example
│   ├── data/               # Source documents used by RAG examples
│   ├── faiss_index/        # Local/generated FAISS artifacts
│   ├── notebooks/          # RAG exploration notebooks
│   └── src/                # Reusable loading, embedding, search, and storage
├── vectorless_rag/         # PageIndex-based RAG example and input files
├── mcp/                    # Math and weather MCP servers plus async client
├── deep_agents/            # Deep-agent notebook examples
├── guardrails/             # Guardrail examples
├── llm-evaluation/         # LLM/RAG evaluation notebooks and reference data
├── pyproject.toml          # Project metadata and dependency declarations
├── uv.lock                 # Resolved dependency lock file
└── README.md               # Setup and execution documentation
```

Executable examples generally use one script per example and an
`if __name__ == "__main__":` guard. `rag/src` contains the reusable classes
`EmbeddingPipeline`, `FaissVectorStore`, and `RAGSearch`. MCP tools are
module-level functions registered with `FastMCP`.

There is no database, HTTP application framework, frontend, ORM, or shared API
contract. Do not invent controllers, routes, repositories, React components, or
service layers unless the task explicitly asks to introduce one.

## 2. Tech Stack & Dependencies

### Runtime and tooling

- Python `>=3.12`; `.python-version` selects `3.12`.
- `uv` is the package manager and runner. Use `uv sync` and `uv run ...`.
- Dependencies are declared in `pyproject.toml` and resolved in `uv.lock`.
- Jupyter notebooks use `ipykernel`; VS Code is the documented environment.
- No formatter, linter, type checker, test runner, Docker configuration, or CI
  workflow is currently configured. Do not claim one is present.

### AI and application libraries

The current resolved direct versions include:

- LangChain `1.4.2`, LangChain Core `1.6.3`, Community `0.4.2`, Groq `1.1.3`,
  text splitters `1.1.2`, Tavily `0.2.18`, and LangSmith `0.13.0`.
- LangGraph `1.2.11`, DeepAgents `0.7.15`, and MCP `1.29.0`.
- `langchain-mcp-adapters` `0.3.2` for MCP client integration.
- FAISS CPU `1.15.0`, ChromaDB `1.5.9`, Sentence Transformers `6.0.0`, and
  PageIndex `0.2.18` for retrieval and indexing.
- PyPDF, PyMuPDF, BeautifulSoup, Requests, and LangChain community loaders
  for document ingestion.
- `python-dotenv` `1.2.2` for local environment variables and NumPy through the
  embedding/indexing stack.

Use the versions in `pyproject.toml` for declared compatibility and let
`uv.lock` provide reproducibility. When adding or changing a dependency, use the
normal `uv` workflow so the lock file is updated too.

## 3. Code Quality & Formatting Rules

### Naming and layout

- Use four spaces for indentation and normal PEP 8 Python formatting.
- Use `snake_case` for modules, functions, parameters, and local variables.
- Use `PascalCase` for classes, such as `FaissVectorStore` and
  `EmbeddingPipeline`.
- Use uppercase names for constants only when a value is genuinely constant.
- Keep topic directories descriptive and preserve the existing numeric-prefix
  style for ordered notebooks, such as `1-...` and `2-...`.
- Keep imports at module scope, grouped by standard library, third-party, and
  local imports. Use explicit imports; do not use wildcard imports.
- Do not add unnecessary package plumbing or `__all__` declarations.

### Types and documentation

- Add type annotations to new public functions, methods, tools, and meaningful
  class attributes. Prefer built-in generics such as `list[str]`,
  `dict[str, object]`, and `tuple[...]` for new Python 3.12 code.
- Existing code uses `typing.List`, `typing.Any`, and `np.ndarray`; preserve
  compatibility when editing a nearby example, but avoid new `Any` when a useful
  concrete type exists.
- Use LangChain `Document` types or a precise protocol/type alias when a
  function expects documents. Isolate uncertainty at third-party boundaries.
- Add concise docstrings to public reusable functions and MCP tools. MCP
  docstrings are part of the model-facing tool description and should document
  inputs and returned meaning.
- Keep comments focused on non-obvious provider behavior, notebook teaching
  context, or path/persistence decisions. Do not narrate obvious syntax.

### Configuration and secrets

- Load provider credentials from environment variables with `load_dotenv()` at
  executable boundaries, as current examples do.
- Use the established names `GROQ_API_KEY`, `HF_TOKEN`, `GOOGLE_API_KEY`,
  `OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `PAGEINDEX_API_KEY`, and
  `LANGSMITH_API_KEY`.
- Never hard-code, print, or commit API keys, tokens, credentials, or private
  document contents. Keep actual values in the ignored `.env` file.
- Add new credential names to `.env.example` with empty values and document new
  setup requirements in `README.md`.

## 4. Architectural Patterns & Component Structure

### New standalone example

Place a new example in the topic directory that owns its concept. Keep setup
close to the example and use this shape:

```python
def main() -> None:
    # Configure and run the smallest useful demonstration.
    ...


if __name__ == "__main__":
    main()
```

Use `async def main()` and `asyncio.run(main())` for asynchronous model or MCP
work, following `mcp/client.py`. Keep model construction, file loading, index
creation, network connections, and server startup out of import-time code.

### Reusable RAG code

Keep responsibilities separated under `rag/src`:

- `data_loader.py` discovers files and converts supported formats to LangChain
  documents.
- `embedding.py` chunks documents and creates CPU sentence embeddings.
- `vectorstore.py` owns FAISS construction, persistence, loading, and querying.
- `search.py` coordinates retrieval and LLM summarization.
- `rag/app.py` is the thin executable entry point.

For a RAG change, update the narrowest owning layer. Preserve this flow:

```text
source files -> document loaders -> chunks -> embeddings -> FAISS index + metadata
                                             -> query embedding -> nearest results
                                             -> context prompt -> chat model response
```

Reuse `RecursiveCharacterTextSplitter`, `SentenceTransformer`, FAISS, and the
existing RAG classes rather than duplicating chunking, embedding, or nearest
neighbor logic. Preserve the default embedding model and chunk settings unless
the task specifically changes retrieval behavior. If changing metadata shape,
update persistence and query consumers together.

### MCP examples

- Define servers with `FastMCP` and register callable functions using
  `@mcp.tool()`.
- Give every tool typed parameters, a concrete return type, and a concise useful
  docstring.
- Keep server startup under the main guard and select transport explicitly:
  math uses stdio and weather uses streamable HTTP.
- Keep orchestration in the async client. Retrieve tools with
  `MultiServerMCPClient`, pass them to the LangChain agent, and await calls.

### Paths and notebooks

The README intentionally runs some programs from their owning directory, for
example `cd rag` before `uv run python app.py` and `cd mcp` for MCP scripts.
Respect those commands when changing paths. For reusable code, prefer
`pathlib.Path` and paths derived from `Path(__file__)` or explicit configuration
rather than silently changing documented behavior.

Notebooks are instructional artifacts, not libraries. Keep cells runnable from
a fresh kernel in top-to-bottom order. Explain provider setup, expensive
operations, and external services in markdown. Avoid absolute machine paths,
secrets, generated indexes, and large accidental outputs. Move reusable logic
into a focused Python module when it emerges.

## 5. Data Handling & API Conventions

### Model and provider calls

- Keep provider-specific construction localized and configure it from environment
  credentials.
- Use current LangChain `.invoke()` and `.ainvoke()` APIs with the message shape
  expected by the selected library version.
- Treat model responses as library objects until the expected content is
  explicitly extracted.
- Keep prompts explicit and small. In RAG prompts, clearly separate retrieved
  context from the question and do not claim unsupported facts.
- Do not add hidden network calls to imports or default smoke tests.

### Documents and persisted indexes

- Supported ingestion formats are PDF, TXT, CSV, DOCX, XLSX, and JSON through
  LangChain community loaders.
- Validate input directories/files before expensive processing and include the
  affected path in errors.
- Validate index availability, embedding dimensions, empty input, and vector /
  metadata count alignment before querying FAISS.
- Return a clear result or raise a focused error; do not allow an obscure
  `None.search(...)` failure.
- FAISS indexes, SQLite files, binaries, caches, model data, and other generated
  artifacts are local state and must remain ignored.
- Treat retained pickle metadata as trusted local state only; never load it from
  an untrusted path.

### Errors and logging

Small examples currently use `[INFO]`, `[DEBUG]`, `[WARNING]`, and `[ERROR]`
`print` messages. Preserve that style when it supports the lesson; use the
standard `logging` module for reusable or long-running code.

- Catch exceptions only where the example can recover or add meaningful context.
- Include the affected path or operation, but never secrets or full sensitive
  document contents, in diagnostics.
- Do not silently swallow failures. Fail clearly when an operation cannot
  continue.
- Per-file loader failures may be reported and skipped when independent files
  can still be processed.
- Preserve the existing RAG fallback string `No relevant documents found.`
  rather than sending an empty prompt to a paid provider.

## 6. Testing Conventions

There is currently no `tests/` directory, no pytest dependency, no test
configuration, no CI workflow, and no formatter or linter. The notebook named
`langchains/1-langchain_test.ipynb` is a learning notebook, not an automated
test suite.

For every new or materially changed Python module:

- At minimum run `uv run python -m compileall -q main.py mcp rag`, or the narrow
  equivalent for the changed path.
- For non-trivial reusable logic, prefer deterministic `pytest` tests in a
  top-level `tests/` directory named `test_<module>.py`, with functions named
  `test_<behavior>`. Add the dependency and update `uv.lock` through `uv`.
- Test path discovery, empty inputs, chunking, metadata alignment, persistence,
  and error branches using temporary directories and synthetic documents.
- Mock provider, network, model, and MCP boundaries. Do not require API keys,
  live Tavily/Groq/LangSmith calls, downloaded model weights, a running HTTP
  server, or a checked-in FAISS index for ordinary tests.
- Keep integration tests opt-in and document credentials, network access,
  working directory, cost, and resource requirements.
- Validate notebook JSON, kernel selection, rerunnable setup cells, and absence
  of leaked secrets. Do not treat stale cell outputs as proof of correctness.

## 7. Strict "DOs and DON'Ts" (Guardrails)

### DO

1. **DO use the project toolchain:** Python 3.12+, `uv`, `pyproject.toml`, and
   the locked `uv.lock` are the source of truth.
2. **DO keep examples focused and runnable:** use typed helpers, guarded entry
   points, clear setup instructions, and the nearest topic directory.
3. **DO preserve RAG boundaries:** keep loading, chunking, embedding, vector
   storage, retrieval, and summarization separate.
4. **DO use environment variables for credentials** and update `.env.example`
   and `README.md` when setup changes.
5. **DO validate external inputs and persistence state** and avoid network/model
   calls in default smoke checks.

### DON'T

1. **DON'T invent frontend, database, REST, or enterprise service layers** for
   an educational example unless explicitly requested.
2. **DON'T hard-code credentials, absolute paths, private document contents, or
   user-specific environment assumptions.**
3. **DON'T duplicate existing embedding, chunking, FAISS, document-loader, or
   MCP registration logic.**
4. **DON'T perform model calls, filesystem mutation, index creation, or server
   startup merely by importing a module.**
5. **DON'T hide failures with broad `except Exception: pass`, unchecked empty
   indexes, untyped public APIs, or paid live model calls in default tests.**

## Working Commands

From the repository root:

```bash
uv sync
uv run python main.py
uv run python -m compileall -q main.py mcp rag
```

For RAG and MCP examples, follow the working-directory commands in `README.md`.
Before reporting completion, run the narrowest relevant executable check and
mention any validation that requires credentials, network access, or large model
downloads.
