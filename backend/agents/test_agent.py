from agents.rag_agent import rag_chat

def test_chat(query):
    prompt = f"""
You are a senior QA automation engineer.

Generate practical unit/integration tests using the indexed repository context.

Rules:
1. Mention the files being tested.
2. Suggest where the test file should be created.
3. Generate complete test code.
4. Use the project's existing language and framework if visible.
5. If test framework is unclear, suggest the best suitable one.

USER REQUEST:
{query}
"""

    return rag_chat(prompt)