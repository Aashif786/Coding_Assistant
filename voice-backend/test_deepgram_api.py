import os
import io
import wave
import numpy as np
from deepgram.client import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY")

try:
    client = DeepgramClient(api_key=API_KEY)
    
    sample_rate = 16000
    duration = 1
    data = np.zeros(sample_rate, dtype=np.int16)
    
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())
        
    wav_buffer.seek(0)
    audio_bytes = wav_buffer.read()
    
    response = client.listen.v1.media.transcribe_file(
        request=audio_bytes,
        model="nova-2",
        smart_format=True
    )
    
    if hasattr(response, "results") and hasattr(response.results, "channels"):
        alt = response.results.channels[0].alternatives[0]
        print(f"Transcript type: {type(alt.transcript)}")
        print(f"Transcript value: '{alt.transcript}'")

except Exception as e:
    print(f"❌ Error: {e}")
