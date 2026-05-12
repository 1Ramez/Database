from db_connection import get_connection

def get_all_vaccines():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT VACCINEID, VACCINENAME FROM VACCINE")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_vaccine_by_id(vaccine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT VACCINEID, VACCINENAME FROM VACCINE WHERE VACCINEID = ?",
        (vaccine_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def insert_vaccine( vaccine_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO VACCINE (VACCINENAME) VALUES (?)",
        (vaccine_name,)
    )
    conn.commit()
    conn.close()


def update_vaccine(vaccine_id, vaccine_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE VACCINE SET VACCINENAME = ? WHERE VACCINEID = ?",
        (vaccine_name, vaccine_id)
    )
    conn.commit()
    conn.close()


def delete_vaccine(vaccine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VACCINE WHERE VACCINEID = ?", (vaccine_id,))
    conn.commit()
    conn.close()
