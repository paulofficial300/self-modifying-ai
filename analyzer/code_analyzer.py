"""Detailed code analysis for self-modification."""

import ast
from typing import Dict, List, Any
from collections import defaultdict


class CodeAnalyzer:
    """Analyzes code for metrics and improvement opportunities."""

    def __init__(self):
        """Initialize the CodeAnalyzer."""
        self.metrics = {}

    def calculate_complexity(self, code: str) -> Dict[str, int]:
        """Calculate cyclomatic complexity.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Complexity metrics
        """
        tree = ast.parse(code)
        complexity = defaultdict(int)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity['branches'] += 1
            elif isinstance(node, ast.FunctionDef):
                complexity['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                complexity['classes'] += 1
        
        return dict(complexity)

    def calculate_code_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate various code metrics.
        
        Args:
            code: Source code
            
        Returns:
            Dictionary of metrics
        """
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        metrics = {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "avg_line_length": sum(len(l) for l in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0,
            "complexity": self.calculate_complexity(code)
        }
        
        return metrics

    def identify_optimization_opportunities(self, code: str) -> List[Dict[str, str]]:
        """Identify specific optimization opportunities.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of optimization suggestions
        """
        opportunities = []
        tree = ast.parse(code)
        
        # Look for list comprehension opportunities
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                parent = None
                for potential_parent in ast.walk(tree):
                    for child in ast.iter_child_nodes(potential_parent):
                        if child is node:
                            parent = potential_parent
                            break
                
                # Check for common loop patterns
                opportunities.append({
                    "type": "loop_optimization",
                    "line": node.lineno,
                    "suggestion": "Consider using list comprehension"
                })
        
        return opportunities
