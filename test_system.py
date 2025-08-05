"""
Simple test script to verify the system is working
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from config import config
        print("✅ Config imported successfully")
        
        from tools.pdf_tools import PDFExtractorTool
        print("✅ PDF tools imported successfully")
        
        from agents.evaluation_agents import AccessibilityEvaluationAgents
        print("✅ Agents imported successfully")
        
        from tasks.evaluation_tasks import AccessibilityEvaluationTasks
        print("✅ Tasks imported successfully")
        
        print("🎉 All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import config
        
        print(f"Default model: {config.default_model}")
        print(f"Temperature: {config.temperature}")
        print(f"Output directory: {config.output_dir}")
        print(f"Weights sum to 1.0: {config.validate_weights()}")
        
        # Test API key status
        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")
        
        print(f"OpenAI API key: {'✅ Set' if openai_key else '❌ Not set'}")
        print(f"Google API key: {'✅ Set' if google_key else '❌ Not set'}")
        
        if not openai_key and not google_key:
            print("⚠️ No API keys found. Please set up .env file with API keys.")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_pdf_extraction():
    """Test PDF extraction on a sample file."""
    print("\n📄 Testing PDF extraction...")
    
    try:
        from tools.pdf_tools import PDFExtractorTool
        
        # Look for the audit report
        audit_path = Path("../../../1 - Original Report/Accessibility Report - TOA.pdf")
        
        if not audit_path.exists():
            print(f"⚠️ Audit report not found at {audit_path}")
            print("   This is expected if running outside the full workspace")
            return True
        
        extractor = PDFExtractorTool()
        content = extractor._run(str(audit_path))
        
        if content.startswith("Error:"):
            print(f"❌ PDF extraction failed: {content}")
            return False
        
        print(f"✅ PDF extracted successfully ({len(content)} characters)")
        print(f"First 200 characters: {content[:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ PDF extraction test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running system tests...\n")
    
    tests = [
        test_imports,
        test_configuration,
        test_pdf_extraction
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Test Results:")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! System is ready to use.")
        print("\n💡 Next steps:")
        print("1. Set up your .env file with API keys (copy from .env.example)")
        print("2. Run the evaluation with: python main.py --audit-report [path] --plans-dir [path]")
        print("3. Or use VS Code tasks from the Command Palette (Ctrl+Shift+P)")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
