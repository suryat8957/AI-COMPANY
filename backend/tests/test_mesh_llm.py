import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

from config.settings import settings, ROLE_CONFIG
from database.models import EmployeeRole
from agents.llm_manager import LLMManager
from agents.base_agent import BaseAgent
from agents.frontend_developer_agent import FrontendDeveloperAgent
from workflow.workflow_engine import WorkflowEngine
from workflow.state import WorkflowState

class TestMultiModelMesh(unittest.IsolatedAsyncioTestCase):
    """
    Test suite verifying the Multi-Model OpenRouter LLM Mesh:
    Qwen3.8 27B, Inception Mercury Decide, Google Gemini, and Fallback Cascades.
    """
    
    def setUp(self):
        self.llm_manager = LLMManager()

    def test_01_role_affinity_cascades(self):
        """Test 1: Verify correct role affinity and priority cascades"""
        coding_candidates = [c[0] for c in self.llm_manager.get_candidate_providers(EmployeeRole.FRONTEND_DEVELOPER)]
        review_candidates = [c[0] for c in self.llm_manager.get_candidate_providers(EmployeeRole.CEO)]
        
        # Coding roles should prioritize qwen then gemini
        self.assertEqual(ROLE_CONFIG["frontend_developer"]["primary"], "qwen")
        self.assertIn("gemini", ROLE_CONFIG["frontend_developer"]["fallback"])
        
        # Review roles should prioritize gemini then qwen
        self.assertEqual(ROLE_CONFIG["ceo"]["primary"], "gemini")
        self.assertIn("qwen", ROLE_CONFIG["ceo"]["fallback"])

    async def test_02_qwen_failure_fallback_to_gemini(self):
        """Test 2: Verify that when Qwen fails (e.g. 429), it automatically cascades to Gemini"""
        mock_qwen = AsyncMock()
        mock_qwen.ainvoke.side_effect = Exception("429 Rate limit: ResourceExhausted on free tier")
        
        mock_gemini = AsyncMock()
        mock_gemini_resp = MagicMock()
        mock_gemini_resp.content = "export default function App() { return <div>Gemini Fallback Code</div>; }"
        mock_gemini.ainvoke.return_value = mock_gemini_resp
        
        with patch.object(self.llm_manager, 'get_candidate_providers') as mock_cands:
            mock_cands.return_value = [
                ("qwen", "qwen/qwen3.8-27b:free", mock_qwen),
                ("gemini", "gemini-3.6-flash", mock_gemini)
            ]
            
            initial_fallback_count = self.llm_manager.metrics["fallback_count"]
            response = await self.llm_manager.execute_with_fallback(
                role=EmployeeRole.FRONTEND_DEVELOPER,
                prompt="Generate button component",
                agent_name="Frontend Developer"
            )
            
            self.assertIn("Gemini Fallback Code", response)
            self.assertEqual(self.llm_manager.metrics["fallback_count"], initial_fallback_count + 1)
            self.assertGreaterEqual(mock_qwen.ainvoke.call_count, 1)
            mock_gemini.ainvoke.assert_called_once()

    async def test_03_gemini_failure_fallback_to_qwen(self):
        """Test 3: Verify that when Gemini fails, it cascades to Qwen or backup provider"""
        mock_gemini = AsyncMock()
        mock_gemini.ainvoke.side_effect = Exception("503 Service Unavailable / Model Overloaded")
        
        mock_qwen = AsyncMock()
        mock_qwen_resp = MagicMock()
        mock_qwen_resp.content = "Qwen review: High quality architecture approved."
        mock_qwen.ainvoke.return_value = mock_qwen_resp
        
        with patch.object(self.llm_manager, 'get_candidate_providers') as mock_cands:
            mock_cands.return_value = [
                ("gemini", "gemini-3.6-flash", mock_gemini),
                ("qwen", "qwen/qwen3.8-27b:free", mock_qwen)
            ]
            
            response = await self.llm_manager.execute_with_fallback(
                role=EmployeeRole.CEO,
                prompt="Review product spec",
                agent_name="CEO"
            )
            
            self.assertIn("Qwen review", response)

    async def test_04_mercury_decide_valid_decision(self):
        """Test 4: Verify Mercury Decide structured decision parsing & probability threshold"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "model": "inception/mercury-decide",
            "answers": {
                "decision": {
                    "type": "choice",
                    "choice": "yes",
                    "probabilities": {"yes": 0.94, "no": 0.06},
                    "confidence": 0.94
                }
            }
        }
        
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_resp
            decision, prob, reasoning, source = await self.llm_manager.decide(
                question="Should another remediation cycle be executed?",
                context_summary="QA Score: 6/10",
                true_when="Score < 9",
                false_when="Score >= 9",
                threshold=0.80,
                deterministic_fallback=lambda: False
            )
            
            self.assertTrue(decision)
            self.assertAlmostEqual(prob, 0.94, places=2)
            self.assertEqual(source, "mercury")
            self.assertIn("yes", reasoning)

    async def test_05_mercury_failure_triggers_deterministic_fallback(self):
        """Test 5: Verify that Mercury failure smoothly defaults to deterministic logic"""
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = Exception("OpenRouter connection timeout")
            decision, prob, reasoning, source = await self.llm_manager.decide(
                question="Should fix pass run?",
                context_summary="Score: 5/10",
                true_when="Score < 9",
                false_when="Score >= 9",
                threshold=0.80,
                deterministic_fallback=lambda: True
            )
            
            self.assertTrue(decision)
            self.assertEqual(source, "deterministic")

    async def test_06_mercury_http_error_fallback(self):
        """Test 6: Verify non-200 HTTP response from Mercury falls back safely to deterministic rule"""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_resp
            decision, prob, reasoning, source = await self.llm_manager.decide(
                question="Is task coding?",
                context_summary="React build",
                true_when="Frontend app",
                false_when="Other",
                threshold=0.80,
                deterministic_fallback=lambda: True
            )
            
            self.assertTrue(decision)
            self.assertEqual(source, "deterministic")

    def test_07_security_sanitization_never_leaks_keys(self):
        """Test 7: Verify API keys, tokens, and authorization headers are scrubbed from logs/errors"""
        sensitive_error = (
            "API request failed with Authorization: Bearer sk-or-v1-abc123secretxyz "
            "and key=AQ.TEST_GCP_CREDENTIAL "
            "and gsk_TEST_GROQ_CREDENTIAL"
        )
        sanitized = self.llm_manager._sanitize_error(sensitive_error)
        
        self.assertNotIn("sk-or-v1-abc123secretxyz", sanitized)
        self.assertNotIn("AQ.TEST_GCP_CREDENTIAL", sanitized)
        self.assertNotIn("gsk_TEST_GROQ_CREDENTIAL", sanitized)
        self.assertIn("[REDACTED_API_KEY]", sanitized)

    def test_08_remediation_loop_hard_cap(self):
        """Test 8: Verify that WorkflowEngine strictly caps remediation loops at MAX_REMEDIATION_LOOPS"""
        engine = WorkflowEngine()
        
        # When iterations reach limit, must always return "pass"
        state_at_limit = {
            "qa_iterations": settings.MAX_REMEDIATION_LOOPS,
            "remediation_needed": True,
            "quality_score": 5,
            "integrity_passed": False
        }
        self.assertEqual(engine._check_qa_status(state_at_limit), "pass")
        
        # When below limit and remediation needed, returns "fail" to trigger fix pass
        state_below_limit = {
            "qa_iterations": settings.MAX_REMEDIATION_LOOPS - 1,
            "remediation_needed": True,
            "quality_score": 5,
            "integrity_passed": False
        }
        self.assertEqual(engine._check_qa_status(state_below_limit), "fail")

    def test_09_frontend_batching_preserved(self):
        """Test 9: Verify that Frontend Developer Agent preserves the 3-step batched file generation"""
        agent = FrontendDeveloperAgent()
        # Verify methods exist
        self.assertTrue(hasattr(agent, "_scaffold_project"))
        self.assertTrue(hasattr(agent, "_create_components_and_layouts"))
        self.assertTrue(hasattr(agent, "_create_pages_and_routing"))
        self.assertTrue(hasattr(agent, "_create_all_files"))

if __name__ == "__main__":
    unittest.main()
