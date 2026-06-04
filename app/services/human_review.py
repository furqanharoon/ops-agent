def request_human_approval():
  response = input("Please Press Y (Yes) to approve the report. Press anyother key to reject it.")
  return response.lower() == 'y'
