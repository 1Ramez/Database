from db_connection import get_connection

def get_all_worksat():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT W.VETID, V.V_NAME, W.CLINICID, C.C_NAME
        FROM WORKSAT W
        JOIN VETERINARIAN V ON W.VETID = V.VETID
        JOIN CLINIC C ON W.CLINICID = C.CLINICID
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_vets_at_clinic(clinic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT V.VETID, V.V_NAME, V.EXPERTISE, V.PHONE
        FROM WORKSAT W
        JOIN VETERINARIAN V ON W.VETID = V.VETID
        WHERE W.CLINICID = ?
    """, (clinic_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_clinics_of_vet(vet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT C.CLINICID, C.C_NAME, C.LOCATION
        FROM WORKSAT W
        JOIN CLINIC C ON W.CLINICID = C.CLINICID
        WHERE W.VETID = ?
    """, (vet_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_worksat(vet_id, clinic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO WORKSAT (VETID, CLINICID) VALUES (?, ?)",
        (vet_id, clinic_id)
    )
    conn.commit()
    conn.close()


def delete_worksat(vet_id, clinic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM WORKSAT WHERE VETID = ? AND CLINICID = ?",
        (vet_id, clinic_id)
    )
    conn.commit()
    conn.close()