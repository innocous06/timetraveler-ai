"""
TimeTraveler AI:   The Nellai Chronicles
Ultimate Immersive Historical Experience
December 2025

KEY FEATURE:   Dynamic persona generation - the AI identifies the most relevant
historical figure for ANY monument uploaded.  
"""

import streamlit as st
from PIL import Image

from utils import (
    configure_gemini, get_gemini_model, analyze_image,
    generate_dynamic_persona, generate_related_personas,
    generate_full_persona_from_brief, generate_persona_response,
    generate_greeting, get_suggested_questions, DEFAULT_MODEL
)
from voice_engine import (
    generate_persona_speech, get_audio_player_html,
    get_voice_settings_for_dynamic_persona
)
from image_fetcher import fetch_landmark_images, init_image_cache, get_fallback_images
from immersive_view import render_immersive_view

# Page config
st.set_page_config(
    page_title="TimeTraveler AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background:  linear-gradient(135deg, #0a0a15 0%, #1a1a2e 50%, #0f3460 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #e94560, #ff6b6b, #e94560);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
    }
    
    .sub-header {
        text-align: center;
        color: #00fff5;
        font-size: 1.2rem;
        margin-bottom: 25px;
    }
    
    .persona-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border:  2px solid #e94560;
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 30px rgba(233, 69, 96, 0.3);
    }
    
    .persona-avatar {
        font-size:  3.5rem;
        text-align: center;
    }
    
    .persona-name {
        color: #e94560;
        font-size: 1.4rem;
        text-align: center;
        font-weight: bold;
    }
    
    .persona-title {
        color: #a0a0a0;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .persona-era {
        color: #00fff5;
        text-align: center;
        font-style: italic;
    }
    
    .chat-user {
        background: #16213e;
        border-left: 4px solid #00fff5;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 15px 15px 0;
        color: white;
    }
    
    .chat-ai {
        background: #1a1a2e;
        border-left: 4px solid #e94560;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 15px 15px 0;
        color: white;
        line-height: 1.7;
    }
    
    . landmark-badge {
        background:  #0f3460;
        border: 2px solid #00fff5;
        color: #00fff5;
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-block;
        margin: 10px 0;
        font-weight: bold;
    }
    
    .audio-container {
        background: rgba(0,0,0,0.3);
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
    }
    
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Session State
def init_session_state():
    defaults = {
        "chat_history": [],
        "api_configured": False,
        "audio_enabled": True,
        "immersive_mode": False,
        "model": None,
        "greeted": False,
        # Dynamic persona system
        "current_persona": None,
        "related_personas": [],
        "landmark_info": None,
        "landmark_images": [],
        "voice_settings": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()
init_image_cache()


# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    
    # API Key
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
            st.session_state. api_configured = True
            st.caption(f"Model: `{DEFAULT_MODEL}`")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Enter API key")
        st.markdown("[Get Free Key](https://aistudio.google.com/app/apikey)")
    
    st.markdown("---")
    
    # Voice toggle
    st. markdown("### 🔊 Voice")
    st.session_state. audio_enabled = st.checkbox("Enable Voice", value=st.session_state.audio_enabled)
    
    # Immersive mode
    st.markdown("### 🎬 Immersive Mode")
    st.session_state.immersive_mode = st.checkbox("Enable Immersive View", value=st.session_state.immersive_mode)
    
    st.markdown("---")
    
    # Change Persona (if related personas available)
    if st.session_state.related_personas and len(st.session_state.related_personas) > 1:
        st.markdown("### 🎭 Change Narrator")
        st.caption("Other people connected to this monument:")
        
        for i, p in enumerate(st.session_state.related_personas):
            btn_label = f"{p. get('avatar', '👤')} {p.get('name', 'Unknown')}"
            if st.button(btn_label, key=f"persona_{i}", use_container_width=True):
                with st.spinner(f"Summoning {p.get('name')}..."):
                    full_persona = generate_full_persona_from_brief(
                        p, 
                        st.session_state.landmark_info or {},
                        st.session_state.model
                    )
                    st.session_state. current_persona = full_persona
                    st.session_state. voice_settings = get_voice_settings_for_dynamic_persona(full_persona)
                    st. session_state.chat_history = []
                    st.session_state.greeted = False
                    st.rerun()
    
    st.markdown("---")
    
    # Reset
    if st.button("🔄 New Journey", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.current_persona = None
        st.session_state. related_personas = []
        st.session_state.landmark_info = None
        st.session_state.landmark_images = []
        st.session_state.voice_settings = None
        st. session_state.greeted = False
        st.rerun()
    
    st.markdown("---")
    st.caption("🏆 Hackathon 2025")


# Main Content
st.markdown('<h1 class="main-header">🏛️ TimeTraveler AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">✨ Where History Speaks Through Those Who Made It ✨</p>', unsafe_allow_html=True)

col_left, col_right = st. columns([1, 1], gap="large")

# Left Column - Image Upload
with col_left:
    st.markdown("### 📸 Discover Any Monument")
    
    uploaded = st.file_uploader(
        "Upload a photo of ANY historical landmark worldwide",
        type=["jpg", "jpeg", "png", "webp"],
        help="The AI will identify the monument and summon the most relevant historical figure!"
    )
    
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Your Discovery", use_container_width=True)
        
        if st.session_state.api_configured:
            if st.button("🔮 Identify & Summon Historical Guide", use_container_width=True):
                
                # Step 1: Analyze the image
                with st.spinner("🔍 Analyzing monument..."):
                    analysis = analyze_image(image, st.session_state.model)
                    st.session_state.landmark_info = analysis
                    
                    if analysis.get("identified"):
                        st.success(f"**Identified:** {analysis.get('landmark_name')} - {analysis.get('location', 'Unknown')}")
                    else:
                        st.warning("Could not identify clearly, but will try to find a guide...")
                
                # Step 2: Generate the most relevant persona
                with st.spinner("✨ Summoning the most relevant historical figure..."):
                    persona = generate_dynamic_persona(analysis, st.session_state.model)
                    
                    if persona:
                        st.session_state.current_persona = persona
                        st.session_state.voice_settings = get_voice_settings_for_dynamic_persona(persona)
                        st. success(f"**Guide Found:** {persona.get('avatar', '👤')} {persona.get('name')} - {persona.get('title')}")
                        st.info(f"*{persona.get('relationship_to_landmark', '')}*")
                
                # Step 3: Get related personas (for switching)
                with st.spinner("🎭 Finding other connected historical figures..."):
                    related = generate_related_personas(analysis, st.session_state.model)
                    st.session_state.related_personas = related
                    if related:
                        names = [f"{p.get('avatar', '')} {p.get('name', '')}" for p in related[: 4]]
                        st.caption(f"Also available: {', '.join(names)}")
                
                # Step 4: Fetch images
                with st.spinner("🖼️ Loading images..."):
                    landmark_name = analysis.get("landmark_name", "monument")
                    images = fetch_landmark_images(landmark_name, {"wikipedia_search": landmark_name})
                    if images:
                        st.session_state.landmark_images = images
                    else:
                        st.session_state.landmark_images = get_fallback_images(landmark_name, 4)
                
                # Reset chat
                st.session_state. chat_history = []
                st.session_state.greeted = False
                st.rerun()
    
    # Show landmark info and images
    if st.session_state.landmark_info:
        info = st.session_state.landmark_info
        st.markdown("---")
        st.markdown(f'<div class="landmark-badge">📍 {info.get("landmark_name", "Unknown Monument")}</div>', unsafe_allow_html=True)
        st.caption(f"📍 {info.get('location', 'Unknown')} | 🏛️ {info.get('architectural_style', 'Unknown')} | ⏰ {info.get('era', 'Unknown')}")
        
        # Image gallery
        if st.session_state.landmark_images:
            st.markdown("**📷 Gallery:**")
            num_images = min(len(st.session_state.landmark_images), 3)
            cols = st.columns(num_images)
            for i, img in enumerate(st. session_state.landmark_images[: 3]):
                with cols[i]: 
                    st.image(img["url"], caption=img. get("caption", "")[:30], use_container_width=True)


# Right Column - Chat
with col_right:
    st.markdown("### 💬 Speak with History")
    
    if st.session_state.current_persona:
        persona = st.session_state.current_persona
        
        # Persona Card
        st.markdown(f"""
        <div class="persona-card">
            <div class="persona-avatar">{persona.get('avatar', '👤')}</div>
            <div class="persona-name">{persona.get('name', 'Historical Guide')}</div>
            <div class="persona-title">{persona.get('title', '')}</div>
            <div class="persona-era">Era: {persona.get('era', 'Unknown')} • {persona.get('region', 'Unknown')}</div>
            <div class="persona-title" style="margin-top: 10px; font-style: italic;">"{persona.get('relationship_to_landmark', '')}"</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate greeting
        if not st.session_state.greeted and st.session_state.api_configured:
            with st.spinner(f"✨ {persona.get('name')} is awakening..."):
                greeting = generate_greeting(
                    None, None, st.session_state.model,
                    persona, st.session_state.landmark_info
                )
                
                audio_b64 = None
                if st.session_state.audio_enabled:
                    audio_b64 = generate_persona_speech(
                        greeting, "dynamic", st.session_state.voice_settings
                    )
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": greeting,
                    "audio": audio_b64
                })
                st.session_state.greeted = True
        
        # Chat History
        for i, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user": 
                st.markdown(f'<div class="chat-user"><strong>🧑 You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                is_latest = (i == len(st.session_state.chat_history) - 1)
                
                # Immersive mode for latest message
                if is_latest and st.session_state.immersive_mode and st.session_state.landmark_images:
                    render_immersive_view(
                        images=st.session_state.landmark_images,
                        persona_data=persona,
                        subtitle_text=msg["content"],
                        show_audio_visualizer=st.session_state. audio_enabled and msg. get("audio") is not None
                    )
                    
                    # Audio player below immersive view
                    if st.session_state.audio_enabled and msg.get("audio"):
                        st.markdown(
                            f'<div class="audio-container">{get_audio_player_html(msg["audio"], autoplay=True)}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    # Regular chat display
                    st.markdown(f'<div class="chat-ai"><strong>{persona.get("avatar", "👤")} {persona.get("name", "Guide")}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
                    
                    if st.session_state.audio_enabled and msg.get("audio"):
                        st.markdown(
                            f'<div class="audio-container">{get_audio_player_html(msg["audio"], autoplay=is_latest)}</div>',
                            unsafe_allow_html=True
                        )
        
        # Chat Input
        st.markdown("---")
        
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Ask a question:",
                placeholder="Why did you build this monument?",
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("📤 Send", use_container_width=True)
        
        if submitted and user_input and st.session_state.api_configured:
            st.session_state.chat_history.append({
                "role":  "user",
                "content":  user_input,
                "audio": None
            })
            
            with st. spinner("✨ Channeling the past..."):
                response = generate_persona_response(
                    None, None, user_input,
                    [{"role": m["role"], "content": m["content"]} for m in st. session_state.chat_history[:-1]],
                    st.session_state.model,
                    persona,
                    st.session_state.landmark_info
                )
                
                audio_b64 = None
                if st.session_state.audio_enabled:
                    audio_b64 = generate_persona_speech(
                        response, "dynamic", st. session_state.voice_settings
                    )
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "audio": audio_b64
                })
            
            st.rerun()
        
        # Suggested questions
        st.markdown("---")
        st.markdown("**💡 Ask about:**")
        suggestions = [
            "Why did you build this? ",
            "What was your life like?",
            "Tell me a secret about this place"
        ]
        cols = st.columns(3)
        for i, (col, sug) in enumerate(zip(cols, suggestions)):
            with col: 
                if st.button(sug[: 18] + ".. .", key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": sug, "audio": None})
                    
                    with st.spinner("✨"):
                        response = generate_persona_response(
                            None, None, sug,
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]],
                            st.session_state.model,
                            persona,
                            st.session_state.landmark_info
                        )
                        
                        audio_b64 = None
                        if st.session_state. audio_enabled:
                            audio_b64 = generate_persona_speech(
                                response, "dynamic", st.session_state.voice_settings
                            )
                        
                        st. session_state.chat_history. append({
                            "role":  "assistant",
                            "content": response,
                            "audio": audio_b64
                        })
                    st.rerun()
    
    else:
        # Welcome Screen
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; color: #a0a0a0;">
            <h2 style="color: #e94560;">🔮 Begin Your Journey</h2>
            <p style="font-size: 1.1rem;">Upload a photo of ANY historical monument</p>
            <br>
            <p>The AI will: </p>
            <p style="font-size: 1rem;">
                1️⃣ Identify the monument<br>
                2️⃣ Find the most relevant historical figure<br>
                3️⃣ Let you chat with them! 
            </p>
            <br>
            <p style="color: #00fff5;">
                📸 Taj Mahal → 👑 Shah Jahan<br>
                📸 Eiffel Tower → 🗼 Gustave Eiffel<br>
                📸 Colosseum → 🏛️ Emperor Vespasian<br>
                📸 Any Monument → The person who built it! 
            </p>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <h3 style="color: #e94560;">🏛️ TimeTraveler AI</h3>
    <p>Bringing History to Life Through AI</p>
    <p style="font-size: 0.8rem;">
        Powered by Google Gemini 2.0 Flash • Microsoft Edge-TTS • Streamlit<br>
        Built with ❤️ for Hackathon 2025
    </p>
</div>
""", unsafe_allow_html=True)
