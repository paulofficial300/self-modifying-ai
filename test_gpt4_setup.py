"""Test script to verify GPT-4 integration is working."""

import os
import sys

# Check if API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY environment variable not set!")
    print("Set it with: export OPENAI_API_KEY='your-key-here'")
    sys.exit(1)

print("✓ API Key found")

# Try to import and initialize
try:
    from core.ai_engine import AIEngine
    print("✓ AIEngine imported successfully")
    
    engine = AIEngine()
    print("✓ AIEngine initialized")
    print(f"  Model: {engine.model}")
    print(f"  LLM Status: Connected")
    
    # Try to analyze the example code
    if os.path.exists("example_code.py"):
        print("\n📝 Analyzing example_code.py...")
        analysis = engine.analyze_own_code("example_code.py")
        print("Analysis complete!")
        print(f"  File: {analysis['file']}")
        print(f"  Code length: {analysis['code_length']} characters")
        print("\nFull analysis:")
        print(analysis)
    else:
        print("❌ example_code.py not found")
        print("Create it with sample code first")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All checks passed!")
