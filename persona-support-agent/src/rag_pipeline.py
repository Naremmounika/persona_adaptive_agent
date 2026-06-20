import os
import chromadb

# Create persistent database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="support_kb"
)

def add_document(doc_name, content):

    collection.add(
        ids=[doc_name],
        documents=[content]
    )

def search_documents(query):

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results

if __name__ == "__main__":

    files = [
        "data/api_troubleshooting.md",
        "data/billing_policy.txt",
        "data/password_reset_guide.txt"
    ]

    for file_path in files:

        with open(file_path, "r", encoding="utf-8") as f:

            content = f.read()

            try:
                add_document(
                    os.path.basename(file_path),
                    content
                )
            except:
                pass

    print("Documents Added Successfully!")

    query = "How do I reset my password?"

    results = search_documents(query)

    print("\nRESULTS:")
    print(results)