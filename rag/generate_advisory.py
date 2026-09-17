"""
PHASE 6 — RAG Advisory Generation (+ Experiment 2 comparison mode)
=====================================================================
UPDATED VERSION: uses Ollama (free, runs on your own computer) instead of a
paid API. Requires Ollama installed and a model pulled first:
    ollama pull llama3

Given a farmer's question, retrieves relevant chunks from the knowledge base
and asks the LLM to answer USING ONLY those chunks. Also supports --no-rag
so you can run Experiment 2: compare the same question answered with vs.
without retrieval.

Run (with RAG):
    python rag/generate_advisory.py --question "What should I do about aphids on tomato in rainy season?"

Run (without RAG, for comparison):
    python rag/generate_advisory.py --question "What should I do about aphids on tomato in rainy season?" --no-rag
"""

import argparse
import requests
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = "rag/chroma_store"
TOP_K = 4  # number of chunks to retrieve
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


def retrieve_chunks(question: str, top_k: int = TOP_K):
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_collection(name="pest_advisory_docs", embedding_function=embed_fn)
    results = collection.query(query_texts=[question], n_results=top_k)
    return results["documents"][0], results["metadatas"][0]


def ask_llm(prompt: str) -> str:
    """Calls your local Ollama server. Make sure Ollama is running (it starts
    automatically after installation, or run 'ollama serve' manually)."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=300,
    )
    response.raise_for_status()
    return response.json()["response"]


def generate_with_rag(question: str) -> str:
    chunks, metadatas = retrieve_chunks(question)
    context = "\n\n---\n\n".join(
        f"[Source: {m['source']}]\n{c}" for c, m in zip(chunks, metadatas)
    )
    prompt = f"""You are an agricultural advisory assistant. Answer the farmer's
question using ONLY the information in the CONTEXT below. If the context doesn't
cover the question, say so honestly instead of guessing.

CONTEXT:
{context}

FARMER'S QUESTION: {question}

Give a clear, plain-language, actionable answer."""
    return ask_llm(prompt)


def generate_without_rag(question: str) -> str:
    prompt = f"""You are an agricultural advisory assistant. Answer the farmer's
question directly using your own knowledge.

FARMER'S QUESTION: {question}

Give a clear, plain-language, actionable answer."""
    return ask_llm(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--no-rag", action="store_true", help="Skip retrieval, use plain LLM (for Experiment 2 comparison)")
    args = parser.parse_args()

    if args.no_rag:
        print("\n=== PLAIN LLM (no retrieval) ===")
        print(generate_without_rag(args.question))
    else:
        print("\n=== RAG-GROUNDED ANSWER ===")
        print(generate_with_rag(args.question))
