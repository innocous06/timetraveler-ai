"""
Landmark database for TimeTraveler AI.
Contains information about Tirunelveli landmarks for the AI to reference.
"""

LANDMARKS = {
    "nellaiappar_temple": {
        "name": "Nellaiappar Temple",
        "type": "Hindu Temple",
        "location": "Tirunelveli, Tamil Nadu",
        "keywords": ["nellaiappar", "temple", "gopuram", "tower", "shiva", "musical pillars", "திருநெல்வேலி"],
        "default_persona": "temple_priest",
        "image_hints": ["gopuram", "tower", "temple", "pillars", "carved", "hindu", "dravidian"],
        "historical_context": """
NELLAIAPPAR TEMPLE - Key Facts: 

Architecture:
- Ancient Dravidian style temple dedicated to Lord Shiva
- The main Gopuram (tower) rises to about 150 feet
- Famous for its 48 MUSICAL PILLARS carved from single granite stones
- Each pillar produces a different musical note when struck
- The Mani Mandapam (hall) contains these musical pillars

History:
- Original temple is over 1000 years old
- Major renovations by Pandya kings (7th-14th century)
- Further expanded by Nayak rulers (16th-17th century)
- The musical pillars were added during Nayak period

Religious Significance:
- Main deity:  Nellaiappar (form of Shiva)
- Consort deity: Kanthimathi Amman (Parvati)
- Has a sacred tank called Thamarai Kulam (Lotus Tank)
- Major festival: Arudra Darshan, Thai Poosam

Unique Features:
- The musical pillars are an engineering marvel
- Chain carved from single stone hangs in the temple
- Thousand-pillar mandapam with intricate carvings
""",
    },

    "krishnapuram_palace": {
        "name": "Krishnapuram Palace",
        "type": "Palace/Museum",
        "location": "Krishnapuram, near Tirunelveli",
        "keywords": ["krishnapuram", "palace", "mural", "painting", "nayak", "museum", "gajendra"],
        "default_persona": "british_collector",
        "image_hints": ["palace", "mural", "painting", "courtyard", "museum"],
        "historical_context": """
KRISHNAPURAM PALACE - Key Facts:

Architecture:
- Built in the 17th century by Madurai Nayak rulers
- Blend of Kerala and Tamil architectural styles
- Has a typical Kerala-style sloped roof
- Beautiful stucco work on walls and ceilings

The Famous Mural:
- Houses the LARGEST SINGLE MURAL in South India
- The mural depicts "Gajendra Moksha" (Liberation of the Elephant)
- Story:  Elephant Gajendra grabbed by crocodile, saved by Lord Vishnu
- Mural is approximately 22 feet x 14 feet
- Shows incredible artistic detail and color preservation

Current Status:
- Now functions as a museum
- Houses bronze idols, stone sculptures, old coins
- Maintained by Archaeological Survey of India
- Has beautiful gardens surrounding it

Historical Significance:
- Represents the peak of Nayak artistic achievement
- Shows influence of various South Indian styles
- Important example of secular Nayak architecture
""",
    },

    "panchalankurichi":  {
        "name": "Panchalankurichi Fort & Memorial",
        "type": "Historical Site/Memorial",
        "location": "Panchalankurichi, Tirunelveli District",
        "keywords": ["panchalankurichi", "fort", "kattabomman", "memorial", "freedom", "veerapandiya"],
        "default_persona": "freedom_fighter",
        "image_hints": ["fort", "memorial", "statue", "monument", "kattabomman"],
        "historical_context": """
PANCHALANKURICHI - Key Facts:

Historical Background:
- Was the seat of Veerapandiya Kattabomman (1760-1799)
- Kattabomman was a Palayakkarar (feudal lord/chieftain)
- He famously refused to pay tribute to British East India Company
- Fought against British colonial rule

The Resistance:
- Kattabomman's defiance began around 1790
- He refused to accept British supremacy
- Famous confrontation with British Collector Jackson
- His words "I will not bow to you" became legendary

The Fall:
- Betrayed and captured in 1799
- Hanged at Kayathar on October 16, 1799
- Original fort was destroyed by British after his death
- He became a symbol of Tamil resistance

Current Memorial:
- Memorial built at Panchalankurichi in his honor
- Includes his statue and museum
- Commemorates his sacrifice for freedom
- Annual celebrations on his death anniversary

Legacy:
- Considered one of India's earliest freedom fighters
- Inspired later independence movements
- Tamil movie "Veerapandiya Kattabomman" (1959) made him famous
""",
    },

    "tamiraparani_river": {
        "name": "Tamiraparani River",
        "type": "Natural/Sacred Site",
        "location": "Tirunelveli District",
        "keywords": ["tamiraparani", "river", "water", "ghats", "porunai", "sacred"],
        "default_persona": "king_rama_pandya",
        "image_hints": ["river", "water", "ghats", "banks", "flowing"],
        "historical_context": """
TAMIRAPARANI RIVER - Key Facts:

Geography:
- The ONLY perennial river in Tamil Nadu
- Originates from Pothigai hills in Western Ghats
- Flows for about 128 kilometers
- Empties into Gulf of Mannar near Punnakayal

Name Origin:
- "Tamira" means copper in Sanskrit
- Named for the reddish/copper color of its banks
- Ancient Tamil name:  "Porunai"
- Mentioned extensively in Sangam literature

Historical Significance:
- Supported the ancient Pandyan civilization
- Banks have many ancient temples
- Enabled rice cultivation in the region
- Critical for Tirunelveli's prosperity

Sacred Importance:
- Considered a sacred river by Hindus
- Many temples located along its banks
- Bathing ghats used for religious rituals
- Mentioned in ancient Tamil texts as divine

Cultural References:
- Sangam poets praised its beauty
- Called "Dakshina Ganga" (Ganges of the South)
- Integral to Tirunelveli's identity
""",
    }
}


def get_landmark(landmark_key):
    """Get a landmark by its key."""
    return LANDMARKS.get(landmark_key)


def get_all_landmarks():
    """Get all available landmarks."""
    return LANDMARKS


def identify_landmark_from_text(text):
    """Try to identify a landmark from text description."""
    text_lower = text.lower()

    for key, landmark in LANDMARKS.items():
        # Check keywords
        for keyword in landmark["keywords"]: 
            if keyword. lower() in text_lower:
                return key

        # Check image hints
        for hint in landmark["image_hints"]:
            if hint. lower() in text_lower:
                return key

    return None
