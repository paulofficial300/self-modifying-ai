"""Tests for SafetyChecker."""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from self_modifier.safety_checker import SafetyChecker


class TestSafetyChecker:
    """Test suite for SafetyChecker."""

    @pytest.fixture
    def checker(self):
        """Create a SafetyChecker instance."""
        return SafetyChecker()

    def test_valid_syntax(self, checker):
        """Test that valid code passes syntax check."""
        code = "x = 1\nprint(x)"
        is_valid, errors = checker.check_syntax(code)
        assert is_valid is True
        assert len(errors) == 0

    def test_invalid_syntax(self, checker):
        """Test that invalid code fails syntax check."""
        code = "x = "
        is_valid, errors = checker.check_syntax(code)
        assert is_valid is False
        assert len(errors) > 0

    def test_dangerous_operations(self, checker):
        """Test detection of dangerous operations."""
        code = "import os\nos.system('rm -rf /')"
        is_safe, warnings = checker.check_dangerous_operations(code)
        assert is_safe is False
        assert len(warnings) > 0
