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


def generate_persona_speech(text: str, persona_key: str, persona_voice_settings: dict = None) -> Optional[str]:
    """
    Generate speech for a specific persona. 
    Returns base64 encoded audio.
    
    Args:
        text: Text to speak
        persona_key: Key of the persona
        persona_voice_settings: Optional voice settings dict for dynamic personas
    """
    # Use provided voice settings (for dynamic personas) or look up preset
    if persona_voice_settings:
        voice = persona_voice_settings.get("voice", "en-IN-PrabhatNeural")
        rate = persona_voice_settings.get("rate", "-10%")
        pitch = persona_voice_settings.get("pitch", "-5Hz")
    else:
        preset_name = PERSONA_VOICE_MAP.get(persona_key, "indian_male_royal")
        preset = VOICE_PRESETS.get(preset_name, VOICE_PRESETS["indian_male_royal"])
        voice = preset["voice"]
        rate = preset["rate"]
        pitch = preset["pitch"]
    
    audio_bytes = generate_speech(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
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


def generate_voice_settings_for_persona(persona_data: dict) -> dict:
    """
    Generate appropriate voice settings for a dynamically created persona.
    
    Args:
        persona_data: Dict with persona info including region, personality_traits, etc.
        
    Returns:
        Dict with voice settings (voice, rate, pitch)
    """
    region = persona_data.get("region", "").lower()
    personality = persona_data.get("personality_traits", [])
    speaking_style = persona_data.get("speaking_style", "").lower()
    title = persona_data.get("title", "").lower()
    
    # Determine base voice by region and gender hints
    voice = "en-IN-PrabhatNeural"  # Default Indian male
    
    if any(word in region for word in ["india", "tamil", "bengal", "delhi", "mughal", "chola", "pandya"]):
        # Indian voices
        if any(word in title for word in ["queen", "rani", "empress", "princess"]):
            voice = "en-IN-NeerjaNeural"  # Indian female
        else:
            voice = "en-IN-PrabhatNeural"  # Indian male
    elif any(word in region for word in ["britain", "england", "british", "uk", "london"]):
        # British voices
        if any(word in title for word in ["queen", "lady", "duchess"]):
            voice = "en-GB-SoniaNeural"  # British female
        else:
            voice = "en-GB-RyanNeural"  # British male
    elif any(word in region for word in ["egypt", "africa", "alexandria"]):
        voice = "en-US-AriaNeural"  # American female for variety
    elif any(word in region for word in ["europe", "italy", "france", "spain", "rome"]):
        voice = "en-GB-RyanNeural"  # British male for European
    elif any(word in title for word in ["queen", "empress", "lady", "marie", "cleopatra"]):
        voice = "en-US-AriaNeural"  # Female voice
    
    # Determine rate based on personality and speaking style
    rate = "-10%"  # Default moderate
    if any(word in speaking_style for word in ["slow", "contemplative", "wise", "spiritual"]):
        rate = "-15%"
    elif any(word in speaking_style for word in ["fast", "energetic", "passionate", "excited"]):
        rate = "+5%"
    elif any(word in speaking_style for word in ["measured", "dignified", "regal"]):
        rate = "-10%"
    
    # Determine pitch based on role and personality
    pitch = "-5Hz"  # Default
    if any(word in title for word in ["king", "emperor", "warrior", "general"]):
        pitch = "-8Hz"  # Deeper for authority
    elif any(word in title for word in ["priest", "monk", "spiritual"]):
        pitch = "+2Hz"  # Slightly higher, gentle
    elif any(word in title for word in ["queen", "empress", "princess"]):
        pitch = "+3Hz"  # Higher for female
    elif any(word in personality for word in ["gentle", "kind", "peaceful"]):
        pitch = "+2Hz"
    
    return {
        "voice": voice,
        "rate": rate,
        "pitch": pitch
    }


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
