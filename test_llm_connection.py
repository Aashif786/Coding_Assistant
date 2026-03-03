import os
import requests
import json
from dotenv import load_dotenv

# Load env from voice-backend/.env
# Assuming we run this from project root
dotenv_path = os.path.join("voice-backend", ".env")
load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")
if API_KEY:
    print(f"API Key loaded (repr): {repr(API_KEY)}")
    print(f"API Key length: {len(API_KEY)}")
else:
    print("API Key NOT found")

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "VoiceToCode Debug"
}

data = {
    "model": "google/gemini-2.0-flash-lite-preview-02-05:free", # Trying a different free model
    "messages": [
        {"role": "user", "content": "print hello world"}
    ]
}

print(f"Testing URL: {url}")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
