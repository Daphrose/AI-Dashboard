import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(SRC_DIR))

from llm.llm_client import generate_response


def synthesize_answer(question, aggregated_results):
    """
    Generate a natural-language business answer using
    only the verified aggregated analysis results.
    """

    if not aggregated_results:
        return (
            "I could not generate an answer because "
            "no analysis results were available."
        )

    verified_results = []

    for result in aggregated_results:

        name = result.get("name", "Unnamed Analysis")
        success = result.get("success", False)

        if success:

            columns = result.get("columns", [])
            rows = result.get("rows", [])

            verified_results.append({
                "analysis": name,
                "columns": columns,
                "rows": rows
            })

        else:

            verified_results.append({
                "analysis": name,
                "error": result.get(
                    "error",
                    "Analysis failed."
                )
            })

    prompt = f"""
You are the final Answer and Synthesis component of an
AI Data Analyst system for a supermarket business.

The user asked:

{question}

The system has already performed the required analyses.

Below are the VERIFIED results returned by the database:

{verified_results}

Your job is to explain these verified results clearly
and directly to the user.

IMPORTANT RULES:

1. Use ONLY the verified results provided above.
2. Do not invent numbers, facts, products, cities,
   trends, or conclusions that are not supported
   by the results.
3. Do not change or recalculate the numerical values.
4. Explain what the results mean for the business.
5. If multiple analyses are provided, combine them
   into one coherent answer.
6. Use clear business language.
7. Format monetary values clearly.
8. Format percentages clearly.
9. Keep the answer concise but informative.
10. Do not mention SQL, Python, databases, prompts,
    the LLM, or internal system components.
11. If an analysis failed, do not pretend that its
    result exists.
12. Answer the user's original question directly.

FINAL ANSWER:
"""

    try:

        answer = generate_response(prompt)

        return answer.strip()

    except Exception as error:

        print("\nSynthesis error:")
        print(error)

        return (
            "I was able to complete the analysis, "
            "but I could not generate the final explanation."
        )


if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("ANSWER / SYNTHESIS TEST")
    print("=" * 60)

    test_question = "How did the business perform overall?"

    test_results = [
        {
            "name": "Total Revenue",
            "success": True,
            "columns": ["TotalRevenue"],
            "rows": [
                (206209979.90,)
            ]
        },
        {
            "name": "Total Profit",
            "success": True,
            "columns": ["TotalProfit"],
            "rows": [
                (43844719.90,)
            ]
        },
        {
            "name": "Total COGS",
            "success": True,
            "columns": ["TotalCOGS"],
            "rows": [
                (162365260.00,)
            ]
        },
        {
            "name": "Total Quantity Sold",
            "success": True,
            "columns": ["TotalQuantity"],
            "rows": [
                (52076,)
            ]
        },
        {
            "name": "Profit Margin Percentage",
            "success": True,
            "columns": ["ProfitMarginPercentage"],
            "rows": [
                (21.262171656901426,)
            ]
        }
    ]

    answer = synthesize_answer(
        test_question,
        test_results
    )

    print("\n" + "=" * 60)
    print("FINAL SYNTHESIZED ANSWER")
    print("=" * 60)

    print(answer)