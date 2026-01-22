# ========================= #
#   Python Code Templates   #
# ========================= #


def function_template(name: str | None = None) -> str:
    func_name = name if name else "my_function"
    return f"""def {func_name}():
    pass
"""


def class_template(name: str | None = None) -> str:
    class_name = name if name else "MyClass"
    return f"""class {class_name}:
    def __init__(self):
        pass
"""


def for_loop_template() -> str:
    return """for i in range( : ):
    pass
"""


def while_loop_template() -> str:
    return """while True:
    pass
"""


def if_template() -> str:
    return """if condition:
    pass
"""


def if_else_template() -> str:
    return """if condition:
    pass
else:
    pass
"""


def try_except_template() -> str:
    return """try:
    pass
except Exception as e:
    print(e)
"""


def print_template() -> str:
    return """print()"""


def return_template() -> str:
    return """return """


def import_template(module: str | None = None) -> str:
    mod = module if module else "module_name"
    return f"""import {mod}
"""


def main_guard_template() -> str:
    return """if __name__ == "__main__":
    pass
"""


def list_comprehension_template() -> str:
    return """[x for x in iterable]
"""


def dict_template() -> str:
    return """my_dict = {
    "key": "value"
}
"""


def lambda_template() -> str:
    return """lambda x: x
"""


def decorator_template() -> str:
    return """def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
"""
