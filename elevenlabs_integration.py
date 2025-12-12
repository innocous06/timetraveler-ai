# Add to imports
import requests

def elevenlabs_tts(text, api_key, voice_id="21m00Tcm4TlvDq8ikWAM"):
    """Use ElevenLabs for more realistic voice synthesis."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings":  {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None