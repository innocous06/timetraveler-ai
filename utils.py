"""
Utility functions for TimeTraveler AI. 
Handles AI interactions and helper functions.
"""

import streamlit as st
import google.generativeai as genai
import json
from typing import Optional, Dict, List
from landmarks import get_landmark, identify_landmark_from_text
from personas import get_persona

# Configuration
DEFAULT_MODEL = "gemini-2.5-flash"


def configure_gemini(api_key: str = None) -> bool:
    """Configure Gemini API."""
    if api_key: 
        genai.configure(api_key=api_key)
        return True
    elif "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    return False


def get_gemini_model(model_name: str = None):
    """Get Gemini model instance."""
    return genai.GenerativeModel(model_name or DEFAULT_MODEL)


def analyze_image(image, model) -> Dict:
    """Analyze image to identify landmarks."""
    prompt = """Analyze this image and identify the landmark or monument shown. 

Look for:
1. Temple architecture (gopurams, pillars, mandapams)
2. Palaces and forts
3. Ancient monuments and sculptures
4. Historical sites from India or worldwide

Respond with ONLY this JSON format:
{
    "identified":  true/false,
    "landmark_name": "name of landmark",
    "location": "city, country",
    "confidence": "high/medium/low",
    "visual_elements": "what you see in the image",
    "architectural_style": "style of architecture",
    "era": "approximate time period"
}"""

    try:
        response = model.generate_content([prompt, image])
        result_text = response.text. strip()
        
        # Clean markdown
        if "```" in result_text:
            parts = result_text.split("```")
            if len(parts) >= 2:
                result_text = parts[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()
        
        return json.loads(result_text)
    
    except Exception as e:
        return {
            "identified": False,
            "landmark_name": "unknown",
            "confidence": "none",
            "visual_elements":  f"Error: {str(e)}"
        }


def match_to_database(identification: Dict) -> Optional[str]:
    """Match AI identification to landmark database."""
    if not identification. get("identified"):
        return None
    
    search_text = " ".join([
        identification. get("landmark_name", ""),
        identification.get("location", ""),
        identification.get("visual_elements", ""),
        identification.get("architectural_style", "")
    ])
    
    return identify_landmark_from_text(search_text)


def generate_persona_response(
    persona_key: str,
    landmark_key: str,
    user_message: str,
    chat_history: List[Dict],
    model
) -> str:
    """Generate response from historical persona."""
    persona = get_persona(persona_key)
    if not persona:
        return "Error: Persona not found."
    
    # Build context
    system_context = persona["system_prompt"]
    
    if landmark_key:
        landmark = get_landmark(landmark_key)
        if landmark:
            system_context += f"""

CURRENT LOCATION: {landmark['name']}
Location: {landmark. get('location', 'Unknown')}

Historical Context:
{landmark.get('historical_context', '')}

Use this information to make your responses authentic and informative. 
"""
    
    # Build conversation
    conversation = [
        {"role": "user", "parts": [f"[SYSTEM]\n{system_context}"]},
        {"role": "model", "parts": ["I understand.  I am now fully in character."]}
    ]
    
    for msg in chat_history: 
        role = "user" if msg["role"] == "user" else "model"
        conversation.append({"role":  role, "parts": [msg["content"]]})
    
    try:
        chat = model.start_chat(history=conversation)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"*The spirit's voice fades... * (Error: {str(e)})"


def generate_greeting(persona_key: str, landmark_key: str, model) -> str:
    """Generate initial greeting from persona."""
    prompt = """A traveler has just arrived.  Give a warm greeting in character: 
1. Introduce yourself (name and title)
2. Welcome them to this location
3. Make one intriguing comment to spark curiosity
Keep it to 3-4 sentences.  Be engaging and authentic! """
    
    return generate_persona_response(persona_key, landmark_key, prompt, [], model)


def get_suggested_questions(persona_key: str, landmark_key: str = None) -> List[str]:
    """Get contextual suggested questions."""
    suggestions = {
        "king_rama_pandya": [
            "What was daily life like in your royal court?",
            "Tell me about the temples you built",
            "How did you protect your kingdom?"
        ],
        "temple_priest": [
            "How do the musical pillars work?",
            "What rituals do you perform daily?",
            "Tell me about the temple festivals"
        ],
        "british_collector": [
            "How does this compare to European architecture?",
            "What did you document in your journals?",
            "What surprised you most about India?"
        ],
        "freedom_fighter": [
            "Why did you refuse to pay tribute?",
            "Tell me about your warriors",
            "What does freedom mean to you?"
        ],
        "rani_velu_nachiyar": [
            "How did you become a warrior queen?",
            "Tell me about your women's army",
            "How did you defeat the British?"
        ],
        "cleopatra": [
            "Tell me about Alexandria's library",
            "What was ruling Egypt like?",
            "How many languages do you speak?"
        ],
        "leonardo_da_vinci":  [
            "What are you working on now?",
            "How do you see art and science connected?",
            "Tell me about your flying machines"
        ],
        "emperor_ashoka": [
            "What happened at Kalinga?",
            "How did you embrace Buddhism?",
            "Tell me about your rock edicts"
        ],
        "marie_curie": [
            "How did you discover radium?",
            "What challenges did you face as a woman?",
            "Tell me about your research"
        ],
        "chola_king": [
            "Tell me about your naval expeditions",
            "How did you build such magnificent temples?",
            "What made the Chola navy so powerful?"
        ],
    }
    
    return suggestions.get(persona_key, [
        "Tell me about yourself",
        "What was life like in your time?",
        "What should I know about this place?"
    ])
