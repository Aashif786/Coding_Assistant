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
def command(context: EditorContext = Body(...)):
    spoken_text = listen_once()
    intent_result = classify_intent(spoken_text)

    if context.language != "python":
        return CommandAPIResponse(
            status="ok",
            action="message",
            text="Voice coding currently supports Python files only",
            intent=intent_result.model_dump()
        )

    generated_code = generate_code(intent_result)

    return CommandAPIResponse(
        status="ok",
        action="intent",
        text=generated_code if generated_code else spoken_text,
        intent=intent_result.model_dump()
    )
