"""
PDF Processing Tools for Accessibility Plan Evaluation
"""

import os
import PyPDF2
import pdfplumber
from typing import List, Dict, Optional
from pathlib import Path


class BaseTool:
    """Simple base tool class to replace crewai_tools.BaseTool."""
    name: str = ""
    description: str = ""
    
    def _run(self, *args, **kwargs):
        raise NotImplementedError


class PDFExtractorTool(BaseTool):
    """Tool for extracting text from PDF files with fallback methods."""
    
    name: str = "PDF Text Extractor"
    description: str = "Extracts text content from PDF files using multiple methods for best results"
    
    def _run(self, file_path: str) -> str:
        """
        Extract text from a PDF file using multiple extraction methods.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        # Try pdfplumber first (better for complex layouts)
        try:
            text = self._extract_with_pdfplumber(file_path)
            if text and len(text.strip()) > 100:  # Reasonable content threshold
                return text
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
        
        # Fallback to PyPDF2
        try:
            text = self._extract_with_pypdf2(file_path)
            if text and len(text.strip()) > 50:
                return text
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
        
        return f"Error: Could not extract text from {file_path}"
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber (better for tables and complex layouts)."""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2 (fallback method)."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()


class PlanCollectorTool(BaseTool):
    """Tool for collecting and organizing multiple remediation plans."""
    
    name: str = "Plan Collector"
    description: str = "Collects and organizes multiple accessibility remediation plans from a directory"
    
    def _run(self, plans_directory: str) -> Dict[str, str]:
        """
        Collect all PDF plans from a directory and extract their content.
        
        Args:
            plans_directory: Directory containing PDF plan files
            
        Returns:
            Dictionary mapping plan names to their extracted content
        """
        if not os.path.exists(plans_directory):
            return {"error": f"Directory not found: {plans_directory}"}
        
        pdf_extractor = PDFExtractorTool()
        plans = {}
        
        # Get all PDF files in the directory
        pdf_files = list(Path(plans_directory).glob("*.pdf"))
        
        if not pdf_files:
            return {"error": f"No PDF files found in {plans_directory}"}
        
        for pdf_file in pdf_files:
            plan_name = self._generate_plan_name(pdf_file.name)
            content = pdf_extractor._run(str(pdf_file))
            
            if not content.startswith("Error:"):
                plans[plan_name] = content
            else:
                print(f"Failed to extract content from {pdf_file.name}: {content}")
        
        return plans
    
    def _generate_plan_name(self, filename: str) -> str:
        """Generate a clean plan name from filename."""
        # Remove extension and clean up the name
        name = filename.replace('.pdf', '')
        
        # Convert common patterns to plan letters
        plan_mapping = {
            'ChatGPT GPT-4o - a11y plan': 'Plan A',
            'ChatGPT GPT-4o Deep Research - a11y plan': 'Plan B',
            'ChatGPT GPT-4o Think Longer - a11y plan': 'Plan C',
            'Gemini 2.5 Flash - a11y plan': 'Plan D',
            'Gemini 2.5 Pro - a11y plan': 'Plan E',
            'Gemini 2.5 Pro Deep Research- a11y plan': 'Plan F',
            'Grok-3 Fast - a11y plan': 'Plan G'
        }
        
        return plan_mapping.get(name, name)


class DocumentStructureTool(BaseTool):
    """Tool for structuring extracted documents for evaluation."""
    
    name: str = "Document Structure Tool"
    description: str = "Structures extracted document content for evaluation prompt formatting"
    
    def _run(self, audit_report: str, plans: Dict[str, str]) -> str:
        """
        Structure the audit report and plans into the evaluation prompt format.
        
        Args:
            audit_report: Extracted audit report content
            plans: Dictionary of plan names to content
            
        Returns:
            Formatted content ready for evaluation prompt
        """
        # Load the evaluation prompt template
        prompt_template = self._load_evaluation_prompt()
        
        # Insert audit report
        formatted_prompt = prompt_template.replace(
            "### CONTEXT: ACCESSIBILITY AUDIT FINDINGS", 
            f"### CONTEXT: ACCESSIBILITY AUDIT FINDINGS\n\n{audit_report}"
        )
        
        # Insert each plan
        plans_section = "### CANDIDATE REMEDIATION PLANS\n\nHere are the remediation plans you must evaluate:\n\n"
        
        for plan_name, content in plans.items():
            plans_section += f"#### {plan_name}:\n\n{content}\n\n"
        
        formatted_prompt = formatted_prompt.replace(
            "### CANDIDATE REMEDIATION PLANS\n\nHere are the remediation plans you must evaluate:",
            plans_section
        )
        
        return formatted_prompt
    
    def _load_evaluation_prompt(self) -> str:
        """Load the evaluation prompt template."""
        # This will be loaded from the evaluation prompt file
        prompt_path = Path(__file__).parent.parent / "prompts" / "evaluation_prompt.md"
        
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Fallback to a basic template
            return self._get_basic_prompt_template()
    
    def _get_basic_prompt_template(self) -> str:
        """Basic evaluation prompt template as fallback."""
        return """### PERSONA

You are an expert digital accessibility consultant with deep knowledge of WCAG 2.1 and 2.2.

### CORE TASK

Evaluate and compare accessibility remediation plans, providing detailed analysis and scoring.

### CONTEXT: ACCESSIBILITY AUDIT FINDINGS



### CANDIDATE REMEDIATION PLANS

Here are the remediation plans you must evaluate:

### EVALUATION FRAMEWORK & OUTPUT STRUCTURE

Provide comprehensive evaluation with scoring based on:
- Strategic Prioritization (40%)
- Technical Specificity (30%) 
- Comprehensiveness (20%)
- Long-Term Vision (10%)

End with JSON scoring format."""
