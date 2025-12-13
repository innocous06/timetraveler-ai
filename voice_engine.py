"""
Advanced Voice Engine for TimeTraveler AI. 
Uses Edge-TTS for free, high-quality, customizable voices.
"""

import asyncio
import edge_tts
import base64
from io import BytesIO
import tempfile
import os
from typing import Optional, Dict
import streamlit as st

# Voice presets for different character types
VOICE_PRESETS = {
    # Indian voices
    "indian_male_royal": {
        "voice":  "en-IN-PrabhatNeural",
        "rate": "-15%",
        "pitch": "-10Hz",
        "description": "Deep, commanding voice for kings and emperors"
    },
    "indian_male_spiritual": {
        "voice": "en-IN-PrabhatNeural",
        "rate": "-20%",
        "pitch": "+5Hz",
        "description":  "Gentle, wise voice for priests and sages"
    },
    "indian_male_warrior": {
        "voice": "en-IN-PrabhatNeural",
        "rate": "+5%",
        "pitch": "-5Hz",
        "description":  "Passionate, fierce voice for warriors"
    },
    "indian_female_royal": {
        "voice": "en-IN-NeerjaNeural",
        "rate":  "-10%",
        "pitch": "+5Hz",
        "description":  "Regal, commanding female voice"
    },
    "indian_female_gentle": {
        "voice": "en-IN-NeerjaNeural",
        "rate": "-15%",
        "pitch":  "+8Hz",
        "description": "Soft, nurturing female voice"
    },
    
    # British voices
    "british_male_formal": {
        "voice": "en-GB-RyanNeural",
        "rate":  "-5%",
        "pitch": "-3Hz",
        "description": "Formal British colonial officer"
    },
    "british_female_educated": {
        "voice": "en-GB-SoniaNeural",
        "rate": "-5%",
        "pitch": "+2Hz",
        "description":  "Educated British female"
    },
    
    # American voices
    "american_female_professional": {
        "voice": "en-US-JennyNeural",
        "rate": "-5%",
        "pitch":  "+3Hz",
        "description": "Professional American female"
    },
    "american_male_narrator": {
        "voice": "en-US-GuyNeural",
        "rate": "-10%",
        "pitch": "-5Hz",
        "description": "Deep narrator voice"
    },
    
    # European voices
    "italian_male_artistic": {
        "voice": "en-GB-RyanNeural",  # Using British as fallback
        "rate": "-15%",
        "pitch": "-2Hz",
        "description": "Thoughtful artistic voice"
    },
}

# Map personas to voice presets
PERSONA_VOICE_MAP = {
    "king_rama_pandya": "indian_male_royal",
    "temple_priest": "indian_male_spiritual",
    "british_collector": "british_male_formal",
    "freedom_fighter": "indian_male_warrior",
    "rani_velu_nachiyar": "indian_female_royal",
    "cleopatra": "american_female_professional",  # Fallback
    "leonardo_da_vinci": "italian_male_artistic",
    "emperor_ashoka": "indian_male_royal",
    "marie_curie": "british_female_educated",
    "chola_king": "indian_male_royal",
}


async def generate_speech_async(
    text: str,
    voice:  str = "en-IN-PrabhatNeural",
    rate: str = "-10%",
    pitch: str = "-5Hz"
) -> Optional[bytes]:
    """
    Generate speech audio using Edge-TTS asynchronously.
    Returns audio bytes. 
    """
    try: 
        # Clean text for better speech
        clean_text = text.replace("*", "").replace("_", "").replace("#", "")
        clean_text = clean_text.replace("**", "").replace("__", "")
        
        # Limit length
        if len(clean_text) > 5000:
            clean_text = clean_text[:5000] + "..."
        
        # Create communicate object with voice settings
        communicate = edge_tts.Communicate(
            text=clean_text,
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        
        # Generate audio to bytes
        audio_bytes = BytesIO()
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.write(chunk["data"])
        
        audio_bytes.seek(0)
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
    """
    Synchronous wrapper for speech generation.
    """
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop. run_until_complete(
            generate_speech_async(text, voice, rate, pitch)
        )
        loop.close()
        return result
    except Exception as e:
        print(f"Speech generation error: {e}")
        return None


def generate_persona_speech(text: str, persona_key: str) -> Optional[str]:
    """
    Generate speech for a specific persona with their voice settings.
    Returns base64 encoded audio.
    """
    # Get voice preset for persona
    preset_name = PERSONA_VOICE_MAP.get(persona_key, "indian_male_royal")
    preset = VOICE_PRESETS. get(preset_name, VOICE_PRESETS["indian_male_royal"])
    
    # Generate speech
    audio_bytes = generate_speech(
        text=text,
        voice=preset["voice"],
        rate=preset["rate"],
        pitch=preset["pitch"]
    )
    
    if audio_bytes:
        return base64.b64encode(audio_bytes).decode()
    return None


def get_audio_player_html(
    b64_audio: str,
    autoplay: bool = True,
    show_controls: bool = True
) -> str:
    """
    Create HTML audio player from base64 audio.
    """
    if not b64_audio:
        return ""
    
    import time
    unique_id = f"audio_{int(time.time() * 1000)}"
    
    controls_attr = "controls" if show_controls else ""
    autoplay_attr = "autoplay" if autoplay else ""
    
    html = f"""
    <div style="margin:  15px 0;">
        <audio id="{unique_id}" {autoplay_attr} {controls_attr} 
               style="
