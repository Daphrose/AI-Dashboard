from document_loader import load_documents


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks():
    documents = load_documents()

    all_chunks = []

    for document in documents:
        chunks = chunk_text(document["content"])

        for chunk in chunks:
            all_chunks.append({
                "source": document["source"],
                "content": chunk
            })

    return all_chunks


if __name__ == "__main__":
    chunks = create_chunks()

    print(f"Created {len(chunks)} chunks.\n")

    for i, chunk in enumerate(chunks[:5], 1):
        print("=" * 60)
        print(f"Chunk {i}")
        print(f"Source: {chunk['source']}")
        print("=" * 60)
        print(chunk["content"])
        print()