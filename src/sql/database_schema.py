from sql_connection import get_connection


def get_table_schema():

    query = """
    SELECT
        COLUMN_NAME,
        DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'dbo'
      AND TABLE_NAME = 'SupermarketSales'
    ORDER BY ORDINAL_POSITION
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def build_schema_description():

    columns = get_table_schema()

    schema = "Table: dbo.SupermarketSales\n\n"
    schema += "Columns:\n"

    for column in columns:
        column_name = column[0]
        data_type = column[1]

        schema += f"- {column_name} ({data_type})\n"

    return schema


if __name__ == "__main__":

    schema = build_schema_description()

    print(schema)