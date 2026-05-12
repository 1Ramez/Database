from db_connection import get_connection

def get_all_clinical_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT CN.NOTEID, CN.CREATEDDATE, CN.P_WEIGHT, CN.NOTES,
               V.VETID, V.V_NAME
        FROM CLINICAL_NOTE CN
        LEFT JOIN VETERINARIAN V ON CN.VETID = V.VETID
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_clinical_note_by_id(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT CN.NOTEID, CN.CREATEDDATE, CN.P_WEIGHT, CN.NOTES,
               V.VETID, V.V_NAME
        FROM CLINICAL_NOTE CN
        LEFT JOIN VETERINARIAN V ON CN.VETID = V.VETID
        WHERE CN.NOTEID = ?
    """, (note_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_notes_by_vet(vet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT NOTEID, CREATEDDATE, P_WEIGHT, NOTES FROM CLINICAL_NOTE WHERE VETID = ?",
        (vet_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_clinical_note(VETID, weight, created_date, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO CLINICAL_NOTE (VETID, P_WEIGHT, CREATEDDATE, NOTES)
           VALUES (?, ?, ?, ?)""",
        (VETID, weight, created_date, notes)
    )
    conn.commit()
    conn.close()


def update_clinical_note(note_id, vet_id, weight, created_date, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE CLINICAL_NOTE
           SET VETID = ?, P_WEIGHT = ?, CREATEDDATE = ?, NOTES = ?
           WHERE NOTEID = ?""",
        (vet_id, weight, created_date, notes, note_id)
    )
    conn.commit()
    conn.close()


def delete_clinical_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CLINICAL_NOTE WHERE NOTEID = ?", (note_id,))
    conn.commit()
    conn.close()
