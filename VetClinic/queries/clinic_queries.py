from db_connection import get_connection

def get_all_clinics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CLINICID, C_NAME, LOCATION, EMERGENCTDCALILITIES FROM CLINIC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_clinic_by_id(clinic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT CLINICID, C_NAME, LOCATION, EMERGENCTDCALILITIES FROM CLINIC WHERE CLINICID = ?",
        (clinic_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def insert_clinic(clinic_id, name, location, emergency_facilities):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CLINIC (CLINICID, C_NAME, LOCATION, EMERGENCTDCALILITIES) VALUES (?, ?, ?, ?)",
        (clinic_id, name, location, emergency_facilities)
    )
    conn.commit()
    conn.close()


def update_clinic(clinic_id, name, location, emergency_facilities):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE CLINIC
           SET C_NAME = ?, LOCATION = ?, EMERGENCTDCALILITIES = ?
           WHERE CLINICID = ?""",
        (name, location, emergency_facilities, clinic_id)
    )
    conn.commit()
    conn.close()


def delete_clinic(clinic_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CLINIC WHERE CLINICID = ?", (clinic_id,))
    conn.commit()
    conn.close()