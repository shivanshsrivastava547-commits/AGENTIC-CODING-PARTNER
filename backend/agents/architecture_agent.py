from agents.rag_agent import rag_chat

def architecture_chat(query):
    prompt = f"""
You are a Staff Software Architect.

Analyze the indexed repository.

Tasks:
1. Identify major folders.
2. Identify entry points.
3. Explain request flow.
4. Explain backend architecture.
5. Explain frontend architecture.
6. Mention important files.
7. Produce an architecture summary.

USER REQUEST:
{query}
"""

    return rag_chat(prompt)