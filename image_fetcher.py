"""
Image Fetcher for TimeTraveler AI. 
Fetches real images from Wikipedia/Wikimedia Commons with reliable fallbacks.
"""

import requests
import streamlit as st
from typing import List, Dict
import time
import hashlib


# Wikipedia API endpoint
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

# Reliable placeholder images (these ALWAYS work)
PLACEHOLDER_IMAGES = [
    "https://images.unsplash.com/photo-1524492412937-b28074a5d7da? w=800",  # Taj Mahal
    "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800",  # Taj Mahal 2
    "https://images.unsplash.com/photo-1548013146-72479768bada?w=800",  # India monument
    "https://images.unsplash.com/photo-1506461883276-594a12b11cf3?w=800",  # Ancient temple
    "https://images.unsplash.com/photo-1545126550-ece49ce5ca40?w=800",  # Historical building
]


def init_image_cache():
    """Initialize image cache in session state."""
    if 'image_cache' not in st.session_state:
        st.session_state.image_cache = {}


def get_reliable_fallback_images(landmark_name: str = "", count: int = 4) -> List[Dict]:
    """
    Get reliable placeholder images that ALWAYS work.
    Uses Unsplash images which are reliable and free.
    """
    # Create unique but consistent images based on landmark name
    seed = hashlib.md5(landmark_name.encode()).hexdigest()[:8]
    
    images = []
    for i in range(count):
        # Use Lorem Picsum which is very reliable
        url = f"https://picsum.photos/seed/{seed}{i}/800/600"
        images.append({
            "url":  url,
            "caption": f"{landmark_name} - View {i+1}" if landmark_name else f"Historical Monument - View {i+1}"
        })
    
    return images


def search_wikipedia_images(search_term: str, limit: int = 5) -> List[Dict]:
    """
    Search for images on Wikipedia.
    Returns list of dicts with 'url' and 'caption'. 
    """
    try: 
        init_image_cache()
        
        # Check cache
        cache_key = f"wiki_{search_term}_{limit}"
        if cache_key in st.session_state. image_cache:
            return st.session_state.image_cache[cache_key]
        
        images = []
        
        # Step 1: Search for the Wikipedia page
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_term,
            "srlimit": 1
        }
        
        response = requests.get(WIKIPEDIA_API, params=search_params, timeout=10)
        if response.status_code != 200:
            return []
        
        data = response.json()
        search_results = data.get("query", {}).get("search", [])
        
        if not search_results:
            return []
        
        page_title = search_results[0]["title"]
        time.sleep(0.1)  # Rate limiting
        
        # Step 2: Get images from the page
        image_params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "images",
            "imlimit": 20
        }
        
        response = requests.get(WIKIPEDIA_API, params=image_params, timeout=10)
        if response. status_code != 200:
            return []
        
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        image_titles = []
        for page_id, page_data in pages.items():
            for img in page_data.get("images", []):
                title = img.get("title", "")
                # Filter out non-photos
                if any(ext in title.lower() for ext in ['.jpg', '.jpeg', '. png']):
                    if not any(skip in title.lower() for skip in ['icon', 'logo', 'flag', 'map', 'symbol', 'button', 'commons-logo']):
                        image_titles. append(title)
        
        # Step 3: Get actual URLs for each image
        for img_title in image_titles[: limit + 3]: 
            time.sleep(0.1)  # Rate limiting
            
            url_params = {
                "action":  "query",
                "format": "json",
                "titles": img_title,
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": 800
            }
            
            try:
                response = requests.get(WIKIPEDIA_API, params=url_params, timeout=10)
                if response.status_code != 200:
                    continue
                
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                
                for page_id, page_data in pages.items():
                    imageinfo = page_data.get("imageinfo", [])
                    if imageinfo:
                        thumb_url = imageinfo[0]. get("thumburl") or imageinfo[0].get("url")
                        if thumb_url:
                            caption = img_title. replace("File:", "").replace("_", " ")
                            caption = caption.rsplit(".", 1)[0][:50]  # Remove extension, limit length
                            images.append({
                                "url": thumb_url,
                                "caption": caption
                            })
                
                if len(images) >= limit:
                    break
                    
            except Exception:
                continue
        
        # Cache results
        if images:
            st.session_state.image_cache[cache_key] = images
        
        return images[: limit]
        
    except Exception as e:
        print(f"Wikipedia API error: {e}")
        return []


def fetch_landmark_images(landmark_name: str, landmark_info: Dict = None) -> List[Dict]:
    """
    Main function to fetch images for a landmark.
    Tries Wikipedia first, falls back to reliable placeholders.
    """
    init_image_cache()
    
    # Determine search term
    if landmark_info:
        search_term = landmark_info.get("wikipedia_search") or landmark_info.get("name") or landmark_name
    else:
        search_term = landmark_name
    
    # Try Wikipedia first
    images = search_wikipedia_images(search_term, limit=5)
    
    # If not enough images, try with location added
    if len(images) < 3 and landmark_info:
        location = landmark_info.get("location", "")
        if location: 
            more_images = search_wikipedia_images(f"{search_term} {location}", limit=3)
            for img in more_images:
                if img["url"] not in [i["url"] for i in images]: 
                    images.append(img)
    
    # If still not enough, add reliable fallbacks
    if len(images) < 3:
        fallbacks = get_reliable_fallback_images(search_term, count=4 - len(images))
        images.extend(fallbacks)
    
    return images[: 5]


def get_fallback_images(category: str = "monument", count: int = 4) -> List[Dict]:
    """Get fallback images - wrapper for compatibility."""
    return get_reliable_fallback_images(category, count)
