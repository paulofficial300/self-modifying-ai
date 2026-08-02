"""Safety validation for code modifications."""

import ast
import re
from typing import List, Dict, Any, Tuple


class SafetyChecker:
    """Validates modifications for safety."""

    # Dangerous patterns that should not be auto-modified
    DANGEROUS_PATTERNS = [
        r'os\.system',
        r'subprocess\.call',
        r'exec\(',
        r'eval\(',
        r'__import__',
        r'open\(',
    ]

    def __init__(self):
        """Initialize the SafetyChecker."""
        self.violation_count = 0

    def check_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """Check if code has valid syntax.
        
        Args:
            code: Code to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            ast.parse(code)
            return True, []
        except SyntaxError as e:
            return False, [str(e)]

    def check_dangerous_operations(self, code: str) -> Tuple[bool, List[str]]:
        """Check for dangerous operations in code.
        
        Args:
            code: Code to analyze
            
        Returns:
            Tuple of (is_safe, warnings)
        """
        warnings = []
        
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code):
                warnings.append(f"Dangerous pattern detected: {pattern}")
        
        return len(warnings) == 0, warnings

    def validate_modification(self, original: str, modified: str) -> Dict[str, Any]:
        """Perform comprehensive validation.
        
        Args:
            original: Original code
            modified: Modified code
            
        Returns:
            Validation report
        """
        syntax_valid, syntax_errors = self.check_syntax(modified)
        safe, safety_warnings = self.check_dangerous_operations(modified)
        
        report = {
            "syntax_valid": syntax_valid,
            "is_safe": safe,
            "errors": syntax_errors,
            "warnings": safety_warnings,
            "approved": syntax_valid and safe
        }
        
        if not report["approved"]:
            self.violation_count += 1
        
        return report
