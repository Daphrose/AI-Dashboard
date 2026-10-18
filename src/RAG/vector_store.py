import chromadb

from embeddings import create_embeddings


# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path="vector_db")


# Create or load our collection
collection = client.get_or_create_collection(
    name="supermarket_knowledge"
)


def store_embeddings():
    chunks, embeddings = create_embeddings()

    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk["content"])

        metadatas.append({
            "source": chunk["source"]
        })

        ids.append(f"chunk_{i}")

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


if __name__ == "__main__":
    store_embeddings()

    print(f"Collection contains {collection.count()} documents.")