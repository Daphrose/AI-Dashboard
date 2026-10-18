from pathlib import Path

# Locate the knowledge folder
BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents.\n")

    for document in documents:
        print("=" * 60)
        print(f"Source: {document['source']}")
        print("=" * 60)
        print(document["content"][:500])
        print()