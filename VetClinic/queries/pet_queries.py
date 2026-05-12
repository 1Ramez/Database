from db_connection import get_connection

def get_all_pets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT P.PETID, P.P_NAME, P.SPECIE, P.BREED, P.GENDER, P.DATEOFBIRTH,
               O.OWNERID, O.O_NAME
        FROM PET P
        LEFT JOIN OWNER O ON P.OWNERID = O.OWNERID
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_pet_by_id(pet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT P.PETID, P.P_NAME, P.SPECIE, P.BREED, P.GENDER, P.DATEOFBIRTH,
               O.OWNERID, O.O_NAME
        FROM PET P
        LEFT JOIN OWNER O ON P.OWNERID = O.OWNERID
        WHERE P.PETID = ?
    """, (pet_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_pets_by_owner(owner_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT PETID, P_NAME, SPECIE, BREED, GENDER, DATEOFBIRTH FROM PET WHERE OWNERID = ?",
        (owner_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def insert_pet(owner_id, name, breed, date_of_birth, gender, specie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO PET (OWNERID, P_NAME, BREED, DATEOFBIRTH, GENDER, SPECIE)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (owner_id, name, breed, date_of_birth, gender, specie)
    )
    conn.commit()
    conn.close()


def update_pet(pet_id, owner_id, name, breed, date_of_birth, gender, specie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE PET
           SET OWNERID = ?, P_NAME = ?, BREED = ?, DATEOFBIRTH = ?, GENDER = ?, SPECIE = ?
           WHERE PETID = ?""",
        (owner_id, name, breed, date_of_birth, gender, specie, pet_id)
    )
    conn.commit()
    conn.close()


def delete_pet(pet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PET WHERE PETID = ?", (pet_id,))
    conn.commit()
    conn.close()
