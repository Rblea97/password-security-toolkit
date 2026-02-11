# SecurePass Toolkit

[![Tests](https://github.com/Rblea97/password-security-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/Rblea97/password-security-toolkit/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)](https://github.com/Rblea97/password-security-toolkit)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Security: A+](https://img.shields.io/badge/security-A%2B-brightgreen)](docs/SECURITY.md)

A command-line tool for password strength analysis, breach detection, and secure generation. Built with real-world security practices including k-anonymity, CSPRNG, and NIST-aligned scoring.

---

## Why This Matters

Weak passwords remain one of the top causes of security breaches. This tool gives users and auditors a fast, privacy-preserving way to:

- **Analyze** password strength with entropy-based scoring (0-100)
- **Detect** if a password appears in known data breaches (850M+ passwords via HIBP)
- **Generate** cryptographically secure passwords
- **Audit** password lists in batch with exportable reports

All breach checking uses **k-anonymity** — your password never leaves your machine.

---

## Features

### Password Strength Analysis
- 0-100 scoring system based on entropy, character diversity, and pattern detection
- Shannon entropy calculation with estimated crack times
- 8 security criteria checks (length, character classes, patterns, dictionary words)
- Actionable improvement recommendations

### Breach Detection (Have I Been Pwned)
- Checks passwords against 850M+ known breached passwords
- K-anonymity protocol: only first 5 SHA-1 hash characters are transmitted
- Full hash comparison happens locally on your machine

### Secure Password Generation
- Cryptographically secure via Python's `secrets` module
- Configurable length, character sets, and ambiguous character exclusion
- Generated passwords are automatically strength-analyzed

### Batch Processing
- Analyze password lists from files
- Summary statistics with weakest-password identification
- Export to JSON, CSV, or text format

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/Rblea97/password-security-toolkit.git
cd password-security-toolkit/src
pip install -e .

# Check a password (input is hidden)
securepass check

# Generate a secure password
securepass generate --length 20

# Batch analyze a file
securepass batch passwords.txt --export report.json
```

---

## Security Design

| Practice | Implementation |
|----------|---------------|
| Breach checking | K-anonymity — only 5 hash chars sent to HIBP API |
| Password generation | `secrets` module (CSPRNG), never `random` |
| User input | `getpass` — no terminal echo |
| Storage | No plaintext logging or persistence |
| Validation | Input length limits, character encoding checks |

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed component design and data flow diagrams.

---

## Skills Demonstrated

This project showcases:

- **Python**: 1,697 LOC with full type hints and Google-style docstrings
- **Security engineering**: K-anonymity, CSPRNG, NIST/OWASP alignment
- **Testing**: 111 unit tests, 92% coverage, mocked external dependencies
- **CI/CD**: GitHub Actions for testing (Python 3.9-3.12), linting, and security scanning
- **Software design**: Modular architecture, separation of concerns, dataclass models
- **DevOps**: Dependabot, automated security audits (Bandit, pip-audit)
- **Documentation**: Architecture diagrams (Mermaid), security policy, contributing guide

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/ARCHITECTURE.md) | System design, component diagrams, data flow |
| [Security Policy](docs/SECURITY.md) | Vulnerability reporting, security practices |
| [Contributing](docs/CONTRIBUTING.md) | Development setup, code standards, PR process |
| [AI Workflow](docs/AI_WORKFLOW.md) | Structured AI-assisted development methodology |
| [Changelog](CHANGELOG.md) | Version history |

---

## About the Author

**Richard Blea** — Cybersecurity student seeking entry-level security roles (available June 2026).

- Email: rblea97@gmail.com
- LinkedIn: [linkedin.com/in/richard-blea](https://www.linkedin.com/in/richard-blea)
- GitHub: [github.com/Rblea97](https://github.com/Rblea97)

---

## License

[MIT](LICENSE) - Copyright (c) 2026 Richard Blea
