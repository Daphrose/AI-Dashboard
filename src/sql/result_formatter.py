from decimal import Decimal


def format_value(value):

    if isinstance(value, float):

        value = round(value, 2)

        return f"{value:,.2f}"

    if isinstance(value, Decimal):

        return f"{value:,.2f}"

    return value


def format_results(columns, rows):

    formatted_results = []

    for row in rows:

        result = {}

        for column, value in zip(columns, row):

            result[column] = format_value(value)

        formatted_results.append(result)

    return formatted_results


if __name__ == "__main__":

    columns = ["City", "TotalProfit"]

    rows = [
        ("Fujairah", 7195991.950000001)
    ]

    results = format_results(columns, rows)

    print(results)