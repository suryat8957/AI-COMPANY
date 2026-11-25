import asyncio
import sys
import os

# Set UTF-8 encoding for Windows standard output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents import (
    CEOAgent,
    ProjectManagerAgent,
    UIDesignerAgent,
    ReactArchitectAgent,
    FrontendDeveloperAgent,
    FileIntegrityAgent,
    VisualReviewAgent,
    QATesterAgent,
    DocumentationWriterAgent
)

async def test_agent_pipeline():
    print("[*] Testing React-First Multi-Agent Platform Components...")
    
    # 1. CEO Agent Test
    ceo = CEOAgent()
    print(f"[+] Loaded CEO Agent: {ceo.name} ({ceo.role.value})")
    
    # 2. Project Manager Test
    pm = ProjectManagerAgent()
    print(f"[+] Loaded Project Manager: {pm.name} ({pm.role.value})")
    
    # 3. UI Designer Test
    designer = UIDesignerAgent()
    print(f"[+] Loaded UI/UX Designer: {designer.name} ({designer.role.value})")
    
    # 4. React Architect Test
    architect = ReactArchitectAgent()
    print(f"[+] Loaded React Architect: {architect.name} ({architect.role.value})")
    
    # 5. Senior React Developer Test
    developer = FrontendDeveloperAgent()
    print(f"[+] Loaded Senior React Developer: {developer.name} ({developer.role.value})")
    
    # 6. File Integrity Specialist Test
    integrity = FileIntegrityAgent()
    print(f"[+] Loaded File Integrity Specialist: {integrity.name} ({integrity.role.value})")
    
    # 7. Visual Reviewer Test
    visual = VisualReviewAgent()
    print(f"[+] Loaded Visual Reviewer: {visual.name} ({visual.role.value})")
    
    # 8. QA Tester Test
    qa = QATesterAgent()
    print(f"[+] Loaded QA Tester: {qa.name} ({qa.role.value})")
    
    # 9. Documentation Writer Test
    docs = DocumentationWriterAgent()
    print(f"[+] Loaded Documentation Writer: {docs.name} ({docs.role.value})")
    
    # Test Scaffolding logic fallbacks & generator methods
    pkg = developer._get_fallback_package_json("testsaas")
    vite = developer._get_fallback_vite_config()
    html = developer._get_fallback_index_html("TestSaaS", {"google_fonts": {"embed_url": "https://fonts.googleapis.com"}})
    
    assert "react-router-dom" in pkg, "package.json must include react-router-dom"
    assert "vite" in vite or "@vitejs/plugin-react" in vite, "vite.config.js must include react plugin"
    assert "<div id=\"root\"></div>" in html, "index.html must include root container"
    
    print(f"[+] Developer Scaffolding templates verified.")
    print("[SUCCESS] All React-First Multi-Agent platform components verified successfully!")

if __name__ == "__main__":
    asyncio.run(test_agent_pipeline())
