import json
import asyncio
from app.runtime import run_agent_execution_debug

results = []
with open("evals/investigations.json") as f:
  test_cases = json.load(f)

for test_case in test_cases:
  print(test_case["name"])

for test_case in test_cases:
  print("\n" + "=" * 80)
  print(f"RUNNING EVAL: {test_case['name']}")
  print(f"QUERY: {test_case['query']}")
  print("=" * 80)

  response = asyncio.run(run_agent_execution_debug(test_case["query"]))

  print("\nEXPECTED:")
  print(test_case["expected"])

  print("\nAGENT RESPONSE:")
  print(response["final_response"])
  print("\n")
  results.append(
    {
        "name": test_case["name"],
        "query": test_case["query"],
        "expected": test_case.get("expected"),
        "response": response["final_response"]
    }
  )

print("\nSUMMARY")
print("=" * 80)

for result in results:
  print(result["name"])