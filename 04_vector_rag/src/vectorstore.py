import os
import faiss
import numpy as np
import pickle
from typing import List, Any
from sentence_transformers import SentenceTransformer
from src.embedding import EmbeddingPipeline


class FaissVectorStore:
    def __init__(self, persist_dir: str = "faiss_index", embedding_model: str = "all-MiniLM-L6-v2",
                 chunk_size: int = 1000, chunk_overlap: int = 200):
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.index = None
        self.metadata = []
        self.embedding_model_name = embedding_model
        self.embedding_model = SentenceTransformer(
            embedding_model, device="cpu")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        print(
            f"[INFO] Initialized FaissVectorStore with model: {embedding_model}")

    def build_from_documents(self, documents: List[Any]):
        print(f"[INFO] Building FAISS index from {len(documents)} documents.")
        emb_pipeline = EmbeddingPipeline(
            model_name=self.embedding_model_name, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = emb_pipeline.chunk_documents(documents)
        embeddings = emb_pipeline.embed_chunks(chunks)
        metadatas = [{"text": chunk.page_content} for chunk in chunks]
        self.add_embeddings(np.array(embeddings).astype(np.float32), metadatas)
        self.save()
        print(f"[INFO] FAISS index built and saved to {self.persist_dir}.")

    def add_embeddings(self, embeddings: np.ndarray, metadatas: List[dict]):
        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
            print(f"[INFO] Created new FAISS index with dimension: {dim}")
        self.index.add(embeddings)
        if metadatas:
            self.metadata.extend(metadatas)
        print(
            f"[INFO] Added {embeddings.shape[0]} embeddings to the FAISS index.")

    def save(self):
        faiss_path = os.path.join(self.persist_dir, "faiss.index")
        meta_path = os.path.join(self.persist_dir, "metadata.pkl")
        faiss.write_index(self.index, faiss_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"[INFO] FAISS index and metadata saved to {self.persist_dir}.")

    def load(self):
        faiss_path = os.path.join(self.persist_dir, "faiss.index")
        meta_path = os.path.join(self.persist_dir, "metadata.pkl")
        if os.path.exists(faiss_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(faiss_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            print(
                f"[INFO] Loaded FAISS index and metadata from {self.persist_dir}.")
        else:
            print(
                f"[WARNING] FAISS index or metadata not found in {self.persist_dir}. Starting with an empty index.")

    def search(self, query_embeddings: np.ndarray, top_k: int = 5):
        D, I = self.index.search(query_embeddings, top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            meta = self.metadata[idx] if idx < len(self.metadata) else None
            results.append({"index": idx, "distance": dist, "metadata": meta})
        return results

    def query(self, query_text: str, top_k: int = 5):
        query_embedding = self.embedding_model.encode(
            [query_text]).astype("float32")
        results = self.search(query_embedding, top_k)
        return results
