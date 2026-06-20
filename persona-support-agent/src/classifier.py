import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_persona(user_message):
    prompt = f"""
You are a customer persona classifier.

Classify the user into EXACTLY one category:

1. Technical Expert
2. Frustrated User
3. Business Executive

Return ONLY valid JSON.

Example:

{{
    "persona": "Technical Expert",
    "confidence": 0.95,
    "reasoning": "User discusses API authentication."
}}

User Message:
{user_message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Get response text
    clean_text = response.text.strip()

    # Remove markdown code blocks if Gemini adds them
    if clean_text.startswith("```json"):
        clean_text = clean_text.replace("```json", "", 1)

    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]

    clean_text = clean_text.strip()

    try:
        return json.loads(clean_text)

    except Exception as e:
        print("Error parsing JSON:")
        print(e)

        print("\nGemini returned:")
        print(clean_text)

        return {
            "persona": "Unknown",
            "confidence": 0,
            "reasoning": "JSON parsing failed"
        }


if __name__ == "__main__":

    test_message = "What is the timeline for resolving billing disputes?"

    result = classify_persona(test_message)

    print("\nRESULT:")
    print(json.dumps(result, indent=4))