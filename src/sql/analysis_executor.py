import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(SRC_DIR))

from sql.sql_validator import validate_sql
from sql.query_database import run_query


def execute_analysis_plan(plan):
    """
    Execute all SQL queries contained in an analysis plan.

    Each query is validated before execution.
    The function returns the results of every analysis step.
    """

    if not plan:
        return [], "Analysis plan is empty."

    if "queries" not in plan:
        return [], "Analysis plan does not contain any queries."

    queries = plan["queries"]

    if not isinstance(queries, list):
        return [], "Analysis queries must be a list."

    execution_results = []

    for query in queries:

        name = query.get("name", "Unnamed Analysis")
        sql = query.get("sql")

        print("\n" + "-" * 60)
        print(f"ANALYSIS: {name}")
        print("-" * 60)

        if not sql:
            execution_results.append({
                "name": name,
                "success": False,
                "error": "No SQL query was provided."
            })

            print("Error: No SQL query was provided.")
            continue

        print("\nSQL:")
        print(sql)

        print("\nValidating SQL...")

        valid, message = validate_sql(sql)

        print(message)

        if not valid:

            execution_results.append({
                "name": name,
                "success": False,
                "error": message
            })

            print("Query was not executed.")
            continue

        print("\nExecuting SQL...")

        columns, rows = run_query(sql)

        if columns is None:

            execution_results.append({
                "name": name,
                "success": False,
                "error": "SQL query execution failed."
            })

            print("Execution failed.")
            continue

        if not rows:

            execution_results.append({
                "name": name,
                "success": True,
                "columns": columns,
                "rows": []
            })

            print("Query executed successfully, but returned no rows.")
            continue

        execution_results.append({
            "name": name,
            "success": True,
            "columns": columns,
            "rows": rows
        })

        print("\nResults:")

        for row in rows:
            print(row)

    return execution_results, "Analysis plan executed successfully."


if __name__ == "__main__":

    from analysis_planner import create_analysis_plan

    question = input(
        "\nEnter an analytical question: "
    )

    print("\n" + "=" * 60)
    print("CREATING ANALYSIS PLAN")
    print("=" * 60)

    plan, message = create_analysis_plan(question)

    print(message)

    if not plan:
        print("\nCould not create an analysis plan.")
        sys.exit()

    print("\nAnalysis type:")
    print(plan["analysis_type"])

    print("\nReason:")
    print(plan["reason"])

    print("\nPlanned queries:")

    for i, query in enumerate(plan["queries"], 1):

        print(f"\nQuery {i}:")
        print(f"Name: {query['name']}")
        print(query["sql"])

    print("\n" + "=" * 60)
    print("EXECUTING ANALYSIS PLAN")
    print("=" * 60)

    results, execution_message = execute_analysis_plan(plan)

    print("\n" + "=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)

    print(execution_message)

    for result in results:

        print("\nAnalysis:", result["name"])
        print("Success:", result["success"])

        if result["success"]:

            print("Columns:", result.get("columns"))
            print("Rows:", result.get("rows"))

        else:

            print("Error:", result.get("error"))