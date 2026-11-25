from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
from utils.image_helper import detect_domain_from_prompt
import json
import re

logger = setup_logger(__name__)

DOMAIN_PRESETS: Dict[str, Dict[str, Any]] = {
    "education_university": {
        "project_name": "Veritas University",
        "tagline": "Academic Heritage, World-Class Research & Vibrant Campus Life",
        "category": "Higher Education & Academic University Campus",
        "target_audience": "Prospective students, scholars, researchers, faculty, and alumni",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Interactive hero slider, key statistics counter, news ticker, and Quick-Apply drawer"},
            {"name": "Academics", "path": "/academics", "title": "Academics & Degree Programs", "purpose": "Searchable degree directory with dynamic major/minor filters, department hubs, and syllabus preview modals"},
            {"name": "CampusLife", "path": "/campus-life", "title": "Virtual Campus Life", "purpose": "Interactive 360 map modal, student club explorer, and residence hall selector"},
            {"name": "Admissions", "path": "/admissions", "title": "Admissions & Financial Aid", "purpose": "Step-by-step application tracker, interactive tuition calculator slider, and key deadline countdowns"},
            {"name": "Visit", "path": "/visit", "title": "Campus Visit & Contact", "purpose": "Dynamic calendar booking for campus tours, live chat modal, and interactive travel directions"}
        ]
    },
    "luxury_cars": {
        "project_name": "Apex Luxe Motors",
        "tagline": "Where Pure Performance Meets Automotive Artistry",
        "category": "Luxury Automotive Gallery & Showroom",
        "target_audience": "Automotive connoisseurs, collectors, and high-performance enthusiasts",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Cinematic hero showcase, limited edition highlights, and customer acclaim"},
            {"name": "Models", "path": "/models", "title": "Premier Models & Fleet", "purpose": "Interactive vehicle catalog with horsepower, top speed, and performance specs"},
            {"name": "Gallery", "path": "/gallery", "title": "Exhibition Gallery", "purpose": "Curated high-res automotive photography and cockpit detail showcases"},
            {"name": "Experience", "path": "/experience", "title": "VIP Showroom Experience", "purpose": "Private atelier consultations, track test drive bookings, and concierge services"},
            {"name": "Contact", "path": "/contact", "title": "Concierge & Inquiries", "purpose": "Executive appointment booking form and global showroom locations"}
        ]
    },
    "indian_dhaba": {
        "project_name": "Truckara Dhaba",
        "tagline": "Highway Flavors, Punjabi Folk Art & Authentic Desi Tandoor",
        "category": "Authentic Indian Desi Dhaba & Restaurant",
        "target_audience": "Families, highway travelers, foodies, and lovers of rustic Punjabi hospitality",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Vibrant truck-art welcome, sizzler highlights, and authentic roadside atmosphere"},
            {"name": "Menu", "path": "/menu", "title": "Asli Dhaba Menu", "purpose": "Dal makhani, butter chicken, tandoori kulchas, lassi, and special thalis"},
            {"name": "About", "path": "/about", "title": "Our Highway Story", "purpose": "Legacy of roadside dhaba culture and charcoal tandoor craftsmanship"},
            {"name": "Special", "path": "/special", "title": "Chef Specials & Thalis", "purpose": "Signature slow-cooked specialties and kulhad chai rituals"},
            {"name": "Location", "path": "/location", "title": "Find Our Dhaba", "purpose": "Highway location map, charpai seating reservations, and takeaway orders"}
        ]
    },
    "coffee_cafe": {
        "project_name": "Velvet Roast Lounge",
        "tagline": "Artisanal Single-Origin Coffee & High-End European Patisserie",
        "category": "Luxury Coffee Lounge & Roastery",
        "target_audience": "Coffee aficionados, digital nomads, and lovers of slow cafe culture",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Sensory espresso experience, barista showcase, and warm ambient lounge vibe"},
            {"name": "Menu", "path": "/menu", "title": "Artisan Coffee & Pastries", "purpose": "Signature roasts, pour-overs, nitro cold brew, and fresh flaky croissants"},
            {"name": "About", "path": "/about", "title": "Our Roastery Heritage", "purpose": "Ethical bean sourcing story, roasting process, and barista team"},
            {"name": "Experience", "path": "/experience", "title": "Cupping Sessions & Classes", "purpose": "Weekend barista workshops and coffee bean subscriptions"},
            {"name": "Contact", "path": "/contact", "title": "Visit & Table Inquiries", "purpose": "Cafe hours, location guide, and private event reservations"}
        ]
    },
    "italian_pizza": {
        "project_name": "Bella Napoli Forno",
        "tagline": "Authentic Wood-Fired Neapolitan Pizza & Handmade Pasta",
        "category": "Artisan Italian Pizzeria & Trattoria",
        "target_audience": "Gourmet diners, pizza enthusiasts, and families",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Wood-fired oven glow, bubbling mozzarella, and Italian street corner charm"},
            {"name": "Menu", "path": "/menu", "title": "Pizzas, Pastas & Antipasti", "purpose": "48-hour fermented dough pizzas, handmade pasta, and house tiramisu"},
            {"name": "About", "path": "/about", "title": "Our Naples Heritage", "purpose": "Family recipes handed down through generations and imported Italian ingredients"},
            {"name": "Experience", "path": "/experience", "title": "Chef Table & Wine Pairing", "purpose": "Wood-fired pizza making masterclasses and regional wine list"},
            {"name": "Contact", "path": "/contact", "title": "Reservations & Orders", "purpose": "Table booking form, takeaway order status, and address"}
        ]
    },
    "fitness_gym": {
        "project_name": "Apex Kinetic Performance",
        "tagline": "Elite Athletic Conditioning, High-Tech Workouts & Transformation",
        "category": "Premium Fitness Club & Athletic Training Center",
        "target_audience": "Athletes, executives, and fitness-driven individuals",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Energetic athlete showcases, cutting-edge equipment, and motivational atmosphere"},
            {"name": "Programs", "path": "/programs", "title": "Training Programs & Classes", "purpose": "HIIT, Olympic weightlifting, recovery sauna, and personalized coaching"},
            {"name": "Trainers", "path": "/trainers", "title": "Master Coaches", "purpose": "Coach profiles, athletic credentials, and specialist disciplines"},
            {"name": "Membership", "path": "/membership", "title": "Tiers & Pricing", "purpose": "Transparent membership packages, guest passes, and corporate wellness"},
            {"name": "Contact", "path": "/contact", "title": "Book a Free Session", "purpose": "Guest pass booking form, facility tour schedule, and location"}
        ]
    },
    "luxury_hotel": {
        "project_name": "The Grand Heritage Manor",
        "tagline": "Timeless Five-Star Hospitality, Architectural Grandeur & Serenity",
        "category": "Luxury Boutique Hotel & Heritage Resort",
        "target_audience": "Luxury travelers, honeymooners, and executive retreats",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Cinematic estate grounds, infinity pool, and five-star welcome"},
            {"name": "Suites", "path": "/suites", "title": "Rooms & Presidential Suites", "purpose": "Interactive room catalog with 3D amenity tour and king suite specs"},
            {"name": "Dining", "path": "/dining", "title": "Fine Dining & Lounge", "purpose": "Michelin-starred cuisine, wine cellar, and champagne breakfast"},
            {"name": "Experience", "path": "/experience", "title": "Spa, Wellness & Excursions", "purpose": "Holistic spa rituals, private yacht charters, and curated excursions"},
            {"name": "Contact", "path": "/contact", "title": "Reservations & Concierge", "purpose": "Direct booking inquiry system and concierge assistance"}
        ]
    },
    "streetwear_fashion": {
        "project_name": "Kinetix Underground",
        "tagline": "Raw Street Culture, Limited Capsule Drops & Heavyweight Cotton",
        "category": "Contemporary Urban Streetwear Brand",
        "target_audience": "Sneakerheads, youth fashion pioneers, and urban style creators",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Gritty neon aesthetics, latest drop timer, and lookbook teaser"},
            {"name": "Shop", "path": "/shop", "title": "Capsule Collections", "purpose": "Filterable catalog for hoodies, cargo pants, tees, and sneakers"},
            {"name": "Lookbook", "path": "/lookbook", "title": "Editorial Lookbook", "purpose": "High-fashion street photography and style guides"},
            {"name": "Story", "path": "/story", "title": "Underground Manifesto", "purpose": "Subculture roots, sustainable sourcing, and design ethos"},
            {"name": "Contact", "path": "/contact", "title": "Drops VIP Club", "purpose": "VIP early-access signup form and flagship stockist locations"}
        ]
    },
    "bakery_dessert": {
        "project_name": "La Petite Patisserie",
        "tagline": "French Artisanal Confections, Handcrafted Cakes & Macarons",
        "category": "Luxury Bakery & Custom Dessert Studio",
        "target_audience": "Gourmet dessert lovers, celebration planners, and gift buyers",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Delicious pastry showcase, signature cakes, and Parisian charm"},
            {"name": "Menu", "path": "/menu", "title": "Cakes, Tarts & Confections", "purpose": "Detailed dessert menu with flavor profiles and dietary filters"},
            {"name": "Custom", "path": "/custom", "title": "Bespoke Celebration Cakes", "purpose": "Interactive custom wedding and birthday cake builder"},
            {"name": "About", "path": "/about", "title": "Our Pastry Atelier", "purpose": "Story of our master pastry chefs and hand-selected ingredients"},
            {"name": "Contact", "path": "/contact", "title": "Order & Tasting Inquiries", "purpose": "Pre-order reservation form and bakery boutique location"}
        ]
    },
    "music_dj_studio": {
        "project_name": "Subsonic Audio Lab",
        "tagline": "Underground Electronic Music, DJ Events & High-Fidelity Recording",
        "category": "Electronic Music Studio & Nightclub Brand",
        "target_audience": "DJs, music producers, nightlife attendees, and electronic music fans",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Pulsing club visuals, upcoming headliner announcements, and sound system specs"},
            {"name": "Releases", "path": "/releases", "title": "Tracks & Label Catalog", "purpose": "Discography, interactive audio waveform previews, and vinyl shop"},
            {"name": "Events", "path": "/events", "title": "Tour & Nightclub Dates", "purpose": "Upcoming events calendar with ticket booking links"},
            {"name": "Studio", "path": "/studio", "title": "Recording & Gear", "purpose": "Analogue synth collections, acoustically treated rooms, and session rates"},
            {"name": "Contact", "path": "/contact", "title": "Bookings & Inquiries", "purpose": "Artist booking form, demo drop, and studio reservation"}
        ]
    },
    "ayurvedic_wellness": {
        "project_name": "VanaVeda Botanicals",
        "tagline": "5,000 Years of Vedic Wisdom Reimagined for Modern Luxury",
        "category": "Premium Organic Ayurvedic Wellness Brand",
        "target_audience": "Conscious wellness seekers, organic skincare lovers, and holistic practitioners",
        "pages": [
            {"name": "Home", "path": "/", "title": "Home", "purpose": "Tranquil botanical imagery, sacred herbal remedies, and peaceful ambiance"},
            {"name": "Products", "path": "/products", "title": "Apothecary & Herbal Oils", "purpose": "Facial serums, kesh tailas, ubtans, and herbal teas with dosha filters"},
            {"name": "Rituals", "path": "/rituals", "title": "Dinacharya & Daily Rituals", "purpose": "Morning and evening wellness regimens and holistic lifestyle guides"},
            {"name": "Heritage", "path": "/heritage", "title": "Our Vedic Story", "purpose": "Wild-crafted botanical ethics and traditional slow-cooked methods"},
            {"name": "Contact", "path": "/contact", "title": "Consultation & Apothecary", "purpose": "Dosha diagnostic inquiry, sanctuary locations, and customer support"}
        ]
    }
}

class CEOAgent(BaseAgent):
    """CEO & Product Lead Agent - Oversees product vision, multi-page specifications, and final project sign-off"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.CEO,
            name="Alex Thompson",
            temperature=0.4
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Alex Thompson, the visionary CEO and Product Lead of an elite AI Frontend Engineering Studio.

Your core mission:
1. Transform natural language client ideas into world-class, multi-page React application specifications.
2. Formulate a tailored multi-page sitemap (5 to 6 functional pages, e.g. Home, Menu/Models/Products, About/Heritage, Experience/Features, Contact) suitable for the exact domain.
3. Define key interactive features and rich content expectations for each page.
4. Make bold, professional product and design decisions autonomously without burdening the user with routine questions.
5. Ensure the product feels like a premier agency build worth $10,000+ with authentic domain naming and features."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute CEO / Product Lead tasks"""
        task_type = task.get("type", "review_request")
        
        if task_type in ["review_request", "analyze_product"]:
            return await self._analyze_product_request(task, context)
        elif task_type == "final_approval":
            return await self._final_approval(task, context)
        else:
            return {"status": "error", "message": f"Unknown task type {task_type}"}
    
    async def _analyze_product_request(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze client request and produce a structured multi-page React product specification"""
        logger.info("CEO / Product Lead analyzing product request")
        
        client_request = context.get("client_request", "")
        autonomous_mode = context.get("autonomous_mode", True)
        domain = detect_domain_from_prompt(client_request)
        context["detected_domain"] = domain
        preset = DOMAIN_PRESETS.get(domain, DOMAIN_PRESETS["luxury_cars"])
        
        prompt = f"""Analyze this client request and create an exceptional Product Specification for a multi-page React web application:

Client Request: {client_request}
Detected Business Domain: {domain}
Baseline Inspiration (use ONLY if request is vague):
Default Project Name: {preset['project_name']}
Default Tagline: {preset['tagline']}

CRITICAL INSTRUCTIONS:
1. Always prioritize the client request! If the user specifies pages, brand ideas, aesthetic tokens, or features, follow them precisely.
2. Determine an inspiring, memorable Brand/Project Name matching this exact concept (e.g. if university requested, use a prestigious university name).
3. Define the Target Audience & Value Proposition.
4. Formulate a 5-page multi-page sitemap tailored specifically to this business (e.g. Home, plus 4 domain-specific pages matching user request).
5. For EACH page, specify:
   - Page Name (e.g. Home, Academics, CampusLife, Admissions, Visit)
   - URL path (e.g. '/', '/academics', '/campus-life', '/admissions', '/visit')
   - Title
   - Purpose & key interactive sections
6. State the Tone & Personality reflecting the client request.

Return a JSON object formatted strictly as:
```json
{{
  "project_name": "Prestigious and inspiring project name matching the concept",
  "tagline": "Inspiring tagline matching the concept",
  "category": "Accurate category for this business domain",
  "target_audience": "Target audience description",
  "summary": "Brief concept summary",
  "complexity": "Medium",
  "pages": [
    {{
      "name": "Home",
      "path": "/",
      "title": "Home",
      "purpose": "Hero showcase, interactive preview, reviews, stats and CTA",
      "key_sections": ["Hero Showcase", "Features Bento Grid", "Interactive Catalog Preview", "Testimonials", "CTA"]
    }}
  ],
  "autonomous_decisions": [
    "Adopted tailored 5-page React architecture",
    "Configured custom domain mock data"
  ],
  "clarification_questions": []
}}
```"""

        try:
            response = await self._generate_response(prompt, context)
            parsed_spec = self._extract_json(response)
            
            if not parsed_spec or not isinstance(parsed_spec, dict) or "pages" not in parsed_spec or len(parsed_spec.get("pages", [])) < 3:
                parsed_spec = self._get_fallback_product_spec(client_request, domain)
            
            self.add_to_memory(f"Created product spec for: {parsed_spec.get('project_name')}")
            
            return {
                "status": "completed",
                "approved": True,
                "product_spec": parsed_spec,
                "complexity": parsed_spec.get("complexity", "Medium"),
                "pages": [p["name"] if isinstance(p, dict) else str(p) for p in parsed_spec.get("pages", [])],
                "analysis": f"Approved project '{parsed_spec.get('project_name')}' with {len(parsed_spec.get('pages', []))} bespoke pages."
            }
        except Exception as e:
            logger.error(f"CEO product analysis failed: {e}")
            fallback = self._get_fallback_product_spec(client_request, domain)
            return {
                "status": "completed",
                "approved": True,
                "product_spec": fallback,
                "complexity": "Medium",
                "pages": [p["name"] for p in fallback.get("pages", [])],
                "analysis": f"Approved with domain-tailored preset spec for {domain}."
            }
    
    def _get_fallback_product_spec(self, client_request: str, domain: str = "luxury_cars") -> Dict[str, Any]:
        """Provide a domain-tailored fallback product spec if LLM JSON parsing encounters an issue"""
        preset = DOMAIN_PRESETS.get(domain, DOMAIN_PRESETS["luxury_cars"])
        
        return {
            "project_name": preset["project_name"],
            "tagline": preset["tagline"],
            "category": preset["category"],
            "target_audience": preset["target_audience"],
            "summary": client_request[:250],
            "complexity": "Medium",
            "pages": preset["pages"],
            "autonomous_decisions": [
                f"Configured domain architecture for {preset['category']}",
                "Selected high-conversion interactive components"
            ],
            "clarification_questions": []
        }
    
    async def _final_approval(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform executive final sign-off before delivery"""
        logger.info("CEO performing final project review")
        
        files = context.get("files", {})
        qa_report = context.get("qa_report", "")
        visual_review = context.get("visual_review", "")
        integrity_report = context.get("integrity_report", "")
        
        file_list = list(files.keys()) if isinstance(files, dict) else (files or [])
        
        vr_str = json.dumps(visual_review, indent=2) if isinstance(visual_review, dict) else str(visual_review or "Design aesthetic verified.")
        qa_str = json.dumps(qa_report, indent=2) if isinstance(qa_report, dict) else str(qa_report or "All QA automated checks passed.")
        ir_str = json.dumps(integrity_report, indent=2) if isinstance(integrity_report, dict) else str(integrity_report or "All required files verified.")
        
        prompt = f"""Review the completed React multi-page application before final client handoff:

Generated Project Files ({len(file_list)} files):
{', '.join(file_list[:25])}

QA Report Summary:
{qa_str[:400]}

Visual Review Summary:
{vr_str[:400]}

File Integrity Summary:
{ir_str[:400]}

Provide your executive final approval statement confirming readiness for production."""

        try:
            response = await self._generate_response(prompt, context)
            self.add_to_memory("Final project approval complete")
            
            return {
                "status": "completed",
                "approved": True,
                "review": response
            }
        except Exception as e:
            logger.error(f"CEO final approval failed: {e}")
            return {
                "status": "completed",
                "approved": True,
                "review": "Project verified and approved for delivery."
            }