"""
Advanced Voice Engine for TimeTraveler AI. 
Uses Edge-TTS for free, high-quality, customizable voices.
"""

import asyncio
import edge_tts
import base64
from io import BytesIO
from typing import Optional
import time

# Voice presets for different character types
VOICE_PRESETS = {
    # Indian voices
    "indian_male_royal": {
        "voice":  "en-IN-PrabhatNeural",
        "rate":  "-15%",
        "pitch": "-10Hz",
        "description": "Deep, commanding voice for kings"
    },
    "indian_male_spiritual": {
        "voice": "en-IN-PrabhatNeural",
        "rate": "-20%",
        "pitch": "+5Hz",
        "description": "Gentle, wise voice for priests"
    },
    "indian_male_warrior": {
        "voice": "en-IN-PrabhatNeural",
        "rate": "+5%",
        "pitch":  "-5Hz",
        "description": "Passionate voice for warriors"
    },
    "indian_female_royal": {
        "voice": "en-IN-NeerjaNeural",
        "rate": "-10%",
        "pitch": "+3Hz",
        "description": "Regal female voice"
    },
    "british_male_formal": {
        "voice": "en-GB-RyanNeural",
        "rate": "-5%",
        "pitch": "-3Hz",
        "description": "Formal British officer"
    },
    "british_female":  {
        "voice": "en-GB-SoniaNeural",
        "rate": "-5%",
        "pitch": "+2Hz",
        "description":  "British female"
    },
    "american_female":  {
        "voice": "en-US-AriaNeural",
        "rate": "-5%",
        "pitch": "+3Hz",
        "description": "American female"
    },
}

# Map personas to voice presets
PERSONA_VOICE_MAP = {
    "king_rama_pandya": "indian_male_royal",
    "temple_priest": "indian_male_spiritual",
    "british_collector":  "british_male_formal",
    "freedom_fighter": "indian_male_warrior",
    "rani_velu_nachiyar": "indian_female_royal",
    "cleopatra":  "american_female",
    "leonardo_da_vinci": "british_male_formal",
    "emperor_ashoka": "indian_male_royal",
    "marie_curie": "british_female",
    "chola_king": "indian_male_royal",
}


async def _generate_speech_async(
    text: str,
    voice:  str,
    rate: str,
    pitch: str
) -> Optional[bytes]:
    """Generate speech using Edge-TTS asynchronously."""
    try:
        # Clean text
        clean_text = text.replace("*", "").replace("_", "").replace("#", "")
        clean_text = clean_text.replace("**", "").replace("__", "")
        
        if len(clean_text) > 3000:
            clean_text = clean_text[:3000] + "..."
        
        if not clean_text. strip():
            return None
        
        communicate = edge_tts.Communicate(
            text=clean_text,
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        
        audio_bytes = BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.write(chunk["data"])
        
        audio_bytes. seek(0)
        return audio_bytes.read()
    
    except Exception as e:
        print(f"Edge-TTS Error: {e}")
        return None


def generate_speech(
    text: str,
    voice: str = "en-IN-PrabhatNeural",
    rate: str = "-10%",
    pitch: str = "-5Hz"
) -> Optional[bytes]:
    """Synchronous wrapper for speech generation."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop. run_until_complete(
            _generate_speech_async(text, voice, rate, pitch)
        )
        loop.close()
        return result
    except Exception as e:
        print(f"Speech error: {e}")
        return None


def generate_persona_speech(text: str, persona_key:  str) -> Optional[str]:
    """
    Generate speech for a specific persona. 
    Returns base64 encoded audio.
    """
    preset_name = PERSONA_VOICE_MAP.get(persona_key, "indian_male_royal")
    preset = VOICE_PRESETS. get(preset_name, VOICE_PRESETS["indian_male_royal"])
    
    audio_bytes = generate_speech(
        text=text,
        voice=preset["voice"],
        rate=preset["rate"],
        pitch=preset["pitch"]
    )
    
    if audio_bytes:
        return base64.b64encode(audio_bytes).decode()
    return None


def get_audio_player_html(b64_audio: str, autoplay: bool = True) -> str:
    """Create HTML audio player from base64 audio."""
    if not b64_audio:
        return ""
    
    unique_id = f"audio_{int(time.time() * 1000)}"
    autoplay_attr = "autoplay" if autoplay else ""
    
    html = f"""
    <audio id="{unique_id}" {autoplay_attr} controls 
           style="width: 100%; margin: 10px 0; border-radius: 25px;">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
    </audio>
    <script>
        (function() {{
            var audio = document.getElementById('{unique_id}');
            if (audio) {{
                audio.play().catch(function(e) {{ console.log('Autoplay blocked'); }});
            }}
        }})();
    </script>
    """
    return html


def get_available_voices():
    """List all available Edge-TTS voices."""
    async def _list_voices():
        voices = await edge_tts.list_voices()
        return voices
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    voices = loop.run_until_complete(_list_voices())
    loop.close()
    return voices
