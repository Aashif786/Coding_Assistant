from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/command", response_model=CommandAPIResponse)
def command():
    spoken_text = listen_once()
    intent_result = classify_intent(spoken_text)
    generated_code = generate_code(intent_result)

    return CommandAPIResponse(
        status="ok",
        action="intent",
        text=generated_code if generated_code else spoken_text,
        intent=intent_result.model_dump()
    )
