import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq

load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_index", embedding_model: str = "all-MiniLM-L6-v2"):
        self.vector_store = FaissVectorStore(persist_dir, embedding_model)
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("../data")
            self.vector_store.build_from_documents(docs)
        else:
            self.vector_store.load()
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(api_key=groq_api_key, model_name="openai/gpt-oss-120b")
        print(f"[INFO] Initialized RAGSearch with embedding model: {embedding_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vector_store.query(query, top_k)
        texts = [res['metadata'].get('text', '') for res in results if res['metadata'] is not None]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"Context:\n{context}\n\nQuestion: {query}\n"
        response = self.llm.invoke([prompt])
        return response.content