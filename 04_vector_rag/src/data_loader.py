from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader

def load_all_documents(data_dir: str) -> List[Any]:
    """
    Load all documents from the specified directory.

    Args:
        data_dir (str): The path to the directory containing the documents."""

    data_path = Path(data_dir).resolve()
    print(f"[DEBUG] Loading documents from: {data_path}")

    documents = []

    # PDF files
    pdf_files = list(data_path.glob("**/*.pdf"))
    print(f"[DEBUG] Found {len(pdf_files)} PDF files.")
    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded_docs = loader.load()
            documents.extend(loader.load())
            print(f"[DEBUG] Loaded {len(loaded_docs)} documents from {pdf_file}.")
        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}: {e}")

    # Text files
    text_files = list(data_path.glob("**/*.txt"))
    print(f"[DEBUG] Found {len(text_files)} text files.")
    for text_file in text_files:
        try:
            loader = TextLoader(str(text_file))
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"[DEBUG] Loaded {len(loaded_docs)} documents from {text_file}.")
        except Exception as e:
            print(f"[ERROR] Failed to load text file {text_file}: {e}")

    # CSV files
    csv_files = list(data_path.glob("**/*.csv"))
    print(f"[DEBUG] Found {len(csv_files)} CSV files.")
    for csv_file in csv_files:
        try:
            loader = CSVLoader(str(csv_file))
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"[DEBUG] Loaded {len(loaded_docs)} documents from {csv_file}.")
        except Exception as e:
            print(f"[ERROR] Failed to load CSV file {csv_file}: {e}")

    # DOCX files
    docx_files = list(data_path.glob("**/*.docx"))
    print(f"[DEBUG] Found {len(docx_files)} DOCX files.")
    for docx_file in docx_files:
        try:
            loader = Docx2txtLoader(str(docx_file))
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"[DEBUG] Loaded {len(loaded_docs)} documents from {docx_file}.")
        except Exception as e:
            print(f"[ERROR] Failed to load DOCX file {docx_file}: {e}")

    # Excel files
    excel_files = list(data_path.glob("**/*.xlsx"))
    print(f"[DEBUG] Found {len(excel_files)} Excel files.")
    for excel_file in excel_files:
        try:
            loader = UnstructuredExcelLoader(str(excel_file))
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"[DEBUG] Loaded {len(loaded_docs)} documents from {excel_file}.")
        except Exception as e:
            print(f"[ERROR] Failed to load Excel file {excel_file}: {e}")

    # JSON files
    json_files = list(data_path.glob("**/*.json"))
    print(f"[DEBUG] Found {len(json_files)} JSON files.")
    for json_file in json_files:
        try:
            loader = JSONLoader(str(json_file))
            loaded_docs = loader.load()
            documents.extend(loaded_docs)
            print(f"[DEBUG] Loaded {len(loaded_docs)} documents from {json_file}.")
        except Exception as e:
            print(f"[ERROR] Failed to load JSON file {json_file}: {e}")

    print(f"[DEBUG] Total documents loaded: {len(documents)}")
    return documents

    