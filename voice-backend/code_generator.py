from intent_schema import IntentResult
from code_templates import python_function_template

def generate_code(intent: IntentResult) -> str | None:

    if intent.intent == "GENERATE_FUNCTION":
        return python_function_template(intent.name)

    return None
