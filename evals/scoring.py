def compare_facts(expected, actual):
  results = {}
  for field, expected_value in expected.items():
    actual_value = getattr(actual, field)
    results[field] = {
      "expected": expected_value,
      "actual": actual_value,
      "passed": expected_value == actual_value
    }
  return results
