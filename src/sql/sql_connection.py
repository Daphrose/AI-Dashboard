import pyodbc


SERVER = r"DESKTOP-A1KKL02\SQLEXPRESS"
DATABASE = "supermarketAI"
DRIVER = "ODBC Driver 18 for SQL Server"


def get_connection():

    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    connection = pyodbc.connect(connection_string)

    return connection


if __name__ == "__main__":

    connection = get_connection()

    print("Successfully connected to SQL Server!")

    connection.close()

    print("Connection closed.")