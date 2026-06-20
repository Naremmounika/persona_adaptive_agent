import os
from dotenv import load_dotenv
from google import genai
import chromadb
from src.classifier import classify_persona
from src.generator import generate_response

load_dotenv()

# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_collection(
    name="support_kb"
)


def retrieve_context(query):

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    docs = results["documents"][0]

    context = "\n\n".join(docs)

    return context


def check_escalation(user_message):

    sensitive_words = [
        "refund",
        "billing",
        "legal",
        "lawsuit",
        "chargeback"
    ]

    user_lower = user_message.lower()

    for word in sensitive_words:

        if word in user_lower:
            return True

    return False


def main():

    print("\n===== Persona Support Agent =====\n")

    while True:

        user_message = input("User: ")

        if user_message.lower() == "exit":
            break

        # Escalation Check
        if check_escalation(user_message):

            print("\nESCALATION REQUIRED\n")

            print({
                "issue": user_message,
                "recommended_action": "Human Support Review"
            })

            continue

        # Persona Classification
        persona_result = classify_persona(user_message)

        persona = persona_result["persona"]

        print(f"\nDetected Persona: {persona}")

        # Retrieve Context
        context = retrieve_context(user_message)

        # Generate Response
        answer = generate_response(
            user_message,
            persona,
            context
        )

        print("\nAgent:")
        print(answer)
        print()


if __name__ == "__main__":
    main()