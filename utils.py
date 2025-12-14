"""
Utility functions for TimeTraveler AI.  
Handles AI interactions, dynamic persona generation, and helper functions.
"""

import streamlit as st
import google.generativeai as genai
import json
import re
from typing import Optional, Dict, List

# Configuration
DEFAULT_MODEL = "gemini-2.0-flash"


def configure_gemini(api_key:  str = None) -> bool:
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


def clean_json_from_response(text: str) -> Optional[Dict]:
    """
    Extract and parse JSON from AI response.
    Tries multiple methods to handle different response formats.
    """
    text = text.strip()
    
    # Method 1: Direct parse (if response is pure JSON)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Method 2: Extract from markdown code block ```json ...  ```
    match = re.search(r'```(? : json)?\s*(\{.*?\})\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        try: 
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Method 3: Extract from markdown code block ``` ... ```
    match = re.search(r'```\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Method 4: Find JSON object with "identified" key
    match = re.search(r'\{[^{}]*"identified"[^{}]*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json. JSONDecodeError:
            pass
    
    # Method 5: Find JSON object with "name" key (for persona)
    match = re.search(r'\{[^{}]*"name"[^{}]*\}', text, re.DOTALL)
    if match:
        try:
            return json. loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Method 6: Find any JSON object (greedy)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: 
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Method 7: Find JSON array
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try: 
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None


def analyze_image(image, model) -> Dict:
    """Analyze image to identify landmarks."""
    prompt = """Look at this image carefully and identify the historical landmark, monument, or building shown. 

You MUST respond with ONLY a JSON object in this EXACT format (no other text before or after):
{
    "identified": true,
    "landmark_name": "The exact name of the landmark",
    "location": "City, Country",
    "confidence": "high",
    "visual_elements": "Describe what you see - the architecture, materials, distinctive features",
    "architectural_style": "The architectural style (e.g., Mughal, Gothic, Roman, etc.)",
    "era": "When it was built (e.g., 17th century, 1632 CE, etc.)"
}

If you cannot identify the landmark, respond with: 
{
    "identified": false,
    "landmark_name": "Unknown Monument",
    "location": "Unknown",
    "confidence": "low",
    "visual_elements":  "Describe what you see",
    "architectural_style": "Unknown",
    "era": "Unknown"
}

CRITICAL: Return ONLY the JSON object.  No explanations.  No markdown. Just the JSON."""

    try:
        response = model.generate_content([prompt, image])
        result_text = response.text. strip()
        
        # Debug logging
        print(f"[DEBUG] Image Analysis Raw Response:\n{result_text[: 800]}")
        
        # Parse JSON from response
        parsed = clean_json_from_response(result_text)
        
        if parsed and isinstance(parsed, dict):
            # Ensure all required fields exist
            parsed. setdefault("identified", False)
            parsed.setdefault("landmark_name", "Unknown")
            parsed.setdefault("location", "Unknown")
            parsed.setdefault("confidence", "low")
            parsed.setdefault("visual_elements", "")
            parsed.setdefault("architectural_style", "Unknown")
            parsed.setdefault("era", "Unknown")
            
            # Handle string "true"/"false" for identified field
            if isinstance(parsed. get("identified"), str):
                parsed["identified"] = parsed["identified"]. lower() == "true"
            
            print(f"[DEBUG] Parsed landmark: {parsed. get('landmark_name')} - Identified: {parsed.get('identified')}")
            return parsed
        
        # If parsing failed completely
        print(f"[ERROR] Failed to parse image analysis response")
        return {
            "identified": False,
            "landmark_name": "Unknown",
            "location": "Unknown",
            "confidence": "none",
            "visual_elements": f"Could not parse response",
            "architectural_style": "Unknown",
            "era": "Unknown"
        }
    
    except Exception as e:
        print(f"[ERROR] analyze_image exception: {str(e)}")
        return {
            "identified":  False,
            "landmark_name": "Unknown",
            "location": "Unknown",
            "confidence": "none",
            "visual_elements": f"Error: {str(e)}",
            "architectural_style": "Unknown",
            "era": "Unknown"
        }


def generate_dynamic_persona(landmark_info: Dict, model) -> Optional[Dict]:
    """
    Generate the most appropriate historical persona for a landmark.
    This is the KEY function - it identifies WHO should narrate. 
    """
    landmark_name = landmark_info.get("landmark_name", "Unknown Monument")
    location = landmark_info.get("location", "Unknown")
    era = landmark_info.get("era", "Unknown")
    
    prompt = f"""Based on this landmark: 
- Name: {landmark_name}
- Location: {location}
- Era: {era}
- Details: {landmark_info.get('visual_elements', '')}

Identify the SINGLE MOST historically significant person DIRECTLY associated with this specific monument. 

RULES:
- Taj Mahal → Shah Jahan (who BUILT it)
- Eiffel Tower → Gustave Eiffel (who DESIGNED it)
- Colosseum → Emperor Vespasian (who COMMISSIONED it)
- Great Pyramid → Pharaoh Khufu (who BUILT it)
- Statue of Liberty → Frédéric Auguste Bartholdi (who DESIGNED it)
- For temples → The king/ruler who BUILT that specific temple
- For palaces → The ruler who BUILT or LIVED there
- Choose the person MOST DIRECTLY connected to the monument's CREATION

You MUST respond with ONLY this JSON (no other text):
{{
    "name": "Full historical name of the person",
    "title": "Their official title (e.g., Emperor, Architect, King)",
    "era": "Time period they lived (e.g., 1592-1666 CE)",
    "region": "Where they were from (e.g., Mughal Empire, France)",
    "avatar": "Single emoji (👑 for royalty, 🏗️ for architects, ⚔️ for warriors)",
    "relationship_to_landmark": "One sentence explaining their connection",
    "personality_traits": ["trait1", "trait2", "trait3"],
    "speaking_style": "How they speak (formal, poetic, military, etc.)",
    "voice_gender": "male or female",
    "voice_age": "young, middle, or old",
    "historical_facts": ["Fact 1 about them", "Fact 2 about the monument", "Fact 3"],
    "system_prompt": "You are [NAME], [TITLE].  You [DID WHAT] for [LANDMARK]. You speak in a [STYLE] manner. You lived during [ERA]. Share your knowledge about [LANDMARK] and your life.  Never break character. If asked about events after your death, express confusion."
}}

CRITICAL: Return ONLY the JSON.  No explanations before or after."""

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Debug logging
        print(f"[DEBUG] Dynamic Persona Raw Response:\n{result_text[: 800]}")
        
        # Parse JSON from response
        persona = clean_json_from_response(result_text)
        
        if persona and isinstance(persona, dict):
            # Ensure required fields exist
            required_fields = ["name", "title", "era", "avatar"]
            missing = [f for f in required_fields if f not in persona]
            
            if missing:
                print(f"[WARNING] Missing fields in persona: {missing}")
            
            # Set defaults for all fields
            persona.setdefault("name", "Historical Guide")
            persona.setdefault("title", "Keeper of History")
            persona.setdefault("era", "Unknown Era")
            persona.setdefault("region", location)
            persona.setdefault("avatar", "👤")
            persona.setdefault("relationship_to_landmark", f"Associated with {landmark_name}")
            persona.setdefault("personality_traits", ["wise", "knowledgeable", "dignified"])
            persona.setdefault("speaking_style", "formal and dignified")
            persona.setdefault("voice_gender", "male")
            persona.setdefault("voice_age", "middle")
            persona.setdefault("historical_facts", [])
            persona.setdefault("system_prompt", f"You are {persona.get('name')}, {persona.get('title')}. You are connected to {landmark_name}. Share your knowledge authentically.")
            
            print(f"[DEBUG] Generated persona: {persona. get('name')} - {persona.get('title')}")
            return persona
        
        # Fallback if parsing failed
        print(f"[ERROR] Failed to parse persona response, using fallback")
        return create_fallback_persona(landmark_info)
        
    except Exception as e:
        print(f"[ERROR] generate_dynamic_persona exception: {str(e)}")
        return create_fallback_persona(landmark_info)


def create_fallback_persona(landmark_info: Dict) -> Dict:
    """Create a fallback generic historian persona."""
    landmark_name = landmark_info.get("landmark_name", "this monument")
    location = landmark_info.get("location", "Unknown")
    
    return {
        "name": "Ancient Historian",
        "title":  "Keeper of History",
        "era": "Timeless",
        "region": location,
        "avatar": "📜",
        "relationship_to_landmark": f"I have studied {landmark_name} extensively",
        "personality_traits": ["scholarly", "wise", "patient"],
        "speaking_style": "academic yet engaging",
        "voice_gender":  "male",
        "voice_age": "old",
        "historical_facts":  [],
        "system_prompt": f"""You are an ancient historian who has extensively studied {landmark_name}. 
You speak with scholarly wisdom and share fascinating historical details. 
You are knowledgeable about the history, architecture, and cultural significance of this place. 
Engage visitors with interesting stories and facts.  Be warm and welcoming."""
    }


def generate_related_personas(landmark_info: Dict, model) -> List[Dict]:
    """
    Generate multiple related historical figures for a landmark.
    Allows user to choose different narrators.
    """
    landmark_name = landmark_info.get("landmark_name", "Unknown Monument")
    location = landmark_info.get("location", "Unknown")
    
    prompt = f"""For this landmark:  {landmark_name} in {location}

List 3-5 different historical figures DIRECTLY connected to this monument. 
Include people who:  built it, designed it, lived there, were buried there, conquered it, or made it famous.

You MUST respond with ONLY a JSON array (no other text):
[
    {{
        "name":  "Person's full name",
        "title":  "Their title",
        "era": "Time period",
        "avatar": "emoji",
        "connection":  "How they relate to the monument (1 sentence)",
        "voice_gender": "male or female"
    }}
]

Example for Taj Mahal:
[
    {{"name": "Shah Jahan", "title": "Mughal Emperor", "era": "1628-1658", "avatar": "👑", "connection":  "Built the Taj Mahal for his beloved wife Mumtaz Mahal", "voice_gender": "male"}},
    {{"name": "Mumtaz Mahal", "title": "Empress", "era": "1593-1631", "avatar": "👸", "connection": "The Taj Mahal was built as her mausoleum", "voice_gender": "female"}},
    {{"name": "Ustad Ahmad Lahori", "title": "Chief Architect", "era": "17th century", "avatar": "🏗️", "connection": "Designed and supervised the construction", "voice_gender":  "male"}}
]

Return ONLY the JSON array. No other text."""

    try:
        response = model.generate_content(prompt)
        result_text = response. text.strip()
        
        # Debug logging
        print(f"[DEBUG] Related Personas Raw Response:\n{result_text[: 600]}")
        
        # Parse JSON from response
        parsed = clean_json_from_response(result_text)
        
        if parsed and isinstance(parsed, list):
            print(f"[DEBUG] Found {len(parsed)} related personas")
            return parsed
        
        print(f"[WARNING] Could not parse related personas")
        return []
        
    except Exception as e: 
        print(f"[ERROR] generate_related_personas exception:  {str(e)}")
        return []


def generate_full_persona_from_brief(brief_persona: Dict, landmark_info: Dict, model) -> Dict:
    """
    Generate a full persona from a brief persona selection.
    Called when user selects a different narrator.
    """
    name = brief_persona.get('name', 'Historical Figure')
    title = brief_persona.get('title', '')
    era = brief_persona. get('era', 'Unknown')
    connection = brief_persona.get('connection', '')
    avatar = brief_persona.get('avatar', '👤')
    voice_gender = brief_persona.get('voice_gender', 'male')
    landmark_name = landmark_info.get('landmark_name', 'the monument')
    
    prompt = f"""Create a detailed persona for: 
- Name: {name}
- Title: {title}
- Era: {era}
- Connection to {landmark_name}: {connection}

You MUST respond with ONLY this JSON (no other text):
{{
    "name": "{name}",
    "title": "{title}",
    "era": "{era}",
    "region": "Where they were from",
    "avatar": "{avatar}",
    "relationship_to_landmark": "{connection}",
    "personality_traits": ["trait1", "trait2", "trait3"],
    "speaking_style": "How they would speak",
    "voice_gender": "{voice_gender}",
    "voice_age": "young/middle/old",
    "historical_facts": ["fact1", "fact2", "fact3"],
    "system_prompt": "You are {name}, {title}. {connection}. You speak in a [STYLE] manner. Share your knowledge about {landmark_name}. Never break character."
}}

Return ONLY the JSON. No other text."""

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Debug logging
        print(f"[DEBUG] Full Persona Raw Response:\n{result_text[:600]}")
        
        # Parse JSON from response
        persona = clean_json_from_response(result_text)
        
        if persona and isinstance(persona, dict):
            # Set defaults
            persona.setdefault("name", name)
            persona.setdefault("title", title)
            persona.setdefault("era", era)
            persona.setdefault("region", "Unknown")
            persona.setdefault("avatar", avatar)
            persona.setdefault("relationship_to_landmark", connection)
            persona.setdefault("personality_traits", ["wise", "dignified"])
            persona.setdefault("speaking_style", "formal")
            persona.setdefault("voice_gender", voice_gender)
            persona.setdefault("voice_age", "middle")
            persona.setdefault("historical_facts", [])
            persona.setdefault("system_prompt", f"You are {name}, {title}. {connection}.  Speak in character and share your knowledge.")
            
            return persona
        
        # Return brief persona with defaults if parsing failed
        return {
            "name": name,
            "title": title,
            "era": era,
            "region": "Unknown",
            "avatar": avatar,
            "relationship_to_landmark": connection,
            "personality_traits": ["wise", "dignified"],
            "speaking_style": "formal",
            "voice_gender": voice_gender,
            "voice_age": "middle",
            "historical_facts": [],
            "system_prompt": f"You are {name}, {title}. {connection}. Speak in character and share your knowledge of this place."
        }
        
    except Exception as e:
        print(f"[ERROR] generate_full_persona_from_brief exception: {str(e)}")
        return {
            "name": name,
            "title":  title,
            "era": era,
            "region": "Unknown",
            "avatar": avatar,
            "relationship_to_landmark": connection,
            "personality_traits": ["wise", "dignified"],
            "speaking_style":  "formal",
            "voice_gender": voice_gender,
            "voice_age": "middle",
            "historical_facts": [],
            "system_prompt": f"You are {name}, {title}. {connection}. Speak in character."
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
    
    # Get system context from dynamic persona
    if dynamic_persona: 
        system_context = dynamic_persona.get("system_prompt", "You are a historical guide.")
        persona_name = dynamic_persona.get("name", "Guide")
    else:
        system_context = "You are a historical guide.  Share your knowledge warmly."
        persona_name = "Guide"
    
    # Add landmark context
    if landmark_info: 
        landmark_name = landmark_info.get('landmark_name', 'this monument')
        location = landmark_info.get('location', 'Unknown')
        system_context += f"""

CURRENT LOCATION: {landmark_name}
Location: {location}
Era: {landmark_info.get('era', 'Unknown')}
Architecture: {landmark_info.get('architectural_style', 'Unknown')}

Speak authentically about this place. Share stories, facts, and personal experiences.
Keep responses conversational and engaging (2-4 paragraphs max).
"""
    
    # Build conversation history
    conversation = [
        {"role": "user", "parts": [f"[SYSTEM - You must follow these instructions]\n{system_context}"]},
        {"role": "model", "parts": ["I understand completely. I am now fully in character and ready to engage with visitors authentically."]}
    ]
    
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        conversation.append({"role":  role, "parts": [msg["content"]]})
    
    try:
        chat = model.start_chat(history=conversation)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"[ERROR] generate_persona_response exception: {str(e)}")
        return f"*{persona_name}'s voice fades momentarily... * I apologize, could you repeat that? (Error: {str(e)})"


def generate_greeting(
    persona_key: str,
    landmark_key: str,
    model,
    dynamic_persona: Optional[Dict] = None,
    landmark_info: Optional[Dict] = None
) -> str:
    """Generate initial greeting from persona."""
    greeting_prompt = """A new visitor has just arrived at this historical site. 
Give a warm, engaging greeting IN CHARACTER: 
1. Introduce yourself (your name and title)
2. Briefly mention your connection to this place
3. Welcome them and offer to share your stories

Keep it to 3-4 sentences.  Be warm, personal, and inviting! """

    return generate_persona_response(
        persona_key,
        landmark_key,
        greeting_prompt,
        [],
        model,
        dynamic_persona,
        landmark_info
    )


def get_suggested_questions(persona_key: str = None, landmark_key: str = None, dynamic_persona: Dict = None) -> List[str]:
    """Get contextual suggested questions."""
    if dynamic_persona:
        return [
            "Why did you build this monument?",
            "What was your life like? ",
            "Tell me a secret about this place"
        ]
    
    return [
        "Tell me about yourself",
        "What is special about this place?",
        "Share a story from your time"
    ]
