from agents.rag_agent import rag_chat

def pr_review_chat(query):
    prompt = f"""
You are a senior software engineer reviewing a pull request.

Use the indexed repository context and the user's provided code/diff.

Review for:
1. Bugs
2. Security issues
3. Performance issues
4. Code quality
5. Missing error handling
6. Missing tests
7. Better architecture choices

Return your answer in this format:

Summary:
- ...

Issues Found:
1. ...
2. ...

Suggested Fixes:
1. ...

Improved Code:
Only include code if needed.

USER REQUEST / DIFF:
{query}
"""

    return rag_chat(prompt)