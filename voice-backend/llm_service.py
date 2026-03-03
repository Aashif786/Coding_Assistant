import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_code_snippet(prompt: str, language: str) -> str | None:
    if not API_KEY:
        print("❌ Error: API_KEY not found in .env")
        return None

    if not language:
        language = "text"

    system_prompt = (
        f"You are a helpful coding assistant. "
        f"The user will give you a natural language instruction. "
        f"You must provide ONLY the code snippet in {language} that performs the instruction. "
        f"Do not include markdown formatting (like ```python), explanations, or extra text. "
        f"Just the raw code. If the instruction is to assign a variable, just output the assignment line."
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000", # Required by OpenRouter
        "X-Title": "VoiceToCode"
    }
    data = {
        "model": "stepfun/step-3.5-flash:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        code = result['choices'][0]['message']['content'].strip()
        # Cleanup if model still adds markdown blocks despite instructions
        if code.startswith("```"):
            code = code.split("\n", 1)[1]
        if code.endswith("```"):
            code = code.rsplit("\n", 1)[0]
        return code.strip()
    except Exception as e:
        print(f"❌ Error calling OpenRouter: {e}")
        return None
