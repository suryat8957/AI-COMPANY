import asyncio
import json
import logging
import re
import time
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from datetime import datetime
import httpx

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings, MODEL_REGISTRY, ROLE_CONFIG, MODEL_ROLES
from database.models import EmployeeRole
from utils.logger import setup_logger, ProjectLogger

logger = setup_logger(__name__)

class LLMManager:
    """
    Centralized 3-Model LLM Mesh Manager
    Strictly orchestrates:
    1. Inception Mercury Decide (OpenRouter) -> Task Routing & Decision Gate
    2. Qwen3.8 27B (OpenRouter)             -> Main Coding & Implementation Engine
    3. Google Gemini (Google AI Studio)      -> Complex Reasoning & Senior Review Engine
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        
        # Track daily/session request metrics (LLM invocations only, not tool calls)
        self.metrics = {
            "openrouter_total": 0,
            "qwen_requests": 0,
            "mercury_requests": 0,
            "gemini_requests": 0,
            "fallback_count": 0,
            "total_calls": 0,
            "failed_calls": 0,
            "start_time": datetime.utcnow().isoformat()
        }
        
        # Initialize the 3 mesh engines
        self.qwen_llm = self._init_qwen()
        self.mercury_available = self._is_valid_key(settings.OPENROUTER_API_KEY)
        self.gemini_llm = self._init_gemini()
        
        # Log active engines
        active_engines = []
        if self.mercury_available:
            active_engines.append(f"Mercury Decide ({settings.MERCURY_MODEL})")
        if self.qwen_llm is not None:
            active_engines.append(f"Qwen 27B ({settings.QWEN_MODEL})")
        if self.gemini_llm is not None:
            active_engines.append(f"Gemini ({settings.GEMINI_MODEL})")
            
        logger.info(f"✨ 3-Model LLM Mesh Active Engines: [{', '.join(active_engines)}]")
        
    def _is_valid_key(self, key: Optional[str]) -> bool:
        """Check if an API key is present and not a dummy placeholder"""
        if not key:
            return False
        cleaned = key.strip()
        if not cleaned:
            return False
        dummy_markers = ["your_", "_key_here", "placeholder", "xxx", "none"]
        return not any(marker in cleaned.lower() for marker in dummy_markers)
        
    def _init_qwen(self) -> Optional[ChatOpenAI]:
        """Initialize Qwen3.8 27B via OpenRouter for primary coding & architecture"""
        if not self._is_valid_key(settings.OPENROUTER_API_KEY):
            logger.warning("⚠️ OpenRouter API key not configured. Qwen coding engine standby.")
            return None
        try:
            return ChatOpenAI(
                model=settings.QWEN_MODEL,
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
                default_headers={
                    "HTTP-Referer": "https://ai-company.local",
                    "X-Title": "AI Company Studio"
                },
                temperature=0.3,
                timeout=120,
                max_retries=1
            )
        except Exception as e:
            logger.warning(f"Failed to initialize OpenRouter Qwen LLM: {self._sanitize_error(e)}")
            return None

    def _init_gemini(self) -> Optional[ChatGoogleGenerativeAI]:
        """Initialize Google Gemini for reasoning, reviews, and high-context review"""
        if not self._is_valid_key(settings.GEMINI_API_KEY):
            logger.warning("⚠️ Google Gemini API key not configured.")
            return None
        try:
            return ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.3,
                timeout=75,
                max_retries=1,
                convert_system_message_to_human=True
            )
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini LLM: {self._sanitize_error(e)}")
            return None

    def _sanitize_error(self, error: Any) -> str:
        """Sanitize error messages so API keys, bearer tokens, or secret headers are never printed"""
        err_msg = str(error)
        patterns = [
            r"bearer\s+[\w\-\.]+",
            r"key=[^&\s]+",
            r"AQ\.[a-zA-Z0-9_\-]+",
            r"sk-or-v1-[a-zA-Z0-9_\-]+",
            r"gsk_[a-zA-Z0-9_\-]+",
            r"api_key=['\"][^'\"]+['\"]"
        ]
        for pat in patterns:
            err_msg = re.sub(pat, "[REDACTED_API_KEY]", err_msg, flags=re.IGNORECASE)
        return err_msg

    def _normalize_role(self, role: Union[str, EmployeeRole]) -> str:
        """Map role name or EmployeeRole enum to canonical configuration role key"""
        if isinstance(role, EmployeeRole):
            role_val = role.value.lower()
        else:
            role_val = str(role).lower().strip()
            
        role_map = {
            "ceo": "ceo",
            "alex thompson": "ceo",
            "project manager": "project_manager",
            "project_manager": "project_manager",
            "sarah martinez": "project_manager",
            "ui designer": "ui_designer",
            "ui_designer": "ui_designer",
            "lead ui/ux designer": "ui_designer",
            "maya patel": "ui_designer",
            "react architect": "react_architect",
            "react_architect": "react_architect",
            "principal react architect": "react_architect",
            "david vance": "react_architect",
            "frontend developer": "frontend_developer",
            "frontend_developer": "frontend_developer",
            "senior react developer": "frontend_developer",
            "jordan lee": "frontend_developer",
            "file integrity specialist": "file_integrity",
            "file_integrity": "file_integrity",
            "marcus brody": "file_integrity",
            "visual & ux reviewer": "visual_reviewer",
            "visual_reviewer": "visual_reviewer",
            "sophia rossi": "visual_reviewer",
            "qa tester": "qa",
            "qa": "qa",
            "lead react qa auditor": "qa",
            "chris anderson": "qa",
            "remediation": "remediation",
            "remediation developer": "remediation",
            "documentation writer": "documentation",
            "documentation": "documentation",
            "emily zhang": "documentation",
            "final_signoff": "final_signoff",
            "router": "router"
        }
        
        # Check direct map
        for k, v in role_map.items():
            if k in role_val:
                return v
                
        # Semantic fallback from MODEL_ROLES
        if role_val in MODEL_ROLES:
            return role_val
            
        return "frontend_developer" if ("code" in role_val or "dev" in role_val) else "ceo"

    def get_candidate_providers(self, role: Union[str, EmployeeRole]) -> List[Tuple[str, str, Any]]:
        """
        Resolve candidate provider pipeline in priority order based on role configuration.
        Returns: List of tuples: (provider_id, model_name, llm_instance)
        """
        role_key = self._normalize_role(role)
        cfg = ROLE_CONFIG.get(role_key, ROLE_CONFIG.get("frontend_developer", {}))
        
        primary = cfg.get("primary", "qwen")
        fallbacks = cfg.get("fallback", ["gemini"])
        
        ordered_engine_keys = [primary] + [f for f in fallbacks if f != primary]
        
        provider_map = {
            "qwen": ("openrouter", settings.QWEN_MODEL, self.qwen_llm),
            "gemini": ("google", settings.GEMINI_MODEL, self.gemini_llm)
        }
        
        candidates = []
        for engine_key in ordered_engine_keys:
            if engine_key in provider_map:
                p_id, m_name, instance = provider_map[engine_key]
                if instance is not None:
                    candidates.append((engine_key, m_name, instance))
                    
        # Emergency safety: If no configured candidate is initialized, append any available engine
        if not candidates:
            for engine_key in ["qwen", "gemini"]:
                if engine_key in provider_map:
                    p_id, m_name, instance = provider_map[engine_key]
                    if instance is not None and (engine_key, m_name, instance) not in candidates:
                        candidates.append((engine_key, m_name, instance))
                        
        return candidates

    def get_model(self, role: Union[str, EmployeeRole]) -> Optional[Any]:
        """Retrieve the primary available LLM instance for a given role"""
        candidates = self.get_candidate_providers(role)
        return candidates[0][2] if candidates else None

    async def execute_with_fallback(
        self,
        role: Union[str, EmployeeRole],
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        agent_name: str = "Agent",
        temperature: Optional[float] = None,
        project_id: Optional[str] = None
    ) -> str:
        """
        Execute LLM generation with automatic provider cascade failover between Qwen and Gemini.
        Logs detailed latency, attempt counts, and fallback events.
        """
        role_key = self._normalize_role(role)
        candidates = self.get_candidate_providers(role)
        
        if not candidates:
            err_msg = f"No available LLM providers initialized for role '{role_key}'. Check OPENROUTER_API_KEY or GEMINI_API_KEY."
            logger.error(err_msg)
            raise ValueError(err_msg)
            
        proj_logger = ProjectLogger(project_id) if project_id else logger
        
        # Build prompt messages
        formatted_context = self._format_context(context)
        user_content = f"Context:\n{formatted_context}\n\nTask:\n{prompt}" if formatted_context != "None" else prompt
        
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=user_content))
        
        last_error = None
        
        for idx, (engine_key, model_name, llm_instance) in enumerate(candidates):
            attempt_num = idx + 1
            provider_display = "OpenRouter" if engine_key == "qwen" else "Gemini"
            
            if idx > 0:
                self.metrics["fallback_count"] += 1
                fallback_log = f"[LLM] Falling back to {provider_display} ({model_name}) for {agent_name} [{role_key}]"
                logger.info(fallback_log)
                if project_id:
                    proj_logger.info(f"🔄 {fallback_log}")
                    
            # Try this candidate up to 2 times for transient errors (429 rate limit / 503 high demand)
            for inner_try in range(2):
                call_start = time.time()
                
                logger.info(
                    f"\n==================================================\n"
                    f"LLM REQUEST\n"
                    f"Agent: {agent_name}\n"
                    f"Role: {role_key}\n"
                    f"Provider: {provider_display}\n"
                    f"Model: {model_name}\n"
                    f"Attempt: {attempt_num}{f' (retry {inner_try})' if inner_try > 0 else ''}\n"
                    f"=================================================="
                )
                
                try:
                    # Actual LLM invocation
                    response = await llm_instance.ainvoke(messages)
                    latency = time.time() - call_start
                    
                    content = self._extract_text_content(response.content)
                    if not content or not content.strip():
                        raise ValueError(f"Empty response returned from model {model_name}")
                        
                    # Track successful execution metrics
                    self.metrics["total_calls"] += 1
                    if engine_key == "qwen":
                        self.metrics["openrouter_total"] += 1
                        self.metrics["qwen_requests"] += 1
                    elif engine_key == "gemini":
                        self.metrics["gemini_requests"] += 1
                        
                    logger.info(
                        f"Completed in: {latency:.2f}s | Status: SUCCESS | Engine: {engine_key.upper()} ({model_name})"
                    )
                    
                    return content
                    
                except Exception as err:
                    latency = time.time() - call_start
                    last_error = err
                    self.metrics["failed_calls"] += 1
                    clean_err = self._sanitize_error(err)
                    
                    err_str = str(err).lower()
                    is_rate_limit = any(term in err_str for term in [
                        "429", "rate limit", "quota", "too many requests", "resourceexhausted",
                        "credits", "insufficient_quota", "overloaded", "413"
                    ])
                    is_transient = any(term in err_str for term in [
                        "503", "unavailable", "high demand", "overloaded", "timeout", "timed out", "504"
                    ])
                    
                    issue_type = "Rate Limit/Quota Bound (429)" if is_rate_limit else ("High Demand/Unavailable (503)" if is_transient else "Engine Error")
                    
                    logger.warning(
                        f"[LLM] {provider_display} ({model_name}) attempt #{attempt_num}{f' (retry {inner_try})' if inner_try > 0 else ''} failed after {latency:.2f}s "
                        f"[{issue_type}]: {clean_err}"
                    )
                    
                    # If transient or rate-limited, wait 1.5s and retry once on this same provider before falling back
                    if (is_rate_limit or is_transient) and inner_try == 0:
                        logger.info(f"⏳ Pausing 1.5s before retrying {provider_display} ({model_name})...")
                        await asyncio.sleep(1.5)
                        continue
                    break
                    
        # All providers exhausted
        logger.error(f"[LLM] All configured providers in cascade failed for {agent_name} [{role_key}]. Last error: {self._sanitize_error(last_error)}")
        raise last_error

    async def decide(
        self,
        question: str,
        context_summary: str,
        true_when: str,
        false_when: str,
        threshold: float = 0.80,
        deterministic_fallback: Optional[Callable[[], bool]] = None,
        project_id: Optional[str] = None
    ) -> Tuple[bool, float, str, str]:
        """
        Execute structured decision routing using Inception Mercury Decide via OpenRouter's /api/alpha/decisions endpoint.
        Returns: (decision_bool, confidence_probability, reasoning, source)
        Source is either 'mercury' or 'deterministic'.
        """
        proj_logger = ProjectLogger(project_id) if project_id else logger
        
        # Check if OpenRouter key is available for Mercury
        if not self.mercury_available:
            logger.info("ℹ️ Mercury Decide is unavailable. Using deterministic router logic.")
            fallback_val = deterministic_fallback() if deterministic_fallback else False
            return (fallback_val, 1.0, "Deterministic router rule (Mercury offline)", "deterministic")
            
        call_start = time.time()
        try:
            logger.info(f"🧭 [Mercury Router] Evaluating decision: '{question[:80]}...'")
            
            # Inception Mercury Decide uses OpenRouter's dedicated /api/alpha/decisions endpoint
            decisions_url = "https://openrouter.ai/api/alpha/decisions"
            payload = {
                "model": settings.MERCURY_MODEL,
                "state": context_summary,
                "questions": {
                    "decision": {
                        "type": "choice",
                        "instructions": question,
                        "criteria": {
                            "yes": true_when,
                            "no": false_when
                        }
                    }
                }
            }
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-company.local",
                "X-Title": "AI Company Studio"
            }
            
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(decisions_url, headers=headers, json=payload)
                if resp.status_code != 200:
                    raise ValueError(f"HTTP {resp.status_code}: {resp.text}")
                data = resp.json()
                
            latency = time.time() - call_start
            ans = data.get("answers", {}).get("decision", {})
            raw_choice = ans.get("choice")
            raw_decision = (raw_choice == "yes")
            prob = float(ans.get("probabilities", {}).get("yes", ans.get("confidence", 0.5)))
            conf = float(ans.get("confidence", prob))
            reasoning = f"Mercury evaluated '{raw_choice}' with confidence {conf:.2f}"
            
            # Apply confidence threshold
            final_decision = raw_decision if (prob >= threshold or not raw_decision) else False
            
            self.metrics["openrouter_total"] += 1
            self.metrics["mercury_requests"] += 1
            self.metrics["total_calls"] += 1
            
            decision_log = (
                f"🧭 [Mercury Decide] Decision: {final_decision} (prob: {prob:.2f} | threshold: {threshold:.2f}) "
                f"in {latency:.2f}s -> {reasoning}"
            )
            logger.info(decision_log)
            if project_id:
                proj_logger.info(decision_log)
                
            return (final_decision, prob, reasoning, "mercury")
            
        except Exception as err:
            logger.warning(
                f"🧭 [Mercury Router] Mercury decision evaluation encountered error: {self._sanitize_error(err)}. "
                f"Engaging deterministic fallback."
            )
            fallback_val = deterministic_fallback() if deterministic_fallback else False
            return (fallback_val, 1.0, f"Deterministic rule fallback after error: {self._sanitize_error(err)}", "deterministic")

    def _extract_text_content(self, content: Any) -> str:
        """Extract plain string cleanly from LLM response block"""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            blocks = []
            for item in content:
                if isinstance(item, str):
                    blocks.append(item)
                elif isinstance(item, dict) and "text" in item:
                    blocks.append(str(item["text"]))
                elif hasattr(item, "text"):
                    blocks.append(str(getattr(item, "text")))
                else:
                    blocks.append(str(item))
            return "\n".join(blocks)
        return str(content)

    def _extract_json(self, text: str) -> Optional[Any]:
        """Safely parse JSON from text or markdown blocks"""
        try:
            return json.loads(text.strip())
        except Exception:
            pass
            
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass
                
        # Regex search for top-level object
        match = re.search(r"(\{[\s\S]*\})", text)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass
                
        return None

    def _format_context(self, context: Optional[Dict]) -> str:
        """Format context dictionary cleanly and compactly for LLM prompt"""
        if not context:
            return "None"
        formatted_lines = []
        for k, v in context.items():
            if k == "files" and isinstance(v, dict):
                formatted_lines.append(f"- **existing_files**: {list(v.keys())}")
            elif isinstance(v, dict):
                clean_dict = {
                    dk: (list(dv.keys()) if dk == "files" and isinstance(dv, dict) else dv)
                    for dk, dv in v.items()
                }
                serialized = json.dumps(clean_dict, indent=2)
                if len(serialized) > 1500:
                    serialized = serialized[:1500] + "... [truncated]"
                formatted_lines.append(f"- **{k}**: {serialized}")
            elif isinstance(v, list):
                serialized = json.dumps(v, indent=2)
                if len(serialized) > 1500:
                    serialized = serialized[:1500] + "... [truncated]"
                formatted_lines.append(f"- **{k}**: {serialized}")
            elif isinstance(v, str) and len(v) > 1500:
                formatted_lines.append(f"- **{k}**:\n{v[:1500]}... [truncated]")
            else:
                formatted_lines.append(f"- **{k}**: {v}")
        return "\n".join(formatted_lines)

    def get_usage_summary(self) -> str:
        """Generate formatted operational usage report strictly for the 3 active LLM engines"""
        return f"""
==================================================
Multi-Model LLM Mesh Usage Summary (3-Model Mesh)
--------------------------------------------------
OpenRouter Mercury Decide calls: {self.metrics['mercury_requests']}
OpenRouter Qwen 27B calls:       {self.metrics['qwen_requests']}
Total OpenRouter calls:          {self.metrics['openrouter_total']}
Google Gemini calls:             {self.metrics['gemini_requests']}
Total LLM Invocations:           {self.metrics['total_calls']}
Total Fallback Events:           {self.metrics['fallback_count']}
Failed / Aborted Calls:          {self.metrics['failed_calls']}
==================================================
""".strip()

# Global Singleton instance
llm_manager = LLMManager()
