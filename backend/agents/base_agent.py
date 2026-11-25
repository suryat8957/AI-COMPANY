from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple, Union
import json
import re
from database.models import EmployeeRole
from utils.logger import setup_logger
from agents.llm_manager import llm_manager

logger = setup_logger(__name__)

class BaseAgent(ABC):
    """
    Base class for all AI agents in the Multi-Model Mesh.
    Seamlessly integrates with centralized LLMManager for role-based routing,
    Qwen/Gemini/Mercury model selection, and automatic fallback cascades.
    """
    
    def __init__(
        self, 
        role: EmployeeRole, 
        name: str, 
        temperature: float = 0.7,
        preferred_provider: str = "auto"
    ):
        self.role = role
        self.name = name
        self.temperature = temperature
        self.preferred_provider = preferred_provider
        self.llm_manager = llm_manager
        
        self.system_prompt = self._get_system_prompt()
        self.memory: List[str] = []
        
        # Pipeline discovery via centralized LLMManager
        self.candidate_providers = self.llm_manager.get_candidate_providers(self.role)
        self.primary_provider = self.candidate_providers[0][0] if self.candidate_providers else "none"
        self.primary_llm = self.candidate_providers[0][2] if self.candidate_providers else None
        self.llm = self.primary_llm
        
        pipeline_display = " -> ".join([p[0].upper() for p in self.candidate_providers]) if self.candidate_providers else "NONE"
        logger.info(f"Agent [{self.name} - {self.role.value}] initialized with Mesh Pipeline: [{pipeline_display}]")

    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task"""
        pass

    async def _generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate response through centralized LLMManager with automatic role routing,
        retry logic, and multi-model cascade failover.
        """
        project_id = context.get("project_id") if context else None
        return await self.llm_manager.execute_with_fallback(
            role=self.role,
            prompt=prompt,
            system_prompt=self.system_prompt,
            context=context,
            agent_name=self.name,
            temperature=self.temperature,
            project_id=project_id
        )

    def _format_context(self, context: Optional[Dict]) -> str:
        """Format context dictionary cleanly and compactly for LLM input"""
        return self.llm_manager._format_context(context)
    
    def _extract_code(self, response: str, language: str = "") -> str:
        """Extract code from markdown code blocks safely"""
        pattern = r"```(?:\w+)?\n?(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        if matches:
            longest_block = max(matches, key=len)
            return longest_block.strip()
        return response.strip()
    
    def _extract_json(self, response: str) -> Optional[Any]:
        """Extract and parse JSON object or array from response text"""
        return self.llm_manager._extract_json(response)
    
    def _extract_multi_files(self, response: str) -> Dict[str, str]:
        """Extract multiple files demarcated by headers like `### filepath` or `--- filepath ---`"""
        files: Dict[str, str] = {}
        file_sections = re.findall(
            r"(?:###|---|===\s*FILE:\s*)\s*([a-zA-Z0-9_\-./\\]+\.[a-zA-Z0-9]+)\s*(?:---|===)?\s*\n```(?:[a-zA-Z0-9_-]+)?\n?(.*?)```",
            response,
            re.DOTALL | re.IGNORECASE
        )
        for filepath, content in file_sections:
            clean_path = filepath.strip().replace('\\', '/')
            files[clean_path] = content.strip()
        return files
    
    def add_to_memory(self, message: str):
        """Add message to agent's memory"""
        self.memory.append(message)
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]
            
    def get_memory(self) -> List[str]:
        """Retrieve recent agent memory"""
        return self.memory
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "role": self.role.value,
            "pipeline": [p[0] for p in self.candidate_providers],
            "primary_provider": self.primary_provider,
            "memory_size": len(self.memory)
        }