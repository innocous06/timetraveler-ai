"""
TimeTraveler AI:  The Nellai Chronicles
Ultimate Immersive Historical Experience
December 2025
"""

import streamlit as st
from PIL import Image
import google.generativeai as genai

from personas import get_persona, get_all_personas, get_persona_names, PERSONAS
from landmarks import get_landmark, get_all_landmarks, identify_landmark_from_text, LANDMARKS
from utils import (
    configure_gemini, get_gemini_model, analyze_image,
    match_to_database, generate_persona_response,
    generate_greeting, get_suggested_questions, DEFAULT_MODEL
)
from voice_engine import generate_persona_speech, get_audio_player_html
from presentation_mode import create_mini_presentation, get_presentation_css

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="TimeTraveler AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a15 0%, #1a1a2e 50%, #0f3460 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(90deg, #e94560, #ff6b6b, #e94560);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3. 5rem;
        font-weight: bold;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    .sub-header {
        text-align: center;
        color: #00fff5;
        font-size: 1.3rem;
        margin-bottom:  30px;
        letter-spacing: 2px;
    }
    
    .persona-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #e94560;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 0 40px rgba(233, 69, 96, 0.3);
        transition: all 0.3s;
    }
    
    .persona-card:hover {
        box-shadow: 0 0 60px rgba(233, 69, 96, 0.5);
        transform: translateY(-5px);
    }
    
    .persona-avatar {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .persona-name {
        color: #e94560;
        font-size: 1.6rem;
        text-align: center;
        font-weight: bold;
    }
    
    .persona-title {
        color: #a0a0a0;
        text-align: center;
        font-size: 1rem;
    }
    
    .persona-era {
        color: #00fff5;
        text-align: center;
        font-style: italic;
        margin-top: 5px;
    }
    
    .chat-user {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        border-left: 4px solid #00fff5;
        padding: 20px;
        margin: 15px 0;
        border-radius: 0 15px 15px 0;
        color: #ffffff;
    }
    
    .chat-ai {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        border-left: 4px solid #e94560;
        padding: 20px;
        margin: 15px 0;
        border-radius: 0 15px 15px 0;
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    .landmark-badge {
        background: linear-gradient(90deg, #0f3460, #16213e);
        border: 2px solid #00fff5;
        color: #00fff5;
        padding: 12px 25px;
        border-radius: 30px;
        display: inline-block;
        margin: 15px 0;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(0, 255, 245, 0.2);
    }
    
    .gallery-container {
        display: flex;
        gap: 15px;
        overflow-x: auto;
        padding: 15px 0;
        margin: 15px 0;
    }
    
    .gallery-img {
        height: 150px;
        border-radius: 15px;
        border: 3px solid #333;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .gallery-img:hover {
        border-color: #e94560;
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
    }
    
    . demo-button {
        background: linear-gradient(90deg, #e94560, #ff6b6b);
        border: none;
        color: white;
        padding: 15px 30px;
        border-radius: 30px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        margin:  8px 0;
    }
    
    .demo-button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(233, 69, 96, 0.5);
    }
    
    .audio-container {
        background: rgba(0,0,0,0.3);
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 30px;
        margin-top: 50px;
        border-top: 1px solid #333;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Suggestion buttons */
    .suggestion-btn {
        background: rgba(233, 69, 96, 0.1);
        border: 1px solid #e94560;
        color: #e94560;
        padding: 10px 20px;
        border-radius: 20px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .suggestion-btn:hover {
        background: #e94560;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ============== SESSION STATE ==============
def init_session_state():
    defaults = {
        "chat_history": [],
        "current_persona": None,
        "current_landmark": None,
        "api_configured": False,
        "audio_enabled": True,
        "model":  None,
        "greeted": False,
        "presentation_mode": False,
        "current_image_index": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# ============== SIDEBAR ==============
def render_sidebar():
    with st.sidebar:
        st. markdown("## ⚙️ Control Panel")
        
        # API Configuration
        st.markdown("### 🔑 API Key")
        has_secret = "GEMINI_API_KEY" in st.secrets
        
        if has_secret:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✅ API Key loaded")
        else:
            api_key = st.text_input("Gemini API Key", type="password")
        
        if api_key: 
            try:
                configure_gemini(api_key)
                st.session_state. model = get_gemini_model()
                st.session_state.api_configured = True
                st.caption(f"📦 Model: `{DEFAULT_MODEL}`")
            except Exception as e:
                st.error(f"Error:  {e}")
        else:
            st.info("Enter API key")
            st.markdown("[Get Free Key →](https://aistudio.google. com/app/apikey)")
        
        st.markdown("---")
        
        # Voice Settings
        st.markdown("### 🔊 Voice Settings")
        st.session_state.audio_enabled = st.checkbox(
            "Enable Voice Narration",
            value=st.session_state.audio_enabled,
            help="AI will speak responses with character-appropriate voices"
        )
        
        st.markdown("---")
        
        # Region Selection
        st.markdown("### 🌍 Select Region")
        region = st.selectbox(
            "Filter by region:",
            ["All", "Tamil Nadu", "India", "Worldwide"]
        )
        
        st.markdown("---")
        
        # Quick Demo Section
        st.markdown("### 🎭 Quick Experiences")
        st.caption("Click to start an immersive journey:")
        
        demos = [
            ("🛕 Temple Priest at Nellaiappar", "nellaiappar_temple", "temple_priest"),
            ("👑 Pandya King's Court", "nellaiappar_temple", "king_rama_pandya"),
            ("⚔️ Kattabomman's Valor", "panchalankurichi", "freedom_fighter"),
            ("🎩 British Collector's Journal", "krishnapuram_palace", "british_collector"),
            ("👸 Queen Velu Nachiyar", "panchalankurichi", "rani_velu_nachiyar"),
            ("🦁 Chola Emperor's Glory", "brihadisvara_temple", "chola_king"),
            ("☸️ Emperor Ashoka's Wisdom", "sanchi_stupa", "emperor_ashoka"),
            ("🏺 Cleopatra's Egypt", "pyramids_giza", "cleopatra"),
            ("🎨 Leonardo's Workshop", "colosseum", "leonardo_da_vinci"),
        ]
        
        for label, landmark, persona in demos:
            if st.button(label, use_container_width=True, key=f"demo_{persona}"):
                st.session_state.current_landmark = landmark
                st.session_state.current_persona = persona
                st.session_state.chat_history = []
                st. session_state.greeted = False
                st.rerun()
        
        st. markdown("---")
        
        # Manual Persona Selection
        st.markdown("### 👤 Choose Guide")
        persona_options = {"":  "Select a guide... "}
        persona_options.update(get_persona_names())
        
        selected = st.selectbox(
            "Historical Figure:",
            options=list(persona_options.keys()),
            format_func=lambda x: persona_options. get(x, x)
        )
        
        if selected and selected != st.session_state.current_persona:
            if st.button("🎭 Activate", use_container_width=True):
                st.session_state.current_persona = selected
                st. session_state.chat_history = []
                st.session_state.greeted = False
                st.rerun()
        
        st.markdown("---")
        
        # Reset
        if st.button("🔄 New Journey", use_container_width=True):
            for key in ["chat_history", "current_persona", "current_landmark", "greeted"]:
                st.session_state[key] = [] if key == "chat_history" else None if key != "greeted" else False
            st.rerun()
        
        st.markdown("---")
        st.caption("🏆 Built for Hackathon 2025")
        st.caption("Powered by Gemini 2.5 Flash + Edge-TTS")

render_sidebar()


# ============== MAIN CONTENT ==============

# Header
st.markdown('<h1 class="main-header">🏛️ TimeTraveler AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ Where History Comes Alive ✨</p>', unsafe_allow_html=True)

# Layout
col_left, col_right = st.columns([1, 1], gap="large")


# ============== LEFT COLUMN ==============
with col_left:
    st.markdown("### 📸 Discover Monuments")
    
    # Image upload
    uploaded = st.file_uploader(
        "Upload a photo of any historical landmark",
        type=["jpg", "jpeg", "png", "webp"],
        help="Works best with temples, palaces, forts, and monuments"
    )
    
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Your Discovery", use_container_width=True)
        
        if st.session_state.api_configured:
            if st.button("🔍 Identify & Begin Journey", use_container_width=True):
                with st.spinner("🔮 Analyzing monument..."):
                    analysis = analyze_image(image, st.session_state.model)
                    
                    st.info(f"**Detected:** {analysis. get('visual_elements', 'Processing...')}")
                    
                    if analysis.get("identified"):
                        st.success(f"**{analysis. get('landmark_name')}** - {analysis.get('location', 'Unknown')}")
                    
                    landmark_key = match_to_database(analysis)
                    
                    if landmark_key:
                        landmark = get_landmark(landmark_key)
                        st.session_state.current_landmark = landmark_key
                        st.session_state.current_persona = landmark["default_persona"]
                        st. session_state.chat_history = []
                        st.session_state.greeted = False
                        st.rerun()
                    else:
                        st. warning("Landmark not in database. Try selecting a persona manually!")
    
    # Current landmark info
    if st.session_state.current_landmark:
        landmark = get_landmark(st.session_state.current_landmark)
        if landmark:
            st.markdown("---")
            st.markdown(f'<div class="landmark-badge">📍 {landmark["name"]}</div>', unsafe_allow_html=True)
            
            # Image gallery
            gallery = landmark.get("gallery_images", [])
            if gallery:
                st.markdown("**📷 Gallery:**")
                cols = st.columns(min(len(gallery), 3))
                for i, img in enumerate(gallery[: 3]):
                    with cols[i]:
                        st.image(img["url"], caption=img["caption"], use_container_width=True)
            
            with st.expander("📜 Historical Details"):
                st.markdown(landmark. get("historical_context", ""))


# ============== RIGHT COLUMN ==============
with col_right: 
    st.markdown("### 💬 Speak with History")
    
    if st.session_state.current_persona:
        persona = get_persona(st.session_state.current_persona)
        landmark = get_landmark(st.session_state.current_landmark) if st.session_state.current_landmark else None
        
        # Persona Card
        st.markdown(f"""
        <div class="persona-card">
            <div class="persona-avatar">{persona['avatar']}</div>
            <div class="persona-name">{persona['name']}</div>
            <div class="persona-title">{persona['title']}</div>
            <div class="persona-era">Era: {persona['era']} • {persona. get('region', 'Unknown')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate greeting
        if not st.session_state.greeted and st.session_state.api_configured:
            with st.spinner(f"✨ {persona['name']} is awakening..."):
                greeting = generate_greeting(
                    st.session_state.current_persona,
                    st.session_state.current_landmark,
                    st.session_state.model
                )
                
                # Generate voice
                audio_b64 = None
                if st.session_state.audio_enabled:
                    audio_b64 = generate_persona_speech(greeting, st.session_state.current_persona)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": greeting,
                    "audio": audio_b64
                })
                st.session_state.greeted = True
        
        # Chat History
        for i, msg in enumerate(st. session_state.chat_history):
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><strong>🧑 You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><strong>{persona["avatar"]} {persona["name"]}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
                
                # Audio player
                if st.session_state.audio_enabled and msg. get("audio"):
                    is_latest = (i == len(st.session_state.chat_history) - 1)
                    st.markdown(
                        f'<div class="audio-container">{get_audio_player_html(msg["audio"], autoplay=is_latest)}</div>',
                        unsafe_allow_html=True
                    )
        
        # Chat Input
        st.markdown("---")
        
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st. text_input(
                "Ask your question:",
                placeholder="What was life like in your time?",
                label_visibility="collapsed"
            )
            
            col1, col2 = st. columns([4, 1])
            with col1:
                submitted = st.form_submit_button("📤 Send", use_container_width=True)
            with col2:
                st.markdown("🔊" if st.session_state.audio_enabled else "🔇")
        
        if submitted and user_input and st.session_state.api_configured:
            st.session_state.chat_history.append({
                "role":  "user",
                "content":  user_input,
                "audio": None
            })
            
            with st.spinner("✨ Channeling the past..."):
                response = generate_persona_response(
                    st. session_state.current_persona,
                    st.session_state.current_landmark,
                    user_input,
                    [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]],
                    st.session_state.model
                )
                
                audio_b64 = None
                if st.session_state.audio_enabled:
                    audio_b64 = generate_persona_speech(response, st.session_state.current_persona)
                
                st.session_state. chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "audio": audio_b64
                })
            
            st.rerun()
        
        # Suggestions
        st.markdown("---")
        st.markdown("**💡 Suggested Questions:**")
        
        suggestions = get_suggested_questions(
            st.session_state.current_persona,
            st.session_state.current_landmark
        )
        
        cols = st.columns(len(suggestions))
        for i, (col, suggestion) in enumerate(zip(cols, suggestions)):
            with col:
                if st.button(f"❓", key=f"sug_{i}", help=suggestion):
                    st. session_state.chat_history.append({
                        "role": "user", "content": suggestion, "audio": None
                    })
                    
                    with st.spinner("✨"):
                        response = generate_persona_response(
                            st. session_state.current_persona,
                            st.session_state.current_landmark,
                            suggestion,
                            [{"role": m["role"], "content":  m["content"]} for m in st.session_state.chat_history[:-1]],
                            st.session_state.model
                        )
                        
                        audio_b64 = None
                        if st.session_state.audio_enabled:
                            audio_b64 = generate_persona_speech(response, st.session_state.current_persona)
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response,
                            "audio": audio_b64
                        })
                    st.rerun()
                
                st.caption(suggestion[: 25] + "..." if len(suggestion) > 25 else suggestion)
    
    else:
        # Welcome Screen
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; color: #a0a0a0;">
            <h2 style="color: #e94560;">🔮 Begin Your Journey</h2>
            <p style="font-size: 1.2rem;">Upload a monument photo or choose a Quick Experience</p>
            <br>
            <p>Available Guides:</p>
            <p style="font-size: 1.1rem;">
                👑 Pandya Kings • 🙏 Temple Priests • ⚔️ Freedom Fighters<br>
                👸 Warrior Queens • 🦁 Chola Emperors • 🎩 British Collectors<br>
                🏺 Cleopatra • 🎨 Leonardo da Vinci • ☸️ Emperor Ashoka
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============== FOOTER ==============
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3 style="color: #e94560;">🏛️ TimeTraveler AI:  The Nellai Chronicles</h3>
    <p>Bringing History to Life Through AI</p>
    <p style="font-size: 0.9rem; color: #666;">
        Powered by Google Gemini 2.5 Flash • Microsoft Edge-TTS • Streamlit<br>
        Built with ❤️ for Hackathon 2025
    </p>
</div>
""", unsafe_allow_html=True)
