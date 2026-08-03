"""LLM integration module for GPT-4 powered code generation and analysis."""

import os
from typing import Optional, Dict, List, Any
from openai import OpenAI, RateLimitError, APIError

class LLMIntegration:
    """Handles all interactions with GPT-4 LLM for code analysis and generation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """Initialize LLM Integration.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided and not found in environment")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.usage_stats = {
            "total_tokens": 0,
            "total_requests": 0,
            "total_cost": 0.0
        }

    def analyze_code(self, code: str, context: str = "") -> Dict[str, Any]:
        """Analyze code and provide insights using GPT-4.
        
        Args:
            code: Source code to analyze
            context: Additional context about the code
            
        Returns:
            Analysis results with insights and suggestions
        """
        prompt = f"""Analyze the following Python code and provide detailed insights:

Code:
```python
{code}
```

Context: {context}

Please provide:
1. Overview of what the code does
2. Time complexity analysis
3. Space complexity analysis
4. Potential bugs or issues
5. Security concerns (if any)
6. Performance bottlenecks
7. Code quality issues
8. Suggestions for improvement (prioritized by impact)

Format your response as structured JSON."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        return {"analysis": response}

    def generate_improved_code(self, code: str, improvement_goal: str, 
                               context: str = "") -> Dict[str, Any]:
        """Generate improved version of code using GPT-4.
        
        Args:
            code: Original code to improve
            improvement_goal: Specific improvement goal
            context: Additional context
            
        Returns:
            Improved code and explanation
        """
        prompt = f"""You are an expert Python code optimization AI. Improve the following code.

Original Code:
```python
{code}
```

Improvement Goal: {improvement_goal}
Context: {context}

Requirements:
1. Maintain the same functionality
2. Improve performance, readability, or both
3. Follow Python best practices
4. Add meaningful comments
5. Ensure the code is syntactically correct

Provide your response in this format:
IMPROVED_CODE:
```python
[improved code here]
```

EXPLANATION:
[explain the improvements made]

PERFORMANCE_IMPACT:
[explain how this improves performance/readability]"""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        
        # Parse the response to extract code and explanation
        improved_code = self._extract_code_block(response)
        
        return {
            "improved_code": improved_code,
            "explanation": response,
            "status": "success" if improved_code else "parsing_error"
        }

    def refactor_for_performance(self, code: str) -> Dict[str, Any]:
        """Refactor code specifically for performance optimization.
        
        Args:
            code: Code to refactor
            
        Returns:
            Performance-optimized code
        """
        prompt = f"""Refactor this Python code for maximum performance:

```python
{code}
```

Focus on:
1. Algorithm optimization
2. Reducing time complexity
3. Reducing space complexity
4. Eliminating redundant operations
5. Better data structure choices
6. Vectorization opportunities

Provide optimized code with detailed explanation of changes."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        improved_code = self._extract_code_block(response)
        
        return {
            "optimized_code": improved_code,
            "optimization_details": response
        }

    def add_error_handling(self, code: str) -> Dict[str, Any]:
        """Add comprehensive error handling to code.
        
        Args:
            code: Code to enhance with error handling
            
        Returns:
            Code with error handling added
        """
        prompt = f"""Add comprehensive error handling to this Python code:

```python
{code}
```

Include:
1. Try-except blocks for all potential errors
2. Specific exception handling (not generic)
3. Logging of errors
4. Graceful degradation where appropriate
5. Input validation
6. Clear error messages

Maintain the original functionality while adding robustness."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        enhanced_code = self._extract_code_block(response)
        
        return {
            "enhanced_code": enhanced_code,
            "error_handling_details": response
        }

    def add_type_hints(self, code: str) -> Dict[str, Any]:
        """Add type hints to code for better type safety.
        
        Args:
            code: Code to enhance with type hints
            
        Returns:
            Code with type hints added
        """
        prompt = f"""Add comprehensive type hints to this Python code:

```python
{code}
```

Requirements:
1. Add type hints to all function parameters
2. Add return type hints to all functions
3. Use modern Python typing (Union, Optional, etc.)
4. Add type hints for class attributes
5. Use generic types where appropriate
6. Maintain readability

Provide the enhanced code with type hints."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        typed_code = self._extract_code_block(response)
        
        return {
            "typed_code": typed_code,
            "typing_details": response
        }

    def generate_tests(self, code: str) -> Dict[str, Any]:
        """Generate test cases for code using GPT-4.
        
        Args:
            code: Code to generate tests for
            
        Returns:
            Generated test code
        """
        prompt = f"""Generate comprehensive pytest test cases for this Python code:

```python
{code}
```

Requirements:
1. Test normal/happy path cases
2. Test edge cases
3. Test error conditions
4. Use pytest fixtures where appropriate
5. Add docstrings to tests
6. Aim for high code coverage
7. Use meaningful test names

Provide complete, runnable test code."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        test_code = self._extract_code_block(response)
        
        return {
            "test_code": test_code,
            "test_details": response
        }

    def explain_code(self, code: str) -> Dict[str, Any]:
        """Generate detailed explanation of code.
        
        Args:
            code: Code to explain
            
        Returns:
            Detailed explanation
        """
        prompt = f"""Provide a detailed, beginner-friendly explanation of this Python code:

```python
{code}
```

Include:
1. High-level overview of what it does
2. Step-by-step breakdown of the logic
3. Explanation of key algorithms/techniques used
4. Potential inputs and outputs
5. Time and space complexity
6. Any important assumptions or edge cases

Make it educational and thorough."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        
        return {"explanation": response}

    def suggest_refactoring(self, code: str, focus_area: str = "general") -> Dict[str, Any]:
        """Suggest specific refactorings for code.
        
        Args:
            code: Code to refactor
            focus_area: Area to focus on (general, readability, performance, testability)
            
        Returns:
            Refactoring suggestions and improved code
        """
        focus_prompts = {
            "general": "Improve overall code quality, maintainability, and best practices",
            "readability": "Improve code readability and clarity",
            "performance": "Optimize for performance and efficiency",
            "testability": "Improve testability and modularity"
        }
        
        focus_desc = focus_prompts.get(focus_area, focus_prompts["general"])
        
        prompt = f"""Suggest refactorings for this Python code, focusing on: {focus_desc}

Original Code:
```python
{code}
```

Provide:
1. List of specific refactoring suggestions (prioritized by impact)
2. Refactored code implementing the suggestions
3. Explanation of why each change improves the code
4. Any trade-offs or considerations

Format as structured recommendations."""

        response = self._call_gpt4(prompt)
        self._update_usage_stats(response)
        refactored_code = self._extract_code_block(response)
        
        return {
            "suggestions": response,
            "refactored_code": refactored_code
        }

    def _call_gpt4(self, prompt: str, system_prompt: str = None) -> str:
        """Make a call to GPT-4 API.
        
        Args:
            prompt: User prompt/question
            system_prompt: System prompt for the model
            
        Returns:
            Model response
        """
        if system_prompt is None:
            system_prompt = """You are an expert Python code analyst and optimization AI. 
Your task is to analyze, improve, and enhance Python code. 
You provide detailed, practical suggestions with working code examples.
Always ensure code is syntactically correct and maintains original functionality while improving it."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4096,
                top_p=0.95
            )
            
            return response.choices[0].message.content
        
        except RateLimitError:
            return "Error: Rate limit exceeded. Please try again later."
        except APIError as e:
            return f"Error: API error occurred - {str(e)}"

    def _extract_code_block(self, response: str) -> str:
        """Extract code block from response.
        
        Args:
            response: Response containing code block
            
        Returns:
            Extracted code or empty string if not found
        """
        import re
        
        # Try to find python code block
        match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
        if match:
            return match.group(1)
        
        # Try generic code block
        match = re.search(r'```\n(.*?)\n```', response, re.DOTALL)
        if match:
            return match.group(1)
        
        return ""

    def _update_usage_stats(self, response: str) -> None:
        """Update usage statistics.
        
        Args:
            response: Response from API
        """
        self.usage_stats["total_requests"] += 1
        # Note: Actual token counting would require the usage object from API response
        # This is a simplified version

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics.
        
        Returns:
            Usage statistics
        """
        return self.usage_stats.copy()

    def reset_conversation(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []
