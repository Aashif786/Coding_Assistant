from intent_schema import IntentResult
from code_templates import python_templates, java_templates, c_templates, js_templates

LANGUAGE_TEMPLATES = {
    "python": python_templates,
    "java": java_templates,
    "c": c_templates,
    "js": js_templates
}

def generate_code(intent: IntentResult, language: str | None):

    if intent.intent == "GENERATE_FUNCTION":
        if not language :
            return None
        code = LANGUAGE_TEMPLATES.get(language.lower())
        
        if not code :
            return None
        return code.function_template(intent.name)

    if intent.intent == "PRINT":
        if not language :
            return None
        code = LANGUAGE_TEMPLATES.get(language.lower())

        if not code :
            return None
        return code.print_template(intent.name)

    if intent.intent == "GENERATE_CLASS":
        if not language :
            return None
        code = LANGUAGE_TEMPLATES.get(language.lower())

        if not code :
            return None
        return code.class_template(intent.name)

    if intent.intent == "ADD_WHILE_LOOP":
        if not language :
            return None
        code = LANGUAGE_TEMPLATES.get(language.lower())

        if not code :
            return None
        return code.while_loop_template()(intent.name)

    if intent.intent == "ADD_FOR_LOOP":
        if not language :
            return None
        code = LANGUAGE_TEMPLATES.get(language.lower())

        if not code :
            return None
        return code.for_loop_template()(intent.name)

    if intent.intent == "RUN_CODE":
        ...

    return None