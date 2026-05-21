import re

from db_connection import get_connection


MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def _safe_scalar(cur, sql: str, params=()):
    cur.execute(sql, params)
    row = cur.fetchone()
    if not row:
        return None
    return row[0]


def _parse_month_year(text: str):
    t = (text or "").lower()

    m = re.search(r"\b(20\d{2})[-/](\d{1,2})\b", t)  # 2024-06
    if m:
        year = int(m.group(1))
        month = int(m.group(2))
        if 1 <= month <= 12:
            return year, month

    m = re.search(r"\b(\d{1,2})[-/](20\d{2})\b", t)  # 06/2024
    if m:
        month = int(m.group(1))
        year = int(m.group(2))
        if 1 <= month <= 12:
            return year, month

    m = re.search(
        r"\b("
        r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|sep(?:t)?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
        r")\s+(20\d{2})\b",
        t,
    )
    if m:
        month = MONTHS.get(m.group(1), None)
        year = int(m.group(2))
        if month:
            return year, month

    return None


def db_summary() -> str:
    """
    Returns a small DB snapshot (counts + some recent rows) to help the chatbot
    stay grounded when Gemini is unavailable or overloaded.
    """
    try:
        conn = get_connection()
    except Exception as e:
        return f"Database connection failed: {e}"

    try:
        cur = conn.cursor()
        counts = {}
        for table in (
            "OWNER",
            "PET",
            "CLINIC",
            "VETERINARIAN",
            "VIST",
            "VACCINE",
            "VACCINATIONRECORD",
            "CLINICAL_NOTE",
        ):
            try:
                counts[table] = int(_safe_scalar(cur, f"SELECT COUNT(*) FROM {table}") or 0)
            except Exception:
                counts[table] = None

        lines = ["DB snapshot (live):"]
        for k in ("OWNER", "PET", "CLINIC", "VETERINARIAN", "VIST", "VACCINE", "VACCINATIONRECORD", "CLINICAL_NOTE"):
            v = counts.get(k)
            lines.append(f"- {k}: {v if v is not None else 'n/a'} rows")

        try:
            cur.execute(
                """
                SELECT TOP 5 V.VISTID, V.VISTDATE, V.REASON, P.P_NAME, VT.V_NAME, C.C_NAME
                FROM VIST V
                LEFT JOIN PET P ON V.PETID = P.PETID
                LEFT JOIN VETERINARIAN VT ON V.VETID = VT.VETID
                LEFT JOIN CLINIC C ON V.CLINICID = C.CLINICID
                ORDER BY V.VISTDATE DESC
                """
            )
            rows = cur.fetchall()
            if rows:
                lines.append("- Latest visits (top 5):")
                for vist_id, vist_date, reason, pet_name, vet_name, clinic_name in rows:
                    ds = vist_date.strftime("%Y-%m-%d") if hasattr(vist_date, "strftime") else str(vist_date)[:10]
                    lines.append(f"  - #{vist_id} {ds}: {pet_name or 'Unknown pet'} @ {clinic_name or 'Unknown clinic'} ({vet_name or 'Unknown vet'}) - {reason}")
        except Exception:
            pass

        return "\n".join(lines)
    finally:
        try:
            conn.close()
        except Exception:
            pass


def try_answer_from_db(question: str, max_rows: int = 60) -> str | None:
    """
    Attempts to answer common questions deterministically from SQL Server
    (no Gemini). Returns an answer string, or None if not recognized.
    """
    q = (question or "").strip()
    if not q:
        return None
    ql = q.lower()

    try:
        conn = get_connection()
    except Exception as e:
        return f"Database connection failed: {e}"

    try:
        cur = conn.cursor()

        # Counts: visits in a given month, last month, this month, this year
        if "visit" in ql and any(k in ql for k in ("how many", "count", "number of")):
            parsed = _parse_month_year(ql)
            if parsed:
                year, month = parsed
                cur.execute("SELECT COUNT(*) FROM VIST WHERE YEAR(VISTDATE)=? AND MONTH(VISTDATE)=?", (year, month))
                n = int(cur.fetchone()[0] or 0)
                return f"There are {n} visit(s) recorded for {year}-{month:02d}."

            if "last month" in ql:
                n = _safe_scalar(
                    cur,
                    """
                    SELECT COUNT(*)
                    FROM VIST
                    WHERE MONTH(VISTDATE) = MONTH(DATEADD(MONTH, -1, GETDATE()))
                      AND YEAR(VISTDATE)  = YEAR(DATEADD(MONTH, -1, GETDATE()))
                    """,
                )
                return f"There are {int(n or 0)} visit(s) recorded for last month."

            if "this month" in ql:
                n = _safe_scalar(
                    cur,
                    """
                    SELECT COUNT(*)
                    FROM VIST
                    WHERE MONTH(VISTDATE) = MONTH(GETDATE())
                      AND YEAR(VISTDATE)  = YEAR(GETDATE())
                    """,
                )
                return f"There are {int(n or 0)} visit(s) recorded for this month."

            if "this year" in ql:
                n = _safe_scalar(cur, "SELECT COUNT(*) FROM VIST WHERE YEAR(VISTDATE)=YEAR(GETDATE())")
                return f"There are {int(n or 0)} visit(s) recorded for this year."

        # Listing visits / details
        if "visit" in ql and any(k in ql for k in ("details", "list", "show", "every", "all")):
            parsed = _parse_month_year(ql)
            if parsed:
                year, month = parsed
                cur.execute(
                    f"""
                    SELECT TOP {max_rows} V.VISTID, V.VISTDATE, V.REASON,
                           P.P_NAME, VT.V_NAME, C.C_NAME
                    FROM VIST V
                    LEFT JOIN PET P ON V.PETID = P.PETID
                    LEFT JOIN VETERINARIAN VT ON V.VETID = VT.VETID
                    LEFT JOIN CLINIC C ON V.CLINICID = C.CLINICID
                    WHERE YEAR(V.VISTDATE)=? AND MONTH(V.VISTDATE)=?
                    ORDER BY V.VISTDATE ASC
                    """,
                    (year, month),
                )
                rows = cur.fetchall()
                total = int(_safe_scalar(cur, "SELECT COUNT(*) FROM VIST WHERE YEAR(VISTDATE)=? AND MONTH(VISTDATE)=?", (year, month)) or 0)
                if not rows:
                    return f"No visits found for {year}-{month:02d}."
                lines = [f"Visits for {year}-{month:02d} (showing {min(len(rows), max_rows)} of {total}):"]
                for vist_id, vist_date, reason, pet_name, vet_name, clinic_name in rows:
                    ds = vist_date.strftime("%Y-%m-%d") if hasattr(vist_date, "strftime") else str(vist_date)[:10]
                    lines.append(f"- #{vist_id} {ds}: {pet_name or 'Unknown pet'} @ {clinic_name or 'Unknown clinic'} ({vet_name or 'Unknown vet'}) - {reason}")
                if total > max_rows:
                    lines.append(f"(Showing first {max_rows}. Ask for a specific date range or pet/vet name to narrow it down.)")
                return "\n".join(lines)

            # Default: show recent visits
            cur.execute(
                f"""
                SELECT TOP {max_rows} V.VISTID, V.VISTDATE, V.REASON,
                       P.P_NAME, VT.V_NAME, C.C_NAME
                FROM VIST V
                LEFT JOIN PET P ON V.PETID = P.PETID
                LEFT JOIN VETERINARIAN VT ON V.VETID = VT.VETID
                LEFT JOIN CLINIC C ON V.CLINICID = C.CLINICID
                ORDER BY V.VISTDATE DESC
                """
            )
            rows = cur.fetchall()
            total = int(_safe_scalar(cur, "SELECT COUNT(*) FROM VIST") or 0)
            if not rows:
                return "No visits found."
            lines = [f"Latest visits (showing {min(len(rows), max_rows)} of {total}):"]
            for vist_id, vist_date, reason, pet_name, vet_name, clinic_name in rows:
                ds = vist_date.strftime("%Y-%m-%d") if hasattr(vist_date, "strftime") else str(vist_date)[:10]
                lines.append(f"- #{vist_id} {ds}: {pet_name or 'Unknown pet'} @ {clinic_name or 'Unknown clinic'} ({vet_name or 'Unknown vet'}) - {reason}")
            if total > max_rows:
                lines.append(f"(Showing latest {max_rows}. Ask for a month/year like 'June 2024' to filter.)")
            return "\n".join(lines)

        # Owners / Pets / Vets / Clinics: quick lists and counts
        if "owner" in ql and any(k in ql for k in ("how many", "count", "number of")):
            n = _safe_scalar(cur, "SELECT COUNT(*) FROM OWNER")
            return f"There are {int(n or 0)} owner(s) in the database."

        if "pet" in ql and any(k in ql for k in ("how many", "count", "number of")):
            n = _safe_scalar(cur, "SELECT COUNT(*) FROM PET")
            return f"There are {int(n or 0)} pet(s) in the database."

        if any(k in ql for k in ("vet", "veterinarian")) and any(k in ql for k in ("how many", "count", "number of")):
            n = _safe_scalar(cur, "SELECT COUNT(*) FROM VETERINARIAN")
            return f"There are {int(n or 0)} veterinarian(s) in the database."

        if "clinic" in ql and any(k in ql for k in ("how many", "count", "number of")):
            n = _safe_scalar(cur, "SELECT COUNT(*) FROM CLINIC")
            return f"There are {int(n or 0)} clinic(s) in the database."

        if "owner" in ql and any(k in ql for k in ("list", "show", "all")):
            cur.execute(
                f"SELECT TOP {max_rows} OWNERID, O_NAME, PHONE, BILLINGADDRESS FROM OWNER ORDER BY OWNERID DESC"
            )
            rows = cur.fetchall()
            total = int(_safe_scalar(cur, "SELECT COUNT(*) FROM OWNER") or 0)
            if not rows:
                return "No owners found."
            lines = [f"Owners (showing {min(len(rows), max_rows)} of {total}):"]
            for owner_id, name, phone, billing in rows:
                lines.append(f"- #{owner_id}: {name} (phone: {phone or '—'}) (billing: {billing or '—'})")
            if total > max_rows:
                lines.append(f"(Showing latest {max_rows}. Ask for an owner name to narrow it down.)")
            return "\n".join(lines)

        if "pet" in ql and any(k in ql for k in ("list", "show", "all")):
            cur.execute(
                f"""
                SELECT TOP {max_rows} P.PETID, P.P_NAME, P.SPECIE, P.BREED, O.O_NAME
                FROM PET P
                LEFT JOIN OWNER O ON P.OWNERID = O.OWNERID
                ORDER BY P.PETID DESC
                """
            )
            rows = cur.fetchall()
            total = int(_safe_scalar(cur, "SELECT COUNT(*) FROM PET") or 0)
            if not rows:
                return "No pets found."
            lines = [f"Pets (showing {min(len(rows), max_rows)} of {total}):"]
            for pet_id, name, specie, breed, owner_name in rows:
                lines.append(f"- #{pet_id}: {name} ({specie or 'Unknown species'}, {breed or 'Unknown breed'}) owner: {owner_name or '—'}")
            if total > max_rows:
                lines.append(f"(Showing latest {max_rows}. Ask for a pet name/owner name to narrow it down.)")
            return "\n".join(lines)

        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass
