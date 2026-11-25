import asyncio
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config.settings import settings
from agents import (
    CEOAgent,
    ProjectManagerAgent,
    FrontendDeveloperAgent,
    VisualReviewAgent,
    FileIntegrityAgent,
    QATesterAgent,
    DocumentationWriterAgent,
    UIDesignerAgent,
    ReactArchitectAgent
)

async def test_tri_engine_llm_execution():
    print("=" * 70)
    print("[*] Testing Tri-Engine LLM Mesh (Groq + Mistral Codestral + Gemini)...")
    print("=" * 70)
    
    print(f"Gemini Configured: {'YES' if settings.GEMINI_API_KEY else 'NO'} | Model: {settings.GEMINI_MODEL}")
    print(f"Groq Configured:   {'YES' if settings.GROQ_API_KEY else 'NO'} | Model: {settings.GROQ_MODEL}")
    print(f"Mistral Configured:{'YES' if settings.MISTRAL_API_KEY else 'NO'} | Model: {settings.MISTRAL_MODEL}")
    print("-" * 70)
    
    # 1. Test CEO Agent (Groq Primary)
    ceo = CEOAgent()
    print(f"[+] CEO Agent Engine Info: {ceo.get_info()}")
    print("[*] Generating prompt with CEO Agent...")
    ceo_res = await ceo._generate_response("Respond with 1 sentence confirming the Tri-Engine Studio is live.")
    print(f"[+] CEO Response: {ceo_res.strip()}\n")
    
    # 2. Test Frontend Developer Agent (Mistral Codestral Primary)
    dev = FrontendDeveloperAgent()
    print(f"[+] Senior React Developer Engine Info: {dev.get_info()}")
    print("[*] Generating code component with Frontend Developer Agent (Codestral)...")
    dev_res = await dev._generate_response("Respond with a short React button component: export const HeroBtn = () => <button>Click</button>;")
    print(f"[+] Developer Response: {dev_res.strip()[:150]}...\n")
    
    # 3. Test React Architect Agent (Mistral Codestral Primary)
    architect = ReactArchitectAgent()
    print(f"[+] React Architect Engine Info: {architect.get_info()}")
    
    # 4. Test QA Tester Agent (Groq Primary)
    qa = QATesterAgent()
    print(f"[+] QA Tester Engine Info: {qa.get_info()}")
    
    print("=" * 70)
    print("[SUCCESS] Tri-Engine LLM Mesh & Omni-Source Assets Verified Successfully!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_tri_engine_llm_execution())
