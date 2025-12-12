"""
TimeTraveler AI:  The Nellai Chronicles
Main Streamlit Application - December 2025

A Role-Playing Experience that brings history to life through AI personas.
"""

import streamlit as st
from PIL import Image
import google.generativeai as genai

from personas import get_persona, get_all_personas, get_persona_names
from landmarks import get_landmark, get_all_landmarks
from utils import (
    configure_gemini,
    get_gemini_model,
    analyze_image,
    match_to_landmark_database,
    generate_persona_response,
    generate_greeting,
    text_to_speech,
    get_audio_html,
    get_suggested_questions,
    DEFAULT_MODEL,
)

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="TimeTraveler AI:  Nellai Chronicles",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    /* Dark theme background */
    .stApp {
        background:  linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* Main header */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #e94560, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight:  bold;
    }

    . sub-header {
        text-align: center;
        color: #00fff5;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* Persona card */
    .persona-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #e94560;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.3);
    }

    .persona-name {
        color: #e94560;
        font-size: 1.5rem;
        margin:  0;
    }

    .persona-title {
        color: #a0a0a0;
        font-size: 0.9rem;
    }

    .persona-era {
        color: #00fff5;
        font-style: italic;
    }

    /* Chat messages */
    .user-msg {
        background: #16213e;
        border-left: 4px solid #00fff5;
        padding: 15px;
        margin:  10px 0;
        border-radius: 0 10px 10px 0;
        color: #ffffff;
    }

    .ai-msg {
        background: #1a1a2e;
        border-left: 4px solid #e94560;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
        color: #ffffff;
    }

    /* Landmark badge */
    .landmark-badge {
        background: #0f3460;
        border: 1px solid #00fff5;
        color: #00fff5;
        padding: 8px 15px;
        border-radius:  20px;
        display: inline-block;
        margin: 10px 0;
    }

    /* Footer */
    . footer {
        text-align: center;
        color: #666;
        padding: 20px;
        margin-top: 50px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============== SESSION STATE ==============
def init_session_state():
    """Initialize session state variables."""
    defaults = {
        "chat_history": [],
        "current_persona": None,
        "current_landmark": None,
        "api_configured": False,
        "audio_enabled": True,
        "model":  None,
        "greeted": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ============== SIDEBAR ==============
def render_sidebar():
    """Render the sidebar."""
    with st.sidebar:
        st. markdown("## ⚙️ Settings")

        # API Key Section
        st.markdown("### 🔑 API Configuration")

        # Check for secret first
        has_secret = "GEMINI_API_KEY" in st.secrets

        if has_secret:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✅ API Key loaded from secrets")
        else:
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                help="Get FREE key from https://aistudio.google.com/app/apikey"
            )

        if api_key:
            try:
                configure_gemini(api_key)
                st.session_state. model = get_gemini_model()
                st.session_state. api_configured = True
                if not has_secret:
                    st. success("✅ Connected!")
                st.caption(f"📦 Model: `{DEFAULT_MODEL}`")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.session_state.api_configured = False
        else:
            st.info("👆 Enter your API key")
            st.markdown("[Get FREE Key →](https://aistudio.google.com/app/apikey)")

        st.markdown("---")

        # Audio Toggle
        st.markdown("### 🔊 Audio")
        st.session_state.audio_enabled = st.checkbox(
            "Enable Voice Output",
            value=st.session_state.audio_enabled
        )

        st.markdown("---")

        # Manual Persona Selection
        st.markdown("### 👤 Choose Guide")

        persona_options = {"auto": "🔮 Auto-detect"}
        persona_options.update(get_persona_names())

        selected = st.selectbox(
            "Historical figure:",
            options=list(persona_options.keys()),
            format_func=lambda x: persona_options[x]
        )

        if selected != "auto":
            if st.button("🎭 Activate Persona", use_container_width=True):
                st.session_state.current_persona = selected
                st. session_state.chat_history = []
                st. session_state.greeted = False
                st.rerun()

        st.markdown("---")

        # Quick Demo Buttons
        st.markdown("### 📍 Quick Demo")
        st.caption("No images?  Try these:")

        demo_options = [
            ("🛕 Temple + Priest", "nellaiappar_temple", "temple_priest"),
            ("🏰 Palace + Collector", "krishnapuram_palace", "british_collector"),
            ("⚔️ Fort + Warrior", "panchalankurichi", "freedom_fighter"),
            ("👑 River + King", "tamiraparani_river", "king_rama_pandya"),
        ]

        for label, landmark, persona in demo_options:
            if st.button(label, use_container_width=True):
                st.session_state.current_landmark = landmark
                st. session_state.current_persona = persona
                st.session_state.chat_history = []
                st.session_state.greeted = False
                st.rerun()

        st.markdown("---")

        # Reset Button
        if st.button("🔄 Reset Journey", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_persona = None
            st.session_state.current_landmark = None
            st.session_state. greeted = False
            st. rerun()

        st.markdown("---")
        st.caption("Built for Hackathon 2025 🏆")


render_sidebar()


# ============== MAIN CONTENT ==============

# Header
st.markdown('<h1 class="main-header">🏛️ TimeTraveler AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">The Nellai Chronicles — Where History Speaks</p>', unsafe_allow_html=True)

# Two columns layout
col_left, col_right = st.columns([1, 1], gap="large")


# ============== LEFT COLUMN - IMAGE ==============
with col_left: 
    st.markdown("### 📸 Scan a Monument")

    uploaded_image = st.file_uploader(
        "Upload a photo of a Tirunelveli landmark",
        type=["jpg", "jpeg", "png", "webp"],
        help="Nellaiappar Temple, Krishnapuram Palace, etc."
    )

    if uploaded_image: 
        image = Image.open(uploaded_image)
        st.image(image, caption="📷 Your photo", use_container_width=True)

        if st.session_state.api_configured:
            if st.button("🔍 Identify Landmark", use_container_width=True):
                with st.spinner("🔮 Awakening spirits..."):
                    analysis = analyze_image(image, st.session_state.model)

                    st.markdown("**🔎 Analysis:**")
                    st.info(analysis. get("visual_elements", "Processing..."))

                    landmark_key = match_to_landmark_database(analysis)

                    if landmark_key: 
                        landmark = get_landmark(landmark_key)
                        st.success(f"✅ **{landmark['name']}**")

                        st.session_state.current_landmark = landmark_key
                        st.session_state.current_persona = landmark["default_persona"]
                        st. session_state.chat_history = []
                        st.session_state.greeted = False
                        st.rerun()
                    else:
                        st. warning("🔍 Couldn't identify.  Try demo buttons!")
        else:
            st.warning("⚠️ Configure API key first")

    # Show current landmark
    if st.session_state. current_landmark:
        landmark = get_landmark(st.session_state.current_landmark)
        if landmark:
            st.markdown("---")
            st.markdown(f'<div class="landmark-badge">📍 {landmark["name"]}</div>', unsafe_allow_html=True)

            with st.expander("ℹ️ Historical Info"):
                st.markdown(landmark["historical_context"])


# ============== RIGHT COLUMN - CHAT ==============
with col_right:
    st.markdown("### 💬 Speak with History")

    if st.session_state.current_persona:
        persona = get_persona(st.session_state.current_persona)

        # Persona Card
        st.markdown(f"""
        <div class="persona-card">
            <h2 class="persona-name">{persona['avatar']} {persona['name']}</h2>
            <p class="persona-title">{persona['title']}</p>
            <p class="persona-era">Era: {persona['era']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Generate greeting if needed
        if not st.session_state.greeted and st.session_state.api_configured:
            with st.spinner(f"{persona['avatar']} Awakening..."):
                greeting = generate_greeting(
                    st.session_state.current_persona,
                    st.session_state.current_landmark,
                    st.session_state.model
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": greeting
                })
                st.session_state.greeted = True

                if st.session_state.audio_enabled:
                    audio = text_to_speech(greeting)
                    if audio:
                        st.markdown(get_audio_html(audio, autoplay=True), unsafe_allow_html=True)

        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-msg">
                    <strong>🧑 You:</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st. markdown(f"""
                <div class="ai-msg">
                    <strong>{persona['avatar']} {persona['name']}:</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)

        # Chat input
        st.markdown("---")

        user_input = st.text_input(
            "Your question:",
            placeholder="Ask about history, architecture, daily life...",
            key="chat_input",
            label_visibility="collapsed"
        )

        col_send, col_status = st.columns([3, 1])

        with col_send:
            send_clicked = st.button("📤 Send", use_container_width=True)

        with col_status:
            if st.session_state.audio_enabled: 
                st.markdown("🔊 ON")
            else:
                st.markdown("🔇 OFF")

        # Handle send
        if send_clicked and user_input and st.session_state.api_configured:
            st.session_state.chat_history.append({
                "role":  "user",
                "content":  user_input
            })

            with st.spinner("✨ Channeling... "):
                response = generate_persona_response(
                    st. session_state.current_persona,
                    st.session_state.current_landmark,
                    user_input,
                    st. session_state.chat_history[:-1],
                    st.session_state.model
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

                if st.session_state.audio_enabled:
                    audio = text_to_speech(response)
                    if audio:
                        st.markdown(get_audio_html(audio, autoplay=True), unsafe_allow_html=True)

            st.rerun()

        # Suggested questions
        st.markdown("---")
        st.markdown("**💡 Try asking:**")

        suggestions = get_suggested_questions(
            st.session_state.current_persona,
            st.session_state.current_landmark
        )

        for i, suggestion in enumerate(suggestions):
            if st.button(f"❓ {suggestion}", key=f"sug_{i}", use_container_width=True):
                st.session_state. chat_history.append({
                    "role": "user",
                    "content": suggestion
                })

                with st.spinner("✨"):
                    response = generate_persona_response(
                        st. session_state.current_persona,
                        st.session_state.current_landmark,
                        suggestion,
                        st.session_state.chat_history[:-1],
                        st.session_state.model
                    )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })

                st.rerun()

    else:
        # No persona - show instructions
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #a0a0a0;">
            <h2>🔮 Begin Your Journey</h2>
            <p>Upload an image of a landmark</p>
            <p>— or —</p>
            <p>Click a Quick Demo button in sidebar</p>
            <br>
            <p style="font-size: 0.9rem;">
                👑 King Rama Pandya • 🙏 Temple Priest<br>
                🎩 British Collector • ⚔️ Kattabomman
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============== FOOTER ==============
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🏛️ <strong>TimeTraveler AI:  The Nellai Chronicles</strong></p>
    <p>Built with ❤️ for Tirunelveli | Hackathon 2025</p>
    <p style="font-size: 0.8rem;">Powered by Gemini 2.5 Flash | Streamlit | gTTS</p>
</div>
""", unsafe_allow_html=True)
