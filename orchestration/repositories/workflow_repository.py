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

def get_all_workflows():
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
    """
    SELECT id,thread_id,status,created_at,updated_at
    FROM workflow_runs
    ORDER BY created_at DESC;
    """
  )

  rows = cursor.fetchall()

  workflows = []

  for row in rows:
    workflows.append({
      "id": row[0],
      "thread_id": row[1],
      "status": row[2],
      "created_at": row[3],
      "updated_at": row[4]
    })

  cursor.close()
  conn.close()

  return workflows

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

def delete_workflow(thread_id):
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
    """
    DELETE FROM workflow_runs
    WHERE thread_id = %s
    """,
    (thread_id,)
  )

  conn.commit()
  cursor.close()
  conn.close()

def get_workflow(thread_id):
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute(
    """
    SELECT id,thread_id,status,created_at,updated_at FROM workflow_runs
    WHERE thread_id = %s
    """,
    (thread_id,)
  )
  workflow = cursor.fetchone()

  cursor.close()
  conn.close()
  return workflow
