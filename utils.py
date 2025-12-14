"""
Utility functions for TimeTraveler AI. 
Handles AI interactions, dynamic persona generation, and helper functions.
"""

import streamlit as st
import google.generativeai as genai
import json
from typing import Optional, Dict, List

# Configuration
DEFAULT_MODEL = "gemini-2.0-flash"


def configure_gemini(api_key: str = None) -> bool:
    """Configure Gemini API."""
    if api_key: 
        genai.configure(api_key=api_key)
        return True
    elif "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    return False


def get_gemini_model(model_name:  str = None):
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
        response = model. generate_content([prompt, image])
        result_text = response. text. strip()
        
        # Clean markdown
        if "```" in result_text:
            parts = result_text.split("```")
            if len(parts) >= 2:
                result_text = parts[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text. strip()
        
        return json.loads(result_text)
    
    except Exception as e: 
        return {
            "identified": False,
            "landmark_name": "unknown",
            "confidence": "none",
            "visual_elements":  f"Error: {str(e)}"
        }


def generate_dynamic_persona(landmark_info: Dict, model) -> Optional[Dict]:
    """
    Generate the most appropriate historical persona for a landmark.
    This is the KEY function - it identifies WHO should narrate. 
    """
    prompt = f"""Based on this landmark information: 
{json.dumps(landmark_info, indent=2)}

Identify the SINGLE MOST historically significant person DIRECTLY associated with this specific monument. 

IMPORTANT RULES:
- For Taj Mahal → Shah Jahan (who BUILT it for his wife Mumtaz Mahal)
- For Eiffel Tower → Gustave Eiffel (who DESIGNED it)
- For Colosseum → Emperor Vespasian (who COMMISSIONED it)
- For Great Wall → Emperor Qin Shi Huang (who STARTED it)
- For Pyramids of Giza → Pharaoh Khufu (who BUILT the Great Pyramid)
- For temples → The king/ruler who BUILT or COMMISSIONED that specific temple
- Choose the person most DIRECTLY connected to the monument's creation

Return ONLY this JSON (no other text):
{{
    "name": "Full historical name",
    "title": "Their official title/position",
    "era": "Time period (e.g., '1628-1658 CE')",
    "region": "Where they ruled/lived",
    "avatar": "Single emoji representing them (👑 for kings, 🏛️ for builders, etc.)",
    "relationship_to_landmark": "One sentence:  how they are connected",
    "personality_traits": ["trait1", "trait2", "trait3"],
    "speaking_style": "How they would speak (formal, poetic, military, etc.)",
    "voice_gender": "male or female",
    "voice_age": "young, middle, old",
    "historical_facts": ["fact1 about them and the landmark", "fact2", "fact3"],
    "system_prompt": "You are [NAME], [TITLE].  You [RELATIONSHIP TO LANDMARK].  Speak with [STYLE].  You know about [RELEVANT TOPICS]. You lived during [ERA]. Never break character.  If asked about modern things after your death, express confusion."
}}"""

    try: 
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean markdown
        if "```" in result_text:
            parts = result_text. split("```")
            if len(parts) >= 2:
                result_text = parts[1]
                if result_text. startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()
        
        persona = json.loads(result_text)
        
        # Ensure required fields exist
        required_fields = ["name", "title", "era", "avatar", "system_prompt"]
        for field in required_fields:
            if field not in persona:
                raise ValueError(f"Missing field: {field}")
        
        # Set defaults for optional fields
        persona. setdefault("region", "Unknown")
        persona.setdefault("voice_gender", "male")
        persona.setdefault("voice_age", "middle")
        persona.setdefault("personality_traits", ["wise", "dignified"])
        persona.setdefault("speaking_style", "formal and dignified")
        persona.setdefault("historical_facts", [])
        persona.setdefault("relationship_to_landmark", "Associated with this landmark")
        
        return persona
        
    except Exception as e:
        print(f"Error generating dynamic persona: {e}")
        # Return a fallback generic historian
        return {
            "name":  "Ancient Historian",
            "title": "Keeper of History",
            "era":  "Timeless",
            "region": landmark_info.get("location", "Unknown"),
            "avatar": "📜",
            "relationship_to_landmark": f"I have studied {landmark_info.get('landmark_name', 'this monument')} extensively",
            "personality_traits": ["scholarly", "wise", "patient"],
            "speaking_style":  "academic yet engaging",
            "voice_gender":  "male",
            "voice_age": "old",
            "historical_facts": [],
            "system_prompt": f"""You are an ancient historian who has extensively studied {landmark_info.get('landmark_name', 'this monument')}. 
You speak with scholarly wisdom and share fascinating historical details. 
You are knowledgeable about the history, architecture, and cultural significance of this place. 
Engage visitors with interesting stories and facts."""
        }


def generate_related_personas(landmark_info: Dict, model) -> List[Dict]:
    """
    Generate multiple related historical figures for a landmark.
    Allows user to choose different narrators. 
    """
    prompt = f"""Based on this landmark: 
{json.dumps(landmark_info, indent=2)}

List 3-5 different historical figures who are DIRECTLY connected to this monument. 
Include people who:
- Built/commissioned it
- Lived there
- Were buried there
- Made it famous
- Conquered/captured it

For each person, provide brief info. 

Return ONLY this JSON array:
[
    {{
        "name":  "Person's name",
        "title": "Their title",
        "era": "Time period",
        "avatar": "emoji",
        "connection":  "How they relate to the monument (1 sentence)",
        "voice_gender": "male/female"
    }}
]

Example for Taj Mahal:
[
    {{"name": "Shah Jahan", "title": "Mughal Emperor", "era": "1628-1658", "avatar":  "👑", "connection": "Built the Taj Mahal for his beloved wife", "voice_gender": "male"}},
    {{"name": "Mumtaz Mahal", "title": "Empress", "era": "1593-1631", "avatar": "👸", "connection": "The Taj Mahal was built as her mausoleum", "voice_gender": "female"}},
    {{"name": "Ustad Ahmad Lahori", "title": "Chief Architect", "era": "17th century", "avatar": "🏗️", "connection": "Designed and supervised construction", "voice_gender": "male"}},
    {{"name": "Aurangzeb", "title": "Mughal Emperor", "era": "1658-1707", "avatar": "⚔️", "connection": "Son of Shah Jahan, imprisoned his father", "voice_gender": "male"}}
]"""

    try: 
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean markdown
        if "```" in result_text:
            parts = result_text.split("```")
            if len(parts) >= 2:
                result_text = parts[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()
        
        personas = json. loads(result_text)
        return personas if isinstance(personas, list) else []
        
    except Exception as e: 
        print(f"Error generating related personas: {e}")
        return []


def generate_full_persona_from_brief(brief_persona: Dict, landmark_info: Dict, model) -> Dict:
    """
    Generate a full persona from a brief persona selection.
    Called when user selects a different narrator. 
    """
    prompt = f"""Create a detailed persona for this historical figure:
Name: {brief_persona.get('name')}
Title: {brief_persona.get('title')}
Era: {brief_persona.get('era')}
Connection to {landmark_info.get('landmark_name', 'the monument')}: {brief_persona.get('connection')}

Return ONLY this JSON:
{{
    "name": "{brief_persona.get('name')}",
    "title": "{brief_persona.get('title')}",
    "era": "{brief_persona.get('era')}",
    "region": "Where they were from",
    "avatar": "{brief_persona.get('avatar', '👤')}",
    "relationship_to_landmark": "{brief_persona.get('connection')}",
    "personality_traits": ["trait1", "trait2", "trait3"],
    "speaking_style": "How they would speak",
    "voice_gender": "{brief_persona.get('voice_gender', 'male')}",
    "voice_age": "young/middle/old",
    "historical_facts": ["fact1", "fact2", "fact3"],
    "system_prompt": "Complete roleplay prompt for this character..."
}}"""

    try: 
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        if "```" in result_text:
            parts = result_text. split("```")
            if len(parts) >= 2:
                result_text = parts[1]
                if result_text. startswith("json"):
                    result_text = result_text[4:]
            result_text = result_text.strip()
        
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Error generating full persona: {e}")
        # Return the brief persona with defaults
        return {
            "name": brief_persona.get("name", "Historical Figure"),
            "title": brief_persona.get("title", ""),
            "era": brief_persona.get("era", "Unknown"),
            "region": "Unknown",
            "avatar": brief_persona.get("avatar", "👤"),
            "relationship_to_landmark": brief_persona.get("connection", ""),
            "personality_traits": ["wise", "dignified"],
            "speaking_style": "formal",
            "voice_gender": brief_persona.get("voice_gender", "male"),
            "voice_age": "middle",
            "historical_facts":  [],
            "system_prompt":  f"You are {brief_persona.get('name')}, {brief_persona.get('title')}. {brief_persona.get('connection')}. Speak in character and share your knowledge of this place."
        }


def generate_persona_response(
    persona_key: str,
    landmark_key: str,
    user_message: str,
    chat_history: List[Dict],
    model,
    dynamic_persona: Optional[Dict] = None,
    landmark_info: Optional[Dict] = None
) -> str:
    """Generate response from historical persona."""
    
    # Get persona - either dynamic or from database
    if dynamic_persona:
        persona = dynamic_persona
        system_context = persona.get("system_prompt", "You are a historical guide.")
    else:
        from personas import get_persona
        persona = get_persona(persona_key)
        if not persona:
            return "Error:  Persona not found."
        system_context = persona. get("system_prompt", "You are a historical guide.")
    
    # Add landmark context if available
    if landmark_key: 
        from landmarks import get_landmark
        landmark = get_landmark(landmark_key)
        if landmark:
            system_context += f"""

CURRENT LOCATION: {landmark['name']}
Location: {landmark. get('location', 'Unknown')}

Historical Context:
{landmark.get('historical_context', '')}

Use this information to make your responses authentic and informative. 
"""
    elif landmark_info:
        system_context += f"""

CURRENT LOCATION: {landmark_info. get('landmark_name', 'Unknown Monument')}
Location: {landmark_info.get('location', 'Unknown')}

Speak authentically about this place based on your historical knowledge.
"""
    
    # Build conversation
    conversation = [
        {"role": "user", "parts": [f"[SYSTEM INSTRUCTIONS - Follow exactly]\n{system_context}"]},
        {"role": "model", "parts": ["I understand completely. I am now fully in character and ready to engage with visitors."]}
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


def generate_greeting(
    persona_key: str,
    landmark_key: str,
    model,
    dynamic_persona: Optional[Dict] = None,
    landmark_info:  Optional[Dict] = None
) -> str:
    """Generate initial greeting from persona."""
    greeting_prompt = """A new visitor has arrived at this historical site. 
Give a warm, engaging greeting in character: 
1. Introduce yourself (your name and who you are)
2. Mention your connection to this place
3. Welcome them and offer to share stories
Keep it to 3-4 sentences.  Be warm and inviting! """

    return generate_persona_response(
        persona_key,
        landmark_key,
        greeting_prompt,
        [],
        model,
        dynamic_persona,
        landmark_info
    )


def get_suggested_questions(persona_key: str, landmark_key: str = None, dynamic_persona: Dict = None) -> List[str]:
    """Get contextual suggested questions."""
    
    if dynamic_persona:
        name = dynamic_persona.get("name", "")
        relationship = dynamic_persona.get("relationship_to_landmark", "")
        return [
            f"Why did you build this monument?",
            f"What was your life like?",
            f"Tell me a secret about this place"
        ]
    
    # Default suggestions
    return [
        "Tell me about yourself",
        "What is special about this place?",
        "Share a story from your time"
    ]
