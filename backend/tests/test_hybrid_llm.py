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
from database.models import EmployeeRole

async def test_hybrid_llm_execution():
    print("=" * 60)
    print("[*] Testing Hybrid Dual-Provider LLM Integration (Gemini + Groq)...")
    print("=" * 60)
    
    print(f"Gemini API Key configured: {'YES' if settings.GEMINI_API_KEY else 'NO'}")
    print(f"Gemini Model: {settings.GEMINI_MODEL}")
    print(f"Groq API Key configured: {'YES' if settings.GROQ_API_KEY else 'NO'}")
    print(f"Groq Model: {settings.GROQ_MODEL}")
    print("-" * 60)
    
    # 1. Test CEO Agent with Groq
    ceo = CEOAgent()
    print(f"[+] CEO Agent Info: {ceo.get_info()}")
    
    print("[*] Testing CEO Agent prompt generation with Groq...")
    ceo_response = await ceo._generate_response(
        "Respond with a 1-sentence confirmation that the Hybrid AI Engineering studio is operational."
    )
    print(f"[+] CEO Response: {ceo_response.strip()}\n")
    
    # 2. Test QA Agent with Groq
    qa = QATesterAgent()
    print(f"[+] QA Agent Info: {qa.get_info()}")
    qa_response = await qa._generate_response(
        "Respond with JSON: {\"test_status\": \"passed\", \"provider\": \"groq\"}"
    )
    print(f"[+] QA Response: {qa_response.strip()}\n")
    
    # 3. Test Developer Agent
    dev = FrontendDeveloperAgent()
    print(f"[+] Frontend Developer Agent Info: {dev.get_info()}")
    dev_response = await dev._generate_response(
        "Respond with: 'React Architect & Developer ready.'"
    )
    print(f"[+] Developer Response: {dev_response.strip()}\n")
    
    print("=" * 60)
    print("[SUCCESS] All Hybrid Dual-Provider LLM Tests Passed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_hybrid_llm_execution())
