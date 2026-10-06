from pathlib import Path

import chromadb

from backend.knowledge_base import load_knowledge_base


CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="support_knowledge"
)


def build_vector_store():
    documents = load_knowledge_base()

    existing = collection.get()

    if existing["ids"]:
        collection.delete(
            ids=existing["ids"]
        )

    for index, document in enumerate(documents):
        collection.add(
            ids=[f"doc_{index}"],
            documents=[document.page_content],
            metadatas=[{
                "source": document.metadata.get("source", "unknown")
            }]
        )

    return len(documents)


def search_knowledge(query, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return results["documents"][0]