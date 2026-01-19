from intent_schema import IntentResult

def classify_intent(text: str) -> IntentResult:
    text = text.lower()

    if "function" in text:
        return IntentResult(
            intent="GENERATE_FUNCTION",
            language="python" ,# if "python" in text else None,
            name=None
        )

    if "loop" in text:
        return IntentResult(intent="ADD_LOOP")

    if "run" in text:
        return IntentResult(intent="RUN_CODE")

    return IntentResult(intent="UNKNOWN")
