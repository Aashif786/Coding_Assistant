import re
from intent_schema import IntentResult
from text_normalizer import normalize_text

def extract_name(text: str) -> str | None:
    words = text.split()
    
    keywords = ["function", "class", "variable", "find", "goto", "go to"]
    target_idx = -1
    
    # Find the keyword that triggers the name extraction
    for kw in keywords:
        if kw in text:
            try:
                # Handle "go to" separate from "goto"
                if kw == "go to":
                    target_idx = text.find("go to") + 5
                    break
                
                # Check for word boundary
                if kw in words:
                   target_idx = text.find(kw) + len(kw) + 1
                   break
            except:
                continue

    if target_idx != -1 and target_idx < len(text):
        raw_name = text[target_idx:].strip()
        # Convert "calculate total price" -> "calculate_total_price"
        return raw_name.replace(" ", "_")
        
    return None


def classify_intent(text: str) -> IntentResult:
    
    print(f"🔍 Original text: '{text}'")  # Debug
    normalized_text = normalize_text(text)
    print(f"🔍 Normalized text: '{normalized_text}'")  # Debug

    # Heuristic: "nine" often sounds like "line", and "9" at start is rarely a command on its own.
    if normalized_text.startswith("9 "):
        normalized_text = normalized_text.replace("9 ", "line ", 1)
        print(f"🔄 Adjusted '9' -> 'line': '{normalized_text}'")

    
    # 1. STOP COMMANDS (High Priority)
    stop_keywords = ["stop listening", "deactivate", "exit voice", "kill", "exit", "shut down", "stop"]
    if any(kw in normalized_text for kw in stop_keywords):
        return IntentResult(intent="STOP_LISTENING")

    if "remove line" in normalized_text or "delete line" in normalized_text:
        match = re.search(r"line\s+(\d+)", normalized_text)
        if match:
            line_num = int(match.group(1))
            return IntentResult(intent="REMOVE_LINE", line=line_num)
        return IntentResult(intent="REMOVE_LINE", name=None)

    if "line" in normalized_text: 
        match = re.search(r"line\s+(\d+)", normalized_text) 
        if match: 
            line_num = int(match.group(1))
            return IntentResult(intent="GOTO_LINE", line=line_num)

    # Function/Class Generation
    if "function" in normalized_text and "create" in normalized_text:
        return IntentResult(
            intent="GENERATE_FUNCTION",
            name=extract_name(normalized_text)
        )
    
    if "class" in normalized_text and "create" in normalized_text:
        return IntentResult(
            intent="GENERATE_CLASS",
            name=extract_name(normalized_text)
        )

    # Advanced Navigation (Go to / Find)
    if "go to" in normalized_text or "find" in normalized_text:
        # Avoid conflict with "go to line"
        if "line" not in normalized_text:
            return IntentResult(
                intent="GOTO_DEFINITION",
                name=extract_name(normalized_text)
            )

    if "function" in normalized_text:
        return IntentResult(
            intent="GENERATE_FUNCTION",
            name=extract_name(normalized_text)
        )

    if "class" in normalized_text:
        return IntentResult(
            intent="GENERATE_CLASS",
            name=extract_name(normalized_text)
        )

    if "for" in normalized_text:
        return IntentResult(intent="ADD_FOR_LOOP")

    if "while" in normalized_text:
        return IntentResult(intent="ADD_WHILE_LOOP")

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
        return IntentResult(intent="RUN_CODE")

    if "undo" in normalized_text:
        return IntentResult(intent="UNDO")

    if "redo" in normalized_text:
        return IntentResult(intent="REDO")
    
    return IntentResult(intent="UNKNOWN")
