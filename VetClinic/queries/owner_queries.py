from db_connection import get_connection

def get_all_owners():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OWNERID, O_NAME, BILLINGADDRESS, EMERGENCYCONTACT, PHONE FROM OWNER")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_owner_by_id(owner_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT OWNERID, O_NAME, BILLINGADDRESS, EMERGENCYCONTACT, PHONE FROM OWNER WHERE OWNERID = ?",
        (owner_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def insert_owner(owner_id, name, billing_address, emergency_contact, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO OWNER (OWNERID, O_NAME, BILLINGADDRESS, EMERGENCYCONTACT, PHONE) VALUES (?, ?, ?, ?, ?)",
        (owner_id, name, billing_address, emergency_contact, phone)
    )
    conn.commit()
    conn.close()


def update_owner(owner_id, name, billing_address, emergency_contact, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE OWNER
           SET O_NAME = ?, BILLINGADDRESS = ?, EMERGENCYCONTACT = ?, PHONE = ?
           WHERE OWNERID = ?""",
        (name, billing_address, emergency_contact, phone, owner_id)
    )
    conn.commit()
    conn.close()


def delete_owner(owner_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM OWNER WHERE OWNERID = ?", (owner_id,))
    conn.commit()
    conn.close()
