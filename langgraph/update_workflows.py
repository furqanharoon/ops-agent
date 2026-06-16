from database.connection import get_connection

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
