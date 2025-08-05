# Accessibility Plan Evaluation System

A CrewAI-powered system for evaluating web accessibility remediation plans using LLMs as expert judges.

## 🚀 Quick Start from GitHub

```bash
# Clone the repository
git clone https://github.com/yourusername/accessibility-eval-crew.git
cd accessibility-eval-crew

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test with sample data
python simple_eval.py --audit-report data/sample-data/sample-audit-report.pdf --plans-dir data/sample-data/
```

## Features

- **PDF Text Extraction**: Automatically extracts text from accessibility reports and remediation plans
- **Multi-Agent Evaluation**: Uses specialized CrewAI agents for comprehensive assessment
- **WCAG Compliance Analysis**: Evaluates plans against Web Content Accessibility Guidelines
- **Gap Analysis**: Identifies missing elements and improvement opportunities  
- **Structured Scoring**: Provides weighted scores based on strategic, technical, and structural criteria
- **Champion Plan Synthesis**: Generates recommendations for optimal remediation strategies

## Quick Start

### Option 1: Simplified Evaluation (No API Keys Required)

1. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Simple Evaluation** (generates prompt for manual LLM use):
   ```bash
   python simple_eval.py --audit-report path/to/audit.pdf --plans-dir path/to/plans/
   ```

### Option 2: Full Automated Evaluation (Requires API Keys)

1. **Install Dependencies** (same as above)

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI or Google API keys
   ```

3. **Run Full Evaluation**:
   ```bash
   python main.py --audit-report path/to/audit.pdf --plans-dir path/to/plans/
   ```

## Project Structure

```
accessibility-eval-crew/
├── agents/              # CrewAI agent definitions
├── tasks/               # Task definitions for agents
├── tools/               # Custom tools for PDF processing
├── config/              # Configuration files
├── prompts/             # Evaluation prompt templates
├── data/                # PDF files for evaluation
│   ├── audit-reports/   # Original accessibility audit reports
│   ├── remediation-plans/ # Plans to be evaluated
│   └── sample-data/     # Sample files for testing
├── outputs/             # Generated evaluation reports
├── main.py              # Main execution script (full CrewAI)
├── simple_eval.py       # Simplified evaluation (no API keys)
├── crew.py              # CrewAI setup and orchestration
└── requirements.txt     # Python dependencies
```

## Configuration

The system uses weighted evaluation criteria:
- **Strategic Prioritization (40%)**: Task sequencing and user impact
- **Technical Specificity (30%)**: Solution clarity and correctness  
- **Comprehensiveness (20%)**: Complete coverage and structure
- **Long-Term Vision (10%)**: Sustainability and monitoring provisions

## Usage Examples

### Basic Evaluation (Simplified)
```bash
# Test with sample data
python simple_eval.py --audit-report data/sample-data/sample-audit-report.pdf --plans-dir data/sample-data/

# Use your own files
python simple_eval.py --audit-report data/audit-reports/your-audit.pdf --plans-dir data/remediation-plans/
```

### Full Automated Evaluation
```bash
python main.py --audit-report data/audit-reports/your-audit.pdf --plans-dir data/remediation-plans/
```

### Custom Configuration
```bash
python main.py --config custom_config.yaml --output-dir results/
```

### VS Code Tasks
- Use `Ctrl+Shift+P` → `Tasks: Run Task` to access pre-configured tasks
- Available tasks: "Run Accessibility Evaluation", "Test PDF Extraction", etc.

## How It Works

### 1. PDF Processing
The system extracts text from PDF files using multiple methods (pdfplumber, PyPDF2) for best results.

### 2. Evaluation Framework
Plans are evaluated on four weighted criteria:
- **Strategic Prioritization (40%)**: Task sequencing and user impact logic
- **Technical Specificity (30%)**: Solution clarity and correctness  
- **Comprehensiveness (20%)**: Complete coverage and structure
- **Long-Term Vision (10%)**: Sustainability and monitoring provisions

### 3. Multi-Agent Analysis
- **Strategic Agent**: Evaluates prioritization and sequencing logic
- **Technical Agent**: Assesses solution specificity and correctness
- **Comprehensive Agent**: Checks coverage and POUR principle understanding
- **Long-term Agent**: Reviews sustainability and continuous improvement
- **Synthesis Agent**: Creates final recommendations and champion plan

### 4. Output Generation
- Detailed evaluation reports (Markdown)
- Structured scores (JSON)
- Gap analysis and recommendations
- Champion plan synthesis

## Output

The system generates:
- Detailed evaluation report (Markdown)
- Structured scores (JSON)
- Gap analysis recommendations
- Champion plan synthesis suggestions

## Requirements

- Python 3.8+
- OpenAI API key (or other LLM provider)
- PDF files for audit report and remediation plans
