import json
import asyncio
from app.runtime import run_agent_execution_debug
from app.services.facts_extractor import build_investigation_facts
from app.services.analyzer import analyze_incident
from app.services.report_generator import generate_report
from evals.scoring import compare_facts


results = []
with open("evals/investigations.json") as f:
  test_cases = json.load(f)
all_passed = True
total_tests = 0
passed_tests = 0

for test_case in test_cases:
  total_tests+=1
  test_passed = True
  print("\n" + "=" * 80)
  print(f"RUNNING EVAL: {test_case['name']}")
  print(f"QUERY: {test_case['query']}")
  print("=" * 80)
  response = asyncio.run(run_agent_execution_debug(test_case["query"]))
  if response:
    print("\n\n RESPONSEEEE", response)
    facts = build_investigation_facts(response["incident"], response["duration"], response["timeline"])
    print("\n\n FACTSSSSSS", facts)
    if facts.case_id:
      analyzer = analyze_incident(facts)
      print("\n\n ANALYZER RESULTS", analyzer)
      report_output = generate_report(facts, analyzer)
      print("\n\n report_output", report_output)
    comparison = compare_facts(test_case.get("expected"), facts)
    print("\n COMPARISON VALUESSS \n", comparison.values())
    for result in comparison.values():
      if not result['passed']:
        all_passed = False
        test_passed = False
        break

    print("comparison_results", comparison)
    print("\n ALL PASSED \n", all_passed)
    if test_passed:
      passed_tests+=1
  
  # print("\nEXPECTED:")
  # print(test_case["expected"])


  results.append(
    {
      "name": test_case["name"],
      "query": test_case["query"],
      "expected": test_case.get("expected"),
      "response": response["final_response"]
    }
  )

# print("\nSUMMARY")
# print("=" * 80)

# for result in results:
#   print(result["name"])

print("\n total_tests \n", total_tests)
print("\n passed_tests \n", passed_tests)
pass_rate = (passed_tests/total_tests)*100
print("\n pass_rate \n", pass_rate)
