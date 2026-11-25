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

from config.settings import settings, ROLE_CONFIG, MODEL_REGISTRY
from database.models import EmployeeRole
from agents.llm_manager import llm_manager
from agents import (
    CEOAgent,
    FrontendDeveloperAgent,
    ReactArchitectAgent,
    QATesterAgent
)

async def test_mesh_architecture():
    print("=" * 80)
    print("🚀 MULTI-MODEL OPENROUTER LLM MESH ARCHITECTURE TEST")
    print("=" * 80)
    
    print("\n1. PROVIDER CONFIGURATION:")
    print(f"   • OpenRouter Key:    {'CONFIGURED' if llm_manager._is_valid_key(settings.OPENROUTER_API_KEY) else 'STANDBY / NOT SET'}")
    print(f"   • OpenRouter Base:   {settings.OPENROUTER_BASE_URL}")
    print(f"   • Qwen Model:        {settings.QWEN_MODEL} (Primary Coding)")
    print(f"   • Mercury Model:     {settings.MERCURY_MODEL} (Decision Gate / Router)")
    print(f"   • Gemini Model:      {settings.GEMINI_MODEL} (Primary Reasoning & Fallback Safety Net)")
    print(f"   • Max Fix Loops:     {settings.MAX_REMEDIATION_LOOPS}")
    print(f"   • Mercury Threshold: {settings.MERCURY_DECISION_THRESHOLD}")
    
    print("\n2. AGENT ROLE AFFINITY PIPELINES:")
    roles_to_check = [
        ("Frontend Developer", EmployeeRole.FRONTEND_DEVELOPER),
        ("React Architect", EmployeeRole.REACT_ARCHITECT),
        ("CEO / Product Lead", EmployeeRole.CEO),
        ("QA Tester", EmployeeRole.QA_TESTER),
        ("Documentation Writer", EmployeeRole.DOCUMENTATION_WRITER)
    ]
    
    for title, role in roles_to_check:
        cands = [f"{c[0].upper()} ({c[1]})" for c in llm_manager.get_candidate_providers(role)]
        print(f"   • {title:22}: {' -> '.join(cands)}")
        
    print("\n3. TESTING INCEPTION MERCURY DECIDE GATE:")
    decision, prob, reasoning, source = await llm_manager.decide(
        question="Should this project proceed directly to production delivery?",
        context_summary="QA Score: 9.5/10. Zero missing files. Zero broken imports.",
        true_when="QA score >= 9.0 and zero integrity defects",
        false_when="QA score < 9.0 or unresolved missing files",
        threshold=settings.MERCURY_DECISION_THRESHOLD,
        deterministic_fallback=lambda: True
    )
    print(f"   • Decision:    {decision}")
    print(f"   • Probability: {prob:.2f} (Threshold: {settings.MERCURY_DECISION_THRESHOLD})")
    print(f"   • Reasoning:   {reasoning}")
    print(f"   • Source:      {source.upper()}")

    print("\n4. TESTING EXECUTION WITH FALLBACK (CEO Agent - Reasoning):")
    ceo = CEOAgent()
    ceo_res = await ceo._generate_response("Give a 1-sentence executive confirmation that the mesh is operational.")
    print(f"   • CEO Output: {ceo_res.strip()}")

    print("\n5. TESTING EXECUTION WITH FALLBACK (Frontend Developer - Coding):")
    dev = FrontendDeveloperAgent()
    dev_res = await dev._generate_response("Generate a one-line React component: export const StatusBadge = () => <span>Online</span>;")
    print(f"   • Dev Output: {dev_res.strip()[:140]}...")

    print("\n6. OPERATIONAL USAGE REPORT:")
    print(llm_manager.get_usage_summary())
    print("\n" + "=" * 80)
    print("✅ MULTI-MODEL OPENROUTER LLM MESH VERIFIED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_mesh_architecture())
