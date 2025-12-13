"""
Image Fetcher for TimeTraveler AI.
Fetches real images from Wikipedia/Wikimedia Commons API with caching.
"""

import requests
import streamlit as st
from typing import List, Dict, Optional
import urllib.parse
import re


# Wikipedia API endpoint
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Unsplash fallback URLs (free to use)
UNSPLASH_FALLBACKS = {
    "temple": "https://source.unsplash.com/800x600/?indian,temple,architecture",
    "palace": "https://source.unsplash.com/800x600/?palace,architecture,historical",
    "fort": "https://source.unsplash.com/800x600/?fort,castle,historical",
    "monument": "https://source.unsplash.com/800x600/?monument,historical,architecture",
    "pyramid": "https://source.unsplash.com/800x600/?pyramid,egypt,ancient",
    "rome": "https://source.unsplash.com/800x600/?rome,colosseum,ancient",
    "taj": "https://source.unsplash.com/800x600/?taj,mahal,india",
    "stupa": "https://source.unsplash.com/800x600/?stupa,buddhist,temple",
}


def init_image_cache():
    """Initialize image cache in session state."""
    if 'image_cache' not in st.session_state:
        st.session_state.image_cache = {}


def search_wikipedia_images(search_term: str, limit: int = 5) -> List[Dict]:
    """
    Search for images on Wikipedia/Wikimedia Commons.
    
    Args:
        search_term: Term to search for
        limit: Maximum number of images to return
        
    Returns:
        List of dicts with 'url' and 'caption' keys
    """
    try:
        # Check cache first
        cache_key = f"{search_term}_{limit}"
        if cache_key in st.session_state.get('image_cache', {}):
            return st.session_state.image_cache[cache_key]
        
        images = []
        
        # Step 1: Search for the page
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_term,
            "srlimit": 1
        }
        
        response = requests.get(WIKIPEDIA_API_URL, params=search_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("query", {}).get("search"):
            return []
        
        page_title = data["query"]["search"][0]["title"]
        
        # Step 2: Get images from the page
        image_params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "images",
            "imlimit": limit * 3  # Get more to filter
        }
        
        response = requests.get(WIKIPEDIA_API_URL, params=image_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()), {})
        image_list = page.get("images", [])
        
        # Step 3: Get image URLs
        for img in image_list[:limit * 2]:
            img_title = img.get("title", "")
            
            # Skip non-image files
            if not any(ext in img_title.lower() for ext in ['.jpg', '.jpeg', '.png', '.svg']):
                continue
            
            # Skip icons, logos, flags
            if any(skip in img_title.lower() for skip in ['icon', 'logo', 'flag', 'button', 'symbol']):
                continue
            
            # Get image info
            info_params = {
                "action": "query",
                "format": "json",
                "titles": img_title,
                "prop": "imageinfo",
                "iiprop": "url|extmetadata",
                "iiurlwidth": 800
            }
            
            response = requests.get(WIKIPEDIA_API_URL, params=info_params, timeout=10)
            response.raise_for_status()
            info_data = response.json()
            
            info_pages = info_data.get("query", {}).get("pages", {})
            info_page = next(iter(info_pages.values()), {})
            imageinfo = info_page.get("imageinfo", [{}])[0]
            
            if imageinfo.get("thumburl"):
                # Get caption from metadata
                extmetadata = imageinfo.get("extmetadata", {})
                caption = extmetadata.get("ImageDescription", {}).get("value", "")
                if not caption:
                    caption = extmetadata.get("ObjectName", {}).get("value", img_title)
                
                # Clean HTML from caption
                caption = re.sub('<[^<]+?>', '', caption)
                caption = caption[:100] if len(caption) > 100 else caption
                
                images.append({
                    "url": imageinfo["thumburl"],
                    "caption": caption or img_title.replace("File:", "").replace("_", " ")
                })
            
            if len(images) >= limit:
                break
        
        # Cache the results
        if images:
            if 'image_cache' not in st.session_state:
                st.session_state.image_cache = {}
            st.session_state.image_cache[cache_key] = images
        
        return images
    
    except Exception as e:
        print(f"Wikipedia image search error for '{search_term}': {e}")
        return []


def get_fallback_images(category: str = "monument", count: int = 3) -> List[Dict]:
    """
    Get fallback images from Unsplash.
    
    Args:
        category: Category of images (temple, palace, fort, etc.)
        count: Number of images to generate
        
    Returns:
        List of dicts with 'url' and 'caption' keys
    """
    base_url = UNSPLASH_FALLBACKS.get(category, UNSPLASH_FALLBACKS["monument"])
    
    images = []
    for i in range(count):
        # Add random parameter to get different images
        url = f"{base_url}&sig={i}"
        images.append({
            "url": url,
            "caption": f"Historical {category.title()} View {i+1}"
        })
    
    return images


def fetch_landmark_images(landmark_key: str, landmark_data: Dict) -> List[Dict]:
    """
    Fetch images for a landmark using Wikipedia search or fallback.
    
    Args:
        landmark_key: Key of the landmark
        landmark_data: Landmark data dict
        
    Returns:
        List of image dicts with 'url' and 'caption' keys
    """
    init_image_cache()
    
    # Check if images already exist in landmark data
    if landmark_data.get("gallery_images"):
        existing = landmark_data["gallery_images"]
        if existing and all(img.get("url") for img in existing):
            return existing
    
    # Try Wikipedia search
    search_term = landmark_data.get("wikipedia_search") or landmark_data.get("name")
    images = search_wikipedia_images(search_term, limit=5)
    
    # If not enough images, try alternate search terms
    if len(images) < 3:
        # Try with location
        location = landmark_data.get("location", "")
        if location:
            alt_search = f"{search_term} {location}"
            more_images = search_wikipedia_images(alt_search, limit=3)
            images.extend(more_images)
    
    # Remove duplicates
    seen_urls = set()
    unique_images = []
    for img in images:
        if img["url"] not in seen_urls:
            seen_urls.add(img["url"])
            unique_images.append(img)
    
    images = unique_images[:5]
    
    # If still not enough, use fallback
    if len(images) < 2:
        # Determine category from landmark type
        landmark_type = landmark_data.get("type", "").lower()
        category = "monument"
        if "temple" in landmark_type:
            category = "temple"
        elif "palace" in landmark_type:
            category = "palace"
        elif "fort" in landmark_type:
            category = "fort"
        elif "pyramid" in landmark_key:
            category = "pyramid"
        elif "colosseum" in landmark_key:
            category = "rome"
        elif "taj" in landmark_key:
            category = "taj"
        elif "stupa" in landmark_key:
            category = "stupa"
        
        fallback = get_fallback_images(category, count=3)
        images.extend(fallback)
        images = images[:5]
    
    return images


def get_persona_avatar_url(persona_key: str) -> Optional[str]:
    """
    Get avatar image URL for a persona (placeholder for now).
    Could be extended to fetch from Wikipedia.
    
    Args:
        persona_key: Key of the persona
        
    Returns:
        URL string or None
    """
    # For now, return None to use emoji avatars
    # Could be extended to search Wikipedia for historical figure portraits
    return None
