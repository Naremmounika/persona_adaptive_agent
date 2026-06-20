import os
from dotenv import load_dotenv
import chromadb

from src.classifier import classify_persona
from src.generator import generate_response

import streamlit as st

load_dotenv()

st.set_page_config(page_title="Persona Support Agent")

st.title("Persona-Adaptive Customer Support Agent")

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="support_kb")


def retrieve_context(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return "\n\n".join(results["documents"][0])


def check_escalation(user_message):
    sensitive_words = [
        "refund",
        "billing",
        "chargeback",
        "lawsuit",
        "legal"
    ]

    return any(word in user_message.lower() for word in sensitive_words)


user_message = st.text_area("Enter your support request")

if st.button("Submit"):

    if not user_message.strip():
        st.warning("Please enter a message.")

    elif check_escalation(user_message):

        st.error("Escalation Required")

        st.json({
            "issue": user_message,
            "recommended_action": "Human Support Review"
        })

    else:

        persona_result = classify_persona(user_message)

        persona = persona_result["persona"]

        st.info(f"Detected Persona: {persona}")

        context = retrieve_context(user_message)

        answer = generate_response(
            user_message,
            persona,
            context
        )

        st.success("Agent Response")

        st.write(answer)