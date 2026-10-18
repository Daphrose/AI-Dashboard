import sys
from pathlib import Path

# Add src to Python's module search path
SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from llm.llm_client import generate_response
from sql.database_schema import build_schema_description


def generate_sql(question):

    schema = build_schema_description()

    prompt = f"""
You are an SQL query generator for a supermarket sales analytics system.

Your job is to convert the user's natural-language question into
a SQL Server query.

DATABASE:
supermarketAI

TABLE:
dbo.SupermarketSales

DATABASE SCHEMA:
{schema}

RULES:

1. Generate SQL Server compatible SQL.
2. Only generate SELECT statements.
3. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
   CREATE, or other data-modifying statements.
4. Use only columns that exist in the provided schema.
5. Use dbo.SupermarketSales as the table.
6. For revenue questions, use the Revenue column.
7. For profit questions, use the Profit column.
8. For COGS questions, use the COGS column.
9. For quantity questions, use the Quantity column.
10. When the question asks for a total, use SUM().
11. When the question asks for the highest or lowest value,
    use appropriate GROUP BY and ORDER BY logic.
12. Return ONLY the SQL query.
13. Do not include markdown code fences.
14. Do not explain the query.

USER QUESTION:
{question}

SQL QUERY:
"""

    sql = generate_response(prompt)

    return sql.strip()


if __name__ == "__main__":

    question = input("Ask an analytical question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)