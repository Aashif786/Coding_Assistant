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
        f"You are a strict code inserter for an IDE.\n"
        f"Your job is to convert the user's instruction into code in {language}.\n\n"

        f"CRITICAL RULES:\n"
        f"- Output ONLY code. No explanations, no markdown, no comments.\n"
        f"- DO NOT assume or invent any values, variables, or logic not explicitly mentioned.\n"
        f"- DO NOT add default values (e.g., do not assign numbers like p=10 unless specified).\n"
        f"- DO NOT complete or expand the logic beyond the user's request.\n"
        f"- If the instruction is incomplete, generate a minimal structural template ONLY.\n"
        f"- Use variable names exactly as given, without defining them unless explicitly requested.\n\n"

        f"Your output must be the most minimal valid code that matches the instruction.\n"
        f"No additions. No assumptions. No enhancements."
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

def query_llm(system_prompt: str, user_prompt: str) -> str | None:
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found in .env")
        return None

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    for model in MODELS:
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        try:
            print(f"🤖 Querying {model}...")
            response = requests.post(GROQ_URL, headers=headers, json=data, timeout=20)
            
            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 5))
                time.sleep(wait)
                continue

            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except Exception as e:
            print(f"❌ Error with model {model}: {e}")
            continue

    return None
