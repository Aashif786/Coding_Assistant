import os
import io
import wave
import numpy as np
import sounddevice as sd
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration
STT_ENGINE = os.getenv("STT_ENGINE", "whisper").lower()
SAMPLE_RATE = 16000

# Whisper options
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "base")

# Loaded configuration
model = None
deepgram_client = None

print(f"🎙️ Using STT Engine: {STT_ENGINE.upper()}")

if STT_ENGINE == "whisper":
    try:
        import whisper
        print(f"🧠 Loading Whisper model: {WHISPER_MODEL_NAME}...")
        model = whisper.load_model(WHISPER_MODEL_NAME)
        print("✅ Whisper model loaded.")
    except Exception as e:
        print(f"❌ Error loading Whisper model: {e}")
        model = None

elif STT_ENGINE == "deepgram":
    try:
        from deepgram.client import DeepgramClient
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        if not DEEPGRAM_API_KEY:
            print("❌ DEEPGRAM_API_KEY not found in environment.")
        else:
            deepgram_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
            print("✅ Deepgram client loaded.")
    except Exception as e:
        print(f"❌ Error loading Deepgram client: {e}")
        deepgram_client = None

def listen_once() -> Optional[str]:
    """
    Listens for a voice command and transcribes using the configured STT Engine.
    Records for a fixed duration.
    """
    duration = 5  # Seconds
    print(f"🎤 Listening ({STT_ENGINE}) for {duration} seconds...")
    
    try:
        # Record audio
        # sounddevice records float32 in range [-1, 1]
        recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        
        print("🔍 Transcribing...")
        
        if STT_ENGINE == "whisper":
            if model is None:
                print("❌ Whisper model not initialized.")
                return None
            audio = recording.flatten()
            result = model.transcribe(audio, fp16=False)
            text = result.get("text", "").strip()
            
        elif STT_ENGINE == "deepgram":
            if deepgram_client is None:
                print("❌ Deepgram client not initialized.")
                return None
                
            # Convert float32 to int16 PCM
            int_data = (recording * 32767).astype(np.int16)
            
            # Create WAV in-memory
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(int_data.tobytes())
                
            wav_buffer.seek(0)
            audio_bytes = wav_buffer.read()
            
            response = deepgram_client.listen.v1.media.transcribe_file(
                request=audio_bytes,
                model="nova-2",
                smart_format=True
            )
            
            if hasattr(response, "results") and hasattr(response.results, "channels"):
                text = response.results.channels[0].alternatives[0].transcript.strip()
            else:
                text = ""
                
        else:
            print(f"❌ Unknown STT Engine: {STT_ENGINE}")
            return None

        if text:
            print(f"📝 Recognized: {text}")
            return text
        else:
            print("📭 No speech recognized.")
            return None
            
    except Exception as e:
        print(f"❌ Error during STT: {e}")
        return None

if __name__ == "__main__":
    # Test
    text = listen_once()
    print(f"Final Outcome: {text}")
