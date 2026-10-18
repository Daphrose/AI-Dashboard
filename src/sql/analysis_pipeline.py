import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(SRC_DIR))

from sql.analysis_planner import create_analysis_plan
from sql.analysis_executor import execute_analysis_plan
from sql.result_aggregator import aggregate_results
from sql.answer_synthesis import synthesize_answer


def run_analysis_pipeline(question):
    """
    Run the complete multi-step analysis pipeline:

    Question
        ↓
    Analysis Planner
        ↓
    Analysis Executor
        ↓
    Result Aggregator
        ↓
    Answer Synthesis
        ↓
    Final Answer
    """

    # --------------------------------------------------
    # STEP 1: CREATE ANALYSIS PLAN
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 1 — ANALYSIS PLANNER")
    print("=" * 70)

    plan, message = create_analysis_plan(question)

    print(message)

    if not plan:

        return (
            "I could not create a reliable analysis plan "
            "for that question."
        )

    print("\nAnalysis type:")
    print(plan["analysis_type"])

    print("\nReason:")
    print(plan["reason"])

    print("\nPlanned analyses:")

    for i, query in enumerate(plan["queries"], 1):

        print(f"\n{i}. {query['name']}")
        print(query["sql"])

    # --------------------------------------------------
    # STEP 2: EXECUTE ANALYSIS PLAN
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 2 — ANALYSIS EXECUTOR")
    print("=" * 70)

    execution_results, execution_message = execute_analysis_plan(
        plan
    )

    print("\n" + execution_message)

    if not execution_results:

        return (
            "The analysis plan was created, but no "
            "analysis results were produced."
        )

    # --------------------------------------------------
    # STEP 3: AGGREGATE RESULTS
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 3 — RESULT AGGREGATOR")
    print("=" * 70)

    aggregated_results = aggregate_results(
        execution_results
    )

    print("\nAggregated results:")

    for result in aggregated_results:

        print(f"\nAnalysis: {result['name']}")
        print(f"Success: {result['success']}")

        if result["success"]:

            print(f"Columns: {result.get('columns')}")
            print(f"Rows: {result.get('rows')}")

        else:

            print(f"Error: {result.get('error')}")

    # --------------------------------------------------
    # STEP 4: SYNTHESIZE FINAL ANSWER
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 4 — ANSWER / SYNTHESIS")
    print("=" * 70)

    final_answer = synthesize_answer(
        question,
        aggregated_results
    )

    return final_answer


if __name__ == "__main__":

    print("\n" + "=" * 70)
    print(" SUPERMARKET AI DATA ANALYST")
    print("MULTI-STEP ANALYSIS PIPELINE")
    print("=" * 70)

    question = input(
        "\nEnter an analytical question: "
    )

    if not question.strip():

        print("\nPlease enter a question.")

        sys.exit()

    answer = run_analysis_pipeline(
        question
    )

    print("\n" + "=" * 70)
    print("FINAL AI ANSWER")
    print("=" * 70)

    print("\n" + answer)