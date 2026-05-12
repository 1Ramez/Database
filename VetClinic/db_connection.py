import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=VetClinic;"
        "Trusted_Connection=yes;"
        "Connection Timeout=5;"
    )
    return conn