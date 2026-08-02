"""Tests for AI Engine."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ai_engine import AIEngine


class TestAIEngine:
    """Test suite for AIEngine."""

    @pytest.fixture
    def engine(self):
        """Create an AIEngine instance for testing."""
        return AIEngine()

    def test_initialization(self, engine):
        """Test that AIEngine initializes correctly."""
        assert engine.model == "gpt-4"
        assert engine.current_version == "1.0.0"
        assert len(engine.modification_history) == 0

    def test_validate_modification_valid_syntax(self, engine):
        """Test validation of syntactically correct code."""
        original = "x = 1"
        modified = "x = 2"
        assert engine.validate_modification(original, modified) is True

    def test_validate_modification_invalid_syntax(self, engine):
        """Test validation catches syntax errors."""
        original = "x = 1"
        modified = "x = "
        assert engine.validate_modification(original, modified) is False

    def test_modification_history(self, engine):
        """Test modification history tracking."""
        assert len(engine.get_modification_history()) == 0
