from db_connection import get_connection

def get_all_visits():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT V.VISTID, V.VISTDATE, V.REASON,
               P.PETID, P.P_NAME,
               VT.VETID, VT.V_NAME,
               C.CLINICID, C.C_NAME
        FROM VIST V
        LEFT JOIN PET P ON V.PETID = P.PETID
        LEFT JOIN VETERINARIAN VT ON V.VETID = VT.VETID
        LEFT JOIN CLINIC C ON V.CLINICID = C.CLINICID
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_visit_by_id(visit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT V.VISTID, V.VISTDATE, V.REASON,
               P.PETID, P.P_NAME,
               VT.VETID, VT.V_NAME,
               C.CLINICID, C.C_NAME
        FROM VIST V
        LEFT JOIN PET P ON V.PETID = P.PETID
        LEFT JOIN VETERINARIAN VT ON V.VETID = VT.VETID
        LEFT JOIN CLINIC C ON V.CLINICID = C.CLINICID
        WHERE V.VISTID = ?
    """, (visit_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_visits_by_pet(pet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT V.VISTID, V.VISTDATE, V.REASON, VT.V_NAME, C.C_NAME
        FROM VIST V
        LEFT JOIN VETERINARIAN VT ON V.VETID = VT.VETID
        LEFT JOIN CLINIC C ON V.CLINICID = C.CLINICID
        WHERE V.PETID = ?
    """, (pet_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_visit(visit_id, clinic_id, pet_id, vet_id, visit_date, reason):
    """Insert a new visit."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO VIST (VISTID, CLINICID, PETID, VETID, VISTDATE, REASON)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (visit_id, clinic_id, pet_id, vet_id, visit_date, reason)
    )
    conn.commit()
    conn.close()


def update_visit(visit_id, clinic_id, pet_id, vet_id, visit_date, reason):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE VIST
           SET CLINICID = ?, PETID = ?, VETID = ?, VISTDATE = ?, REASON = ?
           WHERE VISTID = ?""",
        (clinic_id, pet_id, vet_id, visit_date, reason, visit_id)
    )
    conn.commit()
    conn.close()


def delete_visit(visit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VIST WHERE VISTID = ?", (visit_id,))
    conn.commit()
    conn.close()
