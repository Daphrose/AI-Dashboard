from sql_connection import get_connection


def run_query(query):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query)

        # Some SQL statements may not return a result set.
        if cursor.description is None:
            return [], []

        columns = [column[0] for column in cursor.description]

        rows = cursor.fetchall()

        return columns, rows

    except Exception as error:

        print("\nSQL execution error:")
        print(error)

        return None, None

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":

    query = """
    SELECT TOP 1
        Product,
        SUM(Revenue) AS TotalRevenue
    FROM dbo.SupermarketSales
    GROUP BY Product
    ORDER BY TotalRevenue DESC
    """

    columns, rows = run_query(query)

    if columns is not None:

        print("Columns:")
        print(columns)

        print("\nResults:")

        for row in rows:
            print(row)