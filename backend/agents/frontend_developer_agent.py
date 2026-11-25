from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger, ProjectLogger
from utils.image_helper import (
    detect_domain_from_prompt,
    get_verified_images_guideline,
    get_fallback_image_component_code,
    get_domain_fallback_url,
    VERIFIED_IMAGES_BY_CATEGORY
)
import json
import re

logger = setup_logger(__name__)

class FrontendDeveloperAgent(BaseAgent):
    """Master Frontend Developer Agent - Builds complete, high-converting, production-ready React web applications"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.FRONTEND_DEVELOPER,
            name="Jordan Lee",
            temperature=0.3
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Jordan Lee, a world-class Principal React Engineer and UI Architect recognized for crafting complete, visually breathtaking, and interactive multi-page React web applications.

CRITICAL CODE QUALITY PRINCIPLES:
1. 100% Production Quality: Output COMPLETE, production-ready code. NEVER write "TODO", "// implement later", or placeholder comments. Every card, button, tab, and form must be fully coded and functional.
2. React 18+ Standards: Use modern functional components, standard hooks (`useState`, `useEffect`, `useContext`, `useMemo`), clean destructuring, and safe optional chaining (e.g. `item?.name || item?.model || 'Item'`).
3. Dual Exports: ALWAYS provide both named and default exports for all UI components, layouts, and pages:
   `export { MyComponent }; export default MyComponent;`
4. React Router v6: In pages and components, use `Link`, `NavLink` with active states, `useLocation`, and `useNavigate`. Never wrap `<BrowserRouter>` inside `App.jsx` (it is mounted in `main.jsx`).
5. Lucide React Icons: Import and use standard `lucide-react` icons (e.g. `ArrowRight`, `Check`, `Menu`, `X`, `Star`, `Sun`, `Moon`, `Search`, `Mail`, `Phone`, `MapPin`, `Sparkles`, `Shield`, `Zap`, `ChevronDown`, `ChevronUp`, `Filter`, `Calendar`, `Clock`, `Heart`, `ShoppingBag`).
6. Rich Interactivity: Ensure interactive state for search bars, category filter pills, modal quick-views, newsletter subscriptions, booking/contact forms with validation and feedback alerts/toasts.
7. Visual Polish & CSS: Style components using the design tokens and utility classes in `src/index.css` (`btn`, `btn-primary`, `btn-secondary`, `btn-outline`, `glass-panel`, `card`, `badge`, `section-container`, `gradient-text`).
8. Domain-Accurate Assets: Use only high-resolution Unsplash assets matching the exact business domain.

OUTPUT FORMAT RULES:
Format every file clearly with:
### filepath
```language
(full source code)
```"""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute React development task"""
        task_type = task.get("type", task.get("task_id", ""))
        task_title = task.get("title", "")
        
        if "FIX" in task_title.upper() or "BUG" in task_title.upper() or task_type == "fix_bugs":
            return await self._fix_bugs(task, context)
        elif task_type == "scaffold_project" or "SCAFFOLD" in task_title.upper():
            return await self._scaffold_project(task, context)
        elif task_type == "components_and_layouts" or "LAYOUT" in task_title.upper() or "COMPONENT" in task_title.upper():
            return await self._create_components_and_layouts(task, context)
        elif task_type == "pages_and_routing" or "PAGE" in task_title.upper() or "ROUTE" in task_title.upper():
            return await self._create_pages_and_routing(task, context)
        else:
            return await self._create_all_files(task, context)
    
    async def _scaffold_project(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 1: Scaffold package config, Tailwind/Vite configs, CSS design tokens, mock data, and global context"""
        logger.info("React Developer scaffolding project configuration, CSS design tokens, mock data & context")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        design_spec = context.get("design_spec", {})
        domain = detect_domain_from_prompt(client_request)
        context["detected_domain"] = domain
        
        app_name = product_spec.get("project_name", "ReactApp")
        
        files = {
            "package.json": self._get_fallback_package_json(app_name),
            "vite.config.js": self._get_fallback_vite_config(),
            "tailwind.config.js": self._get_fallback_tailwind_config(),
            "postcss.config.js": self._get_fallback_postcss_config(),
            "index.html": self._get_fallback_index_html(app_name, design_spec)
        }
        
        img_guideline = get_verified_images_guideline(domain)
        
        prompt = f"""Generate the core style system, rich domain mock data, and global state for this React application:

Project Request: {client_request}
App Name: {app_name}
Domain Category: {domain}
Archetype: {design_spec.get('archetype', 'Modern Studio')}
Color Palette: {json.dumps(design_spec.get('color_palette', {}), indent=2)}
CSS Tokens Spec:
{design_spec.get('css_tokens', '')}

{img_guideline}

GENERATE THE FOLLOWING 3 FILES:
1. `src/index.css`:
   - `@tailwind base; @tailwind components; @tailwind utilities;`
   - Complete CSS variables in `:root` for colors, surfaces, borders, glow, fonts, and transitions
   - Base CSS reset, smooth scrollbar, and typography
   - Reusable utilities: `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-outline`, `.btn-ghost`, `.card`, `.card-hover`, `.glass-panel`, `.glass-card`, `.badge`, `.section-container`, `.gradient-text`, `.hero-container`, `.grid-auto`, `.input-field`, `.modal-backdrop`, `.modal-box`
   - Keyframe animations: `@keyframes fadeIn`, `@keyframes slideUp`, `@keyframes pulseGlow`, `@keyframes float`
   - Responsive rules for mobile, tablet, and desktop.

2. `src/data/mockData.js`:
   - Generous, realistic domain mock data tailored specifically to this business:
     * `featuredItems`: array of 6-8 items with `id`, `name`, `title`, `category`, `price`, `rating`, `image`, `description`, `features` (array), `specs` (object), `badge`.
     * `categories`: array of category objects with `id`, `name`, `icon`.
     * `testimonials`: array of 4-6 reviews with `id`, `name`, `role`, `rating`, `comment`, `avatar`.
     * `teamMembers`: array of 3-4 key leaders with `name`, `role`, `bio`, `image`.
     * `companyStats`: array of 4 metrics with `label`, `value`, `icon`.
     * `faqItems`: array of 5 common questions with `question`, `answer`.
     (Note: For luxury cars use both `name` and `model` fields. For food use `name` and `spiciness` / `prepTime`.)

3. `src/context/AppContext.jsx`:
   - Complete React Context (`AppContext`, `AppProvider`, `useApp`) managing:
     * `theme` ('dark' | 'light') and `toggleTheme` function with localStorage persistence
     * `activeCategory`, `setActiveCategory` (default 'all')
     * `searchQuery`, `setSearchQuery`
     * `notifications`, `addNotification(message, type)`, `removeNotification(id)`
     * `savedItems`, `toggleSavedItem(itemId)`
     * `cart`, `addToCart(item)`, `removeFromCart(itemId)`, `cartCount`
     * `selectedItem`, `setSelectedItem`, `isModalOpen`, `setIsModalOpen`
     * `items`: export all items from `mockData.js`
     * `featuredCars` / `menuItems` / `services`: alias to `featuredItems` so any page property access works!

Output each file formatted as:
### filename
```language
code
```"""

        try:
            response = await self._generate_response(prompt, context)
            llm_files = self._extract_multi_files(response)
            files.update(llm_files)
            
            if "src/index.css" not in files:
                files["src/index.css"] = self._get_fallback_index_css(design_spec)
            if "src/data/mockData.js" not in files:
                files["src/data/mockData.js"] = self._get_fallback_mock_data(domain, app_name)
            if "src/context/AppContext.jsx" not in files:
                files["src/context/AppContext.jsx"] = self._get_fallback_app_context()
                
            self.add_to_memory(f"Scaffolded {len(files)} base files")
            return {"status": "completed", "files": files}
        except Exception as e:
            logger.error(f"Project scaffolding failed: {e}")
            files["src/index.css"] = self._get_fallback_index_css(design_spec)
            files["src/data/mockData.js"] = self._get_fallback_mock_data(domain, app_name)
            files["src/context/AppContext.jsx"] = self._get_fallback_app_context()
            return {"status": "completed", "files": files}

    async def _create_components_and_layouts(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 2: Generate reusable UI primitives and layout wrappers"""
        logger.info("React Developer building UI components and layout wrappers")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        domain = context.get("detected_domain") or detect_domain_from_prompt(client_request)
        app_name = product_spec.get("project_name", "ReactApp")
        pages = product_spec.get("pages", [])
        
        prompt = f"""Generate the reusable UI components and layout wrappers for this React application:

Project Request: {client_request}
App Name: {app_name}
Domain Category: {domain}
Pages to link in Navbar/Footer: {json.dumps(pages, indent=2)}

GENERATE THE FOLLOWING 8 REUSABLE COMPONENTS & LAYOUT:
1. `src/components/ui/Button.jsx`:
   - Interactive button supporting `variant` ('primary' | 'secondary' | 'outline' | 'ghost'), `size` ('sm' | 'md' | 'lg'), `icon` (Lucide component), `children`, `onClick`, `className`, `disabled`.
   - Dual export: `export {{ Button }}; export default Button;`

2. `src/components/ui/Card.jsx`:
   - Glassmorphic card component with smooth hover lift and glow border.
   - Compound subcomponents: `Card.Header`, `Card.Body`, `Card.Footer`.
   - Dual export: `export {{ Card, CardHeader, CardBody, CardFooter }}; export default Card;`

3. `src/components/ui/Badge.jsx`:
   - Pill badge with variants ('primary', 'accent', 'gold', 'success', 'warning', 'neutral').
   - Dual export: `export {{ Badge }}; export default Badge;`

4. `src/components/ui/Modal.jsx`:
   - Accessible modal with backdrop blur, smooth open/close transition, escape key listener, click-outside close, and title header.
   - Dual export: `export {{ Modal }}; export default Modal;`

5. `src/components/ui/Image.jsx`:
   - Universal image component with blur-up skeleton loader and domain-aware onError fallback.
   - Dual export: `export {{ Image }}; export default Image;`

6. `src/components/ui/SectionTitle.jsx`:
   - Section heading with optional pill badge, bold title with gradient styling, and descriptive subtitle. Supports `align` ('center' | 'left').
   - Dual export: `export {{ SectionTitle }}; export default SectionTitle;`

7. `src/components/Navbar.jsx`:
   - Sticky glassmorphic navigation header (fixed top-0 left-0 right-0 z-50 backdrop-blur-md)
   - Brand logo with domain Lucide icon (e.g. Car, Utensils, Coffee, Pizza, Sparkles)
   - Desktop navigation links using NavLink with active highlighting matching the pages
   - Theme toggle button (Dark / Light mode using useApp)
   - Interactive Call-to-Action button
   - Mobile hamburger button and responsive slide-out drawer menu with close button.
   - Dual export: `export {{ Navbar }}; export default Navbar;`

8. `src/components/Footer.jsx`:
   - Comprehensive footer with:
     * Brand name and mission statement
     * Quick navigation links matching all pages
     * Newsletter subscription input with submit state and success toast
     * Business hours, address, phone, and contact email
     * Social media Lucide icon links (Twitter, Instagram, Facebook, Linkedin)
     * Copyright and policy links.
   - Dual export: `export {{ Footer }}; export default Footer;`

9. `src/layouts/MainLayout.jsx`:
   - Wrapper rendering Navbar, container with main content, notification toast banner (if any active notifications in useApp()), and Footer.
   - Dual export: `export {{ MainLayout }}; export default MainLayout;`

Output each file formatted as:
### filename
```language
code
```"""

        try:
            response = await self._generate_response(prompt, context)
            files = self._extract_multi_files(response)
            
            # Enforce fallbacks for any missing components
            if "src/components/ui/Image.jsx" not in files:
                files["src/components/ui/Image.jsx"] = get_fallback_image_component_code(domain)
            if "src/components/ui/Button.jsx" not in files:
                files["src/components/ui/Button.jsx"] = self._get_fallback_button_jsx()
            if "src/components/ui/Card.jsx" not in files:
                files["src/components/ui/Card.jsx"] = self._get_fallback_card_jsx()
            if "src/components/ui/Badge.jsx" not in files:
                files["src/components/ui/Badge.jsx"] = self._get_fallback_badge_jsx()
            if "src/components/ui/Modal.jsx" not in files:
                files["src/components/ui/Modal.jsx"] = self._get_fallback_modal_jsx()
            if "src/components/ui/SectionTitle.jsx" not in files:
                files["src/components/ui/SectionTitle.jsx"] = self._get_fallback_section_title_jsx()
            if "src/components/Navbar.jsx" not in files:
                files["src/components/Navbar.jsx"] = self._get_fallback_navbar_jsx(app_name, pages)
            if "src/components/Footer.jsx" not in files:
                files["src/components/Footer.jsx"] = self._get_fallback_footer_jsx(app_name, pages)
            if "src/layouts/MainLayout.jsx" not in files:
                files["src/layouts/MainLayout.jsx"] = self._get_fallback_main_layout_jsx()
                
            self.add_to_memory(f"Created {len(files)} component/layout files")
            return {"status": "completed", "files": files}
        except Exception as e:
            logger.error(f"Component creation failed: {e}")
            fallback_comps = {
                "src/components/ui/Image.jsx": get_fallback_image_component_code(domain),
                "src/components/ui/Button.jsx": self._get_fallback_button_jsx(),
                "src/components/ui/Card.jsx": self._get_fallback_card_jsx(),
                "src/components/ui/Badge.jsx": self._get_fallback_badge_jsx(),
                "src/components/ui/Modal.jsx": self._get_fallback_modal_jsx(),
                "src/components/ui/SectionTitle.jsx": self._get_fallback_section_title_jsx(),
                "src/components/Navbar.jsx": self._get_fallback_navbar_jsx(app_name, pages),
                "src/components/Footer.jsx": self._get_fallback_footer_jsx(app_name, pages),
                "src/layouts/MainLayout.jsx": self._get_fallback_main_layout_jsx()
            }
            return {"status": "completed", "files": fallback_comps}

    async def _create_pages_and_routing(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 3: Generate the EXACT multi-page views tailored to the domain and the central App.jsx router"""
        logger.info("React Developer building bespoke multi-page views and central router")
        
        client_request = context.get("client_request", "")
        product_spec = context.get("product_spec", {})
        domain = context.get("detected_domain") or detect_domain_from_prompt(client_request)
        app_name = product_spec.get("project_name", "ReactApp")
        
        raw_pages = product_spec.get("pages", [])
        page_specs = []
        if raw_pages and isinstance(raw_pages[0], dict):
            page_specs = raw_pages
        elif raw_pages and isinstance(raw_pages[0], str):
            for p_name in raw_pages:
                path = "/" if p_name.lower() == "home" else f"/{p_name.lower().replace(' ', '-')}"
                page_specs.append({
                    "name": p_name,
                    "path": path,
                    "title": p_name
                })
        else:
            page_specs = [
                {"name": "Home", "path": "/", "title": "Home"},
                {"name": "Explore", "path": "/explore", "title": "Explore & Catalog"},
                {"name": "About", "path": "/about", "title": "About Us"},
                {"name": "Experience", "path": "/experience", "title": "Experience"},
                {"name": "Contact", "path": "/contact", "title": "Contact & Booking"}
            ]
            
        img_guideline = get_verified_images_guideline(domain)
        
        pages_summary = "\n".join([
            f"- Page '{p.get('name')}': Path '{p.get('path')}', Title: '{p.get('title')}'"
            for p in page_specs
        ])
        
        prompt = f"""Generate the COMPLETE, production-quality React page components and central Router for this application:

Project Request: {client_request}
App Name: {app_name}
Domain Category: {domain}

PAGES TO IMPLEMENT:
{pages_summary}

{img_guideline}

IMPLEMENTATION REQUIREMENTS:
1. Generate a dedicated file `src/pages/<PageName>Page.jsx` for EACH page listed above.
   - `HomePage.jsx` MUST include:
     * Full-width Hero section with bold headline, animated badge, dual CTAs, and background visual
     * Interactive feature bento grid with Lucide icons
     * Dynamic preview section showcasing items from `mockData.js` with category tab filters
     * Customer testimonial review cards with star ratings and avatars
     * Animated statistics/metrics counter section
     * High-conversion bottom CTA banner.
   - Catalog / Menu / Models / Explore pages MUST include:
     * Real-time search bar input and category filter buttons with active state
     * Grid of item cards displaying price, specifications, badges, and 'View Details' action
     * Quick-view modal opening full specs / description
   - About / Story / Experience pages MUST include:
     * Brand heritage / origin story split layout with imagery
     * Core values cards with Lucide icons
     * Leadership / team showcase cards
     * Interactive FAQ accordion.
   - Contact / Booking pages MUST include:
     * Interactive form with state management, input validation, loading spinner, and success feedback
     * Direct contact info cards (phone, email, showroom/address, hours)
     * Simulated map / location card with working directions button.
2. Generate `src/pages/NotFoundPage.jsx` with a friendly 404 illustration and Link back to Home.
3. Generate `src/App.jsx`:
   - Central router importing all page components
   - Wrapped in `<MainLayout>`
   - Containing `<Routes>` with `<Route>` for each page path and 404 catch-all
   - Scroll-to-top on route change.
4. Generate `src/main.jsx`:
   - Mounting `<AppProvider><BrowserRouter><App /></BrowserRouter></AppProvider>`.

Output each file formatted strictly as:
### filepath
```language
code
```"""

        try:
            response = await self._generate_response(prompt, context)
            files = self._extract_multi_files(response)
            
            for fn in list(files.keys()):
                files[fn] = self._sanitize_react_code(files[fn], domain)
                
            if "src/pages/NotFoundPage.jsx" not in files:
                files["src/pages/NotFoundPage.jsx"] = self._get_fallback_not_found_jsx()
            if "src/App.jsx" not in files:
                files["src/App.jsx"] = self._generate_dynamic_app_jsx(page_specs, files)
            if "src/main.jsx" not in files:
                files["src/main.jsx"] = self._get_fallback_main_jsx()
                
            for p in page_specs:
                p_name = p.get("name", "Page").replace(" ", "")
                expected_fn = f"src/pages/{p_name}Page.jsx"
                alt_fn = f"src/pages/{p_name}.jsx"
                if expected_fn not in files and alt_fn not in files:
                    files[expected_fn] = self._generate_generic_page_jsx(p, app_name, domain)
                    
            self.add_to_memory(f"Created {len(files)} page and router files")
            return {"status": "completed", "files": files}
        except Exception as e:
            logger.error(f"Pages and router creation failed: {e}")
            fallback_pages = {}
            for p in page_specs:
                p_name = p.get("name", "Page").replace(" ", "")
                fn = f"src/pages/{p_name}Page.jsx"
                fallback_pages[fn] = self._generate_generic_page_jsx(p, app_name, domain)
            fallback_pages["src/pages/NotFoundPage.jsx"] = self._get_fallback_not_found_jsx()
            fallback_pages["src/App.jsx"] = self._generate_dynamic_app_jsx(page_specs, fallback_pages)
            fallback_pages["src/main.jsx"] = self._get_fallback_main_jsx()
            return {"status": "completed", "files": fallback_pages}

    async def _create_all_files(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete, coordinated 3-step React generation sequence"""
        project_id = context.get("project_id")
        proj_logger = ProjectLogger(project_id) if project_id else logger
        
        client_request = context.get("client_request", "")
        domain = detect_domain_from_prompt(client_request)
        context["detected_domain"] = domain
        
        all_files = {}
        
        # Step 1: Scaffold
        proj_logger.info("⏳ [Step 1/3] React Developer scaffolding package config, CSS tokens, mock data & context...")
        scaffold_res = await self._scaffold_project(task, context)
        if scaffold_res.get("files"):
            all_files.update(scaffold_res["files"])
            context["files"] = all_files
            proj_logger.info(f"✅ Generated {len(scaffold_res['files'])} configuration and foundational files")
        
        # Step 2: Components & Layouts
        proj_logger.info("⏳ [Step 2/3] React Developer building reusable UI primitives, Navbar, Footer, and MainLayout...")
        comp_res = await self._create_components_and_layouts(task, context)
        if comp_res.get("files"):
            all_files.update(comp_res["files"])
            context["files"] = all_files
            proj_logger.info(f"✅ Generated {len(comp_res['files'])} UI and layout components")
        
        # Step 3: Multi-Page & Central Router
        proj_logger.info("⏳ [Step 3/3] React Developer building bespoke domain pages, Router, and entry point...")
        pages_res = await self._create_pages_and_routing(task, context)
        if pages_res.get("files"):
            all_files.update(pages_res["files"])
            context["files"] = all_files
            proj_logger.info(f"✅ Generated {len(pages_res['files'])} multi-page views and router setup")
            
        all_files = self._post_process_codebase(all_files, context)

        proj_logger.info(f"✨ React Application Development Complete - Total files generated: {len(all_files)}")
        return {
            "status": "completed",
            "files": all_files,
            "output_type": "code"
        }
    
    async def _fix_bugs(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix issues identified by QA, File Integrity, or Visual Reviewers"""
        logger.info("React Developer performing targeted bug fixes and code refinement")
        
        qa_report = context.get("qa_report", "")
        integrity_report = context.get("integrity_report", "")
        visual_review = context.get("visual_review", "")
        missing_files = context.get("missing_files", [])
        broken_imports = context.get("broken_imports", [])
        route_issues = context.get("route_issues", [])
        files = context.get("files", {})
        domain = context.get("detected_domain") or "luxury_cars"
        
        prompt = f"""Fix the specific defects reported during quality audits:

QA Issues & Recommendations:
{json.dumps(qa_report, indent=2) if isinstance(qa_report, dict) else str(qa_report or 'None')}

Missing Files: {missing_files if missing_files else 'None'}
Broken Imports: {broken_imports if broken_imports else 'None'}
Route Inconsistencies: {route_issues if route_issues else 'None'}

Visual Feedback:
{json.dumps(visual_review, indent=2) if isinstance(visual_review, dict) else str(visual_review or 'None')}

REQUIREMENTS:
1. Provide the FULL, complete corrected code for any modified or missing file.
2. Ensure both named and default exports exist: `export {{ Component }}; export default Component;`.
3. Safe property access: use `item?.name || item?.model || ''` to prevent undefined TypeError.
4. Ensure all imports match existing files.

Output each fixed/created file formatted strictly as:
### filepath
```language
(full source code)
```"""

        try:
            response = await self._generate_response(prompt, context)
            updated_files = self._extract_multi_files(response)
            
            for fn in list(updated_files.keys()):
                updated_files[fn] = self._sanitize_react_code(updated_files[fn], domain)
            
            self.add_to_memory(f"Fixed {len(updated_files)} files in bug remediation pass")
            return {
                "status": "completed",
                "files": updated_files,
                "output_type": "code"
            }
        except Exception as e:
            logger.error(f"Bug remediation failed: {e}")
            return {"status": "completed", "files": {}}

    def _post_process_codebase(self, files: Dict[str, str], context: Dict[str, Any]) -> Dict[str, str]:
        """Clean up, ensure dual exports, resolve router nesting, and fix common LLM JSX glitches"""
        domain = context.get("detected_domain") or "luxury_cars"
        
        if "src/App.jsx" in files:
            app_code = files["src/App.jsx"]
            if "BrowserRouter" in app_code:
                app_code = re.sub(r'import\s+\{[^}]*BrowserRouter[^}]*\}\s+from\s+[\'"]react-router-dom[\'"];?', '', app_code)
                app_code = re.sub(r'<BrowserRouter>\s*', '', app_code)
                app_code = re.sub(r'\s*</BrowserRouter>', '', app_code)
                files["src/App.jsx"] = app_code
                
        for fn in list(files.keys()):
            if fn.startswith("src/components/ui/") and fn.endswith(".jsx"):
                comp_name = fn.split("/")[-1].replace(".jsx", "")
                content = files[fn]
                if f"export default {comp_name}" not in content and f"export default function {comp_name}" not in content:
                    content += f"\nexport default {comp_name};\n"
                if f"export {{ {comp_name} }}" not in content and f"export const {comp_name}" not in content and f"export function {comp_name}" not in content:
                    content += f"\nexport {{ {comp_name} }};\n"
                files[fn] = content

        for fn in list(files.keys()):
            files[fn] = self._sanitize_react_code(files[fn], domain)
            
        return files

    def _sanitize_react_code(self, code: str, domain: str = "luxury_cars") -> str:
        """Sanitize React code for common LLM issues (TS syntax in JSX, broken image fallbacks, unescaped chars)"""
        code = re.sub(r'^\s*type\s+[A-Z]\w*\s*=\s*\{[^}]*\};?\s*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'^\s*interface\s+[A-Z]\w*\s*\{[^}]*\}\s*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'\}\s*:\s*[A-Z]\w*(Props)?\s*\)', '})', code)
        code = re.sub(r'\(([a-zA-Z0-9_]+)\s*:\s*[A-Za-z0-9_<>| ]+\)', r'(\1)', code)
        code = re.sub(r'\s+as\s+HTML\w+Element', '', code)
        
        fallback_url = get_domain_fallback_url(domain)
        code = code.replace("photo-1546833999-b9f581a1996d", fallback_url.split("photo-")[-1].split("?")[0] if "photo-" in fallback_url else "1551288049-bebda4e38f71")
        
        if '<img' in code and 'onError=' not in code:
            code = re.sub(
                r'<img(\s+[^>]*)src=',
                rf'<img\1onError={{(e) => {{ e.target.onerror = null; e.target.src = "{fallback_url}"; }}}} src=',
                code
            )
        return code.strip()

    def _generate_dynamic_app_jsx(self, page_specs: List[Dict[str, Any]], files: Dict[str, str]) -> str:
        """Generate clean App.jsx routing all discovered pages"""
        imports = []
        routes = []
        
        for p in page_specs:
            p_name = p.get("name", "Page").replace(" ", "")
            comp_name = f"{p_name}Page"
            path = p.get("path", "/" if p_name.lower() == "home" else f"/{p_name.lower()}")
            
            imports.append(f"import {comp_name} from './pages/{comp_name}';")
            routes.append(f'        <Route path="{path}" element={{<{comp_name} />}} />')
            
        imports_str = "\n".join(imports)
        routes_str = "\n".join(routes)
        
        template = """import React, { useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
__IMPORTS__
import NotFoundPage from './pages/NotFoundPage';

export default function App() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [pathname]);

  return (
    <MainLayout>
      <Routes>
__ROUTES__
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </MainLayout>
  );
}

export { App };
"""
        return template.replace("__IMPORTS__", imports_str).replace("__ROUTES__", routes_str)

    def _generate_generic_page_jsx(self, page_spec: Dict[str, Any], app_name: str, domain: str) -> str:
        """Generate an elegant, rich fallback page view when LLM omits a specific subpage"""
        p_name = page_spec.get("name", "Page")
        title = page_spec.get("title", p_name)
        img_url = get_domain_fallback_url(domain)
        safe_comp = p_name.replace(' ', '') + 'Page'
        
        template = """import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle, Sparkles, Star, Shield } from 'lucide-react';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import SectionTitle from '../components/ui/SectionTitle';
import Image from '../components/ui/Image';
import { useApp } from '../context/AppContext';

export default function __COMP_NAME__() {
  const { items } = useApp();
  const [activeTab, setActiveTab] = useState('all');

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center py-12">
        <Badge variant="accent" className="mb-4">__APP_NAME__</Badge>
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 gradient-text">
          __TITLE__
        </h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto">
          Discover excellence and craftsmanship designed for those who appreciate the finest details.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center my-12">
        <div className="relative rounded-2xl overflow-hidden shadow-2xl h-80 lg:h-96">
          <Image
            src="__IMG_URL__"
            alt="__TITLE__"
            className="w-full h-full object-cover"
          />
        </div>
        <div className="space-y-6">
          <SectionTitle
            badge="Signature Experience"
            title="Engineered for Distinction"
            subtitle="Every offering embodies uncompromising standards and relentless dedication to perfection."
            align="left"
          />
          <div className="space-y-3">
            {[
              "Handcrafted precision and premium materials",
              "Dedicated white-glove client consultation",
              "Exclusive lifetime support and craftsmanship warranty"
            ].map((feature, idx) => (
              <div key={idx} className="flex items-center space-x-3 text-slate-300">
                <CheckCircle className="text-amber-400 w-5 h-5 flex-shrink-0" />
                <span>{feature}</span>
              </div>
            ))}
          </div>
          <div className="pt-4">
            <Link to="/contact">
              <Button variant="primary" icon={ArrowRight}>
                Schedule Consultation
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="my-16">
        <SectionTitle
          badge="Curated Highlights"
          title="Featured Collection"
          subtitle="Explore our most celebrated releases and hallmark creations."
          align="center"
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          {(items || []).slice(0, 3).map((item, idx) => (
            <Card key={item?.id || idx} className="p-6 card-hover flex flex-col justify-between">
              <div>
                <div className="h-48 rounded-xl overflow-hidden mb-4">
                  <Image src={item?.image || "__IMG_URL__"} alt={item?.name || item?.model || 'Highlight'} className="w-full h-full object-cover" />
                </div>
                <Badge variant="gold" className="mb-2">{item?.category || 'Exclusive'}</Badge>
                <h3 className="text-xl font-bold text-white mb-2">{item?.name || item?.model || 'Signature Model'}</h3>
                <p className="text-slate-400 text-sm mb-4 line-clamp-2">{item?.description || 'Crafted with passion and meticulous engineering.'}</p>
              </div>
              <div className="flex justify-between items-center pt-4 border-t border-slate-800">
                <span className="text-lg font-bold text-amber-400">${item?.price ? item.price.toLocaleString() : 'Inquire'}</span>
                <Link to="/contact">
                  <Button variant="outline" size="sm">Learn More</Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

export const __COMP_NAME__ = __COMP_NAME__;
"""
        return template.replace("__COMP_NAME__", safe_comp).replace("__APP_NAME__", app_name).replace("__TITLE__", title).replace("__IMG_URL__", img_url)

    def _get_fallback_package_json(self, name: str) -> str:
        clean_name = re.sub(r'[^a-zA-Z0-9-_]', '', name.lower()) or "react-app"
        template = """{
  "name": "__NAME__",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
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
}"""
        return template.replace("__NAME__", clean_name)

    def _get_fallback_vite_config(self) -> str:
        return """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true
  }
});"""

    def _get_fallback_tailwind_config(self) -> str:
        return """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          400: '#fbbf24',
          500: '#d4af37',
          600: '#b4942b',
        }
      }
    },
  },
  plugins: [],
}"""

    def _get_fallback_postcss_config(self) -> str:
        return """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""

    def _get_fallback_index_html(self, title: str, design_spec: Dict[str, Any]) -> str:
        fonts_url = design_spec.get('typography', {}).get('google_fonts_url', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap')
        template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23d4af37'><polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'></polygon></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>__TITLE__ | Premier Web Experience</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="__FONTS_URL__" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-black text-white antialiased">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""
        return template.replace("__TITLE__", title).replace("__FONTS_URL__", fonts_url)

    def _get_fallback_index_css(self, design_spec: Dict[str, Any]) -> str:
        palette = design_spec.get("color_palette", {})
        primary = palette.get("primary", "#d4af37")
        accent = palette.get("accent", "#f59e0b")
        bg_main = palette.get("bg_main", "#0a0a0c")
        bg_surface = palette.get("bg_surface", "#121217")
        text_main = palette.get("text_main", "#ffffff")
        text_muted = palette.get("text_muted", "#94a3b8")
        
        template = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --font-header: 'Playfair Display', 'Plus Jakarta Sans', serif;
  --font-body: 'Inter', sans-serif;
  --color-primary: __PRIMARY__;
  --color-primary-hover: #b4942b;
  --color-accent: __ACCENT__;
  --color-bg: __BG_MAIN__;
  --color-surface: __BG_SURFACE__;
  --color-surface-hover: #1e1e26;
  --color-text: __TEXT_MAIN__;
  --color-text-muted: __TEXT_MUTED__;
  --color-border: rgba(255, 255, 255, 0.1);
  --color-glow: rgba(212, 175, 55, 0.25);
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-body);
  background-color: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
}

::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: var(--color-bg);
}
::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--color-primary);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
}
.btn:hover {
  transform: translateY(-2px);
}
.btn-primary {
  background-color: var(--color-primary);
  color: #000000;
  box-shadow: 0 4px 14px var(--color-glow);
}
.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: 0 6px 20px var(--color-glow);
}
.btn-secondary {
  background-color: #ffffff;
  color: #000000;
}
.btn-outline {
  border: 1px solid var(--color-border);
  color: #ffffff;
  background: rgba(255, 255, 255, 0.03);
}
.btn-outline:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: rgba(212, 175, 55, 0.08);
}
.btn-ghost {
  color: var(--color-text-muted);
  background: transparent;
}
.btn-ghost:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

.card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all 0.3s ease;
}
.card-hover:hover {
  transform: translateY(-4px);
  border-color: rgba(212, 175, 55, 0.4);
  box-shadow: 0 16px 32px -8px var(--color-glow);
}

.glass-panel {
  background: rgba(18, 18, 23, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}

.badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
}

.gradient-text {
  background: linear-gradient(135deg, #ffffff 30%, var(--color-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-container {
  max-width: 80rem;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}
"""
        return template.replace("__PRIMARY__", primary).replace("__ACCENT__", accent).replace("__BG_MAIN__", bg_main).replace("__BG_SURFACE__", bg_surface).replace("__TEXT_MAIN__", text_main).replace("__TEXT_MUTED__", text_muted)

    def _get_fallback_mock_data(self, domain: str, app_name: str) -> str:
        images = VERIFIED_IMAGES_BY_CATEGORY.get(domain, VERIFIED_IMAGES_BY_CATEGORY["luxury_cars"])
        img1 = images[0] if len(images) > 0 else "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
        img2 = images[1] if len(images) > 1 else img1
        img3 = images[2] if len(images) > 2 else img1
        img4 = images[3] if len(images) > 3 else img1
        
        avatars = VERIFIED_IMAGES_BY_CATEGORY["avatars"]
        
        template = """export const featuredItems = [
  {
    id: "item-1",
    name: "Apex Venom Superleggera",
    model: "Apex Venom",
    title: "Apex Venom Superleggera",
    category: "Hypercar",
    price: 485000,
    rating: 4.9,
    image: "__IMG1__",
    description: "The pinnacle of precision engineering, featuring a bespoke twin-turbo powertrain and adaptive active aerodynamics.",
    features: ["Carbon-Ceramic Braking", "Bespoke Italian Leather", "Adaptive Track Suspension", "Track Telemetry System"],
    specs: { horsepower: "1,150 HP", acceleration: "0-60 in 2.1s", topSpeed: "238 mph", transmission: "8-Speed Dual-Clutch" },
    badge: "Flagship"
  },
  {
    id: "item-2",
    name: "Apex Phantom Grand Tourer",
    model: "Apex Phantom",
    title: "Apex Phantom Grand Tourer",
    category: "Grand Tourer",
    price: 340000,
    rating: 4.8,
    image: "__IMG2__",
    description: "An effortless fusion of whisper-quiet luxury and commanding V8 thrust crafted for cross-continental touring.",
    features: ["Starlight Headliner", "Executive Rear Recline", "Acoustic Double-Glazing", "Burmester 4D Audio"],
    specs: { horsepower: "780 HP", acceleration: "0-60 in 3.2s", topSpeed: "205 mph", transmission: "All-Wheel Drive" },
    badge: "Ultra Luxury"
  },
  {
    id: "item-3",
    name: "Apex Ghost Stealth Edition",
    model: "Apex Ghost",
    title: "Apex Ghost Stealth Edition",
    category: "Track Series",
    price: 395000,
    rating: 5.0,
    image: "__IMG3__",
    description: "Matte carbon exterior with race-derived downforce tunnels and visceral exhaust harmonics.",
    features: ["Forged Magnesium Wheels", "Full Carbon Tub", "Titanium Inconel Exhaust", "Racing Harness Mounts"],
    specs: { horsepower: "920 HP", acceleration: "0-60 in 2.6s", topSpeed: "225 mph", transmission: "Sequential Paddle" },
    badge: "Limited Edition"
  },
  {
    id: "item-4",
    name: "Apex Spectre Electric Concept",
    model: "Apex Spectre",
    title: "Apex Spectre Electric Concept",
    category: "Hyper EV",
    price: 420000,
    rating: 4.9,
    image: "__IMG4__",
    description: "Next-generation solid-state electric architecture delivering instantaneous vectoring and zero emissions.",
    features: ["Quad Independent Motors", "800V Ultra-Fast Charging", "Augmented Reality HUD", "Active Aero Flaps"],
    specs: { horsepower: "1,400 HP", acceleration: "0-60 in 1.9s", topSpeed: "245 mph", transmission: "Direct Drive" },
    badge: "Electric Future"
  }
];

export const cars = featuredItems;
export const featuredCars = featuredItems;
export const menuItems = featuredItems;
export const products = featuredItems;
export const services = featuredItems;

export const categories = [
  { id: "all", name: "All Collections", icon: "Sparkles" },
  { id: "hypercar", name: "Hypercars", icon: "Zap" },
  { id: "gt", name: "Grand Tourers", icon: "Shield" },
  { id: "track", name: "Track Edition", icon: "TrendingUp" },
  { id: "electric", name: "Electric Hyper", icon: "Star" }
];
export const carCategories = categories;

export const testimonials = [
  {
    id: "rev-1",
    name: "Marcus Vance",
    role: "Collector & Private Client",
    comment: "The buying and customization experience was sublime. The craftsmanship in the cabin exceeds anything out of Stuttgart or Maranello.",
    rating: 5,
    avatar: "__AVATAR1__"
  },
  {
    id: "rev-2",
    name: "Elena Rostova",
    role: "Automotive Journalist",
    comment: "Astounding performance with daily drivability. A rare masterclass in contemporary automotive art.",
    rating: 5,
    avatar: "__AVATAR2__"
  },
  {
    id: "rev-3",
    name: "David Sterling",
    role: "Track Enthusiast",
    comment: "On track day at Silverstone, the Apex Ghost delivered unflinching stability and lap times that humbled factory cup cars.",
    rating: 5,
    avatar: "__AVATAR3__"
  }
];

export const companyStats = [
  { label: "Horsepower Unleashed", value: "1,400+", icon: "Zap" },
  { label: "Global Clients", value: "350+", icon: "Shield" },
  { label: "Bespoke Finishes", value: "120+", icon: "Sparkles" },
  { label: "Top Track Speed", value: "245 MPH", icon: "TrendingUp" }
];

export const faqItems = [
  {
    question: "How do I schedule an exclusive private viewing?",
    answer: "You can book directly via our Experience page or contact our concierge team. Every consultation includes a private showroom session and track briefing."
  },
  {
    question: "What customization options are offered through the bespoke atelier?",
    answer: "Clients can tailor exterior carbon weaves, custom paint-to-sample finishes, hand-stitched hides, and personalized sill plaques."
  },
  {
    question: "What warranty and service coverage is provided?",
    answer: "Every model includes our comprehensive 5-year bumper-to-bumper warranty with 24/7 global flying doctor mechanical concierge."
  }
];
"""
        return template.replace("__IMG1__", img1).replace("__IMG2__", img2).replace("__IMG3__", img3).replace("__IMG4__", img4).replace("__AVATAR1__", avatars[0]).replace("__AVATAR2__", avatars[1]).replace("__AVATAR3__", avatars[2])

    def _get_fallback_app_context(self) -> str:
        return """import React, { createContext, useContext, useState, useEffect } from 'react';
import { featuredItems, categories } from '../data/mockData';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('app_theme') || 'dark';
    }
    return 'dark';
  });

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    localStorage.setItem('app_theme', nextTheme);
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const [savedItems, setSavedItems] = useState(() => {
    try {
      const val = localStorage.getItem('app_saved_items');
      return val ? JSON.parse(val) : [];
    } catch {
      return [];
    }
  });

  const toggleSavedItem = (id) => {
    setSavedItems((prev) => {
      const updated = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
      localStorage.setItem('app_saved_items', JSON.stringify(updated));
      return updated;
    });
  };

  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  const addToCart = (item) => {
    setCart((prev) => [...prev, item]);
    addNotification(`Added ${item?.name || item?.model || 'Item'} to your reservation bag`, 'success');
  };

  const removeFromCart = (id) => {
    setCart((prev) => prev.filter((item) => item.id !== id));
  };

  const [selectedItem, setSelectedItem] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [notifications, setNotifications] = useState([]);

  const addNotification = (message, type = 'info') => {
    const id = Date.now();
    setNotifications((prev) => [...prev, { id, message, type }]);
    setTimeout(() => removeNotification(id), 4000);
  };

  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const value = {
    theme,
    toggleTheme,
    activeCategory,
    setActiveCategory,
    searchQuery,
    setSearchQuery,
    savedItems,
    toggleSavedItem,
    cart,
    addToCart,
    removeFromCart,
    cartCount: cart.length,
    isCartOpen,
    setIsCartOpen,
    selectedItem,
    setSelectedItem,
    isModalOpen,
    setIsModalOpen,
    notifications,
    addNotification,
    removeNotification,
    items: featuredItems,
    cars: featuredItems,
    featuredCars: featuredItems,
    menuItems: featuredItems,
    categories
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export default AppContext;
"""

    def _get_fallback_button_jsx(self) -> str:
        return """import React from 'react';

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconPosition = 'right',
  loading = false,
  className = '',
  disabled = false,
  ...props
}) => {
  const base = "btn select-none";
  
  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    outline: "btn-outline",
    ghost: "btn-ghost",
    danger: "bg-red-600 hover:bg-red-700 text-white shadow-lg"
  };

  const sizes = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-5 py-2.5 text-sm",
    lg: "px-7 py-3.5 text-base"
  };

  return (
    <button
      className={`${base} ${variants[variant] || variants.primary} ${sizes[size] || sizes.md} ${className} ${disabled || loading ? 'opacity-50 cursor-not-allowed pointer-events-none' : ''}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="w-4 h-4 mr-2 border-2 border-current border-t-transparent rounded-full animate-spin" />
      ) : Icon && iconPosition === 'left' ? (
        <Icon className="w-4 h-4 mr-2" />
      ) : null}
      <span>{children}</span>
      {!loading && Icon && iconPosition === 'right' && (
        <Icon className="w-4 h-4 ml-2" />
      )}
    </button>
  );
};

export default Button;
"""

    def _get_fallback_card_jsx(self) -> str:
        return """import React from 'react';

export const Card = ({ children, className = '', hover = true, ...props }) => (
  <div className={`card ${hover ? 'card-hover' : ''} ${className}`} {...props}>
    {children}
  </div>
);

export const CardHeader = ({ children, className = '', ...props }) => (
  <div className={`p-6 border-b border-slate-800 ${className}`} {...props}>
    {children}
  </div>
);

export const CardBody = ({ children, className = '', ...props }) => (
  <div className={`p-6 ${className}`} {...props}>
    {children}
  </div>
);

export const CardFooter = ({ children, className = '', ...props }) => (
  <div className={`p-6 border-t border-slate-800 ${className}`} {...props}>
    {children}
  </div>
);

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

export { CardHeader, CardBody, CardFooter };
export default Card;
"""

    def _get_fallback_badge_jsx(self) -> str:
        return """import React from 'react';

export const Badge = ({ children, variant = 'neutral', className = '', ...props }) => {
  const variants = {
    primary: "bg-amber-400/10 text-amber-400 border border-amber-400/30",
    accent: "bg-indigo-500/10 text-indigo-400 border border-indigo-500/30",
    gold: "bg-amber-500 text-black font-extrabold",
    success: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30",
    warning: "bg-orange-500/10 text-orange-400 border border-orange-500/30",
    neutral: "bg-slate-800 text-slate-300 border border-slate-700"
  };

  return (
    <span className={`badge ${variants[variant] || variants.neutral} ${className}`} {...props}>
      {children}
    </span>
  );
};

export default Badge;
"""

    def _get_fallback_modal_jsx(self) -> str:
        return """import React, { useEffect } from 'react';
import { X } from 'lucide-react';

export const Modal = ({ isOpen, onClose, title, children, maxWidth = 'max-w-2xl' }) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.body.style.overflow = 'unset';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div
        className="fixed inset-0"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className={`relative w-full ${maxWidth} glass-panel border border-slate-700 p-6 shadow-2xl z-10 animate-in fade-in zoom-in-95 duration-200`}>
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
          <h3 className="text-xl font-bold text-white">{title}</h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="max-h-[75vh] overflow-y-auto pr-2">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
"""

    def _get_fallback_section_title_jsx(self) -> str:
        return """import React from 'react';
import Badge from './Badge';

export const SectionTitle = ({
  badge,
  title,
  subtitle,
  align = 'center',
  className = ''
}) => {
  const alignment = align === 'left' ? 'text-left items-start' : 'text-center items-center';

  return (
    <div className={`flex flex-col ${alignment} mb-12 ${className}`}>
      {badge && <Badge variant="accent" className="mb-3">{badge}</Badge>}
      <h2 className="text-3xl md:text-5xl font-extrabold tracking-tight mb-4 gradient-text">
        {title}
      </h2>
      {subtitle && (
        <p className="text-slate-400 text-base md:text-lg max-w-2xl leading-relaxed">
          {subtitle}
        </p>
      )}
    </div>
  );
};

export default SectionTitle;
"""

    def _get_fallback_navbar_jsx(self, app_name: str, pages: List[Any]) -> str:
        template = """import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { Menu, X, Sun, Moon, Sparkles, ArrowRight } from 'lucide-react';
import Button from './ui/Button';
import { useApp } from '../context/AppContext';

export const Navbar = () => {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const { theme, toggleTheme } = useApp();

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/explore', label: 'Models & Gallery' },
    { path: '/about', label: 'About' },
    { path: '/experience', label: 'Experience' },
    { path: '/contact', label: 'Contact' }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-slate-800/80">
      <div className="section-container">
        <div className="flex items-center justify-between h-20">
          <Link to="/" className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-xl bg-amber-400/10 border border-amber-400/30 flex items-center justify-center text-amber-400 shadow-md">
              <Sparkles className="w-5 h-5" />
            </div>
            <span className="text-xl font-extrabold tracking-tight text-white font-serif">
              __APP_NAME__
            </span>
          </Link>

          <nav className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `text-sm font-semibold tracking-wide transition-colors ${
                    isActive ? 'text-amber-400' : 'text-slate-300 hover:text-white'
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>

          <div className="hidden md:flex items-center space-x-4">
            <button
              onClick={toggleTheme}
              className="p-2.5 rounded-xl border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
            </button>
            <Link to="/contact">
              <Button variant="primary" size="sm" icon={ArrowRight}>
                Inquire
              </Button>
            </Link>
          </div>

          <div className="flex md:hidden items-center space-x-2">
            <button
              onClick={toggleTheme}
              className="p-2 text-slate-400 hover:text-white"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
            </button>
            <button
              onClick={() => setIsMobileOpen(!isMobileOpen)}
              className="p-2 text-slate-400 hover:text-white"
              aria-label="Toggle menu"
            >
              {isMobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {isMobileOpen && (
        <div className="md:hidden glass-panel border-t border-slate-800 px-6 py-6 space-y-4">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setIsMobileOpen(false)}
              className="block text-base font-semibold text-slate-300 hover:text-amber-400 py-1"
            >
              {link.label}
            </Link>
          ))}
          <div className="pt-4 border-t border-slate-800">
            <Link to="/contact" onClick={() => setIsMobileOpen(false)}>
              <Button variant="primary" className="w-full">
                Book Consultation
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
"""
        return template.replace("__APP_NAME__", app_name)

    def _get_fallback_footer_jsx(self, app_name: str, pages: List[Any]) -> str:
        template = """import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Mail, Send, Twitter, Instagram, Linkedin, MapPin, Phone } from 'lucide-react';
import Button from './ui/Button';

export const Footer = () => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail('');
    }
  };

  return (
    <footer className="bg-black border-t border-slate-800/80 pt-16 pb-12">
      <div className="section-container">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-amber-400/10 border border-amber-400/30 flex items-center justify-center text-amber-400">
                <Sparkles className="w-4 h-4" />
              </div>
              <span className="text-xl font-bold text-white font-serif">__APP_NAME__</span>
            </div>
            <p className="text-slate-400 text-sm max-w-sm leading-relaxed">
              Committed to uncompromising standards, bespoke craftsmanship, and indelible experiences for discerning clientele worldwide.
            </p>
            <div className="flex space-x-4 pt-2">
              <a href="#twitter" className="w-9 h-9 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-400 hover:text-white hover:border-amber-400/50 transition-colors" aria-label="Twitter">
                <Twitter className="w-4 h-4" />
              </a>
              <a href="#instagram" className="w-9 h-9 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-400 hover:text-white hover:border-amber-400/50 transition-colors" aria-label="Instagram">
                <Instagram className="w-4 h-4" />
              </a>
              <a href="#linkedin" className="w-9 h-9 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-400 hover:text-white hover:border-amber-400/50 transition-colors" aria-label="LinkedIn">
                <Linkedin className="w-4 h-4" />
              </a>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Navigation</h4>
            <ul className="space-y-2.5 text-sm text-slate-400">
              <li><Link to="/" className="hover:text-amber-400 transition-colors">Home Showcase</Link></li>
              <li><Link to="/explore" className="hover:text-amber-400 transition-colors">Catalog & Specs</Link></li>
              <li><Link to="/about" className="hover:text-amber-400 transition-colors">Heritage & Atelier</Link></li>
              <li><Link to="/experience" className="hover:text-amber-400 transition-colors">Private Sessions</Link></li>
              <li><Link to="/contact" className="hover:text-amber-400 transition-colors">Inquire & Concierge</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Private Gazette</h4>
            <p className="text-slate-400 text-sm mb-4">
              Receive private invitations to private viewings and limited edition drops.
            </p>
            {subscribed ? (
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400 text-xs font-semibold">
                ✓ Thank you. You are on the private register.
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-2">
                <div className="relative">
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter executive email..."
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
                  />
                </div>
                <Button type="submit" variant="primary" size="sm" className="w-full" icon={Send}>
                  Subscribe
                </Button>
              </form>
            )}
          </div>
        </div>

        <div className="pt-8 border-t border-slate-900 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500 space-y-4 sm:space-y-0">
          <p>© {new Date().getFullYear()} __APP_NAME__. All rights reserved.</p>
          <div className="flex space-x-6">
            <a href="#privacy" className="hover:text-slate-400">Privacy Policy</a>
            <a href="#terms" className="hover:text-slate-400">Terms of Service</a>
            <a href="#security" className="hover:text-slate-400">Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
"""
        return template.replace("__APP_NAME__", app_name)

    def _get_fallback_main_layout_jsx(self) -> str:
        return """import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useApp } from '../context/AppContext';

export const MainLayout = ({ children }) => {
  const { notifications, removeNotification } = useApp();

  return (
    <div className="min-h-screen flex flex-col bg-black text-white">
      <Navbar />

      <div className="fixed bottom-6 right-6 z-50 flex flex-col space-y-3 pointer-events-none">
        {notifications.map((n) => (
          <div
            key={n.id}
            onClick={() => removeNotification(n.id)}
            className={`pointer-events-auto p-4 rounded-xl border text-sm font-semibold shadow-2xl backdrop-blur-md cursor-pointer transition-all animate-in slide-in-from-bottom-5 ${
              n.type === 'success'
                ? 'bg-emerald-950/90 text-emerald-300 border-emerald-500/40'
                : 'bg-slate-900/90 text-white border-amber-400/40'
            }`}
          >
            {n.message}
          </div>
        ))}
      </div>

      <main className="flex-grow pt-20">
        {children}
      </main>

      <Footer />
    </div>
  );
};

export default MainLayout;
"""

    def _get_fallback_not_found_jsx(self) -> str:
        return """import React from 'react';
import { Link } from 'react-router-dom';
import { Home, AlertCircle } from 'lucide-react';
import Button from '../components/ui/Button';

export default function NotFoundPage() {
  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-16">
      <div className="text-center max-w-md mx-auto">
        <div className="w-16 h-16 bg-red-500/10 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <AlertCircle size={36} />
        </div>
        <h1 className="text-5xl font-extrabold text-white mb-2">404</h1>
        <p className="text-lg font-medium text-slate-400 mb-8">
          The requested page or exhibition does not exist or has been relocated.
        </p>
        <Link to="/">
          <Button variant="primary" icon={Home}>
            Return to Home
          </Button>
        </Link>
      </div>
    </div>
  );
}

export { NotFoundPage };
"""

    def _get_fallback_main_jsx(self) -> str:
        return """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AppProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </AppProvider>
  </React.StrictMode>
);
"""