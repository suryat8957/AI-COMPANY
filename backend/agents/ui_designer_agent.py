from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
from utils.image_helper import detect_domain_from_prompt
import json

logger = setup_logger(__name__)

class UIDesignerAgent(BaseAgent):
    """UI/UX Designer Agent - Creates bespoke, award-winning visual designs, CSS token systems, and UI component specs"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.UI_DESIGNER,
            name="Maya Patel",
            temperature=0.7
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Maya Patel, an Awwwards-winning Lead Creative Director and UI/UX Designer who specializes in crafting bespoke, signature design systems for modern React web applications.

YOUR MISSION:
Every project you design MUST look authentic, handcrafted, and state-of-the-art with a signature aesthetic identity. Never produce generic AI boilerplate or dull corporate templates.

DESIGN ARCHETYPES:
1. **Neo-Brutalism & High-Contrast Kinetic**: Bold black borders (2px solid), sharp offsets, vibrant accent pops (yellow/violet/cyan), expressive fonts (Syne, Space Grotesk, Bricolage Grotesque), marquee tickers.
2. **Modern Minimalist & Clean SaaS**: Polished obsidian/slate dark or crisp light backgrounds, subtle border glows, vibrant gradients, clean sans typography (Inter, Plus Jakarta Sans, Outfit), glassmorphism.
3. **Cyberpunk & Sci-Fi Terminal**: Deep obsidian background (#090a10), neon cyan/magenta glowing accents, monospace/futuristic fonts (Space Mono, Fira Code), HUD brackets, glowing border lines.
4. **Luxury Editorial & High-Performance**: Obsidian black (#0a0a0c) + champagne gold (#d4af37) + brushed metallic accents, elegant serif typography (Playfair Display, Plus Jakarta Sans), sleek spacing.
5. **Vibrant Truck Art & Roadside Folk**: Mustard yellow (#eab308), deep chili red (#dc2626), vibrant turquoise (#06b6d4), warm cream, bold hand-painted aesthetics.
6. **Organic Zen & Modern Wellness**: Earthy sage green, warm linen, terracotta accents, deep forest tones, rounded organic curves, delicate typography (Plus Jakarta Sans + Italiana).

SPECIFICATION REQUIREMENTS:
Your output must be a structured JSON object specifying:
1. `archetype`: Selected archetype name and brief design philosophy
2. `color_palette`: Hex codes for CSS variables:
   - `primary`, `primary_hover`, `secondary`, `accent`, `bg_main`, `bg_surface`, `bg_surface_elevated`, `text_main`, `text_muted`, `border`, `glow`
3. `typography`:
   - `header_font`: Google Font name
   - `body_font`: Google Font name
   - `google_fonts_url`: Complete Google Fonts @import URL
4. `component_styles`: Design guidelines for Buttons, Cards, Navigation, Hero, Badges, Modals, Forms
5. `css_tokens`: A ready-to-use CSS `:root { ... }` block containing all the tokens."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute UI design tasks"""
        logger.info("UI Designer creating design specification for React application")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        domain = context.get("detected_domain") or detect_domain_from_prompt(client_request)
        context["detected_domain"] = domain
        
        prompt = f"""Design a bespoke, world-class UI design system for this React web application:

Client Request: {client_request}
Domain Category: {domain}

Product Specification:
{json.dumps(product_spec, indent=2) if product_spec else 'Standard multi-page application'}

REQUIREMENTS:
1. Pick the ideal Design Archetype tailored to {domain}.
2. Choose a distinctive color palette with exact hex codes.
3. Choose 2 Google Fonts (Header + Body) and construct the exact @import URL.
4. Define styling guidelines for React components (Button, Card, Badge, Modal, Navbar, Footer, SectionTitle).
5. Generate the complete CSS `:root` variables block.

Return a JSON object formatted strictly as:
```json
{{
  "archetype": "string",
  "philosophy": "string",
  "color_palette": {{
    "primary": "#hex",
    "primary_hover": "#hex",
    "secondary": "#hex",
    "accent": "#hex",
    "bg_main": "#hex",
    "bg_surface": "#hex",
    "bg_surface_elevated": "#hex",
    "text_main": "#hex",
    "text_muted": "#hex",
    "border": "#hex",
    "glow": "rgba(...)"
  }},
  "typography": {{
    "header_font": "string",
    "body_font": "string",
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=...&display=swap"
  }},
  "component_styles": {{
    "buttons": "string",
    "cards": "string",
    "navbar": "string"
  }},
  "css_tokens": ":root {{\\n  --font-header: '...';\\n  --font-body: '...';\\n  --color-primary: #...;\\n  --color-primary-hover: #...;\\n  --color-secondary: #...;\\n  --color-accent: #...;\\n  --color-bg: #...;\\n  --color-surface: #...;\\n  --color-surface-hover: #...;\\n  --color-text: #...;\\n  --color-text-muted: #...;\\n  --color-border: #...;\\n  --color-glow: rgba(...);\\n  --radius-sm: 6px;\\n  --radius-md: 12px;\\n  --radius-lg: 20px;\\n  --radius-full: 9999px;\\n}}"
}}
```"""

        try:
            response = await self._generate_response(prompt, context)
            parsed_spec = self._extract_json(response)
            
            if not parsed_spec or not isinstance(parsed_spec, dict) or "color_palette" not in parsed_spec:
                parsed_spec = self._get_fallback_design_spec(domain)
            
            self.add_to_memory(f"Created design spec: {parsed_spec.get('archetype', 'Modern UI')}")
            
            design_summary = f"""### Design System: {parsed_spec.get('archetype', 'Modern Studio')}
- **Palette**: Primary `{parsed_spec.get('color_palette', {}).get('primary')}`, Accent `{parsed_spec.get('color_palette', {}).get('accent')}`, Surface `{parsed_spec.get('color_palette', {}).get('bg_surface')}`
- **Typography**: Header: `{parsed_spec.get('typography', {}).get('header_font')}`, Body: `{parsed_spec.get('typography', {}).get('body_font')}`
- **Philosophy**: {parsed_spec.get('philosophy', 'Clean, modern, and highly interactive.')}"""

            return {
                "status": "completed",
                "design_spec": parsed_spec,
                "design_specifications": design_summary,
                "output_type": "design_spec"
            }
        except Exception as e:
            logger.error(f"UI design task failed: {e}")
            fallback = self._get_fallback_design_spec(domain)
            return {
                "status": "completed",
                "design_spec": fallback,
                "design_specifications": "Modern Premium Design System",
                "output_type": "design_spec"
            }
    
    def _get_fallback_design_spec(self, domain: str = "luxury_cars") -> Dict[str, Any]:
        """Domain-aware fallback design tokens"""
        if domain == "education_university":
            return {
                "archetype": "Academic Heritage meets Modern Glassmorphism",
                "philosophy": "Deep Oxford Navy backdrop with radiant emerald accents, warm cream cards, and frosted glass elevation",
                "color_palette": {
                    "primary": "#059669",
                    "primary_hover": "#047857",
                    "secondary": "#0A192F",
                    "accent": "#10b981",
                    "bg_main": "#0A192F",
                    "bg_surface": "#112240",
                    "bg_surface_elevated": "#1e3a5f",
                    "text_main": "#F8F9FA",
                    "text_muted": "#94a3b8",
                    "border": "rgba(255, 255, 255, 0.12)",
                    "glow": "rgba(5, 150, 105, 0.25)"
                },
                "typography": {
                    "header_font": "Playfair Display",
                    "body_font": "Inter",
                    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap"
                },
                "component_styles": {
                    "buttons": "Radiant emerald with subtle glow and crisp collegiate borders",
                    "cards": "Frosted Oxford Navy glassmorphism with delicate 1px border and backdrop blur",
                    "navbar": "Floating translucent glass header with collegiate crest and emerald highlights"
                },
                "css_tokens": """:root {
  --font-header: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --color-primary: #059669;
  --color-primary-hover: #047857;
  --color-secondary: #0A192F;
  --color-accent: #10b981;
  --color-bg: #0A192F;
  --color-surface: #112240;
  --color-surface-hover: #1e3a5f;
  --color-text: #F8F9FA;
  --color-text-muted: #94a3b8;
  --color-border: rgba(255, 255, 255, 0.12);
  --color-glow: rgba(5, 150, 105, 0.25);
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;
}"""
            }
        elif domain == "luxury_cars":
            return {
                "archetype": "Luxury Automotive & High-Performance Editorial",
                "philosophy": "Deep obsidian backdrop with gold metallic accents and sleek precision geometry",
                "color_palette": {
                    "primary": "#d4af37",
                    "primary_hover": "#b4942b",
                    "secondary": "#ffffff",
                    "accent": "#f59e0b",
                    "bg_main": "#090a10",
                    "bg_surface": "#121217",
                    "bg_surface_elevated": "#1e1e26",
                    "text_main": "#ffffff",
                    "text_muted": "#94a3b8",
                    "border": "rgba(255, 255, 255, 0.1)",
                    "glow": "rgba(212, 175, 55, 0.25)"
                },
                "typography": {
                    "header_font": "Playfair Display",
                    "body_font": "Inter",
                    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap"
                },
                "component_styles": {
                    "buttons": "Brushed gold accents with micro-elevation and sharp metallic borders",
                    "cards": "Smoked obsidian glassmorphism with delicate 1px border",
                    "navbar": "Floating obsidian bar with gold active states"
                },
                "css_tokens": """:root {
  --font-header: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --color-primary: #d4af37;
  --color-primary-hover: #b4942b;
  --color-secondary: #ffffff;
  --color-accent: #f59e0b;
  --color-bg: #090a10;
  --color-surface: #121217;
  --color-surface-hover: #1e1e26;
  --color-text: #ffffff;
  --color-text-muted: #94a3b8;
  --color-border: rgba(255, 255, 255, 0.1);
  --color-glow: rgba(212, 175, 55, 0.25);
  --radius-sm: 4px;
  --radius-md: 10px;
  --radius-lg: 18px;
  --radius-full: 9999px;
}"""
            }
        elif domain == "indian_dhaba":
            return {
                "archetype": "Punjabi Truck Art & Highway Dhaba",
                "philosophy": "Vibrant mustard yellow, chili red, and turquoise folk motifs with rustic warmth",
                "color_palette": {
                    "primary": "#eab308",
                    "primary_hover": "#ca8a04",
                    "secondary": "#dc2626",
                    "accent": "#06b6d4",
                    "bg_main": "#1c1917",
                    "bg_surface": "#292524",
                    "bg_surface_elevated": "#44403c",
                    "text_main": "#fafaf9",
                    "text_muted": "#a8a29e",
                    "border": "rgba(234, 179, 8, 0.25)",
                    "glow": "rgba(234, 179, 8, 0.3)"
                },
                "typography": {
                    "header_font": "Plus Jakarta Sans",
                    "body_font": "Inter",
                    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800;900&display=swap"
                },
                "component_styles": {
                    "buttons": "Bold mustard yellow with deep red hover accents",
                    "cards": "Rustic terracotta panels with folk borders",
                    "navbar": "Vibrant truck-art patterned header"
                },
                "css_tokens": """:root {
  --font-header: 'Plus Jakarta Sans', sans-serif;
  --font-body: 'Inter', sans-serif;
  --color-primary: #eab308;
  --color-primary-hover: #ca8a04;
  --color-secondary: #dc2626;
  --color-accent: #06b6d4;
  --color-bg: #1c1917;
  --color-surface: #292524;
  --color-surface-hover: #44403c;
  --color-text: #fafaf9;
  --color-text-muted: #a8a29e;
  --color-border: rgba(234, 179, 8, 0.25);
  --color-glow: rgba(234, 179, 8, 0.3);
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;
}"""
            }
        else:
            return {
                "archetype": "Modern Glassmorphic Studio",
                "philosophy": "Deep slate background with vibrant indigo accents and frosted glass elevation",
                "color_palette": {
                    "primary": "#6366f1",
                    "primary_hover": "#4f46e5",
                    "secondary": "#a855f7",
                    "accent": "#06b6d4",
                    "bg_main": "#0f172a",
                    "bg_surface": "#1e293b",
                    "bg_surface_elevated": "#334155",
                    "text_main": "#f8fafc",
                    "text_muted": "#94a3b8",
                    "border": "#334155",
                    "glow": "rgba(99, 102, 241, 0.3)"
                },
                "typography": {
                    "header_font": "Plus Jakarta Sans",
                    "body_font": "Inter",
                    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap"
                },
                "component_styles": {
                    "buttons": "Rounded-xl padding with smooth hover elevation and glowing outline",
                    "cards": "Subtle border with backdrop blur and hover lift",
                    "navbar": "Sticky frosted glass header with active link indicators"
                },
                "css_tokens": """:root {
  --font-header: 'Plus Jakarta Sans', sans-serif;
  --font-body: 'Inter', sans-serif;
  --color-primary: #6366f1;
  --color-primary-hover: #4f46e5;
  --color-secondary: #a855f7;
  --color-accent: #06b6d4;
  --color-bg: #0f172a;
  --color-surface: #1e293b;
  --color-surface-hover: #273549;
  --color-text: #f8fafc;
  --color-text-muted: #94a3b8;
  --color-border: #334155;
  --color-glow: rgba(99, 102, 241, 0.25);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 24px;
  --radius-full: 9999px;
}"""
            }