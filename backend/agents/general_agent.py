import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def general_chat(query):
    prompt = f"""
You are a helpful AI software engineering assistant.

Answer clearly and practically.
If the user asks coding/project guidance, give actionable steps.

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
        temperature=0.3
    )

    return response.choices[0].message.content