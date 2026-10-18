import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(SRC_DIR))

from sql.analysis_planner import create_analysis_plan
from sql.analysis_executor import execute_analysis_plan


def aggregate_results(execution_results):
    """
    Organize the results produced by the Analysis Executor
    into one structured analysis result.
    """

    aggregated_results = []

    for result in execution_results:

        analysis = {
            "name": result.get("name"),
            "success": result.get("success")
        }

        if result.get("success"):

            analysis["columns"] = result.get("columns", [])
            analysis["rows"] = result.get("rows", [])

        else:

            analysis["error"] = result.get(
                "error",
                "Unknown analysis error."
            )

        aggregated_results.append(analysis)

    return aggregated_results


def run_analysis(question):

    print("\n" + "=" * 60)
    print("CREATING ANALYSIS PLAN")
    print("=" * 60)

    plan, message = create_analysis_plan(question)

    print(message)

    if not plan:
        return None

    print("\nAnalysis type:")
    print(plan["analysis_type"])

    print("\nReason:")
    print(plan["reason"])

    print("\nPlanned analyses:")

    for i, query in enumerate(plan["queries"], 1):

        print(f"\n{i}. {query['name']}")
        print(query["sql"])

    print("\n" + "=" * 60)
    print("EXECUTING ANALYSIS PLAN")
    print("=" * 60)

    execution_results, execution_message = execute_analysis_plan(
        plan
    )

    print("\n" + "=" * 60)
    print("AGGREGATING RESULTS")
    print("=" * 60)

    print(execution_message)

    aggregated_results = aggregate_results(
        execution_results
    )

    return aggregated_results


if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("SUPERMARKET ANALYSIS AGGREGATOR")
    print("=" * 60)

    question = input(
        "\nEnter an analytical question: "
    )

    results = run_analysis(question)

    if results is None:

        print("\nAnalysis could not be completed.")

        sys.exit()

    print("\n" + "=" * 60)
    print("AGGREGATED ANALYSIS RESULTS")
    print("=" * 60)

    for result in results:

        print("\nAnalysis:", result["name"])
        print("Success:", result["success"])

        if result["success"]:

            print("Columns:", result["columns"])
            print("Rows:", result["rows"])

        else:

            print("Error:", result["error"])