import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost;"
        "DATABASE=VetClinic;"
        "Trusted_Connection=yes;"
    )
    return conn
