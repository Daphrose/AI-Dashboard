import sys
from pathlib import Path

RAG_DIR = Path(__file__).resolve().parent
SRC_DIR = RAG_DIR.parent

sys.path.append(str(SRC_DIR))

from retriever import retrieve
from llm.llm_client import generate_response


def build_context(query, top_k=3):

    results = retrieve(query, top_k=top_k)

    contexts = []

    for i, document in enumerate(results["documents"][0]):

        source = results["metadatas"][0][i]["source"]

        contexts.append(
            f"Source: {source}\n"
            f"{document}"
        )

    return "\n\n".join(contexts)


def build_prompt(query, context):

    prompt = f"""
You are a helpful AI assistant for a supermarket sales analytics system.

Use the provided context to answer the user's question.

Do not invent information that is not supported by the context.

Context:
{context}

User question:
{query}

Answer:
"""

    return prompt


if __name__ == "__main__":

    question = input("Ask a question: ")

    context = build_context(question)

    prompt = build_prompt(question, context)

    print("\n" + "=" * 60)
    print("RETRIEVED CONTEXT")
    print("=" * 60)

    print(context)

    print("\n" + "=" * 60)
    print("PROMPT THAT WILL BE SENT TO THE LLM")
    print("=" * 60)

    print(prompt)

    answer = generate_response(prompt)

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(answer)