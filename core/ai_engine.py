"""Main AI Engine for self-modification capabilities."""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from .llm_integration import LLMIntegration


class AIEngine:
    """Central AI engine with self-modification capabilities powered by GPT-4."""

    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None):
        """Initialize the AI Engine.
        
        Args:
            model: The LLM model to use for code generation and analysis
            api_key: OpenAI API key (optional, can use env variable)
        """
        self.model = model
        self.llm = LLMIntegration(api_key=api_key, model=model)
        self.modification_history: List[Dict[str, Any]] = []
        self.current_version = "1.0.0"
        self.performance_metrics: Dict[str, float] = {}
        self.improvement_strategies = [
            "refactor_for_performance",
            "add_error_handling",
            "add_type_hints",
            "improve_readability"
        ]

    def analyze_own_code(self, code_path: str) -> Dict[str, Any]:
        """Analyze own codebase for improvement opportunities using GPT-4.
        
        Args:
            code_path: Path to the code file to analyze
            
        Returns:
            Analysis results with improvement suggestions
        """
        if not os.path.exists(code_path):
            raise FileNotFoundError(f"Code file not found: {code_path}")
        
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        # Use GPT-4 for detailed analysis
        llm_analysis = self.llm.analyze_code(code_content, f"File: {code_path}")
        
        analysis = {
            "file": code_path,
            "timestamp": datetime.now().isoformat(),
            "code_length": len(code_content),
            "llm_analysis": llm_analysis,
            "suggestions": self._extract_suggestions(llm_analysis)
        }
        
        return analysis

    def generate_improved_code(self, code_path: str, improvement_goal: str) -> Dict[str, Any]:
        """Generate improved version of code based on analysis using GPT-4.
        
        Args:
            code_path: Path to the code to improve
            improvement_goal: Description of desired improvement
            
        Returns:
            Dictionary with improved code and explanation
        """
        with open(code_path, 'r') as f:
            original_code = f.read()
        
        # Use GPT-4 to generate improved code
        result = self.llm.generate_improved_code(
            original_code,
            improvement_goal,
            context=f"File: {code_path}"
        )
        
        return result

    def refactor_for_performance(self, code_path: str) -> Dict[str, Any]:
        """Refactor code specifically for performance optimization.
        
        Args:
            code_path: Path to code file to refactor
            
        Returns:
            Performance-optimized code and details
        """
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        return self.llm.refactor_for_performance(code_content)

    def enhance_error_handling(self, code_path: str) -> Dict[str, Any]:
        """Add comprehensive error handling to code.
        
        Args:
            code_path: Path to code file
            
        Returns:
            Enhanced code with error handling
        """
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        return self.llm.add_error_handling(code_content)

    def add_type_hints(self, code_path: str) -> Dict[str, Any]:
        """Add type hints to code for better type safety.
        
        Args:
            code_path: Path to code file
            
        Returns:
            Code with type hints added
        """
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        return self.llm.add_type_hints(code_content)

    def generate_test_cases(self, code_path: str) -> Dict[str, Any]:
        """Generate test cases for code.
        
        Args:
            code_path: Path to code file to test
            
        Returns:
            Generated test code
        """
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        return self.llm.generate_tests(code_content)

    def explain_code(self, code_path: str) -> Dict[str, Any]:
        """Generate detailed explanation of code.
        
        Args:
            code_path: Path to code file
            
        Returns:
            Detailed explanation
        """
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        return self.llm.explain_code(code_content)

    def suggest_refactoring(self, code_path: str, focus_area: str = "general") -> Dict[str, Any]:
        """Suggest specific refactorings for code.
        
        Args:
            code_path: Path to code file
            focus_area: Area to focus on (general, readability, performance, testability)
            
        Returns:
            Refactoring suggestions and improved code
        """
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        return self.llm.suggest_refactoring(code_content, focus_area)

    def self_improve(self, code_path: str, strategy: str = "general") -> Dict[str, Any]:
        """Apply self-improvement to code using specified strategy.
        
        Args:
            code_path: Path to code file to improve
            strategy: Improvement strategy (general, performance, robustness, maintainability)
            
        Returns:
            Improvement results
        """
        strategies = {
            "performance": lambda cp: self.refactor_for_performance(cp),
            "robustness": lambda cp: self.enhance_error_handling(cp),
            "maintainability": lambda cp: self.suggest_refactoring(cp, "readability"),
            "general": lambda cp: self.generate_improved_code(cp, "Overall improvement for quality, performance, and maintainability")
        }
        
        strategy_func = strategies.get(strategy, strategies["general"])
        return strategy_func(code_path)

    def validate_modification(self, original_code: str, modified_code: str) -> bool:
        """Validate that modifications are safe and valid.
        
        Args:
            original_code: Original code before modification
            modified_code: Modified code to validate
            
        Returns:
            True if modification is valid, False otherwise
        """
        try:
            compile(modified_code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    def apply_modification(self, file_path: str, modified_code: str, 
                          improvement_goal: str) -> bool:
        """Apply validated modification to file.
        
        Args:
            file_path: Path to file to modify
            modified_code: The improved code
            improvement_goal: Description of the improvement
            
        Returns:
            True if modification was successful
        """
        if not self.validate_modification("", modified_code):
            print(f"Warning: Modified code has syntax errors, not applying to {file_path}")
            return False
        
        with open(file_path, 'w') as f:
            f.write(modified_code)
        
        # Log the modification
        self.modification_history.append({
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "goal": improvement_goal,
            "version": self.current_version,
            "status": "applied"
        })
        
        return True

    def get_modification_history(self) -> List[Dict[str, Any]]:
        """Get all self-modifications made by the AI.
        
        Returns:
            List of modification records
        """
        return self.modification_history

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics.
        
        Returns:
            Usage statistics from LLM calls
        """
        return self.llm.get_usage_stats()

    def _extract_suggestions(self, llm_analysis: Dict[str, Any]) -> List[str]:
        """Extract suggestions from LLM analysis.
        
        Args:
            llm_analysis: Analysis result from LLM
            
        Returns:
            List of suggestions
        """
        # This could be enhanced to parse JSON from LLM response
        return ["See full analysis for detailed suggestions"]

    def generate_improvement_plan(self, code_path: str) -> Dict[str, Any]:
        """Generate a comprehensive improvement plan for code.
        
        Args:
            code_path: Path to code file
            
        Returns:
            Detailed improvement plan with multiple strategies
        """
        analysis = self.analyze_own_code(code_path)
        
        plan = {
            "file": code_path,
            "timestamp": datetime.now().isoformat(),
            "initial_analysis": analysis,
            "improvement_strategies": {}
        }
        
        # Apply multiple improvement strategies
        strategies_to_try = ["performance", "robustness", "maintainability"]
        
        for strategy in strategies_to_try:
            try:
                result = self.self_improve(code_path, strategy)
                plan["improvement_strategies"][strategy] = result
            except Exception as e:
                plan["improvement_strategies"][strategy] = {"error": str(e)}
        
        return plan
