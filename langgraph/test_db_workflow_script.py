from langgraph.workflow_runs import (
  create_workflow_run
)
from langgraph.update_workflows import update_workflow_status
import uuid

# thread_id = "test-workflow-1"
# thread_id=str(uuid.uuid4())

# create_workflow_run(thread_id)

thread_id = "cf9facc7-27ef-49f1-a488-2abae896925c"
update_workflow_status(
  thread_id,
  "waiting_for_approval"
)

print("Done")
