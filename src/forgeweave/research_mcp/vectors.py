"""Vector embeddings and semantic search — ChromaDB with built-in ONNX embeddings.

Skill used: vector-embeddings
Pattern: ChromaDB PersistentClient for storage, default embedding function (all-MiniLM-L6-v2 via ONNX),
         cosine similarity, metadata filtering with $operators
"""

import hashlib
from pathlib import Path

import chromadb

HERE = Path(__file__).resolve().parent.parent
CHROMA_DIR = str(HERE / "chroma_db")
COLLECTION_NAME = "research_docs"


_client: chromadb.PersistentClient | None = None
_collection: chromadb.Collection | None = None


def get_collection() -> chromadb.Collection:
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
    if _collection is None:
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def make_doc_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def index_document(url: str, title: str, text: str, source: str, date: str = "") -> None:
    collection = get_collection()
    doc_id = make_doc_id(url)
    collection.upsert(
        ids=[doc_id],
        documents=[text],
        metadatas=[
            {"url": url, "title": title, "source": source, "date": date, "doc_type": "article"}
        ],
    )


def index_documents(
    ids: list[str],
    documents: list[str],
    metadatas: list[dict] | None = None,
) -> None:
    collection = get_collection()
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)


def search_documents(query: str, n_results: int = 5, where: dict | None = None) -> list[dict]:
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where,
    )
    output = []
    if results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            output.append(
                {
                    "doc_id": doc_id,
                    "text": results["documents"][0][i] if results.get("documents") else "",
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                    "distance": results["distances"][0][i] if results.get("distances") else None,
                }
            )
    return output


def delete_documents(ids: list[str]) -> None:
    collection = get_collection()
    collection.delete(ids=ids)


def collection_stats() -> dict:
    collection = get_collection()
    return {"name": collection.name, "count": collection.count()}


def warmup() -> None:
    col = get_collection()
    col.query(query_texts=["warmup"], n_results=1)
