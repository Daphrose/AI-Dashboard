import sys
from pathlib import Path

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parents[1]
RAG_DIR = SRC_DIR / "rag"

sys.path.append(str(SRC_DIR))
sys.path.append(str(RAG_DIR))


# --------------------------------------------------
# IMPORTS
# --------------------------------------------------

from sql.question_router import classify_question
from sql.sql_generator import generate_sql
from sql.sql_validator import validate_sql
from sql.query_database import run_query
from sql.result_formatter import format_results

from rag_pipeline import build_context

from llm.llm_client import generate_response


# --------------------------------------------------
# RAG ANSWER
# --------------------------------------------------

def answer_with_rag(question):

    try:

        context = build_context(question)

        prompt = f"""
You are a helpful AI Data Analyst for a supermarket sales
analytics system.

Answer the user's question using the provided knowledge context.

Do not invent information that is not supported by the context.

Knowledge context:
{context}

User question:
{question}

Answer:
"""

        return generate_response(prompt)

    except Exception as error:

        print("\nRAG error:")
        print(error)

        return (
            "I couldn't retrieve the required business knowledge "
            "to answer that question."
        )


# --------------------------------------------------
# SQL ANSWER
# --------------------------------------------------

def answer_with_sql(question):

    try:

        print("\nGenerating SQL...\n")

        sql = generate_sql(question)

        print("Generated SQL:")
        print(sql)

        print("\nValidating SQL...\n")

        valid, message = validate_sql(sql)

        print(message)

        if not valid:

            return (
                "I couldn't safely execute the generated database "
                "query because it failed validation."
            )

        print("\nExecuting SQL...\n")

        columns, rows = run_query(sql)

        # Database execution failed
        if columns is None:

            return (
                "I couldn't retrieve the requested data because "
                "the database query could not be executed."
            )

        # Query worked but returned nothing
        if not rows:

            return (
                "The query was executed successfully, but no "
                "matching data was found."
            )

        print("Columns:")
        print(columns)

        print("\nResults:")

        for row in rows:
            print(row)

        # Format results before sending them to the LLM
        results = format_results(columns, rows)

        prompt = f"""
You are a helpful AI Data Analyst for a supermarket sales
analytics system.

The user asked:

{question}

SQL Server returned these verified results:

{results}

Answer the user's question using ONLY these verified results.

Rules:

1. Do not invent information.
2. Do not change the numerical results.
3. Answer the question directly.
4. Explain the result clearly.
5. Format monetary values clearly.
6. Keep the answer concise.
7. Do not mention SQL, Python, databases, prompts,
   or internal system details.

Answer:
"""

        return generate_response(prompt)

    except Exception as error:

        print("\nSQL analyst error:")
        print(error)

        return (
            "I encountered a problem while analyzing the "
            "requested data."
        )


# --------------------------------------------------
# BOTH RAG + SQL
# --------------------------------------------------

def answer_with_both(question):

    try:

        # ------------------------------------------
        # Retrieve business knowledge
        # ------------------------------------------

        print("\nRetrieving business knowledge...\n")

        knowledge_context = build_context(question)

        # ------------------------------------------
        # Generate SQL
        # ------------------------------------------

        print("Generating SQL...\n")

        sql = generate_sql(question)

        print("Generated SQL:")
        print(sql)

        # ------------------------------------------
        # Validate SQL
        # ------------------------------------------

        print("\nValidating SQL...\n")

        valid, message = validate_sql(sql)

        print(message)

        if not valid:

            return (
                "I retrieved the relevant business knowledge, "
                "but the database query failed the safety "
                "validation and was not executed."
            )

        # ------------------------------------------
        # Execute SQL
        # ------------------------------------------

        print("\nExecuting SQL...\n")

        columns, rows = run_query(sql)

        # Database execution failed
        if columns is None:

            return (
                "I retrieved the relevant business knowledge, "
                "but I couldn't retrieve the required data "
                "from the database."
            )

        # Query worked but returned nothing
        if not rows:

            return (
                "I retrieved the relevant business knowledge, "
                "but the database query returned no matching data."
            )

        print("\nColumns:")
        print(columns)

        print("\nResults:")

        for row in rows:
            print(row)

        # ------------------------------------------
        # Format SQL results
        # ------------------------------------------

        results = format_results(columns, rows)

        # ------------------------------------------
        # Combine RAG + SQL
        # ------------------------------------------

        prompt = f"""
You are a helpful AI Data Analyst for a supermarket sales
analytics system.

The user asked:

{question}

BUSINESS KNOWLEDGE:

{knowledge_context}

VERIFIED DATA FROM SQL SERVER:

{results}

Use both the business knowledge and the verified data
to answer the user's question.

Rules:

1. Use SQL results for numerical facts.
2. Use the knowledge context for definitions,
   formulas, and business meaning.
3. Do not invent information.
4. Do not change numerical results.
5. Clearly explain the answer.
6. Format monetary values clearly.
7. Keep the response concise.
8. Do not mention SQL, Python, databases, prompts,
   or internal system details.

Answer:
"""

        return generate_response(prompt)

    except Exception as error:

        print("\nCombined analyst error:")
        print(error)

        return (
            "I encountered a problem while combining the "
            "business knowledge and data analysis."
        )


# --------------------------------------------------
# MAIN AI ANALYST
# --------------------------------------------------

def answer_question(question):

    route = classify_question(question)

    print("\n" + "=" * 60)
    print("QUESTION ROUTER")
    print("=" * 60)

    print(f"Question: {question}")
    print(f"Route: {route}")

    # ----------------------------------------------
    # RAG
    # ----------------------------------------------

    if route == "RAG":

        print("\nSending question to RAG...\n")

        return answer_with_rag(question)

    # ----------------------------------------------
    # SQL
    # ----------------------------------------------

    elif route == "SQL":

        print("\nSending question to SQL...\n")

        return answer_with_sql(question)

    # ----------------------------------------------
    # BOTH
    # ----------------------------------------------

    elif route == "BOTH":

        print("\nSending question to BOTH RAG and SQL...\n")

        return answer_with_both(question)

    # ----------------------------------------------
    # UNKNOWN
    # ----------------------------------------------

    else:

        return (
            "I'm designed to answer questions about the "
            "supermarket sales data and its business concepts. "
            "Please ask a question related to the dataset."
        )



if __name__ == "__main__":

    print("\n" + "=" * 60)
    print(" SUPERMARKET AI DATA ANALYST")
    print("=" * 60)

    print("\nAsk your questions below.")
    print("Type 'exit' to close the analyst.\n")

    while True:

        question = input("You: ")

        if question.lower().strip() in ["exit", "quit", "q"]:

            print("\nGoodbye! ")
            break

        if not question.strip():

            print("Please enter a question.\n")
            continue

        answer = answer_question(question)

        print("\n" + "=" * 60)
        print("FINAL AI ANSWER")
        print("=" * 60)

        print(answer)
        print("\n")