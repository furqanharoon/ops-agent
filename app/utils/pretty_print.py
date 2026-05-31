def print_llm_response(llm_response):
  print("\n" + "=" * 80)
  print("LLM RESPONSE")
  print("=" * 80)

  for block in llm_response.content:
    if block.type == "text":
      print("\nTEXT RESPONSE:\n")
      print(block.text)

    elif block.type == "tool_use":
      print(
          f"\nTOOL -> {block.name}"
      )
      print(
          f"INPUT -> {block.input}"
      )

  print("\nTOKEN USAGE")
  print(
    f"Input: {llm_response.usage.input_tokens}"
  )
  print(
    f"Output: {llm_response.usage.output_tokens}"
  )
