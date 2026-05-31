from app.db import get_connection

async def get_incident(case_id: str):
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute("""
          SELECT
            case_id,priority,reporter,issue_type,short_description,customer_satisfaction
            FROM incidents where case_id = %s""",(case_id,))
      row=cursor.fetchone()
      if not row:
        return {
          "error": f"Incident with {case_id} not found"
        }
      return {
        "case_id": row[0],
        "priority": row[1],
        "reporter": row[2],
        "issue_type": row[3],
        "short_description": row[4],
        "customer_satisfaction": row[5]
      }
  finally:
    conn.close()

async def get_incident_duration(case_id: str):
  conn = get_connection()

  try:
    with conn.cursor() as cursor:
      cursor.execute("""
          SELECT
              MIN(event_timestamp),
              MAX(event_timestamp)
            FROM events
            WHERE case_id = %s
        """, (case_id,))

      row = cursor.fetchone()

      if not row or not row[0]:
        return {
          "error": f"Incident {case_id} not found"
        }

      duration = row[1] - row[0]
      # raise Exception("Simulated DB timeout")
      return {
        "case_id": case_id,
        "opened_at": row[0].isoformat(),
        "closed_at": row[1].isoformat(),
        "duration": str(duration)
      }
  finally:
    conn.close()

async def get_incident_timeline(case_id: str):
  conn = get_connection()

  try:
    with conn.cursor() as cursor:
      cursor.execute("""
        SELECT
            event_timestamp,
            event_type,
            resolver
        FROM events
        WHERE case_id = %s
        ORDER BY event_timestamp
        """, (case_id,))
      
      rows = cursor.fetchall()

      return [
        {
          "timestamp": row[0].isoformat(),
          "event_type": row[1],
          "resolver": row[2]
        }
        for row in rows
      ]
  finally:
    conn.close()
