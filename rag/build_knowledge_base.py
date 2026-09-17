"""
PHASE 5 — Build the RAG Knowledge Base
=========================================
Takes real government pest-management PDFs (NIPHM IPM packages, ICAR
advisories — see docs/data_sources.md) and stores them in a local vector
database (ChromaDB) so your LLM can retrieve relevant chunks later.

Setup: put your downloaded PDFs in rag/source_pdfs/ first.

Run:
    python rag/build_knowledge_base.py
"""

import os
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions

SOURCE_DIR = "rag/source_pdfs"
CHROMA_DIR = "rag/chroma_store"
CHUNK_SIZE = 800   # characters per chunk
CHUNK_OVERLAP = 150


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]


def build_knowledge_base():
    if not os.path.isdir(SOURCE_DIR) or not os.listdir(SOURCE_DIR):
        print(f"No PDFs found in {SOURCE_DIR}/. Download some first — see docs/data_sources.md")
        return

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(
        name="pest_advisory_docs", embedding_function=embed_fn
    )

    doc_id = 0
    for filename in os.listdir(SOURCE_DIR):
        if not filename.lower().endswith(".pdf"):
            continue
        path = os.path.join(SOURCE_DIR, filename)
        print(f"Processing {filename}...")
        text = extract_text(path)
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        collection.add(
            documents=chunks,
            ids=[f"{filename}_{i}" for i in range(len(chunks))],
            metadatas=[{"source": filename} for _ in chunks],
        )
        doc_id += len(chunks)
        print(f"  -> added {len(chunks)} chunks")

    print(f"\nDone. {doc_id} total chunks stored in {CHROMA_DIR}/")


if __name__ == "__main__":
    build_knowledge_base()
