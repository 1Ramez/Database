from db_connection import get_connection

def get_all_vets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT VETID, V_NAME, PHONE, EXPERTISE FROM VETERINARIAN")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_vet_by_id(vet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT VETID, V_NAME, PHONE, EXPERTISE FROM VETERINARIAN WHERE VETID = ?",
        (vet_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def insert_vet( name, phone, expertise):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO VETERINARIAN (V_NAME, PHONE, EXPERTISE) VALUES (?, ?, ?)",
        (name, phone, expertise)
    )
    conn.commit()
    conn.close()


def update_vet(vet_id, name, phone, expertise):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE VETERINARIAN
           SET V_NAME = ?, PHONE = ?, EXPERTISE = ?
           WHERE VETID = ?""",
        (name, phone, expertise, vet_id)
    )
    conn.commit()
    conn.close()


def delete_vet(vet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VETERINARIAN WHERE VETID = ?", (vet_id,))
    conn.commit()
    conn.close()
