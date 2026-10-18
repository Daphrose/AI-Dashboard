import chromadb

from sentence_transformers import SentenceTransformer


# Load the same embedding model used when storing the chunks
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to the existing ChromaDB
client = chromadb.PersistentClient(path="vector_db")

collection = client.get_collection(
    name="supermarket_knowledge"
)


def retrieve(query, top_k=3):
    # Convert the user's question into an embedding
    query_embedding = model.encode([query]).tolist()

    # Search ChromaDB for the most similar chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = input("Ask a question: ")

    results = retrieve(question)

    print("\nRetrieved knowledge:\n")

    for i, document in enumerate(results["documents"][0], 1):

        source = results["metadatas"][0][i - 1]["source"]

        print("=" * 60)
        print(f"Result {i}")
        print(f"Source: {source}")
        print("=" * 60)
        print(document)
        print()