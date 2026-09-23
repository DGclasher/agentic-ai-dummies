# Agentic AI for Dummies

A hands-on collection of LangChain, LangGraph, RAG, MCP, guardrail, and deep-agent examples. The notebooks and small Python programs follow the material from [this course](https://www.youtube.com/watch?v=rV3HJ4LEZ7k&list=PLv9ppQ4ScBnWtMRCa2dk43izcnYTW11lX&index=1).

## Project Sections

- `langchains/`: Introductory LangChain examples, model integration, and tools.
- `langgraphs/`: Graph-based agents, including a basic chatbot and human-in-the-loop flow.
- `rag/`: Retrieval-augmented generation with document loading, embeddings, and a FAISS vector store.
- `vectorless_rag/`: A PageIndex-based RAG approach without a traditional vector store.
- `mcp/`: Model Context Protocol servers for math and weather tools, plus an MCP client.
- `deep_agents/`: Deep-agent architecture with planning, tools, and specialized agent behavior.
- `guardrails/`: Examples of adding guardrails to model interactions.
- `main.py`: Minimal project smoke test.
- `pyproject.toml`: Project metadata and Python dependencies.

## Requirements

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- API keys for the providers used by the example you want to run

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

The notebooks are grouped under `langchains/`, `langgraphs/`, `rag/notebooks/`, `deep_agents/`, `guardrails/`, and `vectorless_rag/`.

### RAG example

The RAG application uses documents under `rag/data/` and the FAISS index under `rag/faiss_index/`:

```bash
cd rag
uv run python app.py
```

### MCP example

The MCP client connects to the local math server and the weather server. Start the weather server in one terminal:

```bash
cd mcp
uv run python weather.py
```

Then run the client from another terminal:

```bash
cd mcp
uv run python client.py
```

## Notes

- Run commands from the directory shown in each example so relative paths resolve correctly.
- Model calls may incur provider usage limits or costs.
- The weather server returns a placeholder response and is intended for MCP demonstration purposes.