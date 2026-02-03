
import re
from text_normalizer import normalize_text

def test_extraction(text):
    print(f"Original: '{text}'")
    normalized = normalize_text(text)
    print(f"Normalized: '{normalized}'")
    
    match = re.search(r"line\s+(\d+)", normalized)
    if match:
        print(f"Extracted Line: {match.group(1)}")
    else:
        print("No line number extracted")
    print("-" * 20)

cases = [
    "line twenty",
    "line 20",
    "line two zero",
    "remove line 5",
    "goto line 40"
]

for c in cases:
    test_extraction(c)
