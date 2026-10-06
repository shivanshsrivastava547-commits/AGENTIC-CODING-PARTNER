from fastapi import APIRouter
from pydantic import BaseModel

from services.github_service import clone_repo
from rag.chunker import read_repo_files
from rag.vector_store import create_vector_store
from graph.workflow import run_graph

router = APIRouter()


class RepoRequest(BaseModel):
    repo_url: str


class ChatRequest(BaseModel):
    query: str


@router.post("/ingest")
def ingest_repo(data: RepoRequest):
    try:
        path = clone_repo(data.repo_url)

        documents = read_repo_files(path)

        print("Files found:", len(documents))

        vectorstore = create_vector_store(documents)

        if vectorstore is None:
            return {
                "success": False,
                "message": "No valid code files found to index",
                "total_files": len(documents)
            }

        return {
            "success": True,
            "message": "Repository indexed successfully",
            "total_files": len(documents),
            "chunks": vectorstore._collection.count()
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Repository indexing failed",
            "error": str(e)
        }


@router.post("/chat")
def chat(data: ChatRequest):
    try:
        result = run_graph(data.query)

        return {
            "success": True,
            "agent_used": result["agent_type"],
            "response": result["response"]
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Chat failed",
            "error": str(e)
        }