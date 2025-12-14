"""
Immersive Fullscreen View for TimeTraveler AI.
Creates a cinematic fullscreen experience with slideshow, avatar, and subtitles.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Optional
import json


def create_immersive_html(
    images: List[Dict],
    persona_data: Dict,
    subtitle_text: str,
    current_index: int = 0,
    show_audio_visualizer: bool = False
) -> str:
    """
    Create fullscreen immersive HTML/CSS/JS component.
    
    Args:
        images: List of image dicts with 'url' and 'caption'
        persona_data: Persona data dict
        subtitle_text: Text to display as subtitle
        current_index: Current image index
        show_audio_visualizer: Whether to show audio visualizer
        
    Returns:
        HTML string
    """
    
    # Prepare images JSON
    images_json = json.dumps([{
        "url": img.get("url", ""),
        "caption": img.get("caption", "")
    } for img in images])
    
    # Get persona details
    avatar = persona_data.get("avatar", "👤")
    name = persona_data.get("name", "Guide")
    title = persona_data.get("title", "")
    era = persona_data.get("era", "")
    
    # Create audio visualizer bars
    visualizer_bars = ""
    if show_audio_visualizer:
        bars = []
        for i in range(20):
            delay = i * 0.05
            bars.append(f'<div class="viz-bar" style="animation-delay: {delay}s;"></div>')
        visualizer_bars = "".join(bars)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #000;
                overflow: hidden;
                width: 100vw;
                height: 100vh;
            }}
            
            .immersive-container {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #0a0a15 0%, #1a1a2e 50%, #0f3460 100%);
                display: flex;
                flex-direction: column;
                z-index: 9999;
            }}
            
            /* Close Button */
            .close-btn {{
                position: absolute;
                top: 20px;
                right: 20px;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: rgba(233, 69, 96, 0.8);
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                z-index: 10001;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .close-btn:hover {{
                background: #e94560;
                transform: scale(1.1);
            }}
            
            /* Main Content Area */
            .content-area {{
                flex: 1;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }}
            
            /* Slideshow Container */
            .slideshow {{
                position: relative;
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .slide {{
                position: absolute;
                width: 100%;
                height: 100%;
                display: none;
                align-items: center;
                justify-content: center;
                animation: fadeIn 1s ease-in-out;
            }}
            
            .slide.active {{
                display: flex;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.95); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}
            
            .slide-image {{
                max-width: 85%;
                max-height: 75vh;
                object-fit: contain;
                border-radius: 15px;
                box-shadow: 0 0 60px rgba(233, 69, 96, 0.4);
                background: rgba(0,0,0,0.2);
            }}
            
            .slide-image.error {{
                background: rgba(233, 69, 96, 0.2);
                border: 2px dashed #e94560;
            }}
            
            /* Gradient Overlay */
            .gradient-overlay {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 40%;
                background: linear-gradient(to top, rgba(0,0,0,0.95), transparent);
                pointer-events: none;
            }}
            
            /* Navigation Arrows */
            .nav-arrow {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                width: 60px;
                height: 60px;
                background: rgba(233, 69, 96, 0.7);
                border: none;
                border-radius: 50%;
                color: white;
                font-size: 24px;
                cursor: pointer;
                z-index: 10000;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .nav-arrow:hover {{
                background: #e94560;
                transform: translateY(-50%) scale(1.1);
            }}
            
            .nav-arrow.prev {{ left: 30px; }}
            .nav-arrow.next {{ right: 30px; }}
            
            /* Slide Indicators */
            .indicators {{
                position: absolute;
                top: 30px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
                z-index: 10000;
            }}
            
            .indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                cursor: pointer;
                transition: all 0.3s;
            }}
            
            .indicator.active {{
                background: #e94560;
                width: 30px;
                border-radius: 6px;
            }}
            
            /* Image Caption */
            .image-caption {{
                position: absolute;
                top: 70px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.7);
                color: #00fff5;
                padding: 10px 25px;
                border-radius: 25px;
                font-size: 14px;
                border: 1px solid #00fff5;
                max-width: 80%;
                text-align: center;
                z-index: 10000;
            }}
            
            /* Avatar Section */
            .avatar-section {{
                position: absolute;
                bottom: 180px;
                left: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
                animation: slideInLeft 0.8s ease-out;
                z-index: 10000;
            }}
            
            @keyframes slideInLeft {{
                from {{ transform: translateX(-100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            
            .avatar-emoji {{
                font-size: 100px;
                margin-bottom: 15px;
                animation: pulse 2s ease-in-out infinite;
                filter: drop-shadow(0 0 20px rgba(233, 69, 96, 0.6));
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); filter: drop-shadow(0 0 20px rgba(233, 69, 96, 0.6)); }}
                50% {{ transform: scale(1.05); filter: drop-shadow(0 0 30px rgba(233, 69, 96, 0.9)); }}
            }}
            
            .avatar-name {{
                color: #e94560;
                font-size: 22px;
                font-weight: bold;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }}
            
            .avatar-title {{
                color: #00fff5;
                font-size: 14px;
                text-align: center;
                margin-top: 5px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }}
            
            /* Subtitle Section */
            .subtitle-section {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 40px 60px;
                background: linear-gradient(to top, rgba(0,0,0,0.95), transparent);
                z-index: 10000;
            }}
            
            .subtitle-text {{
                color: #ffffff;
                font-size: 22px;
                line-height: 1.8;
                text-align: center;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.9);
                max-width: 1000px;
                margin: 0 auto;
                animation: subtitleFade 1s ease-in;
            }}
            
            @keyframes subtitleFade {{
                from {{ opacity: 0; transform: translateY(30px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            /* Audio Visualizer */
            .audio-visualizer {{
                position: absolute;
                bottom: 150px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 5px;
                align-items: flex-end;
                height: 50px;
                z-index: 10000;
            }}
            
            .viz-bar {{
                width: 5px;
                background: linear-gradient(to top, #e94560, #00fff5);
                border-radius: 3px;
                animation: visualize 0.6s ease-in-out infinite alternate;
            }}
            
            @keyframes visualize {{
                from {{ height: 10px; opacity: 0.6; }}
                to {{ height: 45px; opacity: 1; }}
            }}
            
            /* Responsive */
            @media (max-width: 768px) {{
                .slide-image {{
                    max-width: 95%;
                    max-height: 60vh;
                }}
                
                .avatar-section {{
                    bottom: 200px;
                    left: 20px;
                }}
                
                .avatar-emoji {{
                    font-size: 60px;
                }}
                
                .avatar-name {{
                    font-size: 16px;
                }}
                
                .subtitle-text {{
                    font-size: 16px;
                    padding: 0 20px;
                }}
                
                .nav-arrow {{
                    width: 45px;
                    height: 45px;
                    font-size: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="immersive-container">
            <button class="close-btn" onclick="closeImmersive()">×</button>
            
            <div class="content-area">
                <div class="slideshow" id="slideshow">
                    <!-- Slides will be generated by JS -->
                </div>
                
                <div class="gradient-overlay"></div>
                
                <button class="nav-arrow prev" onclick="changeSlide(-1)">‹</button>
                <button class="nav-arrow next" onclick="changeSlide(1)">›</button>
                
                <div class="indicators" id="indicators">
                    <!-- Indicators will be generated by JS -->
                </div>
                
                <div class="image-caption" id="imageCaption"></div>
                
                <div class="avatar-section">
                    <div class="avatar-emoji">{avatar}</div>
                    <div class="avatar-name">{name}</div>
                    <div class="avatar-title">{title}</div>
                    <div class="avatar-title">{era}</div>
                </div>
                
                {f'<div class="audio-visualizer">{visualizer_bars}</div>' if show_audio_visualizer else ''}
                
                <div class="subtitle-section">
                    <div class="subtitle-text">{subtitle_text}</div>
                </div>
            </div>
        </div>
        
        <script>
            const images = {images_json};
            let currentSlide = {current_index};
            
            function initSlideshow() {{
                const slideshow = document.getElementById('slideshow');
                const indicators = document.getElementById('indicators');
                
                // Create slides
                images.forEach((img, index) => {{
                    const slide = document.createElement('div');
                    slide.className = 'slide' + (index === currentSlide ? ' active' : '');
                    const imgElement = document.createElement('img');
                    imgElement.src = img.url;
                    imgElement.className = 'slide-image';
                    imgElement.alt = img.caption;
                    imgElement.onerror = function() {{
                        this.classList.add('error');
                        this.alt = 'Image failed to load';
                    }};
                    slide.appendChild(imgElement);
                    slideshow.appendChild(slide);
                    
                    // Create indicator
                    const indicator = document.createElement('div');
                    indicator.className = 'indicator' + (index === currentSlide ? ' active' : '');
                    indicator.onclick = () => goToSlide(index);
                    indicators.appendChild(indicator);
                }});
                
                updateCaption();
            }}
            
            function changeSlide(direction) {{
                const slides = document.querySelectorAll('.slide');
                const indicators = document.querySelectorAll('.indicator');
                
                slides[currentSlide].classList.remove('active');
                indicators[currentSlide].classList.remove('active');
                
                currentSlide = (currentSlide + direction + images.length) % images.length;
                
                slides[currentSlide].classList.add('active');
                indicators[currentSlide].classList.add('active');
                
                updateCaption();
            }}
            
            function goToSlide(index) {{
                const slides = document.querySelectorAll('.slide');
                const indicators = document.querySelectorAll('.indicator');
                
                slides[currentSlide].classList.remove('active');
                indicators[currentSlide].classList.remove('active');
                
                currentSlide = index;
                
                slides[currentSlide].classList.add('active');
                indicators[currentSlide].classList.add('active');
                
                updateCaption();
            }}
            
            function updateCaption() {{
                const caption = document.getElementById('imageCaption');
                if (images[currentSlide]) {{
                    caption.textContent = images[currentSlide].caption;
                }}
            }}
            
            function closeImmersive() {{
                // Signal to Streamlit to close immersive mode
                window.parent.postMessage({{type: 'streamlit:closeImmersive'}}, '*');
            }}
            
            // Auto-advance slides every 8 seconds
            let autoAdvance = setInterval(() => {{
                changeSlide(1);
            }}, 8000);
            
            // Pause auto-advance on hover
            document.querySelector('.slideshow').addEventListener('mouseenter', () => {{
                clearInterval(autoAdvance);
            }});
            
            document.querySelector('.slideshow').addEventListener('mouseleave', () => {{
                autoAdvance = setInterval(() => {{
                    changeSlide(1);
                }}, 8000);
            }});
            
            // Keyboard navigation
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft') changeSlide(-1);
                if (e.key === 'ArrowRight') changeSlide(1);
                if (e.key === 'Escape') closeImmersive();
            }});
            
            // Initialize
            initSlideshow();
        </script>
    </body>
    </html>
    """
    
    return html


def render_immersive_view(
    images: List[Dict],
    persona_data: Dict,
    subtitle_text: str,
    current_index: int = 0,
    show_audio_visualizer: bool = False
):
    """
    Render the immersive fullscreen view using Streamlit components.
    
    Args:
        images: List of image dicts
        persona_data: Persona data dict
        subtitle_text: Subtitle text
        current_index: Current image index
        show_audio_visualizer: Show audio visualizer
    """
    # Ensure we have valid images
    if not images or len(images) == 0:
        st.warning("⚠️ No images available for immersive mode")
        return
    
    html = create_immersive_html(
        images=images,
        persona_data=persona_data,
        subtitle_text=subtitle_text,
        current_index=current_index,
        show_audio_visualizer=show_audio_visualizer
    )
    
    # Use explicit height for better rendering
    components.html(html, height=800, scrolling=False)
