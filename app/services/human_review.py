def request_human_approval()-> tuple[bool, str| None]:
  response = input("Please Press Y (Yes) to approve the report. Press anyother key to reject it.")
  reason=None
  approved = response.lower() == 'y'

  if not approved:
    while True:
      reason=input("\n Please enter a reason to deny this request. Its mandatory to add reason.\n").strip()
      if reason:
        break
  return approved,reason
