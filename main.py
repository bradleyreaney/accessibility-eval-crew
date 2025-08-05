"""
Main entry point for the Accessibility Plan Evaluation System
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from crew import AccessibilityEvaluationCrew
from config import config


def validate_inputs(audit_report: str, plans_dir: str) -> tuple[bool, str]:
    """Validate input files and directories."""
    if not os.path.exists(audit_report):
        return False, f"Audit report not found: {audit_report}"
    
    if not audit_report.lower().endswith('.pdf'):
        return False, f"Audit report must be a PDF file: {audit_report}"
    
    if not os.path.exists(plans_dir):
        return False, f"Plans directory not found: {plans_dir}"
    
    if not os.path.isdir(plans_dir):
        return False, f"Plans path is not a directory: {plans_dir}"
    
    # Check for PDF files in plans directory
    pdf_files = list(Path(plans_dir).glob("*.pdf"))
    if not pdf_files:
        return False, f"No PDF files found in plans directory: {plans_dir}"
    
    return True, "Inputs are valid"


def check_api_keys() -> tuple[bool, str]:
    """Check if required API keys are available."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if not openai_key and not google_key:
        return False, "No API keys found. Please set OPENAI_API_KEY or GOOGLE_API_KEY in your .env file"
    
    if not openai_key:
        print("⚠️ OpenAI API key not found. Some models may not be available.")
    
    if not google_key:
        print("⚠️ Google API key not found. Gemini models will not be available.")
    
    return True, "API keys are configured"


def print_banner():
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        🚀 Accessibility Plan Evaluation System 🚀           ║
║                                                               ║
║     Powered by CrewAI • Expert LLM Judges • WCAG Analysis    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main application entry point."""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Evaluate accessibility remediation plans using CrewAI and LLM judges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation
  python main.py --audit-report audit.pdf --plans-dir plans/
  
  # Use specific model
  python main.py --audit-report audit.pdf --plans-dir plans/ --model gpt-4-turbo-preview
  
  # Custom output location
  python main.py --audit-report audit.pdf --plans-dir plans/ --output-dir results/
        """
    )
    
    parser.add_argument(
        "--audit-report", 
        required=True, 
        help="Path to the original accessibility audit report (PDF)"
    )
    parser.add_argument(
        "--plans-dir", 
        required=True, 
        help="Directory containing remediation plan PDFs to evaluate"
    )
    parser.add_argument(
        "--model", 
        help=f"LLM model to use (default: {config.default_model})",
        default=config.default_model
    )
    parser.add_argument(
        "--output-dir", 
        help=f"Output directory for results (default: {config.output_dir})",
        default=config.output_dir
    )
    parser.add_argument(
        "--temperature", 
        type=float,
        help=f"Model temperature for creativity vs consistency (default: {config.temperature})",
        default=config.temperature
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    print("🔍 Validating inputs...")
    valid, message = validate_inputs(args.audit_report, args.plans_dir)
    if not valid:
        print(f"❌ {message}")
        sys.exit(1)
    print(f"✅ {message}")
    
    # Check API keys
    print("🔑 Checking API keys...")
    valid, message = check_api_keys()
    if not valid:
        print(f"❌ {message}")
        print("\n💡 Tip: Copy .env.example to .env and add your API keys")
        sys.exit(1)
    print(f"✅ {message}")
    
    # Update configuration
    if args.output_dir != config.output_dir:
        config.output_dir = args.output_dir
    if args.verbose:
        config.verbose = True
    
    # Show configuration
    print(f"\n⚙️  Configuration:")
    print(f"   Model: {args.model}")
    print(f"   Temperature: {args.temperature}")
    print(f"   Output Directory: {args.output_dir}")
    print(f"   Audit Report: {args.audit_report}")
    print(f"   Plans Directory: {args.plans_dir}")
    
    # Count plans
    pdf_files = list(Path(args.plans_dir).glob("*.pdf"))
    print(f"   Plans to Evaluate: {len(pdf_files)}")
    
    try:
        # Create and run evaluation crew
        print(f"\n🏗️  Initializing evaluation crew...")
        crew = AccessibilityEvaluationCrew(
            model_name=args.model,
            temperature=args.temperature
        )
        
        print(f"🚀 Starting evaluation process...")
        results = crew.evaluate_plans(args.audit_report, args.plans_dir)
        
        # Show summary
        print(f"\n📊 Evaluation Summary:")
        if "scores" in results:
            for plan_name, score_data in results["scores"].items():
                score = score_data.get("score", 0)
                print(f"   {plan_name}: {score:.1f}/10")
        
        print(f"\n🎉 Evaluation completed successfully!")
        print(f"📁 Results saved to: {args.output_dir}/")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
