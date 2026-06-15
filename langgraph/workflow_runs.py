# from connection import get_connection

from app.connection import get_connection
import uuid

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

# thread_id=str(uuid.uuid4())
# create_workflow_run(thread_id)
