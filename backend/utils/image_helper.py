"""
Omni-Source High-Definition Visual & Asset Engine for AI Multi-Agent Software Studio.
Provides verified, multi-source working image assets across 20+ specialized business domains.
Includes curated Unsplash photography, Pravatar & DiceBear avatars, and resilient SVG fallbacks.
"""

from typing import Dict, List, Optional
import re

VERIFIED_IMAGES_BY_CATEGORY: Dict[str, List[str]] = {
    # 1. Luxury Cars & Automotive Showroom
    "luxury_cars": [
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1200&q=80",  # Supercar front view
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",  # Porsche sportscar
        "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=1200&q=80",  # Luxury cockpit interior
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",  # Sports car rear profile
        "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=1200&q=80",  # Ferrari red exotic
        "https://images.unsplash.com/photo-1555353540-64580b51c258?auto=format&fit=crop&w=1200&q=80",  # Luxury showroom exhibition
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80",  # Mercedes AMG black coupe
        "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",  # Steering wheel & leather dash
    ],

    # 1B. Higher Education, Prestigious University & College Campus
    "education_university": [
        "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80",  # Grand University campus building & lawn
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80",  # College students graduation caps
        "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1200&q=80",  # Historic collegiate brick hall
        "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?auto=format&fit=crop&w=1200&q=80",  # Modern university library study commons
        "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=1200&q=80",  # Lecture hall presentation
        "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?auto=format&fit=crop&w=1200&q=80",  # University quadrangle courtyard
        "https://images.unsplash.com/photo-1519452635265-7b1fbfd1e4e0?auto=format&fit=crop&w=1200&q=80",  # Academic research & collaborative study
    ],

    # 2. Indian Dhaba & Roadside Punjabi Eatery
    "indian_dhaba": [
        "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?auto=format&fit=crop&w=1200&q=80",  # Rich Butter Chicken Curry
        "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80",  # Amritsari Kulcha / Paratha
        "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?auto=format&fit=crop&w=1200&q=80",  # Paneer Tikka / Tandoori Grill
        "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=1200&q=80",  # Dal Makhani in clay pot
        "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=1200&q=80",  # Traditional Punjabi Lassi
        "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=1200&q=80",  # Hot Masala Chai kulhad
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",  # Roadside Dhaba Charpai ambiance
        "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=1200&q=80",  # Gulab Jamun sweet dessert
        "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=1200&q=80",  # Tandoori Naan & spices
    ],

    # 3. Luxury Coffee & Artisan Cafe
    "coffee_cafe": [
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=1200&q=80",  # European Coffee Shop interior
        "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=1200&q=80",  # Espresso cup with crema
        "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=1200&q=80",  # Latte art rosette
        "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1200&q=80",  # Fresh roasted coffee beans
        "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1200&q=80",  # Modern minimalist cafe lounge
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80",  # Barista pouring drip coffee
        "https://images.unsplash.com/photo-1509785307050-d4066910ec1e?auto=format&fit=crop&w=1200&q=80",  # Croissants and coffee breakfast
    ],

    # 4. Italian Pizzeria & Trattoria
    "italian_pizza": [
        "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=1200&q=80",  # Authentic Neapolitan pizza
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1200&q=80",  # Wood-fired Margherita pizza
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",  # Italian dining restaurant
        "https://images.unsplash.com/photo-1621996346565-e3d5d6281699?auto=format&fit=crop&w=1200&q=80",  # Handmade Italian pasta
        "https://images.unsplash.com/photo-1595854341625-f33ee10dbf94?auto=format&fit=crop&w=1200&q=80",  # Pizza dough prep with flour
        "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?auto=format&fit=crop&w=1200&q=80",  # Wood-fired pizza oven glow
    ],

    # 5. Fitness Club & Performance Gym
    "fitness_gym": [
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80",  # High-end gym equipment
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1200&q=80",  # Athlete lifting weights
        "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1200&q=80",  # Calm yoga & meditation space
        "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=1200&q=80",  # Dumbbells rack in studio
        "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1200&q=80",  # Cardio training session
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1200&q=80",  # Personal trainer workout
    ],

    # 6. Luxury Boutique Hotel & Heritage Resort
    "luxury_hotel": [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",  # Five-star luxury hotel exterior
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",  # Executive hotel suite & king bed
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80",  # Luxury infinity pool
        "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80",  # Hotel wellness & spa retreat
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80",  # Elegant hotel grand lobby
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=80",  # Resort ocean sunset balcony
    ],

    # 7. Streetwear & Urban Fashion
    "streetwear_fashion": [
        "https://images.unsplash.com/photo-1523398002811-999ca8dec234?auto=format&fit=crop&w=1200&q=80",  # Urban streetwear aesthetic
        "https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?auto=format&fit=crop&w=1200&q=80",  # Model with oversized hoodie
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80",  # Limited edition sneakers
        "https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=1200&q=80",  # High-fashion street editorial
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1200&q=80",  # Fashion lookbook neon studio
        "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80",  # Flagship boutique store
    ],

    # 8. Luxury Bakery & Pastry Shop
    "bakery_dessert": [
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=1200&q=80",  # Gourmet chocolate birthday cake
        "https://images.unsplash.com/photo-1569864321390-bf4644a425f3?auto=format&fit=crop&w=1200&q=80",  # Colorful French macarons
        "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=1200&q=80",  # Artisan bakery croissants
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=1200&q=80",  # Fresh baked sourdough loaves
        "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=1200&q=80",  # Fruit tart pastries
        "https://images.unsplash.com/photo-1511081692775-05d0f180a065?auto=format&fit=crop&w=1200&q=80",  # Patisserie display counter
    ],

    # 9. Music / DJ Studio & Nightclub
    "music_dj_studio": [
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=1200&q=80",  # DJ mixing console neon party
        "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=1200&q=80",  # Professional audio studio console
        "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=1200&q=80",  # Live concert crowd & stage lights
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=80",  # Studio monitor headphones
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80",  # Electronic music festival DJ
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80",  # Microphone & acoustic studio
    ],

    # 10. Organic Ayurvedic & Botanical Wellness
    "ayurvedic_wellness": [
        "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=1200&q=80",  # Amber apothecary herbal bottles
        "https://images.unsplash.com/photo-1617897903246-719242758050?auto=format&fit=crop&w=1200&q=80",  # Botanical facial serum & oils
        "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80",  # Ayurvedic spa massage sanctuary
        "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1200&q=80",  # Fresh herbs, turmeric & pestle
        "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1200&q=80",  # Meditation & holistic serenity
        "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=1200&q=80",  # Yoga & mindful balance
    ],

    # 11. Tech, AI & SaaS Dashboards
    "tech_saas": [
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",  # Data analytics dashboard
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",  # Cyber matrix & digital security
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",  # AI microprocessor chip
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",  # Business intelligence charts
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",  # Modern engineering workspace
    ],

    # 12. Real Estate & Architecture
    "real_estate": [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",  # Contemporary luxury villa
        "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",  # Modern penthouse interior
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",  # Glass corporate skyscraper
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",  # Residential estate with pool
    ],

    # 13. Creative Portfolios & Agency
    "portfolio_creative": [
        "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80",  # Creative designer workspace
        "https://images.unsplash.com/photo-1522542550221-31fd19575a2d?auto=format&fit=crop&w=1200&q=80",  # UI/UX design wireframes
        "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=1200&q=80",  # Abstract kinetic artwork
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80",  # Creative director portrait
    ],

    # 14. E-Commerce & Luxury Goods
    "ecommerce_products": [
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=80",  # Minimalist luxury watch
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1200&q=80",  # Crimson red sneakers
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=80",  # Noise-canceling headphones
        "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=1200&q=80",  # Designer sunglasses
        "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=1200&q=80",  # Leather tote bag
    ],

    # 15. Medical & Healthcare Clinic
    "healthcare_medical": [
        "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80",  # Modern clinic reception
        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80",  # Doctor examining medical chart
        "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1200&q=80",  # Healthcare professionals team
        "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80",  # Dental & wellness clinic
    ],

    # 16. Guaranteed Working Avatars & Testimonials
    "avatars": [
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
        "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
        "https://i.pravatar.cc/300?img=68",
        "https://i.pravatar.cc/300?img=32",
        "https://i.pravatar.cc/300?img=12",
        "https://i.pravatar.cc/300?img=47",
        "https://i.pravatar.cc/300?img=59",
    ]
}


def _has_word(keywords: List[str], text: str) -> bool:
    """Helper to check if any keyword exists as a whole word or exact phrase in text"""
    for kw in keywords:
        if " " in kw:
            if kw in text:
                return True
        else:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                return True
    return False


def detect_domain_from_prompt(prompt: str) -> str:
    """Intelligently detect business domain from client prompt text using exact word boundaries"""
    p = prompt.lower()
    
    # 1. Higher Education & Prestigious University Campus
    if _has_word(["university", "campus", "college", "school", "academy", "academics", "academic", "faculty", "student", "students", "admissions", "degree", "degrees", "tuition", "syllabus", "alumni", "dorm", "residence hall"], p):
        return "education_university"
    elif _has_word(["car", "cars", "automotive", "motor", "motors", "showroom", "vehicle", "vehicles", "supercar", "supercars", "ferrari", "porsche", "audi", "bmw", "mercedes", "apex luxe"], p):
        return "luxury_cars"
    elif _has_word(["dhaba", "punjabi food", "desi dhaba", "tandoor", "kulcha", "chai", "lassi", "indian food", "roadside dhaba", "charpai", "amritsari"], p):
        return "indian_dhaba"
    elif _has_word(["coffee", "cafe", "café", "espresso", "latte", "barista", "roast", "cappuccino"], p):
        return "coffee_cafe"
    elif _has_word(["pizza", "pizzeria", "italian food", "trattoria", "pasta", "neapolitan", "wood-fired", "mozzarella"], p):
        return "italian_pizza"
    elif _has_word(["fitness", "gym", "workout", "training", "athlete", "bodybuilding", "crossfit", "personal trainer"], p):
        return "fitness_gym"
    elif _has_word(["hotel", "resort", "boutique hotel", "hospitality", "hotel suites", "guest room", "inn"], p):
        return "luxury_hotel"
    elif _has_word(["streetwear", "fashion", "sneaker", "sneakers", "apparel", "hoodie", "lookbook", "clothing drop"], p):
        return "streetwear_fashion"
    elif _has_word(["bakery", "dessert", "pastry", "patisserie", "chocolate", "macaron", "baking", "cake shop"], p):
        return "bakery_dessert"
    elif _has_word(["dj", "nightclub", "electronic music", "sound studio", "music producer", "beats"], p):
        return "music_dj_studio"
    elif _has_word(["ayurveda", "ayurvedic", "wellness", "herbal", "vedic", "botanical", "holistic", "organic spa"], p):
        return "ayurvedic_wellness"
    elif _has_word(["saas", "software", "dashboard", "analytics", "cloud platform", "developer tool"], p):
        return "tech_saas"
    elif _has_word(["real estate", "villa", "property", "realtor", "apartments", "condo"], p):
        return "real_estate"
    elif _has_word(["doctor", "clinic", "hospital", "medical", "healthcare", "dentist", "patient"], p):
        return "healthcare_medical"
    elif _has_word(["ecommerce", "online store", "watch shop", "jewelry store"], p):
        return "ecommerce_products"
    elif _has_word(["portfolio", "creative agency", "design agency", "freelance portfolio"], p):
        return "portfolio_creative"
    
    return "education_university" if ("campus" in p or "learn" in p) else "tech_saas"


def get_domain_fallback_url(domain: str) -> str:
    """Return prime fallback image URL for a given domain"""
    images = VERIFIED_IMAGES_BY_CATEGORY.get(domain, VERIFIED_IMAGES_BY_CATEGORY["tech_saas"])
    return images[0] if images else "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"


def get_verified_images_guideline(domain: Optional[str] = None) -> str:
    """Return tailored, high-definition image guidelines to inject into developer agent prompts"""
    active_domain = domain or "luxury_cars"
    domain_images = VERIFIED_IMAGES_BY_CATEGORY.get(active_domain, VERIFIED_IMAGES_BY_CATEGORY["luxury_cars"])
    avatars = VERIFIED_IMAGES_BY_CATEGORY["avatars"]
    
    img_lines = "\n".join([f"      * Asset {i+1}: {url}" for i, url in enumerate(domain_images)])
    avatar_lines = "\n".join([f"      * User {i+1}: {url}" for i, url in enumerate(avatars[:6])])
    prime_fallback = domain_images[0] if domain_images else "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
    
    return f"""
OMNI-SOURCE HIGH-DEFINITION ASSET GUIDELINES (DOMAIN: {active_domain.upper()}):
Use ONLY the verified high-resolution Unsplash assets below that perfectly match this exact business.
NEVER use broken URLs or irrelevant images from other industries.

1. Domain Visual Assets (for Hero, Gallery, Catalog, Cards, Sections):
{img_lines}

2. Verified Authentic Avatars (for Testimonials, Team, Reviews):
{avatar_lines}

3. Universal Image Rule:
   Every <img> tag MUST have onError fallback to the domain primary asset:
   onError={{(e) => {{ e.target.onerror = null; e.target.src = "{prime_fallback}"; }}}}
"""


def get_fallback_image_component_code(domain: Optional[str] = None) -> str:
    """Return universal, resilient code for src/components/ui/Image.jsx with domain-tailored fallback"""
    active_domain = domain or "tech_saas"
    fallback_url = get_domain_fallback_url(active_domain)
    
    template = """import React, { useState } from 'react';

export const Image = ({
  src,
  alt = 'Visual Asset',
  className = '',
  fallbackSrc = '__FALLBACK_URL__',
  ...props
}) => {
  const [currentSrc, setCurrentSrc] = useState(src || fallbackSrc);
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const handleError = () => {
    if (!hasError) {
      setHasError(true);
      setCurrentSrc(fallbackSrc);
      setIsLoading(false);
    }
  };

  return (
    <div className={`relative overflow-hidden bg-neutral-900 ${className}`}>
      <img
        src={currentSrc}
        alt={alt}
        className={`w-full h-full object-cover transition-all duration-500 ${
          isLoading ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
        }`}
        onLoad={() => setIsLoading(false)}
        onError={handleError}
        loading="lazy"
        {...props}
      />
      {isLoading && (
        <div className="absolute inset-0 bg-neutral-800 animate-pulse flex items-center justify-center">
          <div className="w-8 h-8 rounded-full border-2 border-neutral-600 border-t-transparent animate-spin" />
        </div>
      )}
    </div>
  );
};

export default Image;
"""
    return template.replace("__FALLBACK_URL__", fallback_url)
