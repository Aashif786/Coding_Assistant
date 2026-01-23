# ========================= #
#    Java Code Templates    #
# ========================= #


def function_template(name: str | None = None) -> str:
    method_name = name if name else "myMethod"
    return f"""public void {method_name}() {{\n
}}
"""


def class_template(name: str | None = None) -> str:
    class_name = name if name else "MyClass"
    return f"""public class {class_name} {{\n

    public {class_name}() {{\n
    }}
}}
"""


def for_loop_template() -> str:
    return """for (int i = 0; i < 10; i++) {\n
}
"""


def while_loop_template() -> str:
    return """while (true) {\n
}
"""


def if_template() -> str:
    return """if (condition) {\n
}
"""


def if_else_template() -> str:
    return """if (condition) {\n
} else {\n
}
"""


def try_catch_template() -> str:
    return """try {\n
} catch (Exception e) {
    e.printStackTrace();
}
"""


def print_template(string: str | None = None) -> str:
    content = string if string else ""
    return f"""System.out.println(\"{content}\");\n"""



def return_template() -> str:
    return """return;"""


def import_template(module: str | None = None) -> str:
    mod = module if module else "java.util.*"
    return f"""import {mod};\n
"""


def main_method_template() -> str:
    return """public static void main(String[] args) {\n
}
"""


def list_template() -> str:
    return """List<Type> list = new ArrayList<>();\n
"""


def map_template() -> str:
    return """Map<KeyType, ValueType> map = new HashMap<>();\n
"""


def lambda_template() -> str:
    return """(x) -> x
"""
