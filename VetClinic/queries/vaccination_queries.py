from db_connection import get_connection

def get_all_vaccination_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT VR.RECORDID, VR.BATCHNUM, VR.VACCINETYPE, VR.DATENEXTBOOSTER,
               VK.VACCINEID, VK.VACCINENAME,
               CN.NOTEID, V.V_NAME
        FROM VACCINATIONRECORD VR
        LEFT JOIN VACCINE VK ON VR.VACCINEID = VK.VACCINEID
        LEFT JOIN CLINICAL_NOTE CN ON VR.NOTEID = CN.NOTEID
        LEFT JOIN VETERINARIAN V ON CN.VETID = V.VETID
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_vaccination_record_by_id(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT VR.RECORDID, VR.BATCHNUM, VR.VACCINETYPE, VR.DATENEXTBOOSTER,
               VK.VACCINEID, VK.VACCINENAME,
               CN.NOTEID, V.V_NAME
        FROM VACCINATIONRECORD VR
        LEFT JOIN VACCINE VK ON VR.VACCINEID = VK.VACCINEID
        LEFT JOIN CLINICAL_NOTE CN ON VR.NOTEID = CN.NOTEID
        LEFT JOIN VETERINARIAN V ON CN.VETID = V.VETID
        WHERE VR.RECORDID = ?
    """, (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_vaccinations_by_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT VR.RECORDID, VR.BATCHNUM, VR.VACCINETYPE, VR.DATENEXTBOOSTER,
               VK.VACCINENAME
        FROM VACCINATIONRECORD VR
        LEFT JOIN VACCINE VK ON VR.VACCINEID = VK.VACCINEID
        WHERE VR.NOTEID = ?
    """, (note_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_vaccination_record(record_id, note_id, vaccine_id, batch_num, date_next_booster, vaccine_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO VACCINATIONRECORD (RECORDID, NOTEID, VACCINEID, BATCHNUM, DATENEXTBOOSTER, VACCINETYPE)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (record_id, note_id, vaccine_id, batch_num, date_next_booster, vaccine_type)
    )
    conn.commit()
    conn.close()


def update_vaccination_record(record_id, note_id, vaccine_id, batch_num, date_next_booster, vaccine_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE VACCINATIONRECORD
           SET NOTEID = ?, VACCINEID = ?, BATCHNUM = ?, DATENEXTBOOSTER = ?, VACCINETYPE = ?
           WHERE RECORDID = ?""",
        (note_id, vaccine_id, batch_num, date_next_booster, vaccine_type, record_id)
    )
    conn.commit()
    conn.close()


def delete_vaccination_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VACCINATIONRECORD WHERE RECORDID = ?", (record_id,))
    conn.commit()
    conn.close()
