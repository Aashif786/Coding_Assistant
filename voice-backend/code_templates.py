def python_function_template(name: str | None = None) -> str:
    func_name = name if name else "my_function"
    return f"""
def {func_name}():
    pass
"""
