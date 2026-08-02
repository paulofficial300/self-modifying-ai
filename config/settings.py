"""Configuration settings for the Self-Modifying AI system."""

import os
from typing import Dict, Any


class Settings:
    """Central configuration for the system."""

    # Model configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Safety settings
    ENABLE_SAFETY_CHECKS = True
    SANDBOX_TIMEOUT = 5  # seconds
    MAX_CODE_LENGTH = 50000  # characters
    
    # Evolution settings
    MAX_ITERATIONS = 10
    MODIFICATION_APPROVAL_THRESHOLD = 0.95  # 95% confidence required
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "logs/ai_evolution.log"
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert settings to dictionary.
        
        Returns:
            Dictionary of all settings
        """
        return {
            "llm_model": cls.LLM_MODEL,
            "safety_checks_enabled": cls.ENABLE_SAFETY_CHECKS,
            "sandbox_timeout": cls.SANDBOX_TIMEOUT,
            "max_iterations": cls.MAX_ITERATIONS,
            "approval_threshold": cls.MODIFICATION_APPROVAL_THRESHOLD,
            "log_level": cls.LOG_LEVEL,
        }
