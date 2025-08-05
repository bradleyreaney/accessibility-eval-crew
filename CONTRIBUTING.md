# Contributing to Accessibility Plan Evaluation System

Thank you for your interest in contributing to this project! This guide will help you get started.

## Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/accessibility-eval-crew.git
   cd accessibility-eval-crew
   ```

2. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Test the setup**:
   ```bash
   python test_system.py
   ```

## Project Structure

- `agents/` - CrewAI agent definitions for evaluation
- `tasks/` - Task definitions for different evaluation aspects
- `tools/` - PDF processing and utility tools
- `config/` - Configuration management
- `prompts/` - Evaluation prompt templates
- `data/` - Sample data and user PDF storage

## Types of Contributions

### 🐛 Bug Reports
- Use the issue template
- Include system information
- Provide steps to reproduce

### ✨ Feature Requests
- Describe the use case
- Explain the expected behavior
- Consider accessibility impact

### 🔧 Code Contributions
- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure accessibility compliance

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Include docstrings for public functions
- Keep functions focused and small

### Testing
- Test with sample data before submitting
- Verify PDF extraction works correctly
- Test both simple and full evaluation modes

### Documentation
- Update README.md for new features
- Add docstrings to new functions
- Update GETTING_STARTED.md if needed

## Accessibility Focus

This project is about accessibility evaluation, so contributions should:
- Consider diverse user needs
- Follow WCAG guidelines in any UI changes
- Use semantic HTML and ARIA where appropriate
- Test with assistive technologies when possible

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Test thoroughly
   - Update documentation

3. **Submit pull request**:
   - Use the PR template
   - Link to related issues
   - Describe your changes clearly

4. **Code review**:
   - Address feedback promptly
   - Keep discussions constructive
   - Be open to suggestions

## Areas for Contribution

### High Priority
- Additional LLM provider support
- Improved PDF text extraction
- Better error handling
- Performance optimizations

### Medium Priority
- Additional evaluation criteria
- Custom prompt templates
- Batch processing capabilities
- Export format options

### Ideas Welcome
- Web interface
- API endpoints
- Integration with accessibility tools
- Automated report generation

## Questions?

- Open an issue for questions
- Check existing issues first
- Be respectful and constructive

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment
- Remember we're all learning

Thank you for contributing to making digital accessibility evaluation better! 🌟
