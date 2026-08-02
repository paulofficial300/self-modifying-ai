#!/usr/bin/env python
"""Main entry point for the Self-Modifying AI system."""

import sys
from core.ai_engine import AIEngine
from self_modifier.safety_checker import SafetyChecker
from analyzer.code_analyzer import CodeAnalyzer
from executor.sandbox import Sandbox


def main():
    """Initialize and run the Self-Modifying AI system."""
    print("=" * 50)
    print("Self-Modifying AI System")
    print("=" * 50)
    
    # Initialize components
    ai_engine = AIEngine(model="gpt-4")
    safety_checker = SafetyChecker()
    code_analyzer = CodeAnalyzer()
    sandbox = Sandbox()
    
    print("\n✓ AI Engine initialized")
    print("✓ Safety Checker initialized")
    print("✓ Code Analyzer initialized")
    print("✓ Sandbox environment initialized")
    
    print("\nSystem ready for self-modification tasks.")
    print("\nExample workflow:")
    print("1. Analyze own code with CodeAnalyzer")
    print("2. Identify optimization opportunities")
    print("3. Generate improved code with AI Engine")
    print("4. Validate with SafetyChecker")
    print("5. Test in Sandbox")
    print("6. Apply modifications if safe")
    
    return ai_engine, safety_checker, code_analyzer, sandbox


if __name__ == "__main__":
    main()
