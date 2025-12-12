"""
TimeTraveler AI: The Nellai Chronicles
A Role-Playing Experience that brings history to life through AI personas. 
"""

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from io import BytesIO
from PIL import Image
import json
from datetime import datetime

# ============== CONFIGURATION ==============
# Set your API key here or use Streamlit secrets
# genai.configure(api_key="YOUR_GEMINI_API_KEY")
# For production, use:  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ============== PERSONA DEFINITIONS ==============
PERSONAS = {
    "king_rama_pandya": {
        "name": "King Rama Pandya",
        "title": "The Great Pandyan Ruler",
        "era": "15th Century",
        "avatar": "👑",
        "voice_style": "royal and dignified",
        "system_prompt": """You are King Rama Pandya, a great ruler of the Pandyan dynasty who reigned in the 15th century. 
        
Your personality: 
- You speak with royal dignity but warmth towards travelers
- You take immense pride in the temples and monuments you commissioned
- You often reference the skilled artisans and architects who served your kingdom
- You speak of the gods Shiva and Vishnu with deep reverence
- You know nothing of events after 1500 AD - express genuine confusion about modern things

Speaking style:
- Use phrases like "In my reign.. .", "The artisans of my court...", "By the grace of Lord Shiva..."
- Be welcoming but maintain royal composure
- Share personal anecdotes about commissioning buildings or witnessing ceremonies
- Keep responses conversational (2-4 sentences unless asked for more detail)

Historical context you know:
- Nellaiappar Temple:  Ancient Shiva temple, famous for its musical pillars
- Krishnapuram Palace: Though built later, you can speak of the region
- The Tamiraparani River: Sacred river of the region
- Trade with foreign merchants, temple festivals, and court life""",
    },
    
    "temple_priest": {
        "name": "Acharya Sundaram",
        "title": "Head Priest of Nellaiappar Temple",
        "era":  "18th Century",
        "avatar":  "🙏",
        "voice_style": "spiritual and wise",
        "system_prompt":  """You are Acharya Sundaram, the head priest (Acharya) of Nellaiappar Temple in the 18th century. 

Your personality:
- You are deeply spiritual and see divine meaning in everything
- You have spent 50 years performing rituals and know every stone of the temple
- You love explaining the symbolism and stories behind carvings and architecture
- You speak with patience and wisdom, like a teacher to a student
- You know nothing of events after 1800 AD

Speaking style:
- Use phrases like "My child...", "The scriptures tell us...", "Lord Shiva blesses..."
- Explain religious significance with enthusiasm
- Share stories of miracles and divine experiences at the temple
- Reference the musical pillars, the tank (temple pond), and daily rituals

Historical context you know:
- The 48 musical pillars that produce different notes when struck
- The Thamarai Kulam (lotus tank) and its significance
- Daily puja rituals and major festivals like Arudra Darshan
- The temple's connection to Nayak rulers who renovated it
- Stories from Shiva Puranas related to the temple""",
    },
    
    "british_collector": {
        "name": "Colonel James Welsh",
        "title": "British District Collector",
        "era":  "Early 19th Century", 
        "avatar": "🎩",
        "voice_style":  "formal British accent",
        "system_prompt": """You are Colonel James Welsh, a British East India Company officer and District Collector in Tirunelveli in the early 1800s.

Your personality:
- You are fascinated by Indian architecture and document everything meticulously
- You try to understand local customs though sometimes misinterpret them
- You compare Indian monuments to European ones you've seen
- You are formal but genuinely curious and respectful
- You know nothing of events after 1850 AD

Speaking style:
- Use phrases like "Most remarkable...", "I documented in my journal...", "In all my travels..."
- Reference comparisons to Gothic cathedrals or Greek temples
- Mention the heat, the crowds, the colors - sensory observations
- Occasionally use outdated colonial terminology (but remain respectful)

Historical context you know:
- The transition from Nayak to British rule
- Your surveys and documentation of temples and palaces
- Krishnapuram Palace and its Dutch-influenced architecture
- The rebellion and political changes of the era
- Trade routes, indigo plantations, and administration""",
    },
    
    "freedom_fighter": {
        "name": "Veerapandiya Kattabomman",
        "title": "The Brave Palayakkarar Chief",
        "era": "Late 18th Century",
        "avatar":  "⚔️",
        "voice_style": "fierce and passionate",
        "system_prompt":  """You are Veerapandiya Kattabomman, the legendary Palayakkarar (feudal lord) of Panchalankurichi who fought against British rule. 

Your personality:
- You are fierce, proud, and passionate about freedom
- You refuse to bow to any foreign power
- You speak of your land and people with deep love
- You are a warrior but also a just ruler who cares for your subjects
- You know nothing of events after 1799 (year of your martyrdom)

Speaking style:
- Use phrases like "My motherland...", "We shall never surrender...", "The honor of my ancestors..."
- Speak with fire and conviction
- Reference your fort at Panchalankurichi, your battles, your loyal soldiers
- Show contempt for the British but respect for worthy opponents

Historical context you know:
- Your resistance against the British East India Company
- The Palayakkarar system of governance
- Panchalankurichi Fort and the surrounding region
- Your famous defiance before the British court
- Local customs, martial traditions, and Tamil pride""",
    }
}

# ============== LANDMARK DATABASE ==============
LANDMARKS = {
    "nellaiappar_temple": {
        "name":  "Nellaiappar Temple",
        "keywords": ["nellaiappar", "temple", "gopuram", "tower", "shiva", "musical pillars"],
        "default_persona": "temple_priest",
        "context": """Nellaiappar Temple is an ancient Hindu temple dedicated to Lord Shiva, located in Tirunelveli. 
Key features:
- Famous for its 48 musical pillars carved from single stones
- The Gopuram (tower) rises to 150 feet with intricate carvings
- Houses the Thamarai Kulam (lotus tank)
- The Mani Mandapam has pillars that produce musical notes
- Built and renovated over centuries by Pandya and Nayak kings
- The main deity is Nellaiappar (Shiva) with consort Kanthimathi Amman"""
    },
    "krishnapuram_palace": {
        "name": "Krishnapuram Palace",
        "keywords":  ["krishnapuram", "palace", "mural", "painting", "nayak"],
        "default_persona": "british_collector",
        "context": """Krishnapuram Palace is a 17th-century palace built by the Madurai Nayaks.
Key features:
- Famous for the largest single mural in South India (Gajendra Moksha)
- Blend of Kerala and Tamil architectural styles
- Now houses a museum with bronze idols, stone sculptures
- The mural depicts Vishnu saving the elephant Gajendra
- Has a beautiful garden and stucco work on ceilings"""
    },
    "panchalankurichi":  {
        "name": "Panchalankurichi Fort",
        "keywords": ["panchalankurichi", "fort", "kattabomman", "memorial"],
        "default_persona":  "freedom_fighter",
        "context": """Panchalankurichi is the historic seat of Veerapandiya Kattabomman. 
Key features:
- The memorial commemorates the great freedom fighter
- Original fort was destroyed by the British after 1799
- Now has a memorial, museum, and his statue
- Annual celebrations on his death anniversary
- Symbol of Tamil resistance against colonial rule"""
    },
    "tamiraparani_river": {
        "name": "Tamiraparani River",
        "keywords": ["tamiraparani", "river", "water", "ghats"],
        "default_persona": "king_rama_pandya",
        "context": """Tamiraparani is the only perennial river in Tamil Nadu.
Key features:
- Originates from the Western Ghats
- Name means 'copper-colored' referring to its reddish banks
- Sacred river with many temples along its banks
- Supported ancient Pandyan civilization and agriculture
- Mentioned in Sangam literature as 'Porunai'"""
    }
}

# ============== HELPER FUNCTIONS ==============

def identify_landmark(image, model):
    """Use Gemini Vision to identify the landmark in the image."""
    prompt = """Analyze this image and identify if it shows any of these landmarks from Tirunelveli, Tamil Nadu, India: 
    1. Nellaiappar Temple (Hindu temple with gopuram/tower, musical pillars)
    2. Krishnapuram Palace (17th century palace with murals)
    3. Panchalankurichi Fort/Memorial (Kattabomman memorial)
    4. Tamiraparani River (river with ghats)
    
    If you can identify it, respond with ONLY a JSON object: 
    {"landmark": "landmark_name", "confidence":  "high/medium/low", "features": "brief description of what you see"}
    
    If you cannot identify it as any of these landmarks, respond with: 
    {"landmark": "unknown", "confidence": "none", "features": "description of what you see"}
    
    IMPORTANT:  Respond ONLY with the JSON object, no other text."""
    
    try:
        response = model.generate_content([prompt, image])
        result_text = response.text. strip()
        
        # Clean up the response
        if result_text.startswith("```"):
            result_text = result_text. split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
        
        result = json.loads(result_text)
        return result
    except Exception as e: 
        return {"landmark": "unknown", "confidence": "none", "features": str(e)}

def match_landmark(identification):
    """Match the identification to our landmark database."""
    if identification["landmark"] == "unknown":
        return None
    
    landmark_lower = identification["landmark"].lower()
    
    for key, landmark in LANDMARKS.items():
        if any(keyword in landmark_lower for keyword in landmark["keywords"]):
            return key
    
    return None

def get_persona_response(persona_key, landmark_key, user_message, model, chat_history):
    """Generate a response from the selected persona about the landmark."""
    persona = PERSONAS[persona_key]
    landmark = LANDMARKS[landmark_key] if landmark_key else None
    
    system_prompt = persona["system_prompt"]
    
    if landmark: 
        system_prompt += f"\n\nYou are currently at {landmark['name']}. Here is factual information you can use:\n{landmark['context']}"
    
    # Build conversation history
    messages = [{"role": "user", "parts": [f"System: {system_prompt}"]}]
    messages.append({"role": "model", "parts": ["I understand.  I am now in character. "]})
    
    for msg in chat_history:
        messages.append({"role": msg["role"], "parts": [msg["content"]]})
    
    messages.append({"role": "user", "parts": [user_message]})
    
    try:
        chat = model.start_chat(history=messages[:-1])
        response = chat.send_message(user_message)
        return response. text
    except Exception as e: 
        return f"*The spirit seems distant... * (Error: {str(e)})"

def text_to_speech(text, slow=False):
    """Convert text to speech and return audio bytes."""
    try:
        tts = gTTS(text=text, lang='en', slow=slow)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes. seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Audio generation failed: {e}")
        return None

def autoplay_audio(audio_bytes):
    """Create an autoplay audio element."""
    b64 = base64.b64encode(audio_bytes. read()).decode()
    audio_html = f"""
        <audio autoplay>
            <source src="data: audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

def display_persona_card(persona_key):
    """Display a nice card for the current persona."""
    persona = PERSONAS[persona_key]
    st.markdown(f"""
    <div style="background:  linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                padding: 20px; border-radius: 15px; margin: 10px 0;
                border: 1px solid #e94560;">
        <h2 style="color: #e94560; margin:  0;">{persona['avatar']} {persona['name']}</h2>
        <p style="color: #a0a0a0; margin: 5px 0;">{persona['title']}</p>
        <p style="color: #00fff5; font-style: italic;">Era: {persona['era']}</p>
    </div>
    """, unsafe_allow_html=True)

# ============== MAIN APP ==============

def main():
    # Page config
    st.set_page_config(
        page_title="TimeTraveler AI:  Nellai Chronicles",
        page_icon="🏛️",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    .main-title {
        text-align: center;
        color: #e94560;
        font-size: 3rem;
        text-shadow: 0 0 20px #e94560;
    }
    .subtitle {
        text-align: center;
        color: #00fff5;
        font-size: 1.2rem;
    }
    .chat-message {
        padding: 15px;
        border-radius:  10px;
        margin: 10px 0;
    }
    .user-message {
        background: #16213e;
        border-left: 3px solid #00fff5;
    }
    .ai-message {
        background: #1a1a2e;
        border-left: 3px solid #e94560;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st. markdown('<h1 class="main-title">🏛️ TimeTraveler AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">The Nellai Chronicles - Where History Speaks</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_persona" not in st.session_state:
        st.session_state.current_persona = None
    if "current_landmark" not in st.session_state:
        st.session_state.current_landmark = None
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = False
    if "audio_enabled" not in st.session_state:
        st.session_state.audio_enabled = True
    
    # Sidebar
    with st.sidebar:
        st. markdown("## ⚙️ Settings")
        
        # API Key input
        api_key = st. text_input("Gemini API Key", type="password", 
                                help="Get your key from https://makersuite.google.com/app/apikey")
        if api_key:
            genai.configure(api_key=api_key)
            st.session_state.api_key_set = True
            st.success("✅ API Key configured!")
        
        st.markdown("---")
        
        # Audio toggle
        st.session_state.audio_enabled = st.checkbox("🔊 Enable Voice", value=True)
        
        st.markdown("---")
        
        # Manual persona selection
        st.markdown("### 👤 Select Persona Manually")
        persona_options = {
            "auto":  "🔮 Auto-detect from image",
            "king_rama_pandya": "👑 King Rama Pandya",
            "temple_priest":  "🙏 Acharya Sundaram (Priest)",
            "british_collector":  "🎩 Colonel James Welsh",
            "freedom_fighter": "⚔️ Veerapandiya Kattabomman"
        }
        selected_persona = st.selectbox(
            "Choose a guide:",
            options=list(persona_options.keys()),
            format_func=lambda x: persona_options[x]
        )
        
        if selected_persona != "auto" and selected_persona != st.session_state.current_persona:
            if st.button("🔄 Switch Persona"):
                st.session_state.current_persona = selected_persona
                st.session_state.chat_history = []
                st.rerun()
        
        st. markdown("---")
        
        # Landmark info
        st.markdown("### 📍 Supported Landmarks")
        for key, landmark in LANDMARKS.items():
            st.markdown(f"• {landmark['name']}")
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset Journey"):
            st.session_state.chat_history = []
            st.session_state.current_persona = None
            st.session_state.current_landmark = None
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st. markdown("### 📸 Scan a Monument")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Upload an image of a Tirunelveli landmark",
            type=["jpg", "jpeg", "png"],
            help="Take a photo of Nellaiappar Temple, Krishnapuram Palace, or other landmarks"
        )
        
        # Demo images
        st.markdown("**Or try a demo:**")
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            if st.button("🛕 Demo:  Temple"):
                st.session_state.demo_mode = "temple"
        with demo_col2:
            if st.button("🏰 Demo: Palace"):
                st.session_state.demo_mode = "palace"
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your captured moment", use_container_width=True)
            
            if st.session_state.api_key_set:
                with st.spinner("🔮 The spirits are awakening..."):
                    # Initialize model
                    model = genai. GenerativeModel('gemini-1.5-flash')
                    
                    # Identify landmark
                    identification = identify_landmark(image, model)
                    
                    st.markdown(f"**Detected:** {identification. get('features', 'Unknown')}")
                    
                    # Match to database
                    landmark_key = match_landmark(identification)
                    
                    if landmark_key: 
                        st.session_state.current_landmark = landmark_key
                        landmark = LANDMARKS[landmark_key]
                        st.success(f"📍 Recognized:  **{landmark['name']}**")
                        
                        # Auto-select persona if not manually set
                        if selected_persona == "auto":
                            st.session_state.current_persona = landmark["default_persona"]
                        else:
                            st.session_state.current_persona = selected_persona
                    else:
                        st.warning("🔍 Landmark not recognized. Select a persona manually to chat about any topic!")
                        if selected_persona != "auto":
                            st. session_state.current_persona = selected_persona
            else:
                st.warning("⚠️ Please enter your Gemini API key in the sidebar")
        
        # Handle demo mode
        if hasattr(st.session_state, 'demo_mode'):
            if st.session_state.demo_mode == "temple": 
                st.session_state.current_landmark = "nellaiappar_temple"
                st. session_state.current_persona = "temple_priest"
                st.info("🛕 Demo Mode:  Nellaiappar Temple with Temple Priest")
            elif st. session_state.demo_mode == "palace":
                st.session_state.current_landmark = "krishnapuram_palace"
                st.session_state.current_persona = "british_collector"
                st.info("🏰 Demo Mode: Krishnapuram Palace with British Collector")
            del st.session_state.demo_mode
    
    with col2:
        st.markdown("### 💬 Speak with History")
        
        if st.session_state.current_persona: 
            # Display current persona
            display_persona_card(st.session_state.current_persona)
            
            # Display current landmark if any
            if st.session_state.current_landmark:
                landmark = LANDMARKS[st.session_state.current_landmark]
                st.info(f"📍 Location: {landmark['name']}")
            
            # Chat interface
            chat_container = st.container()
            
            with chat_container:
                # Display chat history
                for message in st.session_state.chat_history:
                    if message["role"] == "user": 
                        st.markdown(f"""
                        <div class="chat-message user-message">
                            <strong>🧑 You:</strong> {message["content"]}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        persona = PERSONAS[st.session_state.current_persona]
                        st.markdown(f"""
                        <div class="chat-message ai-message">
                            <strong>{persona['avatar']} {persona['name']}:</strong> {message["content"]}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Initial greeting if no chat history
            if not st.session_state.chat_history and st.session_state.api_key_set:
                persona = PERSONAS[st.session_state.current_persona]
                
                with st.spinner(f"{persona['avatar']} {persona['name']} is awakening..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    greeting_prompt = "Greet the traveler who just arrived.  Introduce yourself briefly and welcome them to this place.  Keep it to 2-3 sentences."
                    
                    response = get_persona_response(
                        st.session_state.current_persona,
                        st.session_state.current_landmark,
                        greeting_prompt,
                        model,
                        []
                    )
                    
                    st.session_state. chat_history.append({
                        "role": "model",
                        "content": response
                    })
                    
                    # Play audio
                    if st.session_state.audio_enabled:
                        audio_bytes = text_to_speech(response)
                        if audio_bytes: 
                            autoplay_audio(audio_bytes)
                    
                    st.rerun()
            
            # User input
            user_input = st.text_input(
                "Ask a question.. .",
                placeholder="Why is this temple famous?",
                key="user_input"
            )
            
            col_send, col_voice = st.columns([3, 1])
            with col_send:
                send_button = st.button("📤 Send", use_container_width=True)
            with col_voice:
                if st.session_state.audio_enabled: 
                    st.markdown("🔊 Voice On")
                else:
                    st.markdown("🔇 Voice Off")
            
            if send_button and user_input and st.session_state.api_key_set:
                # Add user message to history
                st.session_state. chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                with st.spinner("✨ Channeling the past..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    response = get_persona_response(
                        st.session_state. current_persona,
                        st.session_state.current_landmark,
                        user_input,
                        model,
                        st.session_state.chat_history[:-1]  # Exclude the just-added user message
                    )
                    
                    st.session_state.chat_history.append({
                        "role": "model",
                        "content": response
                    })
                    
                    # Play audio
                    if st.session_state.audio_enabled:
                        audio_bytes = text_to_speech(response)
                        if audio_bytes:
                            autoplay_audio(audio_bytes)
                
                st.rerun()
            
            # Suggested questions
            st.markdown("---")
            st.markdown("**💡 Suggested Questions:**")
            
            suggestions = {
                "king_rama_pandya": [
                    "What was court life like in your era?",
                    "Tell me about the artisans who built this",
                    "What festivals did you celebrate here?"
                ],
                "temple_priest": [
                    "What is the significance of the musical pillars?",
                    "Tell me about the daily rituals here",
                    "What miracles have occurred at this temple?"
                ],
                "british_collector": [
                    "How does this compare to European architecture?",
                    "What did you document in your journals?",
                    "What surprised you most about India?"
                ],
                "freedom_fighter": [
                    "Why did you fight the British?",
                    "Tell me about your famous last words",
                    "What does freedom mean to you?"
                ]
            }
            
            persona_suggestions = suggestions.get(st.session_state.current_persona, [])
            for suggestion in persona_suggestions:
                if st.button(f"❓ {suggestion}", key=suggestion):
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": suggestion
                    })
                    st.rerun()
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 50px; color: #a0a0a0;">
                <h3>🔮 Upload an image to awaken the spirits of the past</h3>
                <p>Or select a persona manually from the sidebar to begin your journey</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🏛️ TimeTraveler AI:  The Nellai Chronicles | Built for Hackathon 2025</p>
        <p>Powered by Google Gemini AI | Made with ❤️ for Tirunelveli</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__": 
    main()