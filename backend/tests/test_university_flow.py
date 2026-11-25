import asyncio
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.ceo_agent import CEOAgent
from agents.ui_designer_agent import UIDesignerAgent

prompt = """Create a modern, high-conversion multi-page React web application for a prestigious modern university campus.

Bespoke Visual Identity & Aesthetic:
- Design Archetype: Academic Heritage meets Modern Glassmorphism
- Color Palette: Deep Oxford Navy (#0A192F), Radiant Emerald (#059669), Warm Cream (#F8F9FA), and Slate Grey (#475569)
- Typography: Playfair Display for editorial headlines paired with Inter for high-legibility UI text

Dedicated Pages & Features:
1. Home: Interactive hero slider, key statistics counter, news ticker, and Quick-Apply drawer.
2. Academics & Programs: Searchable degree directory with dynamic major/minor filters, department hubs, and syllabus preview modals.
3. Virtual Campus Life: 360-degree interactive map modal, student club explorer, and residence hall selector.
4. Admissions & Aid: Step-by-step application tracker, interactive tuition calculator slider, and key deadline countdowns.
5. Campus Visit & Contact: Dynamic calendar booking for campus tours, live chat modal, and interactive travel directions.

Rich Interactivity:
Filterable program catalog, dynamic cost estimator, tabbed syllabus views, multi-step application form with local state persistence, and polished micro-animations.

Tech Stack:
React 18, Vite, React Router v6, Lucide Icons, and a CSS Variables Design System."""

async def run_test():
    print("1. Running CEO Agent...")
    ceo = CEOAgent()
    ceo_res = await ceo.execute({'type': 'review_request'}, {'client_request': prompt, 'autonomous_mode': True})
    spec = ceo_res['product_spec']
    print(f"   • Project Name: {spec.get('project_name')}")
    print(f"   • Category:     {spec.get('category')}")
    print(f"   • Pages:        {[p['name'] if isinstance(p, dict) else str(p) for p in spec.get('pages', [])]}")
    
    print("\n2. Running UI Designer Agent...")
    ui = UIDesignerAgent()
    ui_res = await ui.execute({}, {'client_request': prompt, 'product_spec': spec})
    ds = ui_res['design_spec']
    print(f"   • Archetype:    {ds.get('archetype')}")
    print(f"   • Primary:      {ds.get('color_palette', {}).get('primary')}")
    print(f"   • Header Font:  {ds.get('typography', {}).get('header_font')}")
    print(f"   • Body Font:    {ds.get('typography', {}).get('body_font')}")

if __name__ == "__main__":
    asyncio.run(run_test())
