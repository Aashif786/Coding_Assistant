import sys
import os

# Add voice-backend to path
sys.path.append(os.path.join(os.getcwd(), 'voice-backend'))

from intent_service import classify_intent
from text_normalizer import normalize_text

def test_class_recognition():
    test_cases = [
        ("class User", "GENERATE_CLASS", "User"),
        ("flash class User", "GENERATE_CLASS", "User"),
        ("make class Product", "GENERATE_CLASS", "Product"),
        ("create class Order", "GENERATE_CLASS", "Order")
    ]
    
    print("🧪 Testing Class Generation Intents...")
    
    for text, expected_intent, expected_name in test_cases:
        print(f"\nInput: '{text}'")
        # Check normalization first to see "flash" -> "create"
        norm = normalize_text(text)
        print(f"Normalized: '{norm}'")
        
        result = classify_intent(text)
        print(f"Result: {result.intent}, Name: {result.name}")
        
        if result.intent == expected_intent:
            if result.name == expected_name:
                print("✅ PASS")
            else:
                print(f"⚠️ Intent match, but name mismatch (Expected {expected_name}, got {result.name})")
        else:
            print(f"❌ FAIL (Expected {expected_intent}, got {result.intent})")

if __name__ == "__main__":
    test_class_recognition()
