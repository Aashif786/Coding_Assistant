from intent_schema import IntentResult
from code_templates import python_templates, java_templates, c_templates, js_templates

LANGUAGE_TEMPLATES = {
    "python": python_templates,
    "java": java_templates,
    "c": c_templates,
    "js": js_templates
}

def generate_code(intent: IntentResult, language: str | None):

    template = LANGUAGE_TEMPLATES.get(language.lower()) if language else None

    if not template:
        return None

    match intent.intent:
        case "GENERATE_FUNCTION":
            return template.function_template(intent.name)

        case "GENERATE_CLASS":
            return template.class_template(intent.name)

        case "ADD_FOR_LOOP":
            return template.for_loop_template()

        case "ADD_WHILE_LOOP":
            return template.while_loop_template()

        case "PRINT":
            return template.print_template(intent.name or "")

        case _:
            return None

