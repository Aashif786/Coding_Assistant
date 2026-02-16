import sys
import os

# Add voice-backend to path
sys.path.append(os.path.join(os.getcwd(), 'voice-backend'))

from intent_service import classify_intent

def test_nine_recognition():
    # Test case: "nine fifteen" should become "line 15"
    text = "nine fifteen"
    print(f"Testing input: '{text}'")
    
    result = classify_intent(text)
    
    print(f"Result Intent: {result.intent}")
    print(f"Result Line: {result.line}")
    
    if result.intent == "GOTO_LINE" and result.line == 15:
        print("✅ SUCCESS: 'nine fifteen' correctly interpreted as Line 15")
    else:
        print("❌ FAILURE: Incorrect interpretation")

if __name__ == "__main__":
    test_nine_recognition()
