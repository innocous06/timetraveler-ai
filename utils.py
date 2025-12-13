import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64
import json
from landmarks import get_landmark, identify_landmark_from_text
from personas import get_persona
DEFAULT_MODEL = "gemini-2.5-flash"
def configure_gemini(api_key=None):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    elif "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return True
    else:
        return False
def get_gemini_model(model_name=None):
    if model_name is None:
        model_name = DEFAULT_MODEL
    try:
        model = genai. GenerativeModel(model_name)
        return model
    except Exception as e:
        st.error(f"Failed to load model {model_name}: {e}")
        raise e
def analyze_image(image, model):
    prompt = """Look at this image carefully.  Identify if this shows any landmark from Tirunelveli, Tamil Nadu, India.

Possible landmarks:
1. Nellaiappar Temple - Hindu temple with tall gopuram (tower), musical pillars, Dravidian architecture
2. Krishnapuram Palace - 17th century palace with murals, Kerala-style sloped roof
3. Panchalankurichi Fort/Memorial - Fort ruins or Kattabomman memorial/statue
4. Tamiraparani River - River with ghats, temple banks

Respond with ONLY this JSON format (no other text):
{
    "identified":  true or false,
    "landmark_name": "name if identified, else unknown",
    "confidence": "high", "medium", or "low",
    "visual_elements": "brief description of what you see",
    "matching_features": "features that helped identify"
}"""
    try:
        response = model.generate_content([prompt, image])
        result_text = response.text. strip()
        if "```" in result_text:
            parts = result_text.split("```")
            if len(parts) >= 2:
                result_text = parts[1]
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
            "visual_elements":  "Could not parse AI response",
            "matching_features": ""
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
    if not identification. get("identified", False):
        return None
    landmark_name = identification.get("landmark_name", "").lower()
    visual_elements = identification.get("visual_elements", "").lower()
    search_text = f"{landmark_name} {visual_elements}"
    return identify_landmark_from_text(search_text)
def generate_persona_response(persona_key, landmark_key, user_message, chat_history, model):
    persona = get_persona(persona_key)
    if not persona:
        return "Error: Persona not found."
    system_context = persona["system_prompt"]
    if landmark_key:
        landmark = get_landmark(landmark_key)
        if landmark:
            system_context += f"""

CURRENT LOCATION: {landmark['name']}
You are at this location with the traveler.  Use this information:
{landmark['historical_context']}
"""
    conversation = []
    conversation.append({
        "role": "user",
        "parts": [f"[SYSTEM INSTRUCTIONS - Follow exactly]\n{system_context}"]
    })
    conversation.append({
        "role": "model",
        "parts": ["I understand completely. I am now fully in character. "]
    })
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        conversation.append({
            "role": role,
            "parts": [msg["content"]]
        })
    try:
        chat = model.start_chat(history=conversation)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"*The spirit's voice fades... * (Error: {str(e)})"
def generate_greeting(persona_key, landmark_key, model):
    greeting_prompt = """A new traveler has arrived.  Give a warm greeting in character.
Introduce yourself briefly (name and who you are).
Welcome them and make one interesting comment about this place.
Keep it to 2-3 sentences.  Be engaging! """
    return generate_persona_response(
        persona_key,
        landmark_key,
        greeting_prompt,
        [],
        model
    )
def text_to_speech(text, lang='en', slow=False):
    try:
        clean_text = text.replace("*", "").replace("_", "").replace("#", "")
        clean_text = clean_text.replace("**", "").replace("__", "")
        if len(clean_text) > 5000:
            clean_text = clean_text[:5000]
        tts = gTTS(text=clean_text, lang=lang, slow=slow)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        b64_audio = base64.b64encode(audio_buffer.read()).decode()
        return b64_audio
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
def get_audio_player_html(b64_audio, autoplay=True):
    if b64_audio is None:
        return ""
    import time
    unique_id = f"audio_{int(time.time() * 1000)}"
    autoplay_attr = "autoplay" if autoplay else ""
    html = f"""
    <audio id="{unique_id}" {autoplay_attr} controls style="width: 100%; margin:  10px 0;">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        Your browser does not support audio.
    </audio>
    <script>
        // Ensure audio plays
        var audio = document.getElementById('{unique_id}');
        if (audio) {{
            audio. play().catch(function(e) {{
                console.log('Autoplay prevented:', e);
            }});
        }}
    </script>
    """
    return html
def play_audio_in_streamlit(text, autoplay=True):
    if not text:
        return
    b64_audio = text_to_speech(text)
    if b64_audio:
        audio_html = get_audio_player_html(b64_audio, autoplay)
        st.markdown(audio_html, unsafe_allow_html=True)
def get_suggested_questions(persona_key, landmark_key=None):
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
        "temple_priest":  {
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
        "freedom_fighter": {
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
    if landmark_key and landmark_key in persona_suggestions:
        return persona_suggestions[landmark_key]
    return persona_suggestions.get("general", [
        "Tell me about yourself",
        "What was life like in your time?",
        "What should I know about this place?",
    ])
