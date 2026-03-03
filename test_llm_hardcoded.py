import requests

# Hardcoding the key to test if it's an env loading issue
# User provided: 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
API_KEY = "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"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "VoiceToCode Debug"
}

data = {
    "model": "microsoft/phi-3-mini-128k-instruct:free",
    "messages": [
        {"role": "user", "content": "print hello world"}
    ]
}

print(f"Testing with HARDCODED key...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
