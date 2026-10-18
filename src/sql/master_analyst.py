import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
RAG_DIR = SRC_DIR / "rag"

sys.path.append(str(SRC_DIR))
sys.path.append(str(RAG_DIR))

from sql.question_router import classify_question
from sql.analysis_planner import create_analysis_plan
from sql.analysis_executor import execute_analysis_plan
from sql.result_aggregator import aggregate_results

from rag_pipeline import build_context

from llm.llm_client import generate_response


def run_multi_step_analysis(question):
    """
    Run the complete analytical pipeline:

    Question
        ↓
    Analysis Planner
        ↓
    Analysis Executor
        ↓
    Result Aggregator
        ↓
    Return verified results
    """

    print("\n" + "=" * 70)
    print("ANALYSIS PLANNER")
    print("=" * 70)

    plan, message = create_analysis_plan(question)

    print(message)

    if not plan:
        return None, (
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

    print("\n" + "=" * 70)
    print("ANALYSIS EXECUTOR")
    print("=" * 70)

    execution_results, execution_message = execute_analysis_plan(
        plan
    )

    print("\n" + execution_message)

    if not execution_results:

        return None, (
            "The analysis plan was created, but "
            "no results were produced."
        )

    print("\n" + "=" * 70)
    print("RESULT AGGREGATOR")
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

    return aggregated_results, None


def synthesize_with_knowledge(
    question,
    knowledge_context,
    aggregated_results
):
    """
    Synthesize an answer using both:
    1. Business knowledge from RAG
    2. Verified numerical results
    """

    prompt = f"""
You are the final Answer and Synthesis component of an
AI Data Analyst system for a supermarket business.

The user asked:

{question}

BUSINESS KNOWLEDGE:

{knowledge_context}

VERIFIED DATA ANALYSIS RESULTS:

{aggregated_results}

Use BOTH the business knowledge and the verified data
to answer the user's question.

IMPORTANT RULES:

1. Use verified analysis results for numerical facts.
2. Use business knowledge for definitions,
   formulas, and explanations.
3. Do not invent information.
4. Do not change numerical values.
5. Answer the user's question directly.
6. Combine the knowledge and data into one clear answer.
7. Format monetary values clearly.
8. Format percentages clearly.
9. Keep the answer concise but informative.
10. Do not mention SQL, Python, databases, prompts,
    RAG, or internal system components.

FINAL ANSWER:
"""

    try:

        answer = generate_response(prompt)

        return answer.strip()

    except Exception as error:

        print("\nSynthesis error:")
        print(error)

        return (
            "I was able to retrieve the required information, "
            "but I could not generate the final explanation."
        )


def run_master_analyst(question):

    print("\n" + "=" * 70)
    print("QUESTION ROUTER")
    print("=" * 70)

    route = classify_question(question)

    print(f"Question: {question}")
    print(f"Route: {route}")

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------

    if route == "RAG":

        print("\nRouting to RAG...")

        try:

            context = build_context(question)

            prompt = f"""
You are a helpful AI Data Analyst for a supermarket
sales analytics system.

Use the provided business knowledge to answer the
user's question.

Do not invent information.

BUSINESS KNOWLEDGE:

{context}

USER QUESTION:

{question}

Answer clearly and concisely.
"""

            return generate_response(prompt)

        except Exception as error:

            print("\nRAG error:")
            print(error)

            return (
                "I could not retrieve the required "
                "business knowledge."
            )

    # --------------------------------------------------
    # SQL
    # --------------------------------------------------

    elif route == "SQL":

        print("\nRouting to analytical SQL pipeline...")

        results, error = run_multi_step_analysis(
            question
        )

        if error:

            return error

        print("\n" + "=" * 70)
        print("ANSWER / SYNTHESIS")
        print("=" * 70)

        from sql.answer_synthesis import synthesize_answer

        return synthesize_answer(
            question,
            results
        )

    # --------------------------------------------------
    # BOTH
    # --------------------------------------------------

    elif route == "BOTH":

        print("\nRouting to RAG + analytical SQL pipeline...")

        try:

            knowledge_context = build_context(
                question
            )

        except Exception as error:

            print("\nRAG error:")
            print(error)

            knowledge_context = (
                "No additional business knowledge "
                "could be retrieved."
            )

        results, error = run_multi_step_analysis(
            question
        )

        if error:

            return error

        print("\n" + "=" * 70)
        print("ANSWER / SYNTHESIS")
        print("=" * 70)

        return synthesize_with_knowledge(
            question,
            knowledge_context,
            results
        )

    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------

    else:

        return (
            "I'm designed to answer questions about the "
            "supermarket sales data and its business concepts. "
            "Please ask a question related to the dataset."
        )


if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("SUPERMARKET AI DATA ANALYST")
    print("MASTER ANALYST")
    print("=" * 70)

    print("\nAsk your questions below.")
    print("Type 'exit' to close the analyst.\n")

    while True:

        question = input("Ask a question: ")

        if question.lower().strip() in [
            "exit",
            "quit",
            "q"
        ]:

            print("\nGoodbye! ")
            break

        if not question.strip():

            print("\nPlease enter a question.\n")
            continue

        answer = run_master_analyst(
            question
        )

        print("\n" + "=" * 70)
        print("FINAL AI ANSWER")
        print("=" * 70)

        print("\n" + answer)
        print("\n")