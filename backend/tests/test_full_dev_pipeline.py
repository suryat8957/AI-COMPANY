import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import (
    CEOAgent,
    ProjectManagerAgent,
    UIDesignerAgent,
    ReactArchitectAgent,
    FrontendDeveloperAgent
)

async def test_generation():
    print("=== Testing Full Developer Pipeline ===")
    ceo = CEOAgent()
    dev = FrontendDeveloperAgent()

    context = {
        "client_request": "Luxury Electric Hypercar Showcase & Custom Configurator with Dark Mode and Carbon Aesthetics",
        "product_spec": {
            "project_name": "Apex Hypercars",
            "pages": [
                {"name": "Home", "path": "/", "title": "Home"},
                {"name": "Collection", "path": "/collection", "title": "Models"},
                {"name": "About", "path": "/about", "title": "Heritage"},
                {"name": "Pricing", "path": "/pricing", "title": "Reserve"},
                {"name": "Contact", "path": "/contact", "title": "Concierge"}
            ]
        },
        "design_spec": {
            "archetype": "Luxury Editorial & High-Fashion / Cinematic Automotive",
            "primary_color": "#e5e5e5",
            "typography": {
                "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
            }
        }
    }

    print("[*] Generating all files with FrontendDeveloperAgent...")
    result = await dev._create_all_files({"type": "develop_react_app"}, context)
    files = result.get("files", {})
    print(f"[+] Successfully generated {len(files)} total files!")
    for name in sorted(files.keys()):
        print(f"  - {name} ({len(files[name])} chars)")

    assert len(files) >= 15, "Expected at least 15 files generated"
    assert "src/App.jsx" in files, "src/App.jsx missing"
    assert "src/main.jsx" in files, "src/main.jsx missing"
    assert "src/pages/HomePage.jsx" in files, "src/pages/HomePage.jsx missing"
    assert "src/components/Navbar.jsx" in files, "src/components/Navbar.jsx missing"
    assert "src/components/Footer.jsx" in files, "src/components/Footer.jsx missing"
    assert "src/context/AppContext.jsx" in files, "src/context/AppContext.jsx missing"
    assert "src/data/mockData.js" in files, "src/data/mockData.js missing"
    print("\n[SUCCESS] Pipeline executed cleanly with 0 timeouts and all files produced!")

if __name__ == "__main__":
    asyncio.run(test_generation())
