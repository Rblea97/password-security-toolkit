# Contributing

Thank you for your interest in contributing to SecurePass Toolkit!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Rblea97/password-security-toolkit.git
cd password-security-toolkit/src

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install pytest pytest-cov black mypy

# Verify setup
pytest tests/ -v
```

## Code Standards

### Formatting
All code must be formatted with [Black](https://black.readthedocs.io/):
```bash
black src/
```

### Type Hints
All functions must include type hints:
```python
def analyze_password(password: str, check_breach: bool = True) -> PasswordAnalysis:
    ...
```

### Docstrings
Use Google-style docstrings:
```python
def calculate_entropy(password: str) -> float:
    """Calculate Shannon entropy of a password in bits.

    Args:
        password: The password string to analyze.

    Returns:
        Entropy value in bits.

    Raises:
        ValueError: If password is empty.
    """
```

## Testing

### Running Tests
```bash
# All tests
pytest src/tests/ -v

# With coverage
pytest src/tests/ --cov=securepass --cov-report=term

# Single test file
pytest src/tests/test_entropy.py -v
```

### Writing Tests
- New features require tests before implementation (TDD)
- Target >80% coverage for new code
- Use `unittest.mock` for external dependencies (HTTP calls, file I/O)
- Include edge cases: empty input, boundary values, error conditions

### Test Organization
```
src/tests/
├── test_analyzer.py     # Core analyzer tests
├── test_entropy.py      # Entropy calculation tests
├── test_generator.py    # Password generation tests
├── test_breach.py       # Breach checker tests (mocked HTTP)
├── test_patterns.py     # Pattern detection tests
├── test_wordlist.py     # Wordlist checker tests
├── test_commands.py     # CLI command tests
├── test_formatters.py   # Output formatting tests
└── test_models.py       # Data model tests
```

## Pull Request Process

1. Fork the repository and create a feature branch
2. Write tests for your changes
3. Implement the feature/fix
4. Ensure all tests pass: `pytest src/tests/ -v`
5. Format your code: `black src/`
6. Update CHANGELOG.md with your changes
7. Open a pull request using the PR template

### PR Review Criteria
- All existing tests pass
- New code has test coverage
- Code is formatted with Black
- Type hints are included
- No security regressions (check with `bandit -r src/securepass/`)
