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
    
    if "remove line" in normalized_text or "delete line" in normalized_text:

        match = re.search(r"line\s+(\d+)", normalized_text)

        if match:

            line_num = int(match.group(1))
            print(f"🗑 Removing line number: {line_num}")
            return IntentResult(intent="REMOVE_LINE", line=line_num)

        # no line number → remove current line
        return IntentResult(
            intent="REMOVE_LINE",
            name=None
        )

    if "line" in normalized_text: 
        match = re.search(r"line\s+(\d+)", normalized_text) 
        if match: 
            line_num = int(match.group(1))
            print(f"🔍 Extracted line number: {line_num}") 
            return IntentResult(intent="GOTO_LINE", line=line_num)

    if "function" in normalized_text:
        return IntentResult(
            intent="GENERATE_FUNCTION",
            name=extract_name(normalized_text)
        )

    if "for" in normalized_text:
        return IntentResult(
            intent="ADD_FOR_LOOP"
        )

    if "while" in normalized_text:
        return IntentResult(
            intent="ADD_WHILE_LOOP"
        )

    if "class" in normalized_text:
        return IntentResult(
            intent="GENERATE_CLASS",
            name=extract_name(normalized_text)
        )

    if "print" in normalized_text:
        return IntentResult(
            intent="PRINT",
            name= " ".join(normalized_text.split()[1:])
        )



    if "comment" in normalized_text and "uncomment" not in normalized_text:
        return IntentResult(intent="COMMENT_LINE")

    if "uncomment" in normalized_text:
        return IntentResult(intent="UNCOMMENT_LINE")

    if "top" in normalized_text:
        return IntentResult(intent="GOTO_TOP")

    if "bottom" in normalized_text:
        return IntentResult(intent="GOTO_BOTTOM")

    if "duplicate" in normalized_text or "control shift down" in normalized_text:
        return IntentResult(intent="DUPLICATE_LINE")

    if "run" in normalized_text:
        return IntentResult(
            intent="RUN_CODE"
        )

    if "undo" in normalized_text:
        return IntentResult(intent="UNDO")

    if "redo" in normalized_text:
        return IntentResult(intent="REDO")
    

    return IntentResult(intent="UNKNOWN")
