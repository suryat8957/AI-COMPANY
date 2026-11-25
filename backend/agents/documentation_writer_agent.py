from typing import Dict, Any
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
import json

logger = setup_logger(__name__)

class DocumentationWriterAgent(BaseAgent):
    """Documentation Writer Agent - Technical Documentation Lead creating production-ready README and developer guides"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.DOCUMENTATION_WRITER,
            name="Emily Zhang",
            temperature=0.4
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Emily Zhang, Lead Technical Documentation Specialist at an elite AI Frontend Engineering Studio.

Your mission:
1. Write crystal-clear, developer-friendly, and professional README.md documentation tailored specifically to the generated React application.
2. Structure the README with:
   - Project Title, Domain Description, and Badges (React 18, Vite, React Router, Lucide)
   - Multi-Page Architecture & Feature Guide (detailing each page)
   - Prerequisites (Node.js 18.0+, npm/pnpm/yarn)
   - Step-by-Step Getting Started Guide:
     ```bash
     npm install
     npm run dev
     ```
   - Production Build & Deployment:
     ```bash
     npm run build
     npm run preview
     ```
   - Project Directory Structure
   - Customization & Theming Guide (explaining CSS variables in `src/index.css` and `mockData.js`)
3. Note: clearly state that the developer installs dependencies locally using `npm install`."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute documentation generation"""
        logger.info("Documentation Writer creating comprehensive React project README.md")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        design_spec = context.get("design_spec", {})
        architecture_spec = context.get("architecture_spec", {})
        files = context.get("files", {})
        
        app_name = product_spec.get("project_name", "React Web Application")
        pages = product_spec.get("pages", [])
        
        prompt = f"""Generate a comprehensive, publication-grade README.md for this React project:

Application Name: {app_name}
Client Request: {client_request}
Product Specification:
{json.dumps(product_spec, indent=2) if product_spec else 'Standard multi-page'}

Design System Archetype: {design_spec.get('archetype', 'Modern UI')}
File Manifest ({len(files)} files):
{', '.join(list(files.keys()))}

MANDATORY SECTIONS TO INCLUDE:
1. Header with Title, Tagline, and Badges (React 18, Vite, React Router v6, Lucide Icons)
2. ✨ Project Overview & Value Proposition
3. 🗺️ Multi-Page Architecture & Route Guide (Detail each page and what features it offers)
4. 🛠️ Tech Stack & Key Libraries
5. 📋 Prerequisites (Node.js >= 18.x, npm >= 9.x)
6. 🚀 Quickstart & Installation (Step-by-step: `npm install`, `npm run dev`)
7. 📦 Production Build & Preview (`npm run build`, `npm run preview`)
8. 📂 Project Folder Structure
9. 🎨 Customization & Theming (How to change colors/fonts in `src/index.css` and update content in `src/data/mockData.js`)
10. 📄 License & Credits

Return ONLY the complete Markdown content."""

        try:
            response = await self._generate_response(prompt, context)
            readme_content = self._clean_markdown(response)
            
            self.add_to_memory(f"Generated README for {app_name}")
            
            return {
                "status": "completed",
                "file": "README.md",
                "content": readme_content,
                "output_type": "documentation"
            }
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            fallback = self._get_fallback_readme(app_name, client_request, pages)
            return {
                "status": "completed",
                "file": "README.md",
                "content": fallback,
                "output_type": "documentation"
            }
    
    def _clean_markdown(self, response: str) -> str:
        """Strip markdown wrapper if present"""
        content = response.strip()
        if content.startswith("```markdown") or content.startswith("```md"):
            content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content.rsplit("\n", 1)[0]
        return content.strip()
    
    def _get_fallback_readme(self, app_name: str, client_request: str, pages: list) -> str:
        pages_list = "\n".join([f"- **{p.get('name', 'Page')}** (`{p.get('path', '/')}`): {p.get('purpose', 'Feature view')}" for p in pages]) if pages else "- **Home** (`/`): Main landing and conversion showcase"
        return f"""# {app_name}

> Modern, high-performance multi-page React web application built with React 18, Vite, and React Router v6.

---

## 🌟 Overview
{client_request}

---

## 🗺️ Multi-Page Architecture
{pages_list}

---

## 🛠️ Tech Stack
- **Framework**: React 18 (Functional Components, Hooks, Context)
- **Build Tool**: Vite 5.x
- **Routing**: React Router DOM 6.x
- **Icons**: Lucide React
- **Design System**: Vanilla CSS Variables & Modern Responsive Layouts

---

## 📋 Prerequisites
- **Node.js**: `v18.0.0` or higher
- **npm**: `v9.0.0` or higher (or pnpm / yarn)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser to explore the website.

### 3. Build for Production
```bash
npm run build
```

### 4. Preview Production Build
```bash
npm run preview
```

---

## 📂 Project Structure
```text
src/
├── components/
│   ├── ui/             # Reusable UI primitives (Button, Card, Badge, Modal, SectionTitle)
│   ├── Navbar.jsx      # Sticky responsive navigation with theme toggle
│   └── Footer.jsx      # Multi-column footer with newsletter & sitemap
├── context/
│   └── AppContext.jsx  # Global state (theme, notifications, domain data)
├── data/
│   └── mockData.js     # Realistic domain content
├── layouts/
│   └── MainLayout.jsx  # Page layout wrapper
├── pages/              # Multi-page views (HomePage, AboutPage, ServicesPage, etc.)
├── styles/
│   └── index.css       # Design tokens, variables, resets & utilities
├── App.jsx             # React Router setup
└── main.jsx            # Application entry point
```

---

## 🎨 Customization
- **Theme & Colors**: Modify the CSS variables in `src/index.css` under `:root`.
- **Content & Mock Data**: Edit `src/data/mockData.js` to change testimonials, products, team members, and pricing tiers.
"""
