"""
Voice Engine for TimeTraveler AI.
Uses Edge-TTS for character-appropriate voices.
"""

import asyncio
import edge_tts
import base64
from io import BytesIO
from typing import Optional, Dict
import time


# Voice presets based on characteristics
VOICE_PRESETS = {
    # Indian voices
    "indian_male_royal": {
        "voice":  "en-IN-PrabhatNeural",
        "rate": "-15%",
        "pitch": "-10Hz"
    },
    "indian_male_old": {
        "voice": "en-IN-PrabhatNeural",
        "rate": "-20%",
        "pitch": "-5Hz"
    },
    "indian_female":  {
        "voice": "en-IN-NeerjaNeural",
        "rate": "-10%",
        "pitch": "+5Hz"
    },
    # British/European voices
    "british_male":  {
        "voice": "en-GB-RyanNeural",
        "rate":  "-5%",
        "pitch": "-3Hz"
    },
    "british_female": {
        "voice": "en-GB-SoniaNeural",
        "rate": "-5%",
        "pitch": "+2Hz"
    },
    # American voices (fallback)
    "american_male": {
        "voice": "en-US-GuyNeural",
        "rate": "-10%",
        "pitch": "-5Hz"
    },
    "american_female": {
        "voice": "en-US-JennyNeural",
        "rate": "-5%",
        "pitch": "+3Hz"
    },
    # Arabic/Middle Eastern style (using British as base)
    "middle_eastern_male": {
        "voice": "en-GB-RyanNeural",
        "rate":  "-15%",
        "pitch": "-8Hz"
    },
}

# Persona to voice mapping for preset personas
PERSONA_VOICE_MAP = {
    "king_rama_pandya": "indian_male_royal",
    "temple_priest": "indian_male_old",
    "british_collector": "british_male",
    "freedom_fighter": "indian_male_royal",
    "rani_velu_nachiyar": "indian_female",
    "cleopatra": "british_female",
    "leonardo_da_vinci": "british_male",
    "emperor_ashoka": "indian_male_royal",
    "marie_curie": "british_female",
    "chola_king": "indian_male_royal",
}


def get_voice_settings_for_dynamic_persona(persona:  Dict) -> Dict:
    """
    Generate voice settings based on dynamic persona characteristics.
    """
    region = persona.get("region", "").lower()
    gender = persona.get("voice_gender", "male").lower()
    age = persona.get("voice_age", "middle").lower()
    
    # Determine voice based on region and gender
    if any(r in region for r in ["india", "mughal", "delhi", "agra", "tamil", "bengal"]):
        if gender == "female":
            return VOICE_PRESETS["indian_female"]
        else: 
            if age == "old":
                return VOICE_PRESETS["indian_male_old"]
            else:
                return VOICE_PRESETS["indian_male_royal"]
    
    elif any(r in region for r in ["egypt", "persia", "arabia", "ottoman", "middle east"]):
        if gender == "female":
            return VOICE_PRESETS["british_female"]
        else:
            return VOICE_PRESETS["middle_eastern_male"]
    
    elif any(r in region for r in ["britain", "england", "france", "italy", "europe", "roman"]):
        if gender == "female":
            return VOICE_PRESETS["british_female"]
        else:
            return VOICE_PRESETS["british_male"]
    
    else: 
        # Default fallback
        if gender == "female":
            return VOICE_PRESETS["american_female"]
        else: 
            return VOICE_PRESETS["american_male"]


def generate_voice_settings_for_persona(persona: Dict) -> Dict:
    """Wrapper function for compatibility."""
    return get_voice_settings_for_dynamic_persona(persona)


async def _generate_speech_async(text: str, voice:  str, rate: str, pitch: str) -> Optional[bytes]:
    """Generate speech asynchronously using Edge-TTS."""
    try:
        # Clean text for TTS
        clean_text = text.replace("*", "").replace("_", "").replace("#", "")
        clean_text = clean_text.replace("**", "").replace("__", "")
        
        # Limit length
        if len(clean_text) > 2000:
            clean_text = clean_text[:2000] + "..."
        
        if not clean_text. strip():
            return None
        
        communicate = edge_tts.Communicate(
            text=clean_text,
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        
        audio_buffer = BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": 
                audio_buffer.write(chunk["data"])
        
        audio_buffer.seek(0)
        return audio_buffer.read()
        
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def generate_speech(text: str, voice_settings: Dict) -> Optional[str]:
    """
    Generate speech and return base64 encoded audio. 
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        audio_bytes = loop.run_until_complete(
            _generate_speech_async(
                text,
                voice_settings. get("voice", "en-US-GuyNeural"),
                voice_settings.get("rate", "-10%"),
                voice_settings.get("pitch", "-5Hz")
            )
        )
        
        loop.close()
        
        if audio_bytes: 
            return base64.b64encode(audio_bytes).decode()
        return None
        
    except Exception as e:
        print(f"Speech generation error: {e}")
        return None


def generate_persona_speech(text: str, persona_key: str, voice_settings: Optional[Dict] = None) -> Optional[str]:
    """
    Generate speech for a persona. 
    Uses provided voice_settings or looks up from preset mapping.
    """
    if voice_settings:
        settings = voice_settings
    elif persona_key in PERSONA_VOICE_MAP:
        preset_name = PERSONA_VOICE_MAP[persona_key]
        settings = VOICE_PRESETS. get(preset_name, VOICE_PRESETS["american_male"])
    else:
        settings = VOICE_PRESETS["american_male"]
    
    return generate_speech(text, settings)


def get_audio_player_html(b64_audio: str, autoplay: bool = True) -> str:
    """Create HTML audio player from base64 audio."""
    if not b64_audio:
        return ""
    
    unique_id = f"audio_{int(time.time() * 1000)}"
    autoplay_attr = "autoplay" if autoplay else ""
    
    return f"""
    <audio id="{unique_id}" {autoplay_attr} controls style="width: 100%; margin: 10px 0; border-radius: 25px;">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
    </audio>
    <script>
        (function() {{
            var a = document.getElementById('{unique_id}');
            if(a) a.play().catch(function(e){{}});
        }})();
    </script>
    """
