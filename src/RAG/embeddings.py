from sentence_transformers import SentenceTransformer
from chunker import create_chunks


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings():
    chunks = create_chunks()

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(texts)

    return chunks, embeddings


if __name__ == "__main__":
    chunks, embeddings = create_embeddings()

    print(f"Number of chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")

    print("\nFirst embedding:")
    print(embeddings[0])