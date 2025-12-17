from fastapi import FastAPI, UploadFile, File
from deepgram import DeepgramClient, DeepgramClientOptions
from memory import ClaireMemory
import os
from dotenv import load_dotenv
import google.generativeai as genai
import base64
import httpx
import requests # <--- ensuring requests is imported

load_dotenv()

app = FastAPI()
memory = ClaireMemory()

# Initialize APIs
# 1. DEEPGRAM
config = DeepgramClientOptions(options={"keepalive": "true"})
deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"), config)

# 2. GEMINI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. ELEVENLABS (No SDK needed, we use raw requests)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.post("/chat")
async def chat_endpoint(file: UploadFile = File(...)):
    # 1. Transcribe Audio (Deepgram)
    audio_bytes = await file.read()
    source = {'buffer': audio_bytes, 'mimetype': file.content_type}
    options = {"smart_format": True, "model": "nova-2"}
    
    # Custom timeout for Deepgram
    timeout_settings = httpx.Timeout(300.0, connect=300.0)

    try:
        response = deepgram.listen.prerecorded.v("1").transcribe_file(
            source, 
            options,
            timeout=timeout_settings
        )
    except Exception as e:
        print(f"Deepgram Error: {e}")
        return {"text": "I can't hear you. Try again!", "audio_content": None}
    
    transcript = response.results.channels[0].alternatives[0].transcript

    if not transcript:
        return {"text": "I didn't hear anything.", "audio_content": None}

    # 2. Retrieve Context
    context = memory.retrieve_context(transcript)
    
    # 3. Generate Response (Gemini)
    system_prompt = f"You are Claire, a witty, fast-talking AI assistant. Keep it short (1-2 sentences). Context: {context}"
    genai_response = model.generate_content(f"{system_prompt}\nUser: {transcript}")
    answer = genai_response.text
    
    # 4. Save to Memory
    memory.add_memory(f"User: {transcript}\nClaire: {answer}")
    
    # 5. Convert to Audio (Raw ElevenLabs API)
    # Rachel Voice ID: 21m00Tcm4TlvDq8ikWAM
    voice_id = "21m00Tcm4TlvDq8ikWAM" 
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": answer,
        "model_id": "eleven_flash_v2_5",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            audio_content = response.content
            audio_base64 = base64.b64encode(audio_content).decode("utf-8")
        else:
            print(f"ElevenLabs API Error: {response.text}")
            audio_base64 = None
    except Exception as e:
        print(f"ElevenLabs Connection Error: {e}")
        audio_base64 = None
    
    return {
        "text": answer,
        "audio_content": audio_base64
    }