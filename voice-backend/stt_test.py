import whisper
import sounddevice as sd
import numpy as np

def test_whisper():
    print("🧠 Loading Whisper 'base' model...")
    model = whisper.load_model("base")
    
    fs = 16000
    duration = 5  # seconds
    print(f"🎤 Recording for {duration} seconds...")
    
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    
    print("🔍 Transcribing...")
    audio = recording.flatten()
    result = model.transcribe(audio, fp16=False)
    
    print("-" * 30)
    print("📝 Transcribed Text:")
    print(result.get("text", "").strip())
    print("-" * 30)

if __name__ == "__main__":
    test_whisper()
