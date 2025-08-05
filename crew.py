"""
CrewAI Orchestration for Accessibility Plan Evaluation
"""

from crewai import Crew, Process
from agents import AccessibilityEvaluationAgents
from tasks import AccessibilityEvaluationTasks
from tools import PDFExtractorTool, PlanCollectorTool
from config import config
from typing import Dict, Any
import os
import json
from datetime import datetime
from pathlib import Path


class AccessibilityEvaluationCrew:
    """Main orchestration class for accessibility plan evaluation using CrewAI."""
    
    def __init__(self, model_name: str = None, temperature: float = None):
        """Initialize the evaluation crew."""
        self.model_name = model_name or config.default_model
        self.temperature = temperature or config.temperature
        
        # Initialize agent factory
        self.agent_factory = AccessibilityEvaluationAgents(
            model_name=self.model_name,
            temperature=self.temperature
        )
        
        # Initialize tools
        self.pdf_extractor = PDFExtractorTool()
        self.plan_collector = PlanCollectorTool()
        
        # Create output directory
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def evaluate_plans(self, audit_report_path: str, plans_directory: str) -> Dict[str, Any]:
        """
        Main method to evaluate accessibility plans using CrewAI.
        
        Args:
            audit_report_path: Path to the original accessibility audit report PDF
            plans_directory: Directory containing the remediation plan PDFs
            
        Returns:
            Dictionary containing evaluation results and scores
        """
        print(f"🚀 Starting accessibility plan evaluation...")
        print(f"📋 Audit report: {audit_report_path}")
        print(f"📁 Plans directory: {plans_directory}")
        
        # Step 1: Extract content from PDFs
        print("\n📄 Extracting content from PDFs...")
        audit_content = self._extract_audit_report(audit_report_path)
        plans_content = self._extract_plans(plans_directory)
        
        if not audit_content or not plans_content:
            raise ValueError("Failed to extract content from PDFs")
        
        print(f"✅ Extracted audit report ({len(audit_content)} characters)")
        print(f"✅ Extracted {len(plans_content)} plans")
        
        # Step 2: Create agents
        print("\n🤖 Creating evaluation agents...")
        agents = self._create_agents()
        
        # Step 3: Create tasks
        print("📋 Creating evaluation tasks...")
        tasks = self._create_tasks(agents, audit_content, plans_content)
        
        # Step 4: Create and run crew
        print("🏃 Running evaluation crew...")
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=config.verbose
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Step 5: Process and save results
        print("\n💾 Processing and saving results...")
        evaluation_results = self._process_results(result, plans_content.keys())
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"evaluation_report_{timestamp}.md"
        scores_file = self.output_dir / f"evaluation_scores_{timestamp}.json"
        
        self._save_results(evaluation_results, output_file, scores_file)
        
        print(f"✅ Evaluation complete!")
        print(f"📄 Report saved to: {output_file}")
        print(f"📊 Scores saved to: {scores_file}")
        
        return evaluation_results
    
    def _extract_audit_report(self, audit_report_path: str) -> str:
        """Extract content from the audit report PDF."""
        if not os.path.exists(audit_report_path):
            raise FileNotFoundError(f"Audit report not found: {audit_report_path}")
        
        content = self.pdf_extractor._run(audit_report_path)
        if content.startswith("Error:"):
            raise ValueError(f"Failed to extract audit report: {content}")
        
        return content
    
    def _extract_plans(self, plans_directory: str) -> Dict[str, str]:
        """Extract content from all plan PDFs in the directory."""
        if not os.path.exists(plans_directory):
            raise FileNotFoundError(f"Plans directory not found: {plans_directory}")
        
        plans = self.plan_collector._run(plans_directory)
        if "error" in plans:
            raise ValueError(f"Failed to extract plans: {plans['error']}")
        
        return plans
    
    def _create_agents(self) -> Dict[str, Any]:
        """Create all evaluation agents."""
        return {
            "strategic": self.agent_factory.create_strategic_evaluator(),
            "technical": self.agent_factory.create_technical_evaluator(),
            "comprehensive": self.agent_factory.create_comprehensive_evaluator(),
            "longterm": self.agent_factory.create_longterm_evaluator(),
            "synthesis": self.agent_factory.create_synthesis_agent()
        }
    
    def _create_tasks(self, agents: Dict[str, Any], audit_content: str, 
                     plans_content: Dict[str, str]) -> list:
        """Create all evaluation tasks."""
        tasks = []
        
        # Create evaluation tasks for each dimension
        strategic_task = AccessibilityEvaluationTasks.create_strategic_evaluation_task(
            agents["strategic"], audit_content, plans_content
        )
        tasks.append(strategic_task)
        
        technical_task = AccessibilityEvaluationTasks.create_technical_evaluation_task(
            agents["technical"], audit_content, plans_content
        )
        tasks.append(technical_task)
        
        comprehensive_task = AccessibilityEvaluationTasks.create_comprehensive_evaluation_task(
            agents["comprehensive"], audit_content, plans_content
        )
        tasks.append(comprehensive_task)
        
        longterm_task = AccessibilityEvaluationTasks.create_longterm_evaluation_task(
            agents["longterm"], audit_content, plans_content
        )
        tasks.append(longterm_task)
        
        # Create synthesis task (depends on all previous tasks)
        synthesis_task = AccessibilityEvaluationTasks.create_synthesis_task(
            agents["synthesis"],
            strategic_task.expected_output,
            technical_task.expected_output,
            comprehensive_task.expected_output,
            longterm_task.expected_output
        )
        tasks.append(synthesis_task)
        
        return tasks
    
    def _process_results(self, crew_result: Any, plan_names: list) -> Dict[str, Any]:
        """Process the crew execution results."""
        # Extract the final synthesis result
        final_report = str(crew_result)
        
        # Try to extract JSON scores from the report
        scores = self._extract_scores_from_report(final_report, plan_names)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "model_used": self.model_name,
            "evaluation_report": final_report,
            "scores": scores,
            "plan_names": list(plan_names),
            "evaluation_criteria": config.evaluation_criteria
        }
    
    def _extract_scores_from_report(self, report: str, plan_names: list) -> Dict[str, Any]:
        """Extract JSON scores from the evaluation report."""
        try:
            # Look for JSON block in the report
            json_start = report.rfind('```json')
            json_end = report.rfind('```')
            
            if json_start != -1 and json_end != -1 and json_start < json_end:
                json_str = report[json_start + 7:json_end].strip()
                scores = json.loads(json_str)
                return scores
            else:
                # Fallback: create placeholder scores
                return {plan_name: {"score": 0.0, "rationale": "Score extraction failed"} 
                       for plan_name in plan_names}
        except Exception as e:
            print(f"⚠️ Failed to extract scores: {e}")
            return {plan_name: {"score": 0.0, "rationale": "Score extraction failed"} 
                   for plan_name in plan_names}
    
    def _save_results(self, results: Dict[str, Any], report_path: Path, scores_path: Path):
        """Save evaluation results to files."""
        # Save the full report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Accessibility Plan Evaluation Report\n\n")
            f.write(f"**Generated:** {results['timestamp']}\n")
            f.write(f"**Model:** {results['model_used']}\n")
            f.write(f"**Plans Evaluated:** {', '.join(results['plan_names'])}\n\n")
            f.write("---\n\n")
            f.write(results['evaluation_report'])
        
        # Save the scores as JSON
        with open(scores_path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "timestamp": results['timestamp'],
                    "model_used": results['model_used'],
                    "plan_names": results['plan_names'],
                    "evaluation_criteria": results['evaluation_criteria']
                },
                "scores": results['scores']
            }, f, indent=2, ensure_ascii=False)


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate accessibility remediation plans using CrewAI")
    parser.add_argument("--audit-report", required=True, help="Path to the audit report PDF")
    parser.add_argument("--plans-dir", required=True, help="Directory containing plan PDFs")
    parser.add_argument("--model", help="LLM model to use", default=config.default_model)
    parser.add_argument("--output-dir", help="Output directory", default=config.output_dir)
    
    args = parser.parse_args()
    
    # Update config if needed
    if args.output_dir != config.output_dir:
        config.output_dir = args.output_dir
    
    # Create and run evaluation crew
    crew = AccessibilityEvaluationCrew(model_name=args.model)
    results = crew.evaluate_plans(args.audit_report, args.plans_dir)
    
    print(f"\n🎉 Evaluation completed successfully!")
    return results


if __name__ == "__main__":
    main()
