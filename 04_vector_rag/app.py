from src.data_loader import load_all_documents
from src.embedding import EmbeddingPipeline
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

if __name__ == "__main__":
    # # loaded_documents = load_all_documents("./data")
    # store = FaissVectorStore()
    # # store.build_from_documents(loaded_documents)
    # store.load()
    # query_text = "Tell me about holocaust"
    # context = store.query(query_text)
    
    rag = RAGSearch()

    query = "Tell me about the holocaust in 120 words"
    response = rag.search_and_summarize(query)
    
    print(response)
