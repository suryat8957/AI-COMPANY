from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
import json

logger = setup_logger(__name__)

class ReactArchitectAgent(BaseAgent):
    """React Architect Agent - Defines component hierarchy, routing tree, folder structure, and dependencies"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.REACT_ARCHITECT,
            name="David Vance",
            temperature=0.4
        )
    
    def _get_system_prompt(self) -> str:
        return """You are David Vance, Principal React Architect at an elite AI Frontend Engineering Studio.

Your responsibilities:
1. Design clean, scalable React 18+ application architectures with React Router v6.
2. Formulate the exact multi-page routing tree and navigation structure.
3. Define the component hierarchy (reusable UI primitives, common layout wrappers, domain feature widgets, and page components).
4. Establish the global state & context architecture (theme toggle, active page state, notifications, and domain-specific state).
5. Specify standard, non-bloated npm package dependencies in `package.json` (React 18, React DOM, React Router DOM, Lucide React, Vite).
6. Ensure zero code duplication through component composition and clean layout patterns."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute React architectural planning"""
        logger.info("React Architect creating application architecture blueprint")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        design_spec = context.get("design_spec", {})
        
        prompt = f"""Design the complete React technical architecture for this application:

Client Request: {client_request}

Product Specification:
{json.dumps(product_spec, indent=2) if product_spec else 'Standard multi-page application'}

Design System:
{json.dumps(design_spec, indent=2) if design_spec else 'Standard modern design'}

REQUIREMENTS:
1. Generate the complete routing tree using React Router v6.
2. Define the exact file manifest (all files to be generated).
3. Specify reusable UI components (`Button`, `Card`, `Badge`, `Modal`, `SectionTitle`).
4. Specify layout components (`MainLayout`, `Navbar`, `Footer`).
5. Specify all multi-page view components (e.g., `HomePage`, `AboutPage`, `ServicesPage`, `PricingPage`, `ContactPage`, `NotFoundPage`).
6. Specify `AppContext` and `mockData.js` requirements.
7. Declare standard `package.json` dependencies (Vite + React 18 + React Router DOM 6 + Lucide React).

Return a JSON object formatted strictly as:
```json
{{
  "app_name": "string",
  "routing": [
    {{ "path": "/", "page": "HomePage", "label": "Home" }},
    {{ "path": "/about", "page": "AboutPage", "label": "About" }},
    {{ "path": "/services", "page": "ServicesPage", "label": "Services" }},
    {{ "path": "/pricing", "page": "PricingPage", "label": "Pricing" }},
    {{ "path": "/contact", "page": "ContactPage", "label": "Contact" }},
    {{ "path": "*", "page": "NotFoundPage", "label": "404" }}
  ],
  "file_manifest": [
    "package.json",
    "vite.config.js",
    "index.html",
    "src/main.jsx",
    "src/App.jsx",
    "src/index.css",
    "src/context/AppContext.jsx",
    "src/data/mockData.js",
    "src/components/ui/Button.jsx",
    "src/components/ui/Card.jsx",
    "src/components/ui/Badge.jsx",
    "src/components/ui/Modal.jsx",
    "src/components/ui/SectionTitle.jsx",
    "src/components/Navbar.jsx",
    "src/components/Footer.jsx",
    "src/layouts/MainLayout.jsx",
    "src/pages/HomePage.jsx",
    "src/pages/AboutPage.jsx",
    "src/pages/ServicesPage.jsx",
    "src/pages/PricingPage.jsx",
    "src/pages/ContactPage.jsx",
    "src/pages/NotFoundPage.jsx"
  ],
  "components": {{
    "ui": ["Button", "Card", "Badge", "Modal", "SectionTitle"],
    "layout": ["MainLayout", "Navbar", "Footer"],
    "pages": ["HomePage", "AboutPage", "ServicesPage", "PricingPage", "ContactPage", "NotFoundPage"]
  }},
  "state_management": {{
    "context_name": "AppContext",
    "provided_state": ["theme (dark/light)", "activeTab", "cartOrItems", "notifications", "searchQuery"]
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "lucide-react": "^0.300.0",
    "clsx": "^2.0.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.10"
  }}
}}
```"""

        try:
            response = await self._generate_response(prompt, context)
            parsed_arch = self._extract_json(response)
            
            if not parsed_arch or not isinstance(parsed_arch, dict) or "file_manifest" not in parsed_arch:
                parsed_arch = self._get_fallback_architecture(product_spec)
            
            self.add_to_memory(f"Created React architecture with {len(parsed_arch.get('file_manifest', []))} files")
            
            return {
                "status": "completed",
                "architecture_spec": parsed_arch,
                "file_manifest": parsed_arch.get("file_manifest", []),
                "routing": parsed_arch.get("routing", []),
                "output_type": "architecture_spec"
            }
        except Exception as e:
            logger.error(f"React architecture task failed: {e}")
            fallback = self._get_fallback_architecture(product_spec)
            return {
                "status": "completed",
                "architecture_spec": fallback,
                "file_manifest": fallback.get("file_manifest", []),
                "routing": fallback.get("routing", []),
                "output_type": "architecture_spec"
            }
    
    def _get_fallback_architecture(self, product_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Provide a complete fallback React architecture if parsing encounters an issue"""
        pages = product_spec.get("pages", []) if product_spec else []
        
        routing = []
        page_files = []
        page_names = []
        
        if pages:
            for p in pages:
                p_name = p.get("name", "Home")
                component_name = f"{p_name}Page" if not p_name.endswith("Page") else p_name
                path = p.get("path", f"/{p_name.lower()}")
                routing.append({"path": path, "page": component_name, "label": p_name})
                page_files.append(f"src/pages/{component_name}.jsx")
                page_names.append(component_name)
        else:
            routing = [
                {"path": "/", "page": "HomePage", "label": "Home"},
                {"path": "/about", "page": "AboutPage", "label": "About"},
                {"path": "/services", "page": "ServicesPage", "label": "Services"},
                {"path": "/pricing", "page": "PricingPage", "label": "Pricing"},
                {"path": "/contact", "page": "ContactPage", "label": "Contact"}
            ]
            page_files = [
                "src/pages/HomePage.jsx",
                "src/pages/AboutPage.jsx",
                "src/pages/ServicesPage.jsx",
                "src/pages/PricingPage.jsx",
                "src/pages/ContactPage.jsx"
            ]
            page_names = ["HomePage", "AboutPage", "ServicesPage", "PricingPage", "ContactPage"]
        
        # Always append 404
        routing.append({"path": "*", "page": "NotFoundPage", "label": "404"})
        page_files.append("src/pages/NotFoundPage.jsx")
        page_names.append("NotFoundPage")
        
        file_manifest = [
            "package.json",
            "vite.config.js",
            "index.html",
            "src/main.jsx",
            "src/App.jsx",
            "src/index.css",
            "src/context/AppContext.jsx",
            "src/data/mockData.js",
            "src/components/ui/Button.jsx",
            "src/components/ui/Card.jsx",
            "src/components/ui/Badge.jsx",
            "src/components/ui/Modal.jsx",
            "src/components/ui/SectionTitle.jsx",
            "src/components/Navbar.jsx",
            "src/components/Footer.jsx",
            "src/layouts/MainLayout.jsx"
        ] + page_files
        
        return {
            "app_name": product_spec.get("project_name", "ReactApp") if product_spec else "ReactApp",
            "routing": routing,
            "file_manifest": [
                "package.json",
                "vite.config.js",
                "index.html",
                "src/main.jsx",
                "src/App.jsx",
                "src/index.css",
                "src/context/AppContext.jsx",
                "src/data/mockData.js",
                "src/components/ui/Button.jsx",
                "src/components/ui/Card.jsx",
                "src/components/ui/Badge.jsx",
                "src/components/ui/Modal.jsx",
                "src/components/ui/Image.jsx",
                "src/components/ui/SectionTitle.jsx",
                "src/components/Navbar.jsx",
                "src/components/Footer.jsx",
                "src/layouts/MainLayout.jsx"
            ] + page_files,
            "components": {
                "ui": ["Button", "Card", "Badge", "Modal", "Image", "SectionTitle"],
                "layout": ["MainLayout", "Navbar", "Footer"],
                "pages": page_names
            },
            "state_management": {
                "context_name": "AppContext",
                "provided_state": ["theme", "toggleTheme", "activeCategory", "setActiveCategory", "notifications", "searchQuery", "cart", "savedItems"]
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.21.0",
                "lucide-react": "^0.300.0",
                "clsx": "^2.0.0",
                "framer-motion": "^11.0.0"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.17",
                "postcss": "^8.4.35",
                "tailwindcss": "^3.4.1",
                "vite": "^5.0.10"
            }
        }
