# Audit Reports

Place your original accessibility audit reports in this directory.

## What Goes Here
- Original accessibility audit reports (PDF format)
- Baseline reports that identify accessibility issues and violations
- WCAG compliance assessments
- Third-party accessibility evaluation reports

## Example Files
- `website-accessibility-audit-2024.pdf`
- `mobile-app-wcag-assessment.pdf` 
- `ecommerce-site-audit-report.pdf`

## Usage
Reference these files with the `--audit-report` parameter:
```bash
python simple_eval.py --audit-report data/audit-reports/your-audit.pdf --plans-dir data/remediation-plans/
```
