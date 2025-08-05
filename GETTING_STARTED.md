# 🚀 Getting Started with Accessibility Plan Evaluation

Welcome to your new CrewAI-powered accessibility evaluation system! This guide will help you get up and running quickly.

## 🎯 What This System Does

This system evaluates accessibility remediation plans using AI agents as expert judges. It:

1. **Extracts text** from PDF reports and plans
2. **Evaluates plans** against WCAG criteria using specialized AI agents
3. **Provides scores** and detailed analysis
4. **Identifies gaps** and suggests improvements
5. **Creates champion plan** recommendations

## 🏃 Quick Start (2 Minutes)

### Option 1: Simple Mode (Recommended First Try)

No API keys needed - generates evaluation prompts for manual LLM use:

1. **Test with sample data first**:
   ```bash
   python simple_eval.py --audit-report data/sample-data/sample-audit-report.pdf --plans-dir data/sample-data/
   ```

2. **Add your own files**:
   - Copy your audit report to `data/audit-reports/`
   - Copy your remediation plans to `data/remediation-plans/`
   - Run: `python simple_eval.py --audit-report data/audit-reports/your-audit.pdf --plans-dir data/remediation-plans/`

3. **Check the results** in the `outputs/` folder
4. **Copy the generated prompt** to ChatGPT, Claude, or your preferred LLM

### Option 2: Full Automated Mode

Requires API keys but runs everything automatically:

1. **Set up your API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI or Google API key
   ```

2. **Run the full evaluation**:
   ```bash
   python main.py --audit-report data/audit-reports/your-audit.pdf --plans-dir data/remediation-plans/
   ```

## 🎮 Using VS Code Tasks

The easiest way to run evaluations:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "Test with Sample Data" to try the system, or "Evaluate Plans in Data Directory" for your own files

## 📁 Project Data Structure

The project now includes a dedicated `data/` directory for all your PDF files:

```
data/
├── audit-reports/          # Place your audit reports here
├── remediation-plans/      # Place your remediation plans here
└── sample-data/           # Sample files for testing
    ├── sample-audit-report.pdf
    ├── sample-chatgpt-plan.pdf
    └── sample-gemini-plan.pdf
```

### Adding Your Files
1. **Audit Reports**: Copy to `data/audit-reports/`
2. **Remediation Plans**: Copy to `data/remediation-plans/`
3. **Run Evaluation**: Use the VS Code task or command line

## 📁 Understanding the Output

After running an evaluation, check the `outputs/` folder:

- **`evaluation_prompt_*.md`**: Ready-to-use prompt for LLMs
- **`extracted_content_*.json`**: Raw extracted content from PDFs
- **`evaluation_report_*.md`**: Full evaluation report (automated mode)
- **`evaluation_scores_*.json`**: Structured scoring data (automated mode)

## 🔧 Configuration

Edit the `.env` file to customize:

```bash
# LLM Configuration
DEFAULT_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.1

# Evaluation Weights (must sum to 1.0)
STRATEGIC_WEIGHT=0.4      # Strategic prioritization
TECHNICAL_WEIGHT=0.3      # Technical specificity
COMPREHENSIVE_WEIGHT=0.2  # Comprehensiveness
LONGTERM_WEIGHT=0.1       # Long-term vision

# Output
OUTPUT_DIR=outputs
VERBOSE=true
```

### Available Models
- **OpenAI**: `gpt-4-turbo-preview`, `gpt-4`, `gpt-3.5-turbo`
- **Google Gemini**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro`

## 🚨 Troubleshooting

### PDF Extraction Issues
- Ensure PDF files are not password-protected
- Check file paths are correct
- Try both extraction methods (pdfplumber and PyPDF2)

### API Key Issues
- Verify your API key is set in `.env`
- Check you have sufficient API credits
- Try the simple mode first to test extraction

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version is 3.8+

## 💡 Tips for Best Results

1. **Start with simple mode** to verify PDF extraction works
2. **Review extracted content** in the JSON files to ensure quality
3. **Adjust evaluation weights** in `.env` based on your priorities
4. **Use verbose mode** (`--verbose`) for detailed agent output
5. **Save API costs** by testing with simple mode first

## 📚 Next Steps

1. **Test the system** with your existing files
2. **Review the evaluation criteria** in `prompts/evaluation_prompt.md`
3. **Customize the agents** in `agents/evaluation_agents.py` if needed
4. **Adjust scoring weights** in the configuration
5. **Scale up** to evaluate multiple plan sets

## 🆘 Need Help?

- Check the `README.md` for detailed documentation
- Review the `test_system.py` for diagnostic information
- Look at the example outputs in the `outputs/` folder
- Examine the evaluation prompt template in `prompts/`

**Ready to evaluate some accessibility plans? Run your first evaluation now!** 🎉
