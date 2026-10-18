import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from sql.sql_generator import generate_sql
from sql.sql_validator import validate_sql
from sql.query_database import run_query
from sql.answer_generator import generate_answer


def answer_question(question):

    print("\nGenerating SQL...\n")

    sql = generate_sql(question)

    print("Generated SQL:")
    print(sql)

    print("\nValidating SQL...\n")

    valid, message = validate_sql(sql)

    print(message)

    if not valid:
        return None

    print("\nExecuting SQL...\n")

    columns, rows = run_query(sql)

    print("Columns:")
    print(columns)

    print("\nResults:")
    for row in rows:
        print(row)

    print("\nGenerating AI answer...\n")

    answer = generate_answer(
        question,
        columns,
        rows
    )

    return answer


if __name__ == "__main__":

    question = input("Ask an analytical question: ")

    answer = answer_question(question)

    if answer is not None:

        print("\n" + "=" * 60)
        print("FINAL AI ANSWER")
        print("=" * 60)

        print(answer)