# ========================= #
#    Java Code Templates    #
# ========================= #


def function_template(name: str | None = None) -> str:
    method_name = name if name else "myMethod"
    return f"""public void {method_name}() {{
}}
"""


def class_template(name: str | None = None) -> str:
    class_name = name if name else "MyClass"
    return f"""public class {class_name} {{

    public {class_name}() {{
    }}
}}
"""


def for_loop_template() -> str:
    return """for (int i = 0; i < 10; i++) {
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


def try_catch_template() -> str:
    return """try {
} catch (Exception e) {
    e.printStackTrace();
}
"""


def print_template() -> str:
    return """System.out.println();
"""


def return_template() -> str:
    return """return;
"""


def import_template(module: str | None = None) -> str:
    mod = module if module else "java.util.*"
    return f"""import {mod};
"""


def main_method_template() -> str:
    return """public static void main(String[] args) {
}
"""


def list_template() -> str:
    return """List<Type> list = new ArrayList<>();
"""


def map_template() -> str:
    return """Map<KeyType, ValueType> map = new HashMap<>();
"""


def lambda_template() -> str:
    return """(x) -> x
"""
