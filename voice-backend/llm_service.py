import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Groq free tier: 30 req/min, sub-second responses
MODELS = [
    "llama-3.3-70b-versatile",   # best quality
    "llama3-8b-8192",            # fast fallback
    "mixtral-8x7b-32768",        # secondary fallback
]

def _clean_code(code: str) -> str:
    """Strip markdown fences if the model added them despite instructions."""
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:])
    if code.endswith("```"):
        code = code.rsplit("\n", 1)[0]
    return code.strip()

def generate_code_snippet(prompt: str, language: str) -> str | None:
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found in .env")
        return None

    if not language:
        language = "python"

    system_prompt = (
        f"You are a helpful coding assistant. "
        f"The user will give you a natural language instruction. "
        f"You must provide ONLY the code snippet in {language} that performs the instruction. "
        f"Do not include markdown formatting (like ```python), explanations, or extra text. "
        f"Just the raw code. If the instruction is to assign a variable, just output the assignment line."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    for model in MODELS:
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            print(f"🤖 Trying model: {model}")
            response = requests.post(
                GROQ_URL,
                headers=headers,
                json=data,
                timeout=20
            )

            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 5))
                print(f"⏳ Rate limited. Waiting {wait}s before next model...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            result = response.json()
            code = result['choices'][0]['message']['content'].strip()
            print(f"✅ Success with model: {model}")
            return _clean_code(code)

        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout with model {model}, trying next...")
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Connection error with model {model}: {e}, trying next...")
        except Exception as e:
            print(f"❌ Error with model {model}: {e}, trying next...")

    print("❌ All models failed.")
    return None
