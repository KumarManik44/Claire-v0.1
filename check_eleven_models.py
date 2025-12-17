import requests
import os
from dotenv import load_dotenv

# Load your API key from the backend folder
load_dotenv("backend/.env")
api_key = os.getenv("ELEVENLABS_API_KEY")

print(f"Checking models for key: {api_key[:5]}...")

url = "https://api.elevenlabs.io/v1/models"
headers = {"xi-api-key": api_key}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    models = response.json()
    print("\nAVAILABLE MODELS:")
    for m in models:
        # Only print models that are likely to work (TTS models)
        print(f"- {m['model_id']}")
else:
    print(f"\nERROR: {response.status_code}")
    print(response.text)