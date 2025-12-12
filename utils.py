"""
Utility functions for TimeTraveler AI. 
Handles AI interactions, text-to-speech, and image processing. 
"""

import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64
import json
from landmarks import get_landmark, identify_landmark_from_text, LANDMARKS
from personas import get_persona

# ============== AI FUNCTIONS ==============

def configure_gemini(api_key):
    """Configure the Gemini API with the provided key."""
    genai.configure(api_key=api_key)

def get_gemini_model(model_name="gemini-1.5-flash"):
    """Get a Gemini model instance."""
    return genai.GenerativeModel(model_name)

def analyze_image(image, model):
    """
    Use Gemini Vision to analyze an image and identify landmarks.
    Returns a dictionary with landmark identification.
    """
    prompt = """Look at this image carefully.  I need you to identify if this shows any landmark from Tirunelveli, Tamil Nadu, India. 

Possible landmarks: 
1. Nellaiappar Temple - Hindu temple with tall gopuram (tower), musical pillars, Dravidian architecture
2. Krishnapuram Palace - 17th century palace with murals, Kerala-style sloped roof
3. Panchalankurichi Fort/Memorial - Fort ruins or Kattabomman memorial/statue
4. Tamiraparani River - River with ghats, temple banks

Analyze what you see and respond with ONLY this JSON format:
{
    "identified":  true or false,
    "landmark_name": "name if identified, else unknown",
    "confidence": "high", "medium", or "low",
    "visual_elements": "brief description of what you see in the image",
    "matching_features": "which features helped you identify it"
}

If you cannot identify it as any of these landmarks, set "identified" to false. 
Respond ONLY with the JSON, no other text."""

    try:
        response = model.generate_content([prompt, image])
        result_text = response.text. strip()
        
        # Clean up markdown code blocks if present
        if "```" in result_text:
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()
        
        result = json.loads(result_text)
        return result
    
    except json.JSONDecodeError:
        return {
            "identified": False,
            "landmark_name": "unknown",
            "confidence": "none",
            "visual_elements":  "Could not parse response",
            "matching_features":  ""
        }
    except Exception as e:
        return {
            "identified": False,
            "landmark_name":  "unknown",
            "confidence":  "none",
            "visual_elements": f"Error: {str(e)}",
            "matching_features":  ""
        }

def match_to_landmark_database(identification):
    """
    Match the AI's identification to our landmark database.
    Returns the landmark key or None. 
    """
    if not identification. get("identified", False):
        return None
    
    landmark_name = identification. get("landmark_name", "").lower()
    visual_elements = identification.get("visual_elements", "").lower()
    
    # Combine text for matching
    search_text = f"{landmark_name} {visual_elements}"
    
    return identify_landmark_from_text(search_text)

def generate_persona_response(persona_key, landmark_key, user_message, chat_history, model):
    """
    Generate a response from a historical persona.
    """
    persona = get_persona(persona_key)
    if not persona:
        return "Error: Persona not found."
    
    # Build the system context
    system_context = persona["system_prompt"]
    
    # Add landmark context if available
    if landmark_key:
        landmark = get_landmark(landmark_key)
        if landmark:
            system_context += f"""

CURRENT LOCATION: {landmark['name']}
You are currently at this location with the traveler. Use this information in your responses: 
{landmark['historical_context']}
"""
    
    # Build conversation for the model
    conversation = []
    
    # Add system context as first exchange
    conversation.append({
        "role": "user",
        "parts": [f"[SYSTEM INSTRUCTIONS - Follow these exactly]\n{system_context}"]
    })
    conversation.append({
        "role":  "model", 
        "parts": ["I understand completely. I am now fully in character and will follow all instructions. "]
    })
    
    # Add chat history
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        conversation.append({
            "role":  role,
            "parts": [msg["content"]]
        })
    
    try:
        # Create chat and send message
        chat = model.start_chat(history=conversation)
        response = chat.send_message(user_message)
        return response.text
    
    except Exception as e:
        return f"*The spirit's voice fades momentarily... * (Error: {str(e)})"

def generate_greeting(persona_key, landmark_key, model):
    """
    Generate an initial greeting from the persona.
    """
    greeting_prompt = """A new traveler has just arrived at this location. 
Give them a warm greeting in character.  Introduce yourself briefly (name and who you are).
Welcome them to this place and make one interesting comment about what they're seeing.
Keep it to 2-3 sentences.  Be engaging and make them want to ask questions."""
    
    return generate_persona_response(
        persona_key, 
        landmark_key, 
        greeting_prompt, 
        [], 
        model
    )

# ============== TEXT-TO-SPEECH FUNCTIONS ==============

def text_to_speech(text, lang='en', slow=False):
    """
    Convert text to speech using Google TTS (free).
    Returns audio bytes that can be played. 
    """
    try: 
        # Clean text for better speech
        clean_text = text.replace("*", "").replace("_", "")
        
        tts = gTTS(text=clean_text, lang=lang, slow=slow)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    
    except Exception as e: 
        print(f"TTS Error: {e}")
        return None

def get_audio_html(audio_bytes, autoplay=True):
    """
    Create HTML audio element for Streamlit.
    """
    if audio_bytes is None:
        return ""
    
    b64_audio = base64.b64encode(audio_bytes. read()).decode()
    
    autoplay_attr = "autoplay" if autoplay else ""
    
    html = f"""
    <audio {autoplay_attr} controls>
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        Your browser does not support audio. 
    </audio>
    """
    return html

# ============== SUGGESTION FUNCTIONS ==============

def get_suggested_questions(persona_key, landmark_key=None):
    """
    Get contextual suggested questions based on persona and landmark.
    """
    suggestions = {
        "king_rama_pandya": {
            "general": [
                "What was daily life like in your palace?",
                "Tell me about the wars you fought",
                "What festivals did your kingdom celebrate?",
            ],
            "nellaiappar_temple": [
                "Did you commission any part of this temple?",
                "What offerings did you make to Lord Shiva?",
                "Tell me about the artisans who carved these pillars",
            ],
            "tamiraparani_river": [
                "Why is this river so important to your kingdom?",
                "What ceremonies were held at this river?",
                "How did the river help your people?",
            ],
        },
        "temple_priest": {
            "general": [
                "What is the most sacred part of this temple?",
                "Tell me about the daily rituals you perform",
                "Have you witnessed any miracles here?",
            ],
            "nellaiappar_temple": [
                "How do the musical pillars work?",
                "What is the story of Lord Nellaiappar?",
                "What happens during the Arudra Darshan festival?",
            ],
        },
        "british_collector": {
            "general": [
                "What surprised you most about India?",
                "How does this compare to buildings in England?",
                "What did you write in your journals?",
            ],
            "krishnapuram_palace": [
                "What do you think of the Gajendra Moksha mural?",
                "How does this palace compare to European ones?",
                "What artifacts did you find most interesting?",
            ],
        },
        "freedom_fighter":  {
            "general": [
                "Why did you refuse to pay tribute to the British?",
                "Tell me about your soldiers",
                "What does freedom mean to you?",
            ],
            "panchalankurichi": [
                "What memories do you have of this fort?",
                "How did you prepare for battle here?",
                "Tell me about your last stand",
            ],
        },
    }
    
    persona_suggestions = suggestions.get(persona_key, {})
    
    # Get landmark-specific suggestions if available
    if landmark_key and landmark_key in persona_suggestions:
        return persona_suggestions[landmark_key]
    
    # Fall back to general suggestions
    return persona_suggestions.get("general", [
        "Tell me about yourself",
        "What was life like in your time?",
        "What should I know about this place?",
    ])