from intent_schema import IntentResult

def extract_name(text: str) -> str | None:
    words = text.split()

    if "function" in words:
        idx = words.index("function")
        if idx + 1 < len(words):
            return words[idx + 1]
        
    if "class" in words:
        idx = words.index("class")
        if idx + 1 < len(words):
            return words[idx + 1]
    return None


def classify_intent(text: str) -> IntentResult:
    text = text.lower()

    if "function" in text:
        return IntentResult(
            intent="GENERATE_FUNCTION",
            name=extract_name(text)
        )

    if "for" in text:
        return IntentResult(
            intent="ADD_FOR_LOOP"
        )

    if "while" in text:
        return IntentResult(
            intent="ADD_WHILE_LOOP"
        )

    if "class" in text:
        return IntentResult(
            intent="GENERATE_CLASS",
            name=extract_name(text)
        )

    if "print" in text:
        return IntentResult(
            intent="PRINT"
        )

    if "run" in text:
        return IntentResult(
            intent="RUN_CODE"
        )

    return IntentResult(intent="UNKNOWN")
