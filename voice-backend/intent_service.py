import re
from intent_schema import IntentResult
from text_normalizer import normalize_text

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
    
    print(f"🔍 Original text: '{text}'")  # Debug
    normalized_text = normalize_text(text)
    print(f"🔍 Normalized text: '{normalized_text}'")  # Debug
    
    if "line" in normalized_text:
        print(f"🔍 Found 'line' in text")  # Debug
        match = re.search(r"line\s+(\d+)", normalized_text)
        if match:
            line_num = match.group(1)
            print(f"🔍 Extracted line number: {line_num}")  # Debug
            return IntentResult(
                intent="GOTO_LINE",
                name=line_num
            )

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
            intent="PRINT",
            name= " ".join(text.split()[1:])
        )

    if "run" in text:
        return IntentResult(
            intent="RUN_CODE"
        )

    return IntentResult(intent="UNKNOWN")
