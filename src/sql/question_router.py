import re
import sys
from pathlib import Path

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from llm.llm_client import generate_response


# --------------------------------------------------
# INTENT PATTERNS
# --------------------------------------------------

KNOWLEDGE_PATTERNS = [
    r"\bwhat is\b",
    r"\bwhat does\b",
    r"\bwhat are\b",
    r"\bdefine\b",
    r"\bdefinition\b",
    r"\bmeaning\b",
    r"\bwhat do you mean\b",
    r"\bhow is .* calculated\b",
    r"\bhow are .* calculated\b",
    r"\bformula\b",
]


DATA_PATTERNS = [
    r"\btotal\b",
    r"\bhow much\b",
    r"\bhow many\b",
    r"\bhighest\b",
    r"\blowest\b",
    r"\bmost\b",
    r"\bleast\b",
    r"\btop\b",
    r"\bbottom\b",
    r"\baverage\b",
    r"\bsum\b",
    r"\bwhich product\b",
    r"\bwhich category\b",
    r"\bwhich city\b",
    r"\bwhich country\b",
    r"\bhow many units\b",
    r"\bhow much revenue\b",
    r"\bhow much profit\b",
    r"\bhow much cogs\b",
    r"\btotal revenue\b",
    r"\btotal profit\b",
    r"\btotal cogs\b",
    r"\btotal quantity\b",
    r"\brevenue in\b",
    r"\bprofit in\b",
    r"\bcogs in\b",
    r"\bsales in\b",
    r"\bquantity in\b",
    r"\bper month\b",
    r"\bper year\b",
    r"\bduring\b",
    r"\bbetween\b",

    # --------------------------------------------------
    # PROFIT MARGIN DATA QUESTIONS
    # --------------------------------------------------

    r"\bwhat was .*profit margin\b",
    r"\bwhat is our .*profit margin\b",
    r"\bactual .*profit margin\b",
]


# --------------------------------------------------
# PATTERN CHECKER
# --------------------------------------------------

def matches_pattern(question, patterns):

    return any(
        re.search(pattern, question, re.IGNORECASE)
        for pattern in patterns
    )


# --------------------------------------------------
# LLM FALLBACK ROUTER
# --------------------------------------------------

def llm_classify(question):

    prompt = f"""
You are a question router for a supermarket sales analytics system.

Classify the user's question into exactly ONE of these categories:

RAG
SQL
BOTH
UNKNOWN

Definitions:

RAG:
Use RAG when the user is asking for business knowledge,
definitions, meanings, formulas, column explanations,
or conceptual explanations.

SQL:
Use SQL when the user is asking for actual numerical
information from the supermarket sales database.

Examples:
- total revenue
- total profit
- total COGS
- highest revenue product
- lowest profit category
- quantity sold
- sales by city
- actual profit margin
- what was our profit margin

BOTH:
Use BOTH when the question clearly requires both:
1. business knowledge or explanation, AND
2. actual numerical data from the database.

Examples:
- What is COGS and what was our total COGS?
- What is profit margin and what was our profit margin?

UNKNOWN:
Use UNKNOWN when the question is unrelated to supermarket
sales analytics or cannot be classified confidently.

Important:

A column name alone does NOT mean SQL.

For example:
"What is COGS?"
should be RAG.

"What was our total COGS?"
should be SQL.

"What is COGS and what was our total COGS?"
should be BOTH.

"What is profit margin?"
should be RAG.

"What was our profit margin?"
should be SQL.

"What is profit margin and what was our profit margin?"
should be BOTH.

Return ONLY one word:

RAG
SQL
BOTH
UNKNOWN

USER QUESTION:
{question}

CLASSIFICATION:
"""

    response = generate_response(prompt)

    response = response.strip().upper()

    # Extract only an allowed classification
    allowed_routes = [
        "RAG",
        "SQL",
        "BOTH",
        "UNKNOWN"
    ]

    for route in allowed_routes:

        if route in response:
            return route

    return "UNKNOWN"


# --------------------------------------------------
# MAIN CLASSIFIER
# --------------------------------------------------

def classify_question(question):

    question = question.lower().strip()

    if not question:
        return "UNKNOWN"

    knowledge_match = matches_pattern(
        question,
        KNOWLEDGE_PATTERNS
    )

    data_match = matches_pattern(
        question,
        DATA_PATTERNS
    )

    # --------------------------------------------------
    # CLEAR DATA QUESTION
    # --------------------------------------------------

    if data_match:

        # If the question explicitly asks for both
        # knowledge and numerical information
        if knowledge_match:

            combined_patterns = [
                r"\band\b",
                r"\balso\b",
                r"\bas well as\b",
                r"\btogether\b",
            ]

            if matches_pattern(
                question,
                combined_patterns
            ):
                return "BOTH"

            # Data intent takes priority for questions such as:
            # "Explain which product generated the most revenue."
            return "SQL"

        return "SQL"

    # --------------------------------------------------
    # CLEAR KNOWLEDGE QUESTION
    # --------------------------------------------------

    if knowledge_match:

        return "RAG"

    # --------------------------------------------------
    # AMBIGUOUS QUESTION
    # --------------------------------------------------

    return llm_classify(question)


# --------------------------------------------------
# TEST ROUTER
# --------------------------------------------------

if __name__ == "__main__":

    test_questions = [

        # RAG
        "What is COGS?",
        "What does SKU mean?",
        "How is profit margin calculated?",
        "What is profit margin?",

        # SQL
        "What was our total COGS?",
        "What was our profit margin?",
        "Which product generated the most revenue?",
        "How many units were sold?",

        # SQL despite knowledge wording
        "Explain which product generated the most revenue.",

        # BOTH
        "What is COGS and what was our total COGS?",
        "What is profit margin and what was our profit margin?",

        # LLM fallback / ambiguous
        "Tell me about revenue.",
        "How did the business perform?"
    ]

    for question in test_questions:

        route = classify_question(question)

        print(f"Question: {question}")
        print(f"Route: {route}")
        print("-" * 60)