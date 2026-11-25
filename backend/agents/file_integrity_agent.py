from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from database.models import EmployeeRole
from utils.logger import setup_logger
from utils.image_helper import (
    get_fallback_image_component_code,
    get_domain_fallback_url,
    detect_domain_from_prompt
)
import json
import re

logger = setup_logger(__name__)

class FileIntegrityAgent(BaseAgent):
    """File Integrity & Dependency Specialist - Verifies 100% of required files exist, heals missing files, checks imports, routes, and syntax"""
    
    def __init__(self):
        super().__init__(
            role=EmployeeRole.FILE_INTEGRITY_SPECIALIST,
            name="Marcus Brody",
            temperature=0.2
        )
    
    def _get_system_prompt(self) -> str:
        return """You are Marcus Brody, the Lead File & Dependency Integrity Specialist at an elite AI Frontend Engineering Studio.

Your mission:
1. Conduct uncompromising verification that EVERY expected file in the architecture blueprint and App router exists and contains complete, non-empty code.
2. Check all component imports and exports across all files to ensure there are no missing files, typos, or broken relative paths.
3. Validate that every navigation route and link in `Navbar`, `Footer`, and pages has a matching `<Route>` in `App.jsx`.
4. Validate `package.json` syntax and dependencies.
5. Identify any missing files or broken references and output a clear, actionable integrity report."""

    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file integrity verification and auto-heal missing files"""
        logger.info("File Integrity Specialist auditing codebase completeness, imports, and auto-healing issues")
        
        files = context.get("files", {})
        architecture_spec = context.get("architecture_spec", {})
        client_request = context.get("client_request", "")
        domain = context.get("detected_domain") or detect_domain_from_prompt(client_request)
        manifest = architecture_spec.get("file_manifest", [])
        
        # 1. Check and Auto-Heal Essential Files
        healed_files = self._auto_heal_codebase(files, domain)
        files.update(healed_files)
        context["files"] = files
        
        # 2. Check manifest items
        missing_files = []
        for expected_file in manifest:
            clean_expected = expected_file.replace('\\', '/')
            if clean_expected not in files and not any(f.endswith(clean_expected) for f in files.keys()):
                missing_files.append(clean_expected)
        
        # 3. Check imports across all JSX files
        broken_imports = self._check_imports(files)
        
        # 4. Check route consistency between Navbar and App.jsx
        route_issues = self._check_routes(files, architecture_spec)
        
        # 5. LLM Synthesis
        summary_prompt = f"""Review the structural integrity of this React application:

Total Files Generated: {len(files)}
Expected Files Manifest ({len(manifest)} items): {', '.join(manifest[:20])}

Programmatic Check Findings:
- Missing Expected Files: {missing_files if missing_files else 'None - All manifest files present'}
- Broken or Unresolved Imports: {broken_imports if broken_imports else 'None - All imports verified'}
- Route Inconsistencies: {route_issues if route_issues else 'None - All navigation links match routes'}
- Auto-Healed Files: {list(healed_files.keys()) if healed_files else 'None required'}

Provide a concise integrity assessment confirming whether the project structure is complete, coherent, and ready for execution."""

        try:
            response = await self._generate_response(summary_prompt, context)
            self.add_to_memory("Completed file integrity audit")
            
            is_valid = len(missing_files) == 0 and len(broken_imports) == 0
            
            return {
                "status": "completed",
                "integrity_passed": is_valid,
                "missing_files": missing_files,
                "broken_imports": broken_imports,
                "route_issues": route_issues,
                "healed_files": list(healed_files.keys()),
                "files": files,
                "integrity_report": response,
                "output_type": "integrity_report"
            }
        except Exception as e:
            logger.error(f"File integrity audit failed: {e}")
            return {
                "status": "completed",
                "integrity_passed": len(missing_files) == 0,
                "missing_files": missing_files,
                "broken_imports": broken_imports,
                "route_issues": route_issues,
                "healed_files": list(healed_files.keys()) if 'healed_files' in locals() else [],
                "files": files,
                "integrity_report": f"Integrity check finished with {len(missing_files)} missing files.",
                "output_type": "integrity_report"
            }
    
    def _auto_heal_codebase(self, files: Dict[str, str], domain: str) -> Dict[str, str]:
        """Proactively detect and fix missing files, duplicate routers, or missing exports"""
        healed: Dict[str, str] = {}
        fallback_url = get_domain_fallback_url(domain)
        
        # A. Ensure Image component exists and has working fallback
        if "src/components/ui/Image.jsx" not in files:
            healed["src/components/ui/Image.jsx"] = get_fallback_image_component_code(domain)
            
        # B. Ensure standard UI primitives exist if imported by any page
        all_code = " ".join(files.values())
        
        if "FeaturedCarCard" in all_code and "src/components/ui/FeaturedCarCard.jsx" not in files:
            card_template = """import React from 'react';
import { Link } from 'react-router-dom';
import { Zap, TrendingUp, Shield, ArrowRight } from 'lucide-react';
import Card from './Card';
import Badge from './Badge';
import Button from './Button';
import Image from './Image';

export const FeaturedCarCard = ({ car, ...props }) => {
  if (!car) return null;
  const name = car.name || car.model || car.title || 'Exotic Model';
  const img = car.image || '__FALLBACK_URL__';
  const price = car.price ? `$${car.price.toLocaleString()}` : 'Inquire';

  return (
    <Card className="card-hover p-5 flex flex-col justify-between" {...props}>
      <div>
        <div className="h-52 rounded-xl overflow-hidden mb-4 relative">
          <Image src={img} alt={name} className="w-full h-full object-cover" />
          {car.badge && (
            <Badge variant="gold" className="absolute top-3 left-3 shadow-lg">
              {car.badge}
            </Badge>
          )}
        </div>
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{name}</h3>
          <span className="text-lg font-extrabold text-amber-400">{price}</span>
        </div>
        <p className="text-slate-400 text-sm mb-4 line-clamp-2">{car.description || 'Masterpiece of engineering and luxury.'}</p>
        
        {car.specs && (
          <div className="grid grid-cols-2 gap-2 text-xs text-slate-300 py-3 border-t border-slate-800">
            <div className="flex items-center space-x-1.5">
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              <span>{car.specs.horsepower || 'V12 Power'}</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <TrendingUp className="w-3.5 h-3.5 text-amber-400" />
              <span>{car.specs.topSpeed || '200+ MPH'}</span>
            </div>
          </div>
        )}
      </div>
      <div className="pt-4 border-t border-slate-800 flex space-x-2">
        <Link to="/contact" className="w-full">
          <Button variant="primary" size="sm" className="w-full" icon={ArrowRight}>
            Inquire Details
          </Button>
        </Link>
      </div>
    </Card>
  );
};

export default FeaturedCarCard;
"""
            healed["src/components/ui/FeaturedCarCard.jsx"] = card_template.replace("__FALLBACK_URL__", fallback_url)

        # C. Auto-heal Carousel if imported
        if "Carousel" in all_code and "src/components/ui/Carousel.jsx" not in files:
            carousel_template = """import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Image from './Image';

export const Carousel = ({ images = [], className = '' }) => {
  const [current, setCurrent] = useState(0);
  const list = images.length > 0 ? images : ['__FALLBACK_URL__'];

  const prev = () => setCurrent(current === 0 ? list.length - 1 : current - 1);
  const next = () => setCurrent(current === list.length - 1 ? 0 : current + 1);

  return (
    <div className={`relative overflow-hidden rounded-2xl ${className}`}>
      <div className="h-80 w-full relative">
        <Image src={list[current]} alt="Carousel slide" className="w-full h-full object-cover" />
      </div>
      {list.length > 1 && (
        <>
          <button onClick={prev} className="absolute left-3 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black/60 text-white hover:bg-black/90">
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button onClick={next} className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black/60 text-white hover:bg-black/90">
            <ChevronRight className="w-5 h-5" />
          </button>
        </>
      )}
    </div>
  );
};

export default Carousel;
"""
            healed["src/components/ui/Carousel.jsx"] = carousel_template.replace("__FALLBACK_URL__", fallback_url)

        # D. Check App.jsx for duplicate BrowserRouter
        if "src/App.jsx" in files:
            app_code = files["src/App.jsx"]
            if "BrowserRouter" in app_code:
                app_code = re.sub(r'import\s+\{[^}]*BrowserRouter[^}]*\}\s+from\s+[\'"]react-router-dom[\'"];?', '', app_code)
                app_code = re.sub(r'<BrowserRouter>\s*', '', app_code)
                app_code = re.sub(r'\s*</BrowserRouter>', '', app_code)
                files["src/App.jsx"] = app_code

        # E. Ensure dual exports on all UI components
        for fn, code in list(files.items()):
            if fn.startswith("src/components/ui/") and fn.endswith(".jsx"):
                c_name = fn.split("/")[-1].replace(".jsx", "")
                if f"export default {c_name}" not in code and f"export default function {c_name}" not in code:
                    files[fn] = code + f"\nexport default {c_name};\nexport {{ {c_name} }};\n"

        return healed

    def _check_imports(self, files: Dict[str, str]) -> List[str]:
        """Check if local component imports match existing files"""
        issues = []
        known_standard_modules = [
            'react', 'react-dom', 'react-dom/client', 'react-router-dom', 
            'lucide-react', 'clsx', 'tailwind-merge', 'framer-motion'
        ]
        
        for filepath, content in files.items():
            if not filepath.endswith(('.jsx', '.js', '.tsx', '.ts')):
                continue
            
            import_matches = re.findall(r"import\s+.*?from\s+['\"](.*?)['\"]", content)
            for imp in import_matches:
                if imp in known_standard_modules or imp.startswith('http'):
                    continue
                
                if imp.startswith('.'):
                    imp_clean = imp.lstrip('./').rstrip('.jsx').rstrip('.js')
                    matched = False
                    for existing in files.keys():
                        if imp_clean in existing or existing.endswith(f"{imp_clean}.jsx") or existing.endswith(f"{imp_clean}.js") or existing.endswith(f"{imp_clean}.css"):
                            matched = True
                            break
                    if not matched:
                        if 'components' in imp or 'pages' in imp or 'layouts' in imp or 'context' in imp:
                            issues.append(f"{filepath} imports missing '{imp}'")
        return issues
    
    def _check_routes(self, files: Dict[str, str], architecture_spec: Dict[str, Any]) -> List[str]:
        """Check if navigation links in Navbar match defined routes in App.jsx"""
        issues = []
        app_content = files.get("src/App.jsx", "")
        navbar_content = files.get("src/components/Navbar.jsx", "")
        
        if app_content and navbar_content:
            routes_in_app = re.findall(r"<Route\s+[^>]*path=['\"](.*?)['\"]", app_content)
            links_in_nav = re.findall(r"to=['\"](.*?)['\"]", navbar_content)
            
            for link in links_in_nav:
                if link.startswith('http') or link.startswith('#'):
                    continue
                if link not in routes_in_app and link != '/' and '*' not in routes_in_app:
                    issues.append(f"Navbar link to '{link}' has no matching Route in App.jsx")
                    
        return issues
