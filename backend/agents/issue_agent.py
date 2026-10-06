from agents.rag_agent import rag_chat

def issue_chat(query):
    prompt = f"""
You are a senior open-source maintainer.

Analyze the reported issue using the indexed repository.

Tasks:
1. Find likely files involved.
2. Explain root cause.
3. Suggest fix.
4. Generate code patch.
5. Generate test cases.

ISSUE:
{query}
"""

    return rag_chat(prompt)