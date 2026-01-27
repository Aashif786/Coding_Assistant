from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from response_schema import CommandAPIResponse
from stt_service import listen_once
from intent_service import classify_intent
from code_generator import generate_code

class DebugRequest(BaseModel):
    line: int = 20

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
    print(f"🎤 Speech recognized: '{spoken_text}'")  # Debug
    
    intent = classify_intent(spoken_text)
    print(f"🎯 Intent classified: {intent}")  # Debug

    total_lines = context.get("totalLines", 1)
    
    # Handle GOTO_LINE intent
    if intent.intent == "GOTO_LINE":
        line_number = int(intent.name) if intent.name else 1
        print(f"📍 Moving cursor to line: {line_number}")  # Debug
        
        return CommandAPIResponse(
            status="ok",
            action="move_cursor",
            line=line_number,
            text=f"Moved to line {line_number}"
        )
    code = generate_code(
        intent,
        context.get("language")
    )

    if code:
        # For insert actions
        return CommandAPIResponse(
            status="ok",
            action="insert",
            text=code,
            line=None  # No line for insert actions
        )

    # For unsupported commands
    return CommandAPIResponse(
        status="ok",
        action="message",
        text=f"Unsupported command: {spoken_text}",
        line=None
    )

@app.post("/debug_goto")
async def debug_goto(request: DebugRequest):
    """Simple test endpoint for cursor movement"""
    print(f"🧪 Debug goto requested: line {request.line}")
    
    return CommandAPIResponse(
        status="ok",
        action="move_cursor",
        line=request.line,
        text=f"Test: Moving to line {request.line}"
    )