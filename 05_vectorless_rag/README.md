# Vectorless RAG with PageIndex

This folder demonstrates a vectorless retrieval-augmented generation (RAG) workflow using [PageIndex](https://pageindex.ai/) and a Groq-hosted language model.

The example uses a PDF about data communication and computer networks. Instead of converting document chunks into embedding vectors and searching by cosine similarity, PageIndex creates a hierarchical tree of document sections. An LLM then reasons over that tree to select the sections most likely to answer a question.

## What "vectorless" means

Traditional vector RAG usually follows this path:

```text
PDF -> text chunks -> embeddings -> vector database
question -> question embedding -> similarity search -> relevant chunks -> LLM answer
```

This notebook follows a different path:

```text
PDF -> PageIndex document tree
question + tree outline -> LLM selects node IDs
selected node text + question -> LLM generates an answer
```

The approach is called vectorless because retrieval does not depend on an embedding model, a vector database, or a nearest-neighbor search. The document structure acts like a table of contents, and the language model performs the relevance reasoning.

## Files

- `pageindex_vectorless_rag.ipynb`: The complete executable example.
- `files/data_communication_computer_network_tutorial.pdf`: The PDF submitted to PageIndex. The file must exist before the upload cell is run.

## Requirements and setup

The project uses Python 3.12+ and `uv`. From the repository root:

```bash
uv sync
cp .env.example .env
```

Set these values in `.env`:

```dotenv
PAGEINDEX_API_KEY=your_pageindex_key
GROQ_API_KEY=your_groq_key
```

The notebook also uses the `pageindex`, `langchain-groq`, and `python-dotenv` packages, which are already declared in the repository's `pyproject.toml`.

Open the notebook in VS Code and select the project's Python environment as its kernel.

## Notebook workflow

Run the cells from top to bottom. Each section has one responsibility.

### 1. Load configuration

The first code cell imports `os`, `json`, and `time`, loads `.env` with `load_dotenv()`, and reads `PAGEINDEX_API_KEY`. This keeps credentials outside the notebook source.

### 2. Create API clients

The next cell creates:

- `pi_client`: A `PageIndexClient` used to upload the PDF, check indexing status, and retrieve the document tree.
- `groq_client`: A `ChatGroq` client using the `qwen/qwen3.8-27b` model for tree selection and answer generation.

### 3. Upload the PDF

The `PDF_PATH` cell calls:

```python
upload_res = pi_client.submit_document(PDF_PATH)
doc_id = upload_res["doc_id"]
```

PageIndex processes the PDF asynchronously and returns a document ID. That ID identifies the remote PageIndex document.

### 4. Wait for indexing

The indexing cell repeatedly calls `pi_client.get_document(doc_id)` until the status is either `completed` or `failed`. The five-second delay prevents the notebook from polling continuously while PageIndex builds the tree.

### 5. Retrieve and inspect the tree

The notebook calls:

```python
tree_res = pi_client.get_tree(doc_id, node_summary=True)
pageindex_tree = tree_res.get("result", [])
```

`pageindex_tree` is a nested list of dictionaries. A node generally contains fields such as:

- `node_id`: The identifier used to select and find the node.
- `title`: The section title.
- `page_index`: The source page number.
- `text`: The section content or summary.
- `nodes`: Child sections, when the node has children.

Printing the first item lets you inspect the structure returned by PageIndex before retrieval begins.

### 6. Select relevant nodes with `llm_tree_search`

`llm_tree_search(query, tree)` performs the first LLM call. Its nested `compress` function creates a smaller representation of the tree containing each node's ID, title, page, and the first 150 characters of its text. Child nodes are compressed recursively.

The compressed tree is placed in a prompt that asks the model to return JSON in this shape:

```json
{
  "thinking": "why these sections are relevant",
  "node_list": ["node_id1", "node_id2"]
}
```

The function parses the model response with `json.loads()` and returns the resulting dictionary. This is the retrieval step: the model chooses locations in the document rather than searching a vector index.

### 7. Fetch the selected nodes

`find_node_by_id(tree, target_ids)` recursively walks the full tree. It returns the original node dictionaries whose `node_id` values appear in the model's `node_list`.

Using the original nodes is important because the compressed tree is only an outline. The original nodes contain the fuller text needed to answer the question.

### 8. Generate the answer

`generate_answer(query, nodes)` builds a context string from the selected nodes. Each section is labeled with its title and page number, then sent to Groq with the original question.

If no nodes were selected, it returns:

```text
No relevant nodes found to answer the query.
```

Otherwise, it returns the model's text response.

### 9. Orchestrate the complete workflow

`vectorless_rag(query, tree, verbose=True)` connects the pieces:

1. Ask `llm_tree_search` for relevant node IDs.
2. Print the model's reasoning and selected IDs when `verbose` is enabled.
3. Use `find_node_by_id` to recover the full nodes.
4. Use `generate_answer` to produce the final response.

The final cell asks about CSMA/CD and prints the generated answer.

## Example data flow

For the CSMA/CD question, the tree-search model may select nodes such as `0017` (Data Link Layer Introduction) and `0019` (Data Link Control and Protocols). The notebook then retrieves those nodes' text and gives only that context to the answer-generation model.

This separation is useful because the first model call decides *where* to look, while the second model call decides *how to explain* the selected content.

## Important notebook notes

- The upload cell creates a new PageIndex document ID, but the following indexing cell currently assigns a hard-coded `doc_id`. For a fresh run, use the ID returned by the upload cell instead of the old example ID.
- Indexing is remote and may take time. The notebook waits by polling PageIndex and therefore requires network access.
- Both retrieval and answer generation call Groq, so `GROQ_API_KEY` and network access are required.
- The example is not a local/offline RAG implementation. Although it avoids local vectors, it still uses PageIndex and Groq APIs.
- The notebook's `generate_answer` cell should use different quote styles for the nested `node.get` expression if the Python parser reports a syntax error. For example:

  ```python
  f"[Section: '{node['title']}' | Page: {node.get('page_index', '?')}]\n"
  ```

## Vector RAG versus this example

| Concern | Traditional vector RAG | This PageIndex example |
| --- | --- | --- |
| Representation | Embedding vectors for chunks | Hierarchical document tree |
| Retrieval | Similarity search | LLM reasoning over node summaries |
| Storage | Vector database or FAISS | PageIndex-hosted document index |
| Strength | Fast semantic lookup over large flat collections | Uses document hierarchy and section context |
| Trade-off | Requires embedding and index management | Uses extra LLM reasoning and API calls |

This example is intentionally educational: it exposes the retrieval decisions in small functions so the difference between vector-based and structure-based RAG is easy to follow.
