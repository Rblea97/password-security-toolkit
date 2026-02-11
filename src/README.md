# SecurePass Toolkit 🔒

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-111%20passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)](tests/)

A professional command-line password security analysis tool for cybersecurity learners and practitioners.

---

## 🎯 Overview

SecurePass Toolkit is an **entry-level cybersecurity project** that demonstrates practical understanding of password security, cryptographic hashing, and secure coding practices. Built as a portfolio piece for cybersecurity students, it showcases real-world security tools development.

### Why This Project?

- ✅ **Educational**: Learn cryptographic concepts hands-on
- ✅ **Practical**: Actually usable for password auditing
- ✅ **Portfolio-Ready**: Demonstrates security awareness to employers
- ✅ **Best Practices**: Follows NIST & OWASP guidelines

---

## ✨ Features

### 🔍 Password Strength Analysis
- **0-100 Scoring System**: Comprehensive strength evaluation
- **Entropy Calculation**: Shannon entropy in bits with crack time estimates
- **8 Security Criteria**: Length, character diversity, pattern detection
- **Detailed Reports**: Clear, actionable recommendations

### 🛡️ Breach Detection
- **850M+ Passwords**: Check against Have I Been Pwned database
- **K-Anonymity**: Never sends your password over the network
- **Privacy First**: Only first 5 hash characters transmitted

### 🎲 Secure Password Generation
- **Cryptographically Secure**: Uses Python's `secrets` module
- **Customizable**: Length, character sets, ambiguous character exclusion
- **Validated**: Generated passwords automatically analyzed

### 📊 Batch Processing
- **File Analysis**: Process multiple passwords at once
- **Summary Reports**: Statistics and weakest passwords identified
- **Export Options**: JSON, CSV, or text format

### 🎨 User-Friendly CLI
- **Colorized Output**: Red/yellow/green strength indicators
- **Clear Metrics**: Entropy, crack time, breach status
- **Secure Input**: No password echo to terminal

---

## 📖 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Security Features](#-security-features)
- [Educational Value](#-educational-value)
- [Architecture](#-architecture)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/Rblea97/password-security-toolkit.git
cd securepass-toolkit/src

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Verify Installation

```bash
securepass --version
# Output: SecurePass Toolkit v1.0.0
```

---

## ⚡ Quick Start

### Check Password Strength

```bash
securepass check
```

You'll be prompted to enter a password (input is hidden). The tool will analyze it and display:
- Strength score (0-100)
- Entropy analysis
- Crack time estimates
- Security criteria checklist
- Breach database status
- Improvement recommendations

### Generate Secure Password

```bash
securepass generate --length 20
```

Creates a cryptographically secure random password and shows its strength analysis.

### Batch Analysis

```bash
# Create a file with passwords (one per line)
echo -e "password\nPassword123\nMyP@ssw0rd!2024" > passwords.txt

# Analyze the file
securepass batch passwords.txt
```

---

## 📘 Usage Examples

### Example 1: Interactive Password Check

```bash
$ securepass check

Enter password to analyze (input hidden):
Password: ********

Analyzing password...

======================================================================
  PASSWORD STRENGTH ANALYSIS
======================================================================

Strength Score: 85/100 [STRONG]

Entropy Analysis:
  Entropy: 62.3 bits
  Character Pool: 94 characters
  Password Length: 12 characters

Estimated Crack Time:
  Online Attack (100/sec):  146 trillion years
  Offline Attack (10B/sec): 146 years

Security Criteria:
  ✓ Minimum length (12+ characters)
  ✓ Contains lowercase letters
  ✓ Contains uppercase letters
  ✓ Contains digits
  ✓ Contains symbols
  ✓ No common patterns
  ✓ Not a dictionary word
  ✓ No sequential characters

Breach Database Check:
  ✓ Not found in breach database

Recommendations:
  ✓ Password meets security best practices

======================================================================
```

### Example 2: Generate Custom Password

```bash
$ securepass generate --length 16 --no-symbols --avoid-ambiguous

======================================================================
  GENERATED PASSWORD
======================================================================

  Kd7mPn9QwXz5Yx2T

======================================================================

⚠️  Copy this password to a secure location before closing!

Password Strength Analysis:
  Strength Score: 95/100 (VERY_STRONG)
  Entropy: 95.4 bits
  Character Pool: 62 characters
```

### Example 3: Batch Analysis with Export

```bash
$ securepass batch passwords.txt --export report.json --output json

Analyzing 50 passwords...
Progress: 10/50 20/50 30/50 40/50 50/50 

======================================================================
  BATCH ANALYSIS SUMMARY
======================================================================

Total Passwords Analyzed: 50

Strength Distribution:
  Weak:        15 (30.0%)
  Moderate:    20 (40.0%)
  Strong:      10 (20.0%)
  Very Strong:  5 (10.0%)

Breach Statistics:
  Passwords in breaches: 8 (16.0%)

Weakest Passwords (Top 5):
  1. Score:  15 | Hash: 5baa61e4c9b9...
  2. Score:  20 | Hash: 8621ffdbc5de...
  3. Score:  25 | Hash: 7c6a180b36ab...
  4. Score:  30 | Hash: e10adc3949ba...
  5. Score:  35 | Hash: 25f9e794323b...

Average Metrics:
  Average Score:   58.4/100
  Average Entropy: 52.8 bits
  Average Length:  10.2 characters

======================================================================

✓ Results exported to: report.json (JSON format)
```

### Example 4: Offline Mode (No Breach Check)

```bash
securepass check --no-breach
```

Skips the Have I Been Pwned API check for faster analysis or offline use.

---

## 🔒 Security Features

### 1. **K-Anonymity for Breach Checking**

When checking if a password has been breached, we implement k-anonymity:

```
1. Hash password with SHA-1 → 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
2. Send only first 5 chars → 5BAA6
3. Receive all hashes starting with 5BAA6
4. Check locally if full hash matches
```

**Your password NEVER leaves your machine.**

### 2. **Cryptographically Secure RNG**

Password generation uses Python's `secrets` module:

```python
# ✅ CORRECT - Cryptographically secure
password_char = secrets.choice(character_pool)

# ❌ WRONG - Not for security
password_char = random.choice(character_pool)
```

### 3. **No Plaintext Logging**

- Passwords are never logged or stored
- Only SHA-256 hashes in output (for audit trails)
- Secure input with `getpass` (no terminal echo)

### 4. **Type Safety & Input Validation**

- Full type hints throughout codebase
- Strict input validation (length limits, character sets)
- Protection against injection attacks

---

## 🎓 Educational Value

This project demonstrates understanding of:

### Cryptographic Concepts
- **SHA-1 Hashing**: Used for HIBP API (legacy, not for new systems)
- **SHA-256 Hashing**: Modern standard for password hashing
- **Shannon Entropy**: Mathematical measure of randomness
- **Entropy Formula**: `H = log₂(N) × L` where N=pool size, L=length

### Password Security Best Practices
- **NIST SP 800-63B**: Digital identity guidelines
- **OWASP Standards**: Secure password storage
- **Dictionary Attacks**: Why common words are dangerous
- **Brute Force**: Time complexity of password cracking

### Software Engineering
- **Modular Design**: Separation of concerns (SRP principle)
- **Test-Driven Development**: 111 unit tests, 91% coverage
- **CLI Development**: Professional command-line tools
- **API Integration**: External service communication

### Skills Demonstrated
- Python 3.8+ with type hints
- pytest testing framework
- API design and integration
- Security-focused coding
- Documentation and code quality

---

## 🏗️ Architecture

### Project Structure

```
securepass/
├── core/               # Business logic
│   ├── analyzer.py     # Main password analysis orchestration
│   ├── entropy.py      # Shannon entropy calculation
│   ├── generator.py    # Secure password generation
│   └── breach.py       # HIBP API integration
├── utils/              # Helper modules
│   ├── patterns.py     # Pattern detection (sequential, repeated)
│   └── wordlist.py     # Dictionary word checking
├── cli/                # User interface
│   ├── commands.py     # Command handlers (check, generate, batch)
│   └── formatters.py   # Output formatting with colors
└── models/             # Data structures
    └── analysis.py     # PasswordAnalysis dataclass
```

### Component Flow

```
User Input → CLI Parser → Command Handler → Analyzer
                                             ↓
                    Entropy ← Analyzer → Patterns
                    Breach  ← Analyzer → Wordlist
                                             ↓
                    Formatter ← Results → User Output
```

### Dependencies

**Core**:
- `requests` (2.31+): HTTPS API communication
- `colorama` (0.4.6+): Cross-platform colored output

**Development**:
- `pytest` (7.4+): Testing framework
- `pytest-cov`: Coverage reporting

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=securepass tests/

# Run specific test file
pytest tests/test_analyzer.py -v
```

### Test Coverage

```
Coverage Report:
- core/analyzer.py:    91%
- core/entropy.py:     90%
- core/generator.py:  100%
- core/breach.py:      86%
- utils/patterns.py:  100%
- utils/wordlist.py:   88%

Total: 111 tests, 91% core coverage
```

### Test Categories

- **Unit Tests**: Individual function testing
- **Integration Tests**: End-to-end password analysis
- **Edge Cases**: Empty inputs, extreme values
- **Security Tests**: Validates k-anonymity, secure RNG

---

## 📊 Performance

- Password analysis: < 100ms (local operations)
- Breach check: 200-500ms (network dependent)
- Batch processing: ~100 passwords/minute
- Memory usage: < 50MB

---

## 🤝 Contributing

This is an educational project, but improvements are welcome!

### Areas for Enhancement

- [ ] GUI version (Tkinter/PyQt)
- [ ] Password manager export formats
- [ ] Multi-language dictionary support
- [ ] ML-based pattern detection
- [ ] Passphrase generation (XKCD-style)

### Development Setup

```bash
# Clone and install
git clone https://github.com/Rblea97/password-security-toolkit.git
cd securepass-toolkit/src
pip install -e .[dev]

# Run tests before committing
pytest tests/ --cov=securepass

# Code style
pylint securepass/
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Have I Been Pwned](https://haveibeenpwned.com/)** - Troy Hunt's breach database API
- **[NIST SP 800-63B](https://pages.nist.gov/800-63-3/)** - Password security guidelines
- **[OWASP](https://owasp.org/)** - Security best practices
- **[Anthropic Claude](https://claude.ai)** - AI assistant used in development

---

## 📞 Contact

**Created by**: Richard Blea
**Email**: rblea97@gmail.com
**LinkedIn**: [linkedin.com/in/richard-blea](https://www.linkedin.com/in/richard-blea)
**GitHub**: [github.com/Rblea97](https://github.com/Rblea97)

---

## 🎯 Use Cases

### For Students
- Cybersecurity course projects
- Portfolio building
- Learning cryptographic concepts
- Understanding password security

### For Professionals
- Password policy auditing
- Security awareness training
- Quick password strength checks
- Batch credential analysis

### For Organizations
- Employee password audits
- Security training demonstrations
- Compliance verification
- Migration planning

---

## 🔮 Future Roadmap

### Version 2.0 (Planned)
- [ ] Web interface (Flask/FastAPI)
- [ ] Desktop GUI (Tkinter)
- [ ] Database integration (SQLite)
- [ ] Historical tracking
- [ ] Custom wordlists

### Version 3.0 (Envisioned)
- [ ] Machine learning password strength prediction
- [ ] Multi-language support
- [ ] Enterprise features (SSO, audit logs)
- [ ] Cloud deployment option

---

**⭐ If you found this project helpful, please consider starring it on GitHub!**

**Built with ❤️ for the cybersecurity community**
