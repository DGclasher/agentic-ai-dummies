# Agentic AI for Dummies

A hands-on learning path for building applications with LangChain, LangGraph, retrieval-augmented generation (RAG), guardrails, MCP, and deep-agent patterns. The notebooks and small Python programs follow the material from [this course](https://www.youtube.com/watch?v=rV3HJ4LEZ7k&list=PLv9ppQ4ScBnWtMRCa2dk43izcnYTW11lX&index=1).

The numbered folders are arranged in a recommended learning order. The `01_`, `02_`, and `03_` prefixes on notebooks provide the same ordering within each topic.

## Learning Path

Follow the folders from `01` to `09` for a gradual progression from model calls to production-oriented agent concerns:

1. **`01_langchain_fundamentals/`**: Learn LangChain basics, model integration, messages, and tool integration.
2. **`02_llm_gateway/`**: Explore a gateway approach for working with different model providers, including AWS.
3. **`03_langgraph_workflows/`**: Build stateful graphs with nodes, edges, tool calls, and human-in-the-loop pauses.
4. **`04_vector_rag/`**: Build a traditional RAG pipeline with document loading, chunking, embeddings, and vector search.
5. **`05_vectorless_rag/`**: Compare vector retrieval with PageIndex's hierarchical, tree-based retrieval approach.
6. **`06_guardrails_and_safety/`**: Add deterministic checks, model-based checks, PII handling, and approval workflows.
7. **`07_mcp_integrations/`**: Connect an agent to external tools through the Model Context Protocol.
8. **`08_deep_agents/`**: Study more advanced agent patterns involving planning, tools, and specialized behavior.
9. **`09_llm_evaluation/`**: Measure answer quality and RAG behavior with datasets, graders, and tracing.

This order is intentional: understand model and tool calls first, then learn orchestration, retrieval, safety, external integrations, advanced agents, and evaluation.

## Project Structure

### `01_langchain_fundamentals/`

- `01_langchain_basics.ipynb`: Core LangChain concepts.
- `02_model_integration.ipynb`: Connecting LangChain to chat models.
- `03_tool_integration.ipynb`: Defining and using tools.

### `02_llm_gateway/`

- `01_llm_gateway_basics.ipynb`: Basic gateway usage.
- `02_llm_gateway_aws.ipynb`: Gateway integration with AWS models.
- `files/`: Supporting files for the gateway examples.
- `vector_store/`: Local vector-store artifacts used by the examples.

### `03_langgraph_workflows/`

- `01_basic_chatbot.ipynb`: A basic state graph and tool-calling chatbot.
- `02_human_in_the_loop.ipynb`: Pausing a graph for human feedback and resuming it.

### `04_vector_rag/`

- `notebooks/01_doc_loading.ipynb`: Loading documents.
- `notebooks/02_pdf_loading_and_chunking.ipynb`: Loading PDFs and splitting them into chunks.
- `notebooks/vector_store/`: Notebook-related vector-store artifacts.
- `src/`: Reusable document loading, embedding, vector-store, and search code.
- `data/`: Source documents for the RAG examples.
- `faiss_index/`: Locally generated FAISS index files.
- `app.py`: Command-line RAG example using the reusable code.

### `05_vectorless_rag/`

- `01_pageindex_vectorless_rag.ipynb`: Upload a PDF to PageIndex, inspect its document tree, select relevant nodes with an LLM, and generate an answer from the selected sections.
- `README.md`: Detailed explanation of the vectorless RAG workflow and its functions.
- `files/`: Input files for the PageIndex example.

### `06_guardrails_and_safety/`

- `01_guardrails.ipynb`: Deterministic and model-based checks, PII middleware, human approval, and agent hooks.

### `07_mcp_integrations/`

- `maths.py`: MCP math server.
- `weather.py`: MCP weather server.
- `client.py`: Async client that connects to the MCP servers and uses their tools.

### `08_deep_agents/`

- `01_deep_agents.ipynb`: Deep-agent concepts and advanced agent behavior.

### `09_llm_evaluation/`

- `01_llm_eval_basics.ipynb`: LLM evaluation fundamentals.
- `02_rag_eval.ipynb`: RAG test data, tracing, and answer evaluators.

At the repository root, `main.py` is a minimal smoke-test entry point, `pyproject.toml` contains project metadata and dependencies, and `uv.lock` records the resolved dependency versions.

## Requirements

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- API keys for the providers used by the example you want to run
- Network access for hosted model, search, PageIndex, and evaluation examples

## Setup

Clone the repository and enter its directory:

```bash
git clone <repository-url>
cd langchain_proj
```

Create the environment and install the locked dependencies:

```bash
uv sync
```

Create a local environment file and add the required keys:

```bash
cp .env.example .env
```

The template includes keys for Groq, Hugging Face, Google, OpenRouter, Tavily, and PageIndex. Only configure the keys required by the example you are running. Keep `.env` private.

## Running the Examples

### Smoke test

```bash
uv run python main.py
```

### Notebooks

Open the repository in VS Code, enable the Jupyter extension, and select the project environment as the notebook kernel. Then open and run the notebook for the topic you want to explore.

For the smoothest experience, run the notebooks in numbered order. Notebooks that call hosted models or external services require the relevant API key in `.env`.

### RAG example

The vector RAG application uses documents under `04_vector_rag/data/` and the FAISS index under `04_vector_rag/faiss_index/`:

```bash
cd 04_vector_rag
uv run python app.py
```

### MCP example

The MCP client connects to the local math server and the weather server. Start the weather server in one terminal:

```bash
cd 07_mcp_integrations
uv run python weather.py
```

Then run the client from another terminal:

```bash
cd 07_mcp_integrations
uv run python client.py
```

### Vectorless RAG example

Open `05_vectorless_rag/01_pageindex_vectorless_rag.ipynb` after adding `PAGEINDEX_API_KEY` and `GROQ_API_KEY` to `.env`. The notebook uploads a PDF to PageIndex, waits for the tree index, asks Groq to select relevant nodes, and asks Groq to answer from those nodes. It is an API-backed demonstration rather than an offline example.

## Environment Variables

Copy `.env.example` to `.env` and configure only the credentials required for the topic you are studying:

- `GROQ_API_KEY`: Groq chat models used by many notebooks.
- `PAGEINDEX_API_KEY`: PageIndex indexing and tree retrieval.
- `TAVILY_API_KEY`: Web search tools used in graph and agent examples.
- `HF_TOKEN`: Hugging Face model access used by embedding and evaluation examples.
- `GOOGLE_API_KEY` and `OPENROUTER_API_KEY`: Provider-specific model examples.
- `LANGSMITH_API_KEY`: Tracing and evaluation workflows.

Never commit `.env` or print credential values in notebook output.

## Working Conventions

- Use `uv sync` from the repository root to create or update the project environment.
- Run scripts from the directory shown in their command because some examples use relative paths.
- Keep generated indexes, caches, notebook outputs, and local vector-store data out of commits unless they are intentionally part of an example.
- Model calls may incur provider usage limits or costs.
- The weather server returns a placeholder response and is intended for MCP demonstration purposes.
- Some notebooks contain commented-out cells for optional calls. Enable them only after the required credentials and external services are available.

## Notes

- The examples favor small, readable demonstrations over production application scaffolding.
- For implementation details specific to vectorless RAG, see `05_vectorless_rag/README.md`.