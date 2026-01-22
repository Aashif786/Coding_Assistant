from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from response_schema import CommandAPIResponse
from stt_service import listen_once
from intent_service import classify_intent
from code_generator import generate_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class EditorContext(BaseModel):
    language: Optional[str]
    cursorLine: Optional[int]
    hasSelection: Optional[bool]

@app.post("/command", response_model=CommandAPIResponse)
def command(context: dict):

    spoken_text = listen_once()
    intent = classify_intent(spoken_text)

    code = generate_code(
        intent,
        context.get("language")
    )

    if code:
        return {
            "status": "ok",
            "action": "insert",
            "text": code
        }

    return {
        "status": "ok",
        "action": "message",
        "text": f"Unsupported command: {spoken_text}"
    }
