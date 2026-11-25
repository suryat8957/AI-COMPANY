from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Configuration
    APP_NAME: str = "AI Multi-Agent Software Company"
    VERSION: str = "2.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # 1. OpenRouter API Configuration (Qwen3.8 27B + Mercury Decide)
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    QWEN_MODEL: str = "qwen/qwen3.8-27b:free"
    MERCURY_MODEL: str = "inception/mercury-decide:free"
    
    # 2. Google Gemini API Configuration (Reasoning, Review, Strategic Planning, Fallback)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.6-flash"
    
    # Remediation & Router Controls
    MAX_REMEDIATION_LOOPS: int = 2
    MERCURY_DECISION_THRESHOLD: float = 0.80
    
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "ai_company"
    
    # Project Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    WORKSPACE_DIR: Path = BASE_DIR / "workspace" / "projects"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    class Config:
        env_file = (".env", "../.env")
        case_sensitive = True
        extra = "ignore"

settings = Settings()

# Create necessary directories
settings.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Centralized 3-Model Registry (Mercury Decide + Qwen 27B + Gemini)
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "mercury": {
        "provider": "openrouter",
        "model": settings.MERCURY_MODEL,
        "description": "Task router, decision gate, and QA remediation evaluation"
    },
    "qwen": {
        "provider": "openrouter",
        "model": settings.QWEN_MODEL,
        "description": "Primary coding, component generation, architecture, and code-level remediation engine"
    },
    "gemini": {
        "provider": "google",
        "model": settings.GEMINI_MODEL,
        "description": "Complex reasoning, executive review, visual UX critique, and high-context review"
    }
}

# Role-Based Model Assignment & Strictly 2-Way Fallback Cascades (Qwen <-> Gemini)
ROLE_CONFIG: Dict[str, Dict[str, Any]] = {
    "router": {
        "primary": "mercury",
        "fallback": ["deterministic"]
    },
    # Reasoning & Executive Review Roles -> Gemini Primary (Fallback: Qwen)
    "ceo": {
        "primary": "gemini",
        "fallback": ["qwen"]
    },
    "project_manager": {
        "primary": "gemini",
        "fallback": ["qwen"]
    },
    "visual_reviewer": {
        "primary": "gemini",
        "fallback": ["qwen"]
    },
    "qa": {
        "primary": "gemini",
        "fallback": ["qwen"]
    },
    "final_signoff": {
        "primary": "gemini",
        "fallback": ["qwen"]
    },
    # Coding, Architecture & Implementation Roles -> Qwen Primary (Fallback: Gemini)
    "ui_designer": {
        "primary": "qwen",
        "fallback": ["gemini"]
    },
    "react_architect": {
        "primary": "qwen",
        "fallback": ["gemini"]
    },
    "frontend_developer": {
        "primary": "qwen",
        "fallback": ["gemini"]
    },
    "file_integrity": {
        "primary": "qwen",
        "fallback": ["gemini"]
    },
    "remediation": {
        "primary": "qwen",
        "fallback": ["gemini"]
    },
    "documentation": {
        "primary": "qwen",
        "fallback": ["gemini"]
    }
}

# High-Level Semantic Functional Role Mapping
MODEL_ROLES: Dict[str, str] = {
    "routing": "mercury",
    "planning": "gemini",
    "architecture": "qwen",
    "coding": "qwen",
    "debugging": "qwen",
    "review": "gemini",
    "qa": "gemini",
    "documentation": "qwen"
}