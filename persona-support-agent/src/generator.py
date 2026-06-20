import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_response(user_query, persona, context):

    if persona == "Technical Expert":

        instruction = """
You are a Senior Technical Support Engineer.

Provide:
- Detailed explanations
- Technical terminology
- Step-by-step troubleshooting

Use the provided context only.
"""

    elif persona == "Frustrated User":

        instruction = """
You are an empathetic support specialist.

Start by acknowledging the frustration.

Then provide:
- Simple steps
- Clear instructions
- No technical jargon

Use the provided context only.
"""

    else:

        instruction = """
You are a Business Executive Support Agent.

Provide:
- Short answers
- Business impact
- Resolution timelines

Use the provided context only.
"""

    prompt = f"""
{instruction}

CONTEXT:
{context}

USER QUESTION:
{user_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    persona = "Frustrated User"

    context = """
Password Reset Guide

1. Click Forgot Password.
2. Enter registered email.
3. Open email link.
4. Create new password.
"""

    question = "I can't log in and nothing works!"

    answer = generate_response(
        question,
        persona,
        context
    )

    print(answer)