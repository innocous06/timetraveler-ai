"""
Immersive Presentation Mode for TimeTraveler AI.
Creates fullscreen cinematic experience with images, avatar, and subtitles.
"""

import streamlit as st
from typing import Dict, List, Optional
import time

def get_presentation_css() -> str:
    """Get CSS for immersive presentation mode."""
    return """
    <style>
    /* Fullscreen overlay */
    .presentation-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.95);
        z-index: 9999;
        display: flex;
        flex-direction: column;
    }
    
    /* Main content area */
    .presentation-content {
        flex: 1;
        display:  flex;
        position: relative;
        overflow: hidden;
    }
    
    /* Image gallery section */
    .presentation-gallery {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .gallery-image {
        max-width: 90%;
        max-height: 70vh;
        object-fit: contain;
        border-radius: 15px;
        box-shadow:  0 0 50px rgba(233, 69, 96, 0.3);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform:  scale(0.95); }
        to { opacity:  1; transform: scale(1); }
    }
    
    /* Avatar section */
    . avatar-container {
        position: absolute;
        bottom: 150px;
        left: 30px;
        width: 200px;
        text-align: center;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .avatar-image {
        width: 150px;
        height: 150px;
        border-radius:  50%;
        border: 4px solid #e94560;
        box-shadow: 0 0 30px rgba(233, 69, 96, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 30px rgba(233, 69, 96, 0.5); }
        50% { box-shadow: 0 0 50px rgba(233, 69, 96, 0.8); }
    }
    
    . avatar-name {
        color: #e94560;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 10px;
    }
    
    .avatar-title {
        color: #00fff5;
        font-size: 0.9rem;
    }
    
    /* Subtitle section */
    .subtitle-container {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.9));
        padding: 30px 50px;
    }
    
    .subtitle-text {
        color: #ffffff;
        font-size: 1.4rem;
        line-height: 1.8;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        max-width: 900px;
        margin: 0 auto;
        animation: subtitleFade 0.5s ease-in;
    }
    
    @keyframes subtitleFade {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Close button */
    .close-button {
        position: absolute;
        top: 20px;
        right: 30px;
        background: rgba(233, 69, 96, 0.8);
        border: none;
        color: white;
        font-size: 1.5rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        z-index: 10000;
        transition: all 0.3s;
    }
    
    . close-button:hover {
        background: #e94560;
        transform:  scale(1.1);
    }
    
    /* Gallery navigation */
    .gallery-nav {
        position: absolute;
        top: 50%;
        transform:  translateY(-50%);
        background: rgba(233, 69, 96, 0.6);
        border: none;
        color: white;
        font-size: 2rem;
        padding: 20px 15px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .gallery-nav:hover {
        background:  #e94560;
    }
    
    .gallery-nav.prev { left: 20px; border-radius: 0 10px 10px 0; }
    .gallery-nav.next { right: 20px; border-radius: 10px 0 0 10px; }
    
    /* Image caption */
    .image-caption {
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.7);
        color: #00fff5;
        padding: 10px 25px;
        border-radius:  25px;
        font-size:  1rem;
        border: 1px solid #00fff5;
    }
    
    /* Audio visualizer effect */
    .audio-visualizer {
        position: absolute;
        bottom: 120px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 4px;
        align-items: flex-end;
        height: 40px;
    }
    
    .visualizer-bar {
        width:  4px;
        background: linear-gradient(to top, #e94560, #00fff5);
        border-radius: 2px;
        animation: visualize 0.5s ease-in-out infinite alternate;
    }
    
    @keyframes visualize {
        from { height: 10px; }
        to { height: 35px; }
    }
    
    /* Ambience indicator */
    .ambience-indicator {
        position: absolute;
        top: 20px;
        left: 20px;
        color: #00fff5;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .ambience-icon {
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    </style>
    """


def get_ambience_icon(ambience_type: str) -> str:
    """Get icon for ambience type."""
    icons = {
        "temple_bells": "🔔",
        "royal_court": "👑",
        "war_drums": "🥁",
        "colonial_office": "📜",
        "egyptian_palace": "🏺",
        "workshop": "🔧",
        "buddhist_monastery": "☸️",
        "laboratory": "⚗️",
    }
    return icons.get(ambience_type, "🎵")


def get_ambience_description(ambience_type: str) -> str:
    """Get description for ambience."""
    descriptions = {
        "temple_bells": "Temple bells echoing.. .",
        "royal_court":  "Royal court ambience.. .",
        "war_drums":  "Distant war drums...",
        "colonial_office": "Colonial office sounds...",
        "egyptian_palace": "Desert winds whisper...",
        "workshop":  "Workshop sounds...",
        "buddhist_monastery": "Monks chanting...",
        "laboratory": "Laboratory bubbling...",
    }
    return descriptions.get(ambience_type, "Ambient sounds...")


def create_presentation_html(
    image_url: str,
    image_caption: str,
    avatar_emoji: str,
    persona_name: str,
    persona_title: str,
    subtitle_text: str,
    ambience_type: str = None,
    show_visualizer: bool = True
) -> str:
    """Create HTML for immersive presentation."""
    
    ambience_html = ""
    if ambience_type: 
        icon = get_ambience_icon(ambience_type)
        desc = get_ambience_description(ambience_type)
        ambience_html = f"""
        <div class="ambience-indicator">
            <span class="ambience-icon">{icon}</span>
            <span>{desc}</span>
        </div>
        """
    
    visualizer_html = ""
    if show_visualizer:
        bars = "". join([
            f'<div class="visualizer-bar" style="animation-delay: {i*0.1}s;"></div>'
            for i in range(15)
        ])
        visualizer_html = f'<div class="audio-visualizer">{bars}</div>'
    
    html = f"""
    <div class="presentation-content">
        {ambience_html}
        
        <div class="image-caption">{image_caption}</div>
        
        <div class="presentation-gallery">
            <img src="{image_url}" class="gallery-image" alt="{image_caption}">
        </div>
        
        <div class="avatar-container">
            <div style="font-size: 80px; margin-bottom: 10px;">{avatar_emoji}</div>
            <div class="avatar-name">{persona_name}</div>
            <div class="avatar-title">{persona_title}</div>
        </div>
        
        {visualizer_html}
        
        <div class="subtitle-container">
            <div class="subtitle-text">{subtitle_text}</div>
        </div>
    </div>
    """
    return html


def render_presentation_mode(
    landmark_data: Dict,
    persona_data: Dict,
    current_text: str,
    image_index: int = 0
):
    """Render the immersive presentation mode in Streamlit."""
    
    # Get gallery images
    gallery = landmark_data.get("gallery_images", [])
    if not gallery:
        gallery = [{"url": "https://via.placeholder.com/800x600? text=No+Image", "caption": "Image not available"}]
    
    current_image = gallery[image_index % len(gallery)]
    
    # CSS
    st.markdown(get_presentation_css(), unsafe_allow_html=True)
    
    # Presentation HTML
    presentation_html = create_presentation_html(
        image_url=current_image["url"],
        image_caption=current_image["caption"],
        avatar_emoji=persona_data.get("avatar", "👤"),
        persona_name=persona_data.get("name", "Unknown"),
        persona_title=persona_data.get("title", ""),
        subtitle_text=current_text,
        ambience_type=persona_data.get("ambience"),
        show_visualizer=True
    )
    
    st.markdown(presentation_html, unsafe_allow_html=True)


def create_mini_presentation(
    persona_data: Dict,
    landmark_data: Dict,
    response_text: str,
    audio_b64: str = None
) -> None:
    """Create a mini presentation view within the chat."""
    
    gallery = landmark_data.get("gallery_images", []) if landmark_data else []
    
    # Container with styling
    st.markdown("""
    <style>
    .mini-presentation {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #e94560;
        border-radius:  20px;
        padding:  20px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(233, 69, 96, 0.3);
    }
    . mini-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom:  1px solid #333;
    }
    .mini-avatar {
        font-size: 50px;
    }
    .mini-name {
        color: #e94560;
        font-size: 1.3rem;
        font-weight: bold;
    }
    .mini-title {
        color: #00fff5;
        font-size: 0.9rem;
    }
    .mini-response {
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.8;
        padding: 15px;
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        border-left: 4px solid #e94560;
    }
    .mini-gallery {
        display: flex;
        gap: 10px;
        margin-top: 15px;
        overflow-x: auto;
        padding: 10px 0;
    }
    . mini-gallery img {
        height: 120px;
        border-radius: 10px;
        border: 2px solid #333;
        transition: all 0.3s;
    }
    .mini-gallery img:hover {
        border-color: #e94560;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Build gallery HTML
    gallery_html = ""
    if gallery:
        images_html = "".join([
            f'<img src="{img["url"]}" alt="{img["caption"]}" title="{img["caption"]}">'
            for img in gallery[: 4]
        ])
        gallery_html = f'<div class="mini-gallery">{images_html}</div>'
    
    # Main presentation
    st.markdown(f"""
    <div class="mini-presentation">
        <div class="mini-header">
            <div class="mini-avatar">{persona_data.get('avatar', '👤')}</div>
            <div>
                <div class="mini-name">{persona_data.get('name', 'Unknown')}</div>
                <div class="mini-title">{persona_data.get('title', '')} • {persona_data.get('era', '')}</div>
            </div>
        </div>
        <div class="mini-response">{response_text}</div>
        {gallery_html}
    </div>
    """, unsafe_allow_html=True)
