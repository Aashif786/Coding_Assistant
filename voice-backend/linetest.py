from intent_service import classify_intent
from text_normalizer import normalize_text

# Test cases
test_cases = [
    "line twenty",
    "line 20",
    "lane twenty",
    "line nineteen",
    "go to line five",
    "move to line eight",
]

for test in test_cases:
    print(f"\nTest: '{test}'")
    normalized = normalize_text(test)
    print(f"Normalized: '{normalized}'")
    intent = classify_intent(test)
    print(f"Intent: {intent.intent}, Line: {intent.name}")