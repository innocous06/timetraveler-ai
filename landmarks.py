"""
Extended landmark database for TimeTraveler AI. 
Covers Tamil Nadu comprehensively + major world landmarks.
"""

LANDMARKS = {
    # ============== TAMIL NADU LANDMARKS ==============
    "nellaiappar_temple": {
        "name": "Nellaiappar Temple",
        "type": "Hindu Temple",
        "location": "Tirunelveli, Tamil Nadu",
        "coordinates": (8.7270, 77.6867),
        "keywords": ["nellaiappar", "temple", "gopuram", "tower", "shiva", "musical pillars", 
                    "tirunelveli", "நெல்லையப்பர்", "திருநெல்வேலி", "mani mandapam"],
        "default_persona": "temple_priest",
        "related_personas": ["king_rama_pandya", "temple_priest"],
        "image_hints": ["gopuram", "tower", "temple", "pillars", "carved", "hindu", "dravidian", "tank", "mandapam"],
        "gallery_images": [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Nellaiappar_Temple_Tower. jpg/800px-Nellaiappar_Temple_Tower.jpg", "caption": "The majestic Gopuram of Nellaiappar Temple"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Musical_Pillars_Nellaiappar.jpg/800px-Musical_Pillars_Nellaiappar.jpg", "caption": "The famous Musical Pillars"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Nellaiappar_Temple_Corridor.jpg/800px-Nellaiappar_Temple_Corridor.jpg", "caption": "Ancient corridors with intricate carvings"},
        ],
        "historical_context": """
# NELLAIAPPAR TEMPLE 🛕

## Overview
An ancient Hindu temple dedicated to Lord Shiva, located in the heart of Tirunelveli.  One of the most significant Shiva temples in South India. 

## Architecture
- **Main Gopuram**: Rises to approximately 150 feet with intricate sculptures
- **48 Musical Pillars**: Each carved from a single granite stone, producing different musical notes when struck
- **Mani Mandapam**: The hall housing the musical pillars - an engineering marvel
- **Thamarai Kulam**: Sacred lotus tank for ritual bathing

## History
- Original temple:  Over 1000 years old
- Major renovations:  Pandya kings (7th-14th century)
- Expansion: Nayak rulers (16th-17th century)
- Musical pillars: Added during Nayak period

## Religious Significance
- **Main Deity**:  Nellaiappar (form of Lord Shiva)
- **Consort**: Kanthimathi Amman (Goddess Parvati)
- **Major Festivals**: Arudra Darshan, Thai Poosam, Panguni Uthiram
- **Daily Rituals**: Six-time puja, abhishekam, deepa aradhana

## Unique Features
- Musical pillars producing the seven swaras (musical notes)
- Stone chain carved from a single rock
- Thousand-pillar mandapam with narrative sculptures
- Ancient inscriptions in Tamil and Grantha script
""",
    },

    "meenakshi_temple": {
        "name": "Meenakshi Amman Temple",
        "type": "Hindu Temple",
        "location": "Madurai, Tamil Nadu",
        "coordinates": (9.9195, 78.1193),
        "keywords": ["meenakshi", "madurai", "amman", "temple", "gopuram", "sundareswarar",
                    "மீனாட்சி", "மதுரை", "thousand pillar hall", "golden lotus tank"],
        "default_persona": "temple_priest",
        "related_personas": ["king_rama_pandya", "temple_priest", "chola_king"],
        "image_hints": ["colorful gopuram", "thousand pillars", "lotus tank", "corridor", "sculptures"],
        "gallery_images": [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Madurai_Meenakshi_temple.jpg/1200px-Madurai_Meenakshi_temple.jpg", "caption": "The colorful towers of Meenakshi Temple"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Meenakshi_Temple_Pond.jpg/800px-Meenakshi_Temple_Pond.jpg", "caption": "The Golden Lotus Tank"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Thousand_Pillar_Hall.jpg/800px-Thousand_Pillar_Hall.jpg", "caption": "The magnificent Thousand Pillar Hall"},
        ],
        "historical_context":  """
# MEENAKSHI AMMAN TEMPLE 🏛️

## Overview
One of the largest and most ancient temple complexes in India, dedicated to Goddess Meenakshi (Parvati) and Lord Sundareswarar (Shiva).

## Architecture
- **14 Gateway Towers (Gopurams)**: Covered with thousands of colorful sculptures
- **Tallest Gopuram**: Southern tower at 170 feet
- **Thousand Pillar Hall**: 985 intricately carved pillars
- **Golden Lotus Tank**: Potramarai Kulam, sacred bathing tank
- **Temple Area**: 45 acres with numerous shrines

## History
- Original temple: 6th century BCE (legendary)
- Present structure:  Primarily 16th-17th century
- Built by:  Nayak dynasty, especially Thirumalai Nayak
- Rebuilt after:  Malik Kafur's destruction in 1310

## Religious Significance
- **Main Deities**: Meenakshi and Sundareswarar
- **Legend**: Meenakshi was born with three breasts, destined to marry Shiva
- **Celestial Wedding**: Celebrated as Chithirai Thiruvizha festival
- **Daily Rituals**: Night ceremony where Shiva visits Meenakshi's chamber

## Cultural Importance
- Center of Tamil Sangam literature
- Mentioned in ancient Tamil texts
- Hub of classical arts and music
- One of the New Seven Wonders of the World (finalist)
""",
    },

    "brihadisvara_temple": {
        "name": "Brihadisvara Temple",
        "type": "Hindu Temple",
        "location": "Thanjavur, Tamil Nadu",
        "coordinates": (10.7828, 79.1318),
        "keywords": ["brihadisvara", "thanjavur", "big temple", "chola", "rajaraja",
                    "பெருவுடையார்", "தஞ்சாவூர்", "peruvudaiyar", "unesco"],
        "default_persona": "chola_king",
        "related_personas": ["chola_king", "temple_priest"],
        "image_hints": ["massive tower", "granite temple", "nandi", "chola", "vimana"],
        "gallery_images": [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Brihadeeswarar_Temple_01.jpg/1200px-Brihadeeswarar_Temple_01.jpg", "caption":  "The towering Vimana of Brihadisvara Temple"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Nandi_Thanjavur. jpg/800px-Nandi_Thanjavur.jpg", "caption": "The massive Nandi statue"},
            {"url":  "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Brihadisvara_paintings.jpg/800px-Brihadisvara_paintings.jpg", "caption": "Ancient Chola frescoes"},
        ],
        "historical_context": """
# BRIHADISVARA TEMPLE (BIG TEMPLE) 🏛️

## Overview
A UNESCO World Heritage Site and one of the largest temples in India, built by Rajaraja Chola I.  A masterpiece of Dravidian architecture. 

## Architecture
- **Vimana (Tower)**: 216 feet - tallest of any ancient temple
- **Capstone**: 80-ton granite block at the summit
- **Mystery**:  How the capstone was raised remains debated
- **Nandi**: 16 feet long, 13 feet high monolithic statue
- **No Shadow**: The vimana casts no shadow at noon

## Construction
- **Built by**: Rajaraja Chola I
- **Period**: 1003-1010 CE
- **Material**: Granite (no granite quarries within 50 miles!)
- **Workers**: Thousands of artisans over 7 years

## Artistic Treasures
- **Chola Frescoes**: Ancient paintings under later Nayak paintings
- **Inscriptions**:  Detailed records of temple administration
- **Bronze Sculptures**: Finest examples of Chola bronze art
- **Bharatanatyam Sculptures**: 108 karanas (dance poses)

## Engineering Marvel
- Built without mortar using interlocking stones
- Precisely aligned with cardinal directions
- Acoustic engineering for ritual music
- Advanced water management system
""",
    },

    "krishnapuram_palace": {
        "name": "Krishnapuram Palace",
        "type": "Palace/Museum",
        "location": "Krishnapuram, Tamil Nadu",
        "coordinates": (9.1231, 77.4153),
        "keywords": ["krishnapuram", "palace", "mural", "painting", "nayak", "museum", 
                    "gajendra moksha", "elephant"],
        "default_persona": "british_collector",
        "related_personas":  ["british_collector", "king_rama_pandya"],
        "image_hints": ["palace", "mural", "painting", "courtyard", "museum", "kerala style"],
        "gallery_images":  [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Krishnapuram_Palace. jpg/800px-Krishnapuram_Palace.jpg", "caption": "Krishnapuram Palace exterior"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Gajendra_Moksha_Mural.jpg/800px-Gajendra_Moksha_Mural.jpg", "caption": "The famous Gajendra Moksha mural"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Krishnapuram_courtyard.jpg/800px-Krishnapuram_courtyard.jpg", "caption": "The palace courtyard"},
        ],
        "historical_context": """
# KRISHNAPURAM PALACE 🏰

## Overview
A 17th-century palace built by the Madurai Nayak rulers, now housing a museum.  Famous for having the largest single mural in South India.

## Architecture
- **Style**:  Blend of Kerala and Tamil architectural traditions
- **Roof**: Typical Kerala-style sloped roof
- **Walls**: Beautiful stucco work and decorations
- **Gardens**: Surrounding landscaped gardens

## The Famous Mural
- **Subject**:  Gajendra Moksha (Liberation of the Elephant)
- **Size**:  Approximately 22 feet × 14 feet
- **Story**: Elephant Gajendra grabbed by a crocodile, saved by Lord Vishnu
- **Significance**: Largest single mural in South India
- **Preservation**: Remarkably well-preserved colors

## Museum Collections
- Bronze idols from Chola and Nayak periods
- Stone sculptures and hero stones
- Ancient coins and inscriptions
- Wooden artifacts and temple items

## Historical Significance
- Peak of Nayak artistic achievement
- Shows cultural exchanges between regions
- Important example of secular Nayak architecture
- Window into 17th century royal life
""",
    },

    "panchalankurichi":  {
        "name": "Panchalankurichi Fort & Memorial",
        "type": "Historical Site",
        "location": "Panchalankurichi, Tamil Nadu",
        "coordinates": (8.6833, 77.7167),
        "keywords": ["panchalankurichi", "fort", "kattabomman", "memorial", "freedom fighter",
                    "veerapandiya", "வீரபாண்டிய", "காட்டபொம்மன்", "palayakkarar"],
        "default_persona":  "freedom_fighter",
        "related_personas": ["freedom_fighter", "british_collector"],
        "image_hints":  ["fort", "memorial", "statue", "monument", "kattabomman", "freedom"],
        "gallery_images": [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/k/kattabomman_statue.jpg/800px-kattabomman_statue.jpg", "caption": "Statue of Veerapandiya Kattabomman"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/p/panchalankurichi_memorial.jpg/800px-panchalankurichi_memorial.jpg", "caption": "The memorial complex"},
            {"url":  "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fort_remains.jpg/800px-fort_remains.jpg", "caption": "Remains of the historic fort"},
        ],
        "historical_context": """
# PANCHALANKURICHI FORT & MEMORIAL ⚔️

## Overview
The historic seat of Veerapandiya Kattabomman (1760-1799), one of India's earliest freedom fighters who resisted British colonial rule.

## Kattabomman's Story
- **Born**: 1760 in Panchalankurichi
- **Title**: Palayakkarar (feudal chieftain)
- **Famous For**: Refusing to pay tribute to the British
- **Quote**: "I will not prostrate before you!"
- **Martyrdom**: Hanged at Kayathar, October 16, 1799

## The Resistance
- Defied British East India Company from 1790
- Fought multiple battles against colonial forces
- Allied with other Palayakkarars
- Famous confrontation with Collector Jackson
- Betrayed and captured in 1799

## The Fort
- Original fort destroyed by British after 1799
- Was a symbol of resistance and Tamil pride
- Strategic location for defense
- Center of Kattabomman's administration

## The Memorial Today
- Built to honor the great patriot
- Includes statue and museum
- Annual commemorations on death anniversary
- Symbol of Tamil Nadu's freedom struggle
- Inspired the famous 1959 Tamil film
""",
    },

    "mahabalipuram":  {
        "name": "Mahabalipuram Monuments",
        "type": "UNESCO World Heritage Site",
        "location": "Mahabalipuram, Tamil Nadu",
        "coordinates": (12.6269, 80.1927),
        "keywords": ["mahabalipuram", "mamallapuram", "pallava", "shore temple", 
                    "arjuna's penance", "five rathas", "மாமல்லபுரம்", "rock cut"],
        "default_persona": "temple_priest",
        "related_personas": ["temple_priest", "chola_king"],
        "image_hints": ["shore temple", "rock cut", "bas relief", "rathas", "sculptures", "beach"],
        "gallery_images":  [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/s/shore_temple. jpg/800px-shore_temple.jpg", "caption": "The iconic Shore Temple"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/arjunas_penance.jpg/800px-arjunas_penance.jpg", "caption": "Arjuna's Penance - world's largest bas relief"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/five_rathas.jpg/800px-five_rathas.jpg", "caption": "The Five Rathas (Pancha Rathas)"},
        ],
        "historical_context":  """
# MAHABALIPURAM (MAMALLAPURAM) 🏛️

## Overview
A UNESCO World Heritage Site featuring 7th-8th century Pallava dynasty monuments.  One of the finest examples of rock-cut architecture in India.

## Major Monuments

### Shore Temple
- Built by Narasimhavarman II (700 CE)
- One of oldest structural temples in South India
- Survived centuries of sea erosion
- Three shrines dedicated to Shiva and Vishnu

### Arjuna's Penance
- World's largest open-air rock relief
- 96 feet long × 43 feet high
- Depicts descent of the Ganges
- Hundreds of carved figures including elephants

### Five Rathas (Pancha Rathas)
- Monolithic temples carved from single rocks
- Named after Pandavas and Draupadi
- Each in different architectural style
- Never completed - unfinished carvings visible

### Krishna's Butter Ball
- Giant balanced boulder
- Defies gravity on a slope
- Natural geological formation
- Popular tourist attraction

## Historical Significance
- Major Pallava port city
- Trading hub with Southeast Asia
- Influenced architecture across Asia
- Pallava script spread to Cambodia, Indonesia
""",
    },

    # ============== WORLDWIDE LANDMARKS ==============
    "pyramids_giza": {
        "name":  "Pyramids of Giza",
        "type": "Ancient Monument",
        "location": "Giza, Egypt",
        "coordinates": (29.9792, 31.1342),
        "keywords": ["pyramids", "giza", "egypt", "pharaoh", "khufu", "cheops", 
                    "sphinx", "ancient wonder", "tomb"],
        "default_persona":  "cleopatra",
        "related_personas": ["cleopatra"],
        "image_hints": ["pyramid", "sphinx", "desert", "ancient", "egypt", "pharaoh"],
        "gallery_images": [
            {"url":  "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/1200px-Kheops-Pyramid.jpg", "caption":  "The Great Pyramid of Khufu"},
            {"url":  "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Great_Sphinx_of_Giza.jpg/800px-Great_Sphinx_of_Giza.jpg", "caption": "The Great Sphinx"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/All_Giza_Pyramids. jpg/1200px-All_Giza_Pyramids.jpg", "caption": "All three pyramids at sunset"},
        ],
        "historical_context": """
# PYRAMIDS OF GIZA 🏛️

## Overview
The only surviving wonder of the ancient world.  Built as tombs for pharaohs during Egypt's Old Kingdom period.

## The Great Pyramid (Khufu)
- **Built**: c. 2560 BCE
- **Original Height**: 481 feet (146.5 meters)
- **Base**: 756 feet on each side
- **Stones**: 2.3 million blocks, averaging 2.5 tons each
- **Construction Time**:  Approximately 20 years

## The Three Pyramids
1. **Great Pyramid of Khufu**:  Largest and oldest
2. **Pyramid of Khafre**:  Appears tallest due to elevation
3. **Pyramid of Menkaure**: Smallest of the three

## The Great Sphinx
- **Length**: 240 feet
- **Height**: 66 feet
- **Face**: Believed to be Khafre's
- **Body**: Lion representing power

## Mysteries
- Precise astronomical alignment
- Construction techniques debated
- Internal chambers and passages
- Possible undiscovered rooms
""",
    },

    "colosseum": {
        "name": "Colosseum",
        "type": "Ancient Amphitheater",
        "location": "Rome, Italy",
        "coordinates": (41.8902, 12.4922),
        "keywords": ["colosseum", "rome", "gladiator", "amphitheater", "roman", 
                    "italy", "ancient rome", "flavian"],
        "default_persona": "leonardo_da_vinci",
        "related_personas": ["leonardo_da_vinci"],
        "image_hints": ["colosseum", "roman", "amphitheater", "arches", "ancient", "arena"],
        "gallery_images":  [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Colosseo_2020.jpg/1200px-Colosseo_2020.jpg", "caption": "The Colosseum exterior"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Colosseum_Interior.jpg/800px-Colosseum_Interior.jpg", "caption": "Inside the ancient arena"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Colosseum_night. jpg/800px-Colosseum_night.jpg", "caption": "The Colosseum illuminated at night"},
        ],
        "historical_context": """
# THE COLOSSEUM 🏟️

## Overview
The largest ancient amphitheater ever built, and an iconic symbol of Imperial Rome. 

## Construction
- **Built**: 70-80 CE
- **Commissioned By**: Emperor Vespasian
- **Completed By**: Emperor Titus
- **Capacity**: 50,000-80,000 spectators

## Architecture
- **Shape**: Elliptical
- **Dimensions**: 620 × 513 feet
- **Height**: 157 feet (4 stories)
- **Materials**: Travertine limestone, concrete, tuff

## Events Held
- Gladiatorial contests
- Animal hunts (venationes)
- Executions
- Naval battles (naumachia) - arena could be flooded
- Dramas and reenactments

## Engineering Marvels
- Velarium:  Retractable awning for shade
- Hypogeum: Underground network for animals/gladiators
- 80 entrances for crowd management
- Sophisticated drainage system
""",
    },

    "taj_mahal": {
        "name": "Taj Mahal",
        "type": "Mausoleum",
        "location": "Agra, India",
        "coordinates": (27.1751, 78.0421),
        "keywords": ["taj mahal", "agra", "shah jahan", "mumtaz", "mughal", 
                    "marble", "love", "ताज महल", "india"],
        "default_persona": "emperor_ashoka",
        "related_personas": ["emperor_ashoka"],
        "image_hints": ["taj mahal", "white marble", "dome", "minarets", "reflection", "garden"],
        "gallery_images":  [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Taj_Mahal%2C_Agra%2C_India.jpg/1200px-Taj_Mahal%2C_Agra%2C_India.jpg", "caption": "The Taj Mahal at sunrise"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Taj_Mahal_Reflection.jpg/800px-Taj_Mahal_Reflection. jpg", "caption": "Perfect reflection in the pool"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Taj_interior.jpg/800px-Taj_interior.jpg", "caption":  "Interior craftsmanship"},
        ],
        "historical_context": """
# TAJ MAHAL 🕌

## Overview
A UNESCO World Heritage Site and one of the New Seven Wonders of the World.  Built by Mughal Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal.

## Construction
- **Built**: 1632-1653
- **Duration**: 21 years
- **Workers**: Over 20,000 artisans
- **Cost**: Estimated 32 million rupees (then)
- **Architect**: Ustad Ahmad Lahori

## Architecture
- **Style**: Mughal architecture (Indo-Islamic)
- **Material**: White Makrana marble
- **Height**: 240 feet including platform
- **Dome**: 115 feet high

## Decorative Elements
- Semi-precious stone inlay (pietra dura)
- Calligraphy from the Quran
- Geometric and floral patterns
- 28 types of precious stones

## The Love Story
- Mumtaz Mahal died in 1631 during childbirth
- Her 14th child
- Shah Jahan was devastated
- Promised to build most beautiful tomb
- Imprisoned by his son, viewed Taj from captivity
""",
    },

    "sanchi_stupa": {
        "name": "Sanchi Stupa",
        "type":  "Buddhist Monument",
        "location": "Sanchi, Madhya Pradesh, India",
        "coordinates": (23.4794, 77.7397),
        "keywords": ["sanchi", "stupa", "buddhist", "ashoka", "buddha", "torana",
                    "madhya pradesh", "buddhism", "relics"],
        "default_persona":  "emperor_ashoka",
        "related_personas": ["emperor_ashoka"],
        "image_hints":  ["stupa", "dome", "gateway", "torana", "buddhist", "carved"],
        "gallery_images":  [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Sanchi_Stupa.jpg/1200px-Sanchi_Stupa.jpg", "caption": "The Great Stupa at Sanchi"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/t/torana_gateway.jpg/800px-torana_gateway.jpg", "caption":  "Intricately carved Torana gateway"},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/s/sanchi_carvings.jpg/800px-sanchi_carvings.jpg", "caption": "Buddhist narrative carvings"},
        ],
        "historical_context": """
# SANCHI STUPA ☸️

## Overview
One of the oldest stone structures in India and an important Buddhist monument.  Originally commissioned by Emperor Ashoka in the 3rd century BCE.

## The Great Stupa
- **Original Construction**: 3rd century BCE by Ashoka
- **Enlarged**: 2nd century BCE
- **Diameter**: 120 feet
- **Height**: 54 feet

## The Four Gateways (Toranas)
- Added in 1st century BCE
- Elaborate Buddhist carvings
- Scenes from Buddha's life
- Jataka tales (previous lives)
- No images of Buddha - only symbols

## Buddhist Significance
- Contains relics of Buddha
- Major pilgrimage site
- Example of early Buddhist art
- Shows evolution of Buddhist architecture

## Ashoka's Connection
- Built as part of Ashoka's mission to spread Buddhism
- One of many stupas commissioned across India
- Symbol of Ashoka's transformation
- Spread of Dhamma (righteousness)
""",
    },
}


def get_landmark(landmark_key):
    """Get a landmark by its key."""
    return LANDMARKS. get(landmark_key)


def get_all_landmarks():
    """Get all available landmarks."""
    return LANDMARKS


def get_landmarks_by_region(region):
    """Get landmarks filtered by region/location."""
    return {k: v for k, v in LANDMARKS.items() if region.lower() in v.get("location", "").lower()}


def identify_landmark_from_text(text):
    """Try to identify a landmark from text description."""
    if not text:
        return None
        
    text_lower = text.lower()

    best_match = None
    best_score = 0

    for key, landmark in LANDMARKS.items():
        score = 0
        
        # Check keywords (highest weight)
        for keyword in landmark. get("keywords", []):
            if keyword.lower() in text_lower:
                score += 10
        
        # Check image hints
        for hint in landmark.get("image_hints", []):
            if hint. lower() in text_lower:
                score += 5
        
        # Check name
        if landmark["name"].lower() in text_lower:
            score += 20
        
        # Check location
        if landmark. get("location", "").lower() in text_lower:
            score += 5
        
        if score > best_score:
            best_score = score
            best_match = key

    return best_match if best_score >= 10 else None


def get_landmark_gallery(landmark_key):
    """Get gallery images for a landmark."""
    landmark = LANDMARKS.get(landmark_key)
    if landmark:
        return landmark.get("gallery_images", [])
    return []
