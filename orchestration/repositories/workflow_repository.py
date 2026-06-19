from database.connection import get_connection

def create_workflow_run(thread_id):
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
      """
      INSERT INTO workflow_runs
      (thread_id, status)
      VALUES (%s, %s)
      """,
      (thread_id, "running")
  )

  conn.commit()

  cursor.close()
  conn.close()

def update_workflow_status(thread_id, status):
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
    """
    UPDATE workflow_runs
    SET status = %s,
        updated_at = CURRENT_TIMESTAMP
      WHERE thread_id = %s
    """,
    (status, thread_id)
  )

  conn.commit()

  cursor.close()
  conn.close()
