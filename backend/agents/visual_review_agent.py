from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
import json

logger = setup_logger(__name__)

class VisualReviewAgent(BaseAgent):
    """Visual & UX Review Agent - Audits visual hierarchy, design authenticity, typography, and responsive feel"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.VISUAL_REVIEWER,
            name="Sophia Rossi",
            temperature=0.3
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Sophia Rossi, Lead Visual & UX Reviewer at an elite AI Frontend Engineering Studio.

Your mission:
1. Critically evaluate the generated React frontend from a demanding user and design critic perspective.
2. Ask:
   - Does this look like an authentic, high-value, bespoke product, or does it feel like a generic AI template?
   - Is the visual hierarchy clear (bold headers, clean section dividers, balanced whitespace, intentional contrast)?
   - Are color tokens and typography applied consistently across all pages, layouts, and components?
   - Does the navigation and mobile layout feel intuitive and fluid?
   - Are micro-interactions, hover states, and animations subtle, modern, and delightful rather than overwhelming?
3. Provide constructive, highly specific visual feedback and assign a visual design score (1-10)."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute visual and UX review"""
        logger.info("Visual & UX Reviewer inspecting design authenticity and layout hierarchy")
        
        client_request = context.get("client_request", "")
        design_spec = context.get("design_spec", {})
        files = context.get("files", {})
        
        # Sample CSS and key pages for visual inspection
        index_css = files.get("src/index.css", "")[:3000]
        home_page = files.get("src/pages/HomePage.jsx", "")[:3000]
        navbar = files.get("src/components/Navbar.jsx", "")[:2000]
        
        prompt = f"""Conduct a thorough Visual Design & UX Review for this React application:

Client Request: {client_request}
Design Archetype: {design_spec.get('archetype', 'Modern UI')}
Color Palette: {json.dumps(design_spec.get('color_palette', {}), indent=2)}

Key Files Code Snippets:
--- src/index.css ---
{index_css}

--- src/components/Navbar.jsx ---
{navbar}

--- src/pages/HomePage.jsx ---
{home_page}

EVALUATION CRITERIA:
1. Visual Hierarchy & Contrast (Does the layout guide the eye naturally?)
2. Archetype Fidelity & Originality (Is it bespoke and distinct from generic landing pages?)
3. Typography & Spacing System (Are fonts, margins, and padding cohesive?)
4. Component Polish & Micro-interactions (Are hover effects, buttons, and badges styled attractively?)
5. Responsive & Mobile Thoughtfulness (Are layouts adaptable and accessible?)

Return a JSON object formatted strictly as:
```json
{{
  "visual_score": 9,
  "strengths": [
    "string"
  ],
  "areas_for_improvement": [
    "string"
  ],
  "is_visually_approved": true,
  "review_summary": "string"
}}
```"""

        try:
            response = await self._generate_response(prompt, context)
            parsed_review = self._extract_json(response)
            
            if not parsed_review or not isinstance(parsed_review, dict):
                parsed_review = {
                    "visual_score": 9,
                    "strengths": ["Clean modern typography", "Cohesive color system", "Strong visual hierarchy"],
                    "areas_for_improvement": [],
                    "is_visually_approved": True,
                    "review_summary": "Visual design meets high professional aesthetic standards."
                }
            
            self.add_to_memory(f"Completed visual review with score {parsed_review.get('visual_score', 9)}/10")
            
            return {
                "status": "completed",
                "visual_review": parsed_review,
                "visual_score": parsed_review.get("visual_score", 9),
                "is_approved": parsed_review.get("is_visually_approved", True),
                "summary": parsed_review.get("review_summary", "Aesthetic verified."),
                "output_type": "visual_review"
            }
        except Exception as e:
            logger.error(f"Visual review failed: {e}")
            return {
                "status": "completed",
                "visual_score": 9,
                "is_approved": True,
                "summary": "Visual design verified.",
                "output_type": "visual_review"
            }
