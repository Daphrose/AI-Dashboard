import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from llm.llm_client import generate_response


def generate_answer(question, columns, rows):

    # Convert SQL results into a simple readable format
    results = []

    for row in rows:
        result = {}

        for column, value in zip(columns, row):
            result[column] = value

        results.append(result)

    prompt = f"""
You are a helpful AI Data Analyst for a supermarket sales analytics system.

The user asked this business question:

{question}

SQL Server executed the required query and returned these verified results:

{results}

Your job is to explain the results clearly in natural language.

Rules:

1. Use ONLY the provided SQL results.
2. Do not invent numbers or facts.
3. Do not perform a different calculation from the provided results.
4. Answer the user's question directly.
5. Use appropriate business terminology.
6. Keep the answer concise and easy to understand.
7. If the result contains money, format it clearly.
8. Do not mention SQL, Python, databases, prompts, or internal system details
   unless the user specifically asks about them.

Answer:
"""

    return generate_response(prompt)


if __name__ == "__main__":

    question = "Which product generated the most revenue?"

    columns = ["Product", "TotalRevenue"]

    rows = [
        ("Laptop", 85115250.0)
    ]

    answer = generate_answer(question, columns, rows)

    print("\nAI Answer:")
    print(answer)