from typing import Optional
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# Configuration constants
MODEL_PATH = "models/vosk-model-small-en-in-0.4"
SAMPLE_RATE = 16000

# Global queue for audio data
audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    """
    Callback function to put incoming audio data into the queue.

    Args:
        indata: Numpy array containing the input data.
        frames: Number of frames in indata.
        time: Stream time.
        status: PortAudio status flags.
    """
    if status:
        print(status)
    audio_queue.put(bytes(indata))

def listen_once()-> Optional[str]:
    """
    Listens for a single voice command using VOSK and returns the recognized text.
    """
    try:
        model = Model(MODEL_PATH)
    except Exception as e:
        print(f"Error loading VOSK model: {e}")
        return None

    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    print("🎤 Listening for command...")

    # Use a context manager for the audio stream
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=callback
    ):
        while True:
            try:
                data = audio_queue.get() 
            except queue.Empty:
                continue

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(f"📝 Recognized: {text}")
                    return text
    return None
    

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     recognized_text = listen_once()
#     if recognized_text:
#         print(f"Final Text: {recognized_text}")

