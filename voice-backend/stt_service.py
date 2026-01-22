import sounddevice as sd
import numpy as np
import soundfile as sf
import tempfile
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
RECORD_SECONDS = 4  # good for voice commands

# Load model ONCE (important for performance)
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"  # faster & lower memory
)

def record_audio():
    print("🎤 Listening for command...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    return audio.squeeze()

def listen_once():
    audio_data = record_audio() 

    # Save to temp WAV (Whisper expects audio input)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        sf.write(tmp.name, audio_data, SAMPLE_RATE)

        segments, _ = model.transcribe(
            tmp.name,
            language="en",
            beam_size=5
        )

        text = ""
        for segment in segments:
            text += segment.text

        text = text.strip()

        if text:
            print("📝 Recognized:", text)
            return text

        return ""
