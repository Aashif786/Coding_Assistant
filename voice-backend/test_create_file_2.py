from intent_service import classify_intent

phrase = "create file test2.py"
res = classify_intent(phrase)
print(f"\nPhrase: '{phrase}'")
print(f"Intent:  '{res.intent}'")
print(f"Name:    '{res.name}'")
if res.intent == "GENERATE_CODE_SNIPPET":
    print("WARNING: Triggered AI fallback on target CREATE_FILE phrase!")
