import sys
from pathlib import Path
import json
import re

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from llm.llm_client import generate_response
from sql.database_schema import build_schema_description


def clean_json_response(response):

    response = response.strip()

    # Remove markdown code fences
    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"\s*```$",
        "",
        response
    )

    response = response.strip()

    # If the model added text before/after the JSON,
    # extract the JSON object.
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and end > start:

        response = response[start:end + 1]

    return response.strip()


def parse_plan(response):

    cleaned_response = clean_json_response(response)

    try:
        return json.loads(cleaned_response)

    except json.JSONDecodeError:
        return None


def create_analysis_plan(question):

    schema = build_schema_description()

    prompt = f"""
You are an AI Data Analyst planning an analysis for a
supermarket sales database.

Your job is to determine what SQL queries are needed to answer
the user's question.

DATABASE TABLE:

dbo.SupermarketSales

DATABASE SCHEMA:

{schema}

USER QUESTION:

{question}

RULES:

1. Only use dbo.SupermarketSales.
2. Only generate SELECT statements.
3. Use only columns that exist in the schema.
4. Use Revenue for revenue analysis.
5. Use Profit for profit analysis.
6. Use COGS for COGS analysis.
7. Use Quantity for quantity analysis.
8. Use SUM() for totals.
9. Use appropriate GROUP BY clauses for comparisons.
10. If profit margin is required, calculate:

SUM(Profit) / NULLIF(SUM(Revenue), 0) * 100

11. Create multiple queries when the question requires
multiple independent pieces of analysis.
12. Do not generate unnecessary queries.
13. Do not answer the question yourself.
14. Return ONLY valid JSON.
15. Do not use markdown code fences.
16. Do not include any explanation outside the JSON.
17. Use double quotes for all JSON keys and string values.

The JSON must have exactly this structure:

{{
    "analysis_type": "single" or "multi_step",
    "reason": "short explanation of what needs to be analyzed",
    "queries": [
        {{
            "name": "short descriptive name",
            "sql": "SQL SELECT statement"
        }}
    ]
}}

Example:

{{
    "analysis_type": "multi_step",
    "reason": "The question requires revenue, profit, and profit margin analysis.",
    "queries": [
        {{
            "name": "Total Revenue",
            "sql": "SELECT SUM(Revenue) AS TotalRevenue FROM dbo.SupermarketSales"
        }},
        {{
            "name": "Total Profit",
            "sql": "SELECT SUM(Profit) AS TotalProfit FROM dbo.SupermarketSales"
        }},
        {{
            "name": "Profit Margin",
            "sql": "SELECT SUM(Profit) / NULLIF(SUM(Revenue), 0) * 100 AS ProfitMargin FROM dbo.SupermarketSales"
        }}
    ]
}}

USER QUESTION:
{question}

RETURN ONLY JSON:
"""

    response = generate_response(prompt)

    plan = parse_plan(response)

    # If the first response is not valid JSON,
    # ask the LLM to repair its own output.
    if plan is None:

        repair_prompt = f"""
You are a JSON repair assistant.

Convert the following AI analysis plan into VALID JSON.

IMPORTANT:

- Return ONLY JSON.
- Do not use markdown.
- Do not add explanations.
- Use double quotes for all keys and string values.
- Preserve the original meaning.
- The JSON must contain:
  analysis_type
  reason
  queries
- Each query must contain:
  name
  sql

INVALID RESPONSE:

{response}

RETURN ONLY THE CORRECTED JSON:
"""

        repaired_response = generate_response(
            repair_prompt
        )

        plan = parse_plan(repaired_response)

    if plan is None:
        return None, "The analysis planner returned invalid JSON."

    if not isinstance(plan, dict):
        return None, "Analysis plan must be a JSON object."

    if "analysis_type" not in plan:
        return None, "Analysis plan is missing analysis_type."

    if "queries" not in plan:
        return None, "Analysis plan is missing queries."

    if not isinstance(plan["queries"], list):
        return None, "Analysis queries must be a list."

    if not plan["queries"]:
        return None, "Analysis plan contains no queries."

    # Validate each query structure
    for query in plan["queries"]:

        if not isinstance(query, dict):
            return None, "An analysis query is not a valid object."

        if "name" not in query:
            return None, "An analysis query is missing its name."

        if "sql" not in query:
            return None, "An analysis query is missing SQL."

    return plan, "Analysis plan created successfully."


if __name__ == "__main__":

    question = input(
        "\nEnter a complex analytical question: "
    )

    plan, message = create_analysis_plan(question)

    print("\n" + "=" * 60)
    print("ANALYSIS PLANNER")
    print("=" * 60)

    print(message)

    if plan:

        print("\nAnalysis type:")
        print(plan["analysis_type"])

        print("\nReason:")
        print(plan["reason"])

        print("\nQueries:")

        for i, query in enumerate(plan["queries"], 1):

            print(f"\nQuery {i}:")
            print(f"Name: {query['name']}")
            print(query["sql"])