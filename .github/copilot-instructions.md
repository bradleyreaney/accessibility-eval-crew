<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Accessibility Plan Evaluation System - Copilot Instructions

This is a CrewAI-based Python project for evaluating web accessibility remediation plans using LLMs as expert judges.

## Key Technologies
- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM integration and prompt management
- **PyPDF2/pdfplumber**: PDF text extraction
- **Pydantic**: Data validation and settings management

## Code Style Guidelines
- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all classes and functions
- Use descriptive variable names that reflect accessibility domain concepts

## Domain Knowledge
- Focus on WCAG 2.1/2.2 compliance (A and AA levels)
- Understand POUR principles (Perceivable, Operable, Understandable, Robust)
- Consider user impact and real-world accessibility barriers
- Prioritize strategic, multi-factor approaches over simple checklists

## Architecture Patterns
- Use CrewAI agents for specialized evaluation tasks
- Implement clean separation between PDF processing and evaluation logic
- Create reusable prompt templates for different evaluation criteria
- Design for extensibility to support additional LLM providers

## Testing Considerations
- Mock LLM API calls for unit tests
- Include sample PDF files for integration testing
- Validate JSON output schema for scoring results
- Test error handling for malformed or inaccessible PDF files
