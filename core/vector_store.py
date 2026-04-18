from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import os

CHROMA_DIR = "storage/chroma_db"


def get_db():
    # Ensure directory exists
    os.makedirs(CHROMA_DIR, exist_ok=True)

    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # Create / Load Chroma DB
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    return db