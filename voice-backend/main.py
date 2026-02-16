from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from response_schema import CommandAPIResponse
from stt_service import listen_once # LINE 29
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
    totalLines: Optional[int]
    mock_text: Optional[str] = None

@app.post("/command", response_model=CommandAPIResponse)
def command(context: dict):
    # Check for mock text from simulation command
    if context.get("mock_text"):
        spoken_text = context["mock_text"]
        print(f"🧪 Using mock text: {spoken_text}")
    else:
        spoken_text = listen_once()

    if not spoken_text:
        return {
            "status": "ok",
            "action": "message",
            "text": "No voice command detected"
        }
    intent = classify_intent(spoken_text)
    print(f"🎯 Intent classified: {intent}")  # Debug

    total_lines = context.get("totalLines", 1)
    # Handle GOTO_LINE intent
    if intent.intent == "GOTO_LINE":
        line_number = intent.line if intent.line is not None else (int(intent.name) if intent.name else 1)
        print(f"📍 Moving cursor to line: {line_number}")  # Debug
        
        return CommandAPIResponse(
            status="ok",
            action="move_cursor",
            line=line_number,
            text=f"Moved to line {line_number}"
        )
      
    # Handle REMOVE_LINE intent
    if intent.intent == "REMOVE_LINE":
        line_number = intent.line  # Can be None (current line) or a specific line
        print(f"🗑 Requesting removal of line: {line_number if line_number else 'Current'}")
        
        return CommandAPIResponse(
            status="ok",
            action="remove_line",
            line=line_number,
            text=f"Removed line {line_number if line_number else ''}"
        )

    if intent.intent == "COMMENT_LINE":
        return CommandAPIResponse(status="ok", action="comment_line", text="Commenting line")

    if intent.intent == "UNCOMMENT_LINE":
        return CommandAPIResponse(status="ok", action="uncomment_line", text="Uncommenting line")

    if intent.intent == "GOTO_TOP":
        return CommandAPIResponse(status="ok", action="goto_top", text="Moving to top")

    if intent.intent == "GOTO_BOTTOM":
        return CommandAPIResponse(status="ok", action="goto_bottom", text="Moving to bottom")

    if intent.intent == "DUPLICATE_LINE":
        return CommandAPIResponse(status="ok", action="duplicate_line", text="Duplicating line")

    if intent.intent == "RUN_CODE":
        return CommandAPIResponse(
            status="ok",
            action="run_code",
            text="Running code..."
        )

    if intent.intent == "UNDO":
        return CommandAPIResponse(
            status="ok",
            action="undo",
            text="Undoing..."
        )

    if intent.intent == "REDO":
        return CommandAPIResponse(
            status="ok",
            action="redo",
            text="Redoing..."
        )

    if intent.intent == "REDO":
        return CommandAPIResponse(
            status="ok",
            action="redo",
            text="Redoing..."
        )

    if intent.intent == "STOP_LISTENING":
        return CommandAPIResponse(
            status="ok",
            action="stop_listening",
            text="Deactivating voice mode..."
        )

    if intent.intent == "GOTO_DEFINITION":
        return CommandAPIResponse(
            status="ok",
            action="goto_definition",
            text=f"Going to {intent.name or 'definition'}",
            name=intent.name
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

