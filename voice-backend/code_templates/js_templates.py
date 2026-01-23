# =========================  #
#  JavaScript Code Templates #
# =========================  #


def function_template(name: str | None = None) -> str:
    func_name = name if name else "myFunction"
    return f"""function {func_name}() {{
}}
"""


def arrow_function_template(name: str | None = None) -> str:
    func_name = name if name else "myFunction"
    return f"""const {func_name} = () => {{
}};
"""


def for_loop_template() -> str:
    return """for (let i = 0; i < 10; i++) {
}
"""


def while_loop_template() -> str:
    return """while (true) {
}
"""


def if_template() -> str:
    return """if (condition) {
}
"""


def if_else_template() -> str:
    return """if (condition) {
} else {
}
"""


def console_log_template() -> str:
    return """console.log();
"""


def return_template() -> str:
    return """return;
"""


def import_template(module: str | None = None) -> str:
    mod = module if module else "module"
    return f"""import {{ }} from '{mod}';
"""
