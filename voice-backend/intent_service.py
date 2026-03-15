import re
from intent_schema import IntentResult
from text_normalizer import normalize_text

def extract_name(text: str) -> str | None:
    words = text.split()
    # Updated to avoid collisions with general phrases
    keywords = ["definition", "goto", "go to"]
    target_idx = -1
    for kw in keywords:
        if kw in text:
            try:
                if kw == "go to":
                    target_idx = text.find("go to") + 5
                    break
                if kw in words:
                   target_idx = text.find(kw) + len(kw) + 1
                   break
            except:
                continue
    if target_idx != -1 and target_idx < len(text):
        raw_name = text[target_idx:].strip()
        return raw_name.replace(" ", "_")
    return None

def classify_intent(text: str) -> IntentResult:
    print(f"🔍 Original text: '{text}'")
    normalized_text = normalize_text(text)
    print(f"🔍 Normalized text: '{normalized_text}'")

    if normalized_text.startswith("9 "):
        normalized_text = normalized_text.replace("9 ", "line ", 1)
        print(f"🔄 Adjusted '9' -> 'line': '{normalized_text}'")
    
    # 1. STOP COMMANDS (High Priority)
    stop_keywords = ["stop listening", "deactivate", "exit voice", "kill", "exit", "shut down", "stop"]
    if any(kw in normalized_text for kw in stop_keywords):
        return IntentResult(intent="STOP_LISTENING")

    # 2. FILE OPERATIONS
    if "create" in normalized_text and "file" in normalized_text:
        instruction = normalized_text.replace("create", "", 1).replace("file", "", 1).strip()
        return IntentResult(intent="CREATE_FILE", name=instruction)
    if "open" in normalized_text and "file" in normalized_text:
        name = normalized_text.replace("open", "", 1).replace("file", "", 1).strip()
        return IntentResult(intent="OPEN_FILE", name=name)
    if "save" in normalized_text:
        return IntentResult(intent="SAVE_FILE")
    if "close" in normalized_text and ("file" in normalized_text or "this" in normalized_text or "tab" in normalized_text):
        return IntentResult(intent="CLOSE_FILE")

    # 3. CLIPBOARD & SELECTION
    if "select all" in normalized_text:
        return IntentResult(intent="SELECT_ALL")
    if "copy" in normalized_text:
        return IntentResult(intent="COPY")
    if "paste" in normalized_text:
        return IntentResult(intent="PASTE")

    # 4. AI DEBUGGING & FIXING
    if "explain error" in normalized_text:
        return IntentResult(intent="EXPLAIN_ERROR")
    if "fix" in normalized_text and "error" in normalized_text:
        return IntentResult(intent="FIX_ERROR")
    if "debug" in normalized_text:
        match = re.search(r"line\s+(\d+)", normalized_text)
        line_num = int(match.group(1)) if match else None
        return IntentResult(intent="DEBUG_ERROR", line=line_num)

    # 5. LINE & NAVIGATION OPERATIONS
    if "remove line" in normalized_text or "delete line" in normalized_text:
        match = re.search(r"line\s+(\d+)", normalized_text)
        if match:
             return IntentResult(intent="REMOVE_LINE", line=int(match.group(1)))
        return IntentResult(intent="REMOVE_LINE")
        
    if "line" in normalized_text:
        match = re.search(r"line\s+(\d+)", normalized_text)
        if match:
            return IntentResult(intent="GOTO_LINE", line=int(match.group(1)))

    # Use explicit phrase to avoid collision with general instructions
    if "go to definition" in normalized_text:
        return IntentResult(intent="GOTO_DEFINITION", name=extract_name(normalized_text))

    if "comment" in normalized_text and "uncomment" not in normalized_text:
        return IntentResult(intent="COMMENT_LINE")
    if "uncomment" in normalized_text:
        return IntentResult(intent="UNCOMMENT_LINE")
    if "toggle comment" in normalized_text:
        return IntentResult(intent="TOGGLE_COMMENT")

    if "top" in normalized_text:
        return IntentResult(intent="GOTO_TOP")
    if "bottom" in normalized_text:
        return IntentResult(intent="GOTO_BOTTOM")
    if "start of line" in normalized_text:
        return IntentResult(intent="GO_TO_START_OF_LINE")
    if "end of line" in normalized_text:
        return IntentResult(intent="GO_TO_END_OF_LINE")

    if "duplicate" in normalized_text or "control shift down" in normalized_text:
        return IntentResult(intent="DUPLICATE_LINE")
    if "cut" in normalized_text:
        return IntentResult(intent="CUT")

    if "find" in normalized_text and "file" not in normalized_text:
        return IntentResult(intent="FIND")
    if "replace" in normalized_text:
        return IntentResult(intent="REPLACE")

    if "new line above" in normalized_text:
        return IntentResult(intent="NEW_LINE_ABOVE")
    if "new line below" in normalized_text:
        return IntentResult(intent="NEW_LINE_BELOW")

    if "delete word" in normalized_text:
        return IntentResult(intent="DELETE_WORD")
    if "select word" in normalized_text:
        return IntentResult(intent="SELECT_WORD")
    if "select line" in normalized_text:
        return IntentResult(intent="SELECT_LINE")

    if "run" in normalized_text:
        return IntentResult(intent="RUN_CODE")
    if "undo" in normalized_text:
        return IntentResult(intent="UNDO")
    if "redo" in normalized_text:
        return IntentResult(intent="REDO")

    # DEFAULT: Any unhandled text is sent to the AI snippet generator
    return IntentResult(intent="GENERATE_CODE_SNIPPET", name=normalized_text)
