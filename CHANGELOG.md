# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-10

### Added
- Password strength analysis with 0-100 scoring system
- Shannon entropy calculation with crack time estimates
- Have I Been Pwned breach detection using k-anonymity
- Cryptographically secure password generation via `secrets` module
- Batch password analysis with JSON/CSV/text export
- Colorized CLI output with strength indicators
- 8 security criteria checks (length, character diversity, patterns, dictionary words)
- Customizable password generation (length, character sets, ambiguous character exclusion)
- Offline mode (skip breach checking)
- Comprehensive test suite (111 tests, 92% coverage)
- Full type hints throughout codebase
- Google-style docstrings

### Security
- K-anonymity for HIBP API calls (only first 5 SHA-1 hash characters transmitted)
- CSPRNG via Python `secrets` module (not `random`)
- No plaintext password logging or storage
- Secure terminal input with `getpass`
- Input validation and length limits
