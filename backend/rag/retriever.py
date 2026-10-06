import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "repo_index"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def retrieve_context(query):
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model,
        collection_name=COLLECTION_NAME
    )

    print("Current Chroma count:", vectorstore._collection.count())

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 40
        }
    )

    enhanced_query = query

    if "architecture" in query.lower() or "structure" in query.lower():
        enhanced_query = """
        project architecture folder structure main entry file routes controllers services agents graph workflow backend frontend app
        """

    docs = retriever.invoke(enhanced_query)

    print("\n===== RETRIEVED FILES =====")
    for doc in docs[:10]:
        print("FILE:", doc.metadata.get("source"))
        print(doc.page_content[:200])
        print("=" * 50)

    return docs