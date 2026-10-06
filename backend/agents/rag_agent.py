import os
from dotenv import load_dotenv
from groq import Groq

from rag.retriever import retrieve_context

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def rag_chat(query):
    docs = retrieve_context(query)

    context = "\n\n".join([
    f"""
FILE: {doc.metadata.get("source", "unknown")}

CODE:
{doc.page_content}
"""
    for doc in docs
])

    prompt = f"""
You are an expert software engineering copilot.

You must answer using ONLY the indexed repository context below.

Rules:
1. Mention relevant file paths when possible.
2. Do not guess if context is insufficient.
3. If you are unsure, say exactly: "The indexed code context is insufficient."
4. Explain step-by-step based on actual code.
5. Do not give generic answers.

Do not explain package-lock.json, node_modules, dependency files, or lock files unless the user specifically asks about dependencies.

REPOSITORY CONTEXT:
{context}

USER QUESTION:
{query}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content