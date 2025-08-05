"""
Simplified evaluation script that works without full CrewAI setup
This can be used for testing and demonstration purposes
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from tools.pdf_tools import PDFExtractorTool, PlanCollectorTool
from config import config


def create_evaluation_prompt(audit_content: str, plans_content: dict) -> str:
    """Create the evaluation prompt with audit and plans content."""
    
    # Load the evaluation prompt template
    prompt_path = Path(__file__).parent / "prompts" / "evaluation_prompt.md"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Insert audit report
    prompt_with_audit = prompt_template.replace(
        "### CONTEXT: ACCESSIBILITY AUDIT FINDINGS", 
        f"### CONTEXT: ACCESSIBILITY AUDIT FINDINGS\n\n{audit_content}"
    )
    
    # Insert plans
    plans_section = "### CANDIDATE REMEDIATION PLANS\n\nHere are the remediation plans you must evaluate:\n\n"
    
    for plan_name, content in plans_content.items():
        plans_section += f"#### {plan_name}:\n\n{content}\n\n"
    
    final_prompt = prompt_with_audit.replace(
        "### CANDIDATE REMEDIATION PLANS\n\nHere are the remediation plans you must evaluate:\n\n#### Plan A:\n\n#### Plan B:",
        plans_section.rstrip()
    )
    
    return final_prompt


def simple_evaluate(audit_report_path: str, plans_directory: str) -> dict:
    """
    Simple evaluation that extracts content and creates the evaluation prompt.
    This demonstrates the system without requiring full LLM integration.
    """
    
    print(f"🚀 Starting simplified accessibility plan evaluation...")
    print(f"📋 Audit report: {audit_report_path}")
    print(f"📁 Plans directory: {plans_directory}")
    
    # Step 1: Extract content from PDFs
    print("\n📄 Extracting content from PDFs...")
    
    pdf_extractor = PDFExtractorTool()
    plan_collector = PlanCollectorTool()
    
    # Extract audit report
    audit_content = pdf_extractor._run(audit_report_path)
    if audit_content.startswith("Error:"):
        raise ValueError(f"Failed to extract audit report: {audit_content}")
    
    print(f"✅ Extracted audit report ({len(audit_content)} characters)")
    
    # Extract plans
    plans_content = plan_collector._run(plans_directory)
    if "error" in plans_content:
        raise ValueError(f"Failed to extract plans: {plans_content['error']}")
    
    print(f"✅ Extracted {len(plans_content)} plans:")
    for plan_name in plans_content.keys():
        print(f"   - {plan_name}")
    
    # Step 2: Create evaluation prompt
    print("\n📝 Creating evaluation prompt...")
    evaluation_prompt = create_evaluation_prompt(audit_content, plans_content)
    
    # Step 3: Save results
    print("\n💾 Saving results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory
    output_dir = Path(config.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Save the evaluation prompt
    prompt_file = output_dir / f"evaluation_prompt_{timestamp}.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(f"# Accessibility Plan Evaluation Prompt\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Audit Report:** {audit_report_path}\n")
        f.write(f"**Plans Directory:** {plans_directory}\n")
        f.write(f"**Plans Count:** {len(plans_content)}\n\n")
        f.write("---\n\n")
        f.write(evaluation_prompt)
    
    # Save extracted content as JSON for further processing
    content_file = output_dir / f"extracted_content_{timestamp}.json"
    with open(content_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "audit_report_path": audit_report_path,
            "plans_directory": plans_directory,
            "audit_content": audit_content,
            "plans_content": plans_content,
            "evaluation_prompt": evaluation_prompt
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Evaluation prompt saved to: {prompt_file}")
    print(f"✅ Extracted content saved to: {content_file}")
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Copy the evaluation prompt to your preferred LLM interface")
    print(f"2. Or set up API keys in .env to use the full CrewAI system")
    print(f"3. The prompt is ready to be used with any capable LLM for evaluation")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "audit_report_path": audit_report_path,
        "plans_directory": plans_directory,
        "plans_count": len(plans_content),
        "prompt_file": str(prompt_file),
        "content_file": str(content_file),
        "evaluation_prompt_length": len(evaluation_prompt),
        "audit_content_length": len(audit_content),
        "total_plans_content_length": sum(len(content) for content in plans_content.values())
    }


def main():
    """Main function for simplified evaluation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple accessibility plan evaluation (prompt generation)")
    parser.add_argument("--audit-report", required=True, help="Path to the audit report PDF")
    parser.add_argument("--plans-dir", required=True, help="Directory containing plan PDFs")
    
    args = parser.parse_args()
    
    try:
        results = simple_evaluate(args.audit_report, args.plans_dir)
        
        print(f"\n📊 Summary:")
        print(f"   Plans evaluated: {results['plans_count']}")
        print(f"   Prompt length: {results['evaluation_prompt_length']:,} characters")
        print(f"   Total content: {results['total_plans_content_length']:,} characters")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
