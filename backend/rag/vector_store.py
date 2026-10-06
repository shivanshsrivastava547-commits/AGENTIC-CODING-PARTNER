import os
import shutil

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "repo_index"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def create_vector_store(documents):
    print("Files received for indexing:", len(documents))

    docs = []

    for doc in documents:
        chunks = text_splitter.split_text(doc["content"])

        for chunk in chunks:
            if chunk.strip():
                docs.append(
                    Document(
                        page_content=chunk,
                        metadata=doc["metadata"]
                    )
                )

    print("Total chunks created:", len(docs))

    if len(docs) == 0:
        print("No chunks created. Skipping ChromaDB save.")
        return None

    # Hard reset old Chroma DB
    if os.path.exists(CHROMA_PATH):
        print("Deleting old ChromaDB:", CHROMA_PATH)
        shutil.rmtree(CHROMA_PATH, ignore_errors=True)

    os.makedirs(CHROMA_PATH, exist_ok=True)

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model,
        collection_name=COLLECTION_NAME
    )

    # Extra safety: delete old collection data if it exists
    try:
        vectorstore.delete_collection()
        print("Old collection deleted")
    except Exception:
        pass

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME
    )

    print("Saved to ChromaDB successfully")
    print("Chroma count:", vectorstore._collection.count())

    return vectorstore