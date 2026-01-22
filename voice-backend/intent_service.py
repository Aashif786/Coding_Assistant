from intent_schema import IntentResult

def classify_intent(text: str) -> IntentResult:
    text = text.lower()
    
    if "function" in text:
        return IntentResult(
            intent="GENERATE_FUNCTION",
            language="python" if "python" in text else None,
            name= text.split()[1 + text.split().index('function')]
        )

    if "for"in text:
        return IntentResult(
            intent="ADD_WHILE_LOOP",
            language="python" if "python" in text else None
        )
    
    if "while"in text:
        return IntentResult(
            intent="ADD_WHILE_LOOP",
            language="python" if "python" in text else None
        )

    if "class"in text:
        return IntentResult(
            intent="GENERATE_CLASS",
            language="python" if "python" in text else None
        )


    if "print" in text:
        return IntentResult(
            intent="PRINT",
            language="python" if "python" in text else None
        )
    
    if "run" in text:
        return IntentResult(
            intent="RUN_CODE",
            language= None
        )

    return IntentResult(intent="UNKNOWN")
