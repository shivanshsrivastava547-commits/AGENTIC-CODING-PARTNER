from agents.rag_agent import rag_chat

def readme_chat(query):
    prompt = f"""
You are a technical documentation engineer.

Using the indexed repository context, generate a professional README.md.

Include:
1. Project title
2. Problem statement
3. Features
4. Tech stack
5. Architecture
6. Folder structure
7. Setup instructions
8. API endpoints if backend exists
9. Usage examples
10. Future improvements

USER REQUEST:
{query}
"""

    return rag_chat(prompt)