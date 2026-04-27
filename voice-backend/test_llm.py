from llm_service import generate_code_snippet

prompt = "import map"
code = generate_code_snippet(prompt, "python")
print(f"\nResulting Code output:\n{code}")
