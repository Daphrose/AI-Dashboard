import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "MERGE",
    "EXEC",
    "EXECUTE",
    "GRANT",
    "REVOKE",
]


def validate_sql(sql):

    if not sql:
        return False, "SQL query is empty."

    sql = sql.strip()

    # --------------------------------------------------
    # Remove one trailing semicolon
    # --------------------------------------------------

    cleaned_sql = sql.rstrip(";").strip()

    # --------------------------------------------------
    # Must start with SELECT
    # --------------------------------------------------

    if not re.match(r"^SELECT\b", cleaned_sql, re.IGNORECASE):

        return False, "Only SELECT statements are allowed."

    # --------------------------------------------------
    # Reject SQL comments
    # --------------------------------------------------

    if "--" in cleaned_sql:

        return False, "SQL comments are not allowed."

    if "/*" in cleaned_sql or "*/" in cleaned_sql:

        return False, "SQL block comments are not allowed."

    # --------------------------------------------------
    # Reject multiple statements
    # --------------------------------------------------

    if ";" in cleaned_sql:

        return False, "Multiple SQL statements are not allowed."

    # --------------------------------------------------
    # Reject dangerous keywords
    # --------------------------------------------------

    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            cleaned_sql,
            re.IGNORECASE
        ):

            return False, (
                f"Forbidden SQL keyword detected: {keyword}"
            )

    # --------------------------------------------------
    # Must use our supermarket table
    # --------------------------------------------------

    if not re.search(
        r"\bdbo\.SupermarketSales\b",
        cleaned_sql,
        re.IGNORECASE
    ):

        return False, (
            "Query must use dbo.SupermarketSales."
        )

    return True, "SQL query is valid."


if __name__ == "__main__":

    test_sql = """
    SELECT TOP 1
        Product,
        SUM(Revenue) AS TotalRevenue
    FROM dbo.SupermarketSales
    GROUP BY Product
    ORDER BY TotalRevenue DESC
    """

    valid, message = validate_sql(test_sql)

    print("Valid:", valid)
    print("Message:", message)