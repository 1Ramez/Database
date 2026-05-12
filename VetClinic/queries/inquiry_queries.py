from db_connection import get_connection

def inquiry_1_most_visited_species():
    # Inquiry 1:
    # Which 'species' of pets had the maximum number of medical visits last month?

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 1 P.SPECIE, COUNT(V.VISTID) AS VISIT_COUNT
        FROM VIST V
        JOIN PET P ON V.PETID = P.PETID
        WHERE MONTH(V.VISTDATE) = MONTH(DATEADD(MONTH, -1, GETDATE()))
          AND YEAR(V.VISTDATE)  = YEAR(DATEADD(MONTH, -1, GETDATE()))
        GROUP BY P.SPECIE
        ORDER BY VISIT_COUNT DESC
    """)
    row = cursor.fetchone()
    conn.close()
    return row


def inquiry_2_clinics_with_no_visits():
    
    # Inquiry 2:
    # Which clinic did not host any medical visits during the last month?
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT C.CLINICID, C.C_NAME, C.LOCATION
        FROM CLINIC C
        WHERE C.CLINICID NOT IN (
            SELECT DISTINCT CLINICID
            FROM VIST
            WHERE CLINICID IS NOT NULL
              AND MONTH(VISTDATE) = MONTH(DATEADD(MONTH, -1, GETDATE()))
              AND YEAR(VISTDATE)  = YEAR(DATEADD(MONTH, -1, GETDATE()))
        )
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def inquiry_3_vet_most_vaccinations():
    
    # Inquiry 3:
    # Who was the veterinarian who administered the highest number of vaccinations last month?

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 1 VT.VETID, VT.V_NAME, COUNT(VR.RECORDID) AS VAC_COUNT
        FROM VACCINATIONRECORD VR
        JOIN CLINICAL_NOTE CN ON VR.NOTEID = CN.NOTEID
        JOIN VETERINARIAN VT ON CN.VETID = VT.VETID
        WHERE MONTH(CN.CREATEDDATE) = MONTH(DATEADD(MONTH, -1, GETDATE()))
          AND YEAR(CN.CREATEDDATE)  = YEAR(DATEADD(MONTH, -1, GETDATE()))
        GROUP BY VT.VETID, VT.V_NAME
        ORDER BY VAC_COUNT DESC
    """)
    row = cursor.fetchone()
    conn.close()
    return row


def inquiry_4_owners_no_visits():
    
    # Inquiry 4:
    # Identify pet owners who did not bring their pets for a visit last month.

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT O.OWNERID, O.O_NAME, O.PHONE, O.EMERGENCYCONTACT
        FROM OWNER O
        WHERE O.OWNERID NOT IN (
            SELECT DISTINCT P.OWNERID
            FROM VIST V
            JOIN PET P ON V.PETID = P.PETID
            WHERE P.OWNERID IS NOT NULL
              AND MONTH(V.VISTDATE) = MONTH(DATEADD(MONTH, -1, GETDATE()))
              AND YEAR(V.VISTDATE)  = YEAR(DATEADD(MONTH, -1, GETDATE()))
        )
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def inquiry_5_vaccines_per_clinic():

    # Inquiry 5:
    # What were the specific vaccines administered at each clinic last month?

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT C.C_NAME, VK.VACCINENAME, COUNT(VR.RECORDID) AS TIMES_GIVEN
        FROM VIST VI
        JOIN CLINIC C ON VI.CLINICID = C.CLINICID
        JOIN CLINICAL_NOTE CN ON VI.VETID = CN.VETID
        JOIN VACCINATIONRECORD VR ON CN.NOTEID = VR.NOTEID
        JOIN VACCINE VK ON VR.VACCINEID = VK.VACCINEID
        WHERE MONTH(VI.VISTDATE) = MONTH(DATEADD(MONTH, -1, GETDATE()))
          AND YEAR(VI.VISTDATE)  = YEAR(DATEADD(MONTH, -1, GETDATE()))
        GROUP BY C.C_NAME, VK.VACCINENAME
        ORDER BY C.C_NAME, VK.VACCINENAME
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def inquiry_6_pet_visit_count_this_year():
    
    # Inquiry 6:
    # For each pet, retrieve its name and the total number of visits it has had this year.

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT P.PETID, P.P_NAME, P.SPECIE, COUNT(V.VISTID) AS TOTAL_VISITS
        FROM PET P
        LEFT JOIN VIST V ON P.PETID = V.PETID
                        AND YEAR(V.VISTDATE) = YEAR(GETDATE())
        GROUP BY P.PETID, P.P_NAME, P.SPECIE
        ORDER BY TOTAL_VISITS DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows