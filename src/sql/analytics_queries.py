from sql_connection import get_connection


def get_total_revenue():

    query = """
    SELECT ROUND(SUM(Revenue), 2)
    FROM dbo.SupermarketSales
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]


def get_total_profit():

    query = """
    SELECT ROUND(SUM(Profit), 2)
    FROM dbo.SupermarketSales
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]


def get_total_cogs():

    query = """
    SELECT ROUND(SUM(COGS), 2)
    FROM dbo.SupermarketSales
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]


def get_total_quantity():

    query = """
    SELECT SUM(Quantity)
    FROM dbo.SupermarketSales
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]


def get_revenue_by_product():

    query = """
    SELECT
        Product,
        ROUND(SUM(Revenue), 2) AS TotalRevenue
    FROM dbo.SupermarketSales
    GROUP BY Product
    ORDER BY TotalRevenue DESC
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":

    print("Total Revenue:", get_total_revenue())
    print("Total Profit:", get_total_profit())
    print("Total COGS:", get_total_cogs())
    print("Total Quantity:", get_total_quantity())

    print("\nRevenue by Product:\n")

    results = get_revenue_by_product()

    for row in results:
        print(row[0], ":", row[1])