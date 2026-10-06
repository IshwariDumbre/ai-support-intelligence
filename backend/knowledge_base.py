from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"


def load_knowledge_base():
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    return chunks