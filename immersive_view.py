"""
Immersive Fullscreen View for TimeTraveler AI.
Creates a cinematic experience with slideshow, avatar, and subtitles.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List
import json


def render_immersive_view(
    images: List[Dict],
    persona_data: Dict,
    subtitle_text: str,
    current_index: int = 0,
    show_audio_visualizer: bool = False
):
    """
    Render the immersive fullscreen view.
    """
    
    # Prepare images JSON - ensure we have at least placeholder
    if not images:
        images = [{"url": "https://picsum.photos/800/600", "caption": "Historical Monument"}]
    
    images_json = json.dumps([{
        "url": img. get("url", "https://picsum.photos/800/600"),
        "caption": img.get("caption", "View")[: 50]
    } for img in images[: 5]])
    
    # Get persona details
    avatar = persona_data.get("avatar", "👤")
    name = persona_data.get("name", "Historical Guide")
    title = persona_data.get("title", "")
    era = persona_data.get("era", "")
    
    # Escape subtitle text for HTML
    subtitle_safe = subtitle_text.replace('"', '&quot;').replace("'", "&#39;").replace("\n", "<br>")
    
    # Visualizer bars HTML
    visualizer_html = ""
    if show_audio_visualizer:
        bars = "". join([f'<div class="viz-bar" style="animation-delay: {i*0.05}s;"></div>' for i in range(20)])
        visualizer_html = f'<div class="audio-visualizer">{bars}</div>'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background:  linear-gradient(135deg, #0a0a15 0%, #1a1a2e 50%, #0f3460 100%);
                color: white;
                overflow: hidden;
                height: 100vh;
            }}
            
            .container {{
                position: relative;
                width: 100%;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }}
            
            /* Slideshow */
            .slideshow {{
                flex: 1;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }}
            
            .slide {{
                position: absolute;
                width: 100%;
                height: 100%;
                display: none;
                align-items: center;
                justify-content: center;
                animation: fadeIn 1s ease;
            }}
            
            . slide.active {{ display: flex; }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.95); }}
                to {{ opacity:  1; transform: scale(1); }}
            }}
            
            . slide img {{
                max-width: 80%;
                max-height: 65vh;
                object-fit: contain;
                border-radius: 15px;
                box-shadow: 0 0 50px rgba(233, 69, 96, 0.4);
            }}
            
            /* Gradient overlay */
            .gradient {{
                position: absolute;
                bottom: 0;
                left:  0;
                right: 0;
                height: 50%;
                background: linear-gradient(transparent, rgba(0,0,0,0.9));
                pointer-events: none;
            }}
            
            /* Navigation */
            .nav-btn {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(233, 69, 96, 0.7);
                border: none;
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                font-size: 24px;
                cursor: pointer;
                z-index: 100;
                transition: all 0.3s;
            }}
            
            . nav-btn:hover {{ background: #e94560; transform: translateY(-50%) scale(1.1); }}
            . nav-btn. prev {{ left: 20px; }}
            .nav-btn.next {{ right: 20px; }}
            
            /* Indicators */
            .indicators {{
                position: absolute;
                top: 20px;
                left: 50%;
                transform:  translateX(-50%);
                display: flex;
                gap:  8px;
                z-index:  100;
            }}
            
            .indicator {{
                width: 10px;
                height: 10px;
                border-radius:  50%;
                background: rgba(255,255,255,0.3);
                cursor: pointer;
                transition: all 0.3s;
            }}
            
            .indicator.active {{
                background: #e94560;
                width: 25px;
                border-radius: 5px;
            }}
            
            /* Caption */
            .caption {{
                position: absolute;
                top: 50px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.7);
                color: #00fff5;
                padding: 8px 20px;
                border-radius:  20px;
                font-size:  14px;
                border: 1px solid #00fff5;
                z-index: 100;
            }}
            
            /* Avatar */
            .avatar-section {{
                position: absolute;
                bottom: 160px;
                left: 30px;
                text-align: center;
                animation: slideIn 0.8s ease;
                z-index: 100;
            }}
            
            @keyframes slideIn {{
                from {{ transform: translateX(-100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            
            .avatar-emoji {{
                font-size: 80px;
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
            
            . avatar-name {{
                color: #e94560;
                font-size: 18px;
                font-weight:  bold;
                margin-top: 10px;
            }}
            
            .avatar-title {{
                color: #00fff5;
                font-size: 12px;
            }}
            
            /* Audio visualizer */
            .audio-visualizer {{
                position: absolute;
                bottom: 130px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 4px;
                align-items: flex-end;
                height: 40px;
                z-index:  100;
            }}
            
            .viz-bar {{
                width: 4px;
                background: linear-gradient(to top, #e94560, #00fff5);
                border-radius: 2px;
                animation: viz 0.5s ease-in-out infinite alternate;
            }}
            
            @keyframes viz {{
                from {{ height: 10px; }}
                to {{ height: 35px; }}
            }}
            
            /* Subtitles */
            .subtitles {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 30px 50px;
                text-align: center;
                z-index: 100;
            }}
            
            .subtitle-text {{
                color: white;
                font-size: 18px;
                line-height: 1.7;
                max-width: 900px;
                margin: 0 auto;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="slideshow" id="slideshow"></div>
            <div class="gradient"></div>
            
            <button class="nav-btn prev" onclick="changeSlide(-1)">‹</button>
            <button class="nav-btn next" onclick="changeSlide(1)">›</button>
            
            <div class="indicators" id="indicators"></div>
            <div class="caption" id="caption"></div>
            
            <div class="avatar-section">
                <div class="avatar-emoji">{avatar}</div>
                <div class="avatar-name">{name}</div>
                <div class="avatar-title">{title}</div>
                <div class="avatar-title">{era}</div>
            </div>
            
            {visualizer_html}
            
            <div class="subtitles">
                <div class="subtitle-text">{subtitle_safe}</div>
            </div>
        </div>
        
        <script>
            const images = {images_json};
            let current = 0;
            
            function init() {{
                const slideshow = document.getElementById('slideshow');
                const indicators = document.getElementById('indicators');
                
                images.forEach((img, i) => {{
                    const slide = document.createElement('div');
                    slide.className = 'slide' + (i === 0 ? ' active' : '');
                    slide.innerHTML = '<img src="' + img.url + '" onerror="this.src=\\'https://picsum.photos/800/600? random=' + i + '\\'">';
                    slideshow.appendChild(slide);
                    
                    const dot = document.createElement('div');
                    dot.className = 'indicator' + (i === 0 ?  ' active' : '');
                    dot.onclick = () => goTo(i);
                    indicators. appendChild(dot);
                }});
                
                updateCaption();
                setInterval(() => changeSlide(1), 6000);
            }}
            
            function changeSlide(dir) {{
                const slides = document.querySelectorAll('.slide');
                const dots = document.querySelectorAll('. indicator');
                
                slides[current].classList.remove('active');
                dots[current].classList. remove('active');
                
                current = (current + dir + images. length) % images.length;
                
                slides[current].classList.add('active');
                dots[current].classList.add('active');
                updateCaption();
            }}
            
            function goTo(i) {{
                const slides = document.querySelectorAll('.slide');
                const dots = document.querySelectorAll('.indicator');
                
                slides[current].classList.remove('active');
                dots[current].classList.remove('active');
                
                current = i;
                
                slides[current].classList.add('active');
                dots[current].classList.add('active');
                updateCaption();
            }}
            
            function updateCaption() {{
                document.getElementById('caption').textContent = images[current].caption;
            }}
            
            init();
        </script>
    </body>
    </html>
    """
    
    components.html(html, height=750, scrolling=False)
