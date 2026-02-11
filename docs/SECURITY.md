# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Contact:** rblea97@gmail.com

- You will receive an acknowledgment within 48 hours.
- A fix will be prioritized based on severity.
- Please do not open public issues for security vulnerabilities.

## Security Practices

### K-Anonymity for Breach Detection
Passwords are never sent over the network. Only the first 5 characters of the SHA-1 hash are transmitted to the Have I Been Pwned API. The full hash comparison happens locally.

### Cryptographically Secure Random Number Generation
All password generation uses Python's `secrets` module, which provides access to the operating system's CSPRNG. The `random` module is never used for security-sensitive operations.

### No Plaintext Storage
- Passwords are never logged, stored, or written to disk.
- Terminal input uses `getpass` to suppress echo.
- Only truncated hash representations appear in batch output (for identification, not reversal).

### Input Validation
- Password length limits prevent resource exhaustion.
- Character encoding is validated before processing.
- File paths for batch operations are sanitized.

## Known Limitations

- **SHA-1 for HIBP:** The Have I Been Pwned API requires SHA-1 hashes. SHA-1 is used solely for API compatibility, not for password storage.
- **Network dependency:** Breach checking requires internet access. Use `--no-breach` for offline operation.
- **Local dictionary:** The wordlist is not exhaustive. It covers common passwords and English words but not all languages.

## Security Roadmap

- [ ] Add support for custom wordlists
- [ ] Implement rate limiting for batch HIBP checks
- [ ] Add SBOM generation to CI pipeline
- [ ] Integrate with additional breach databases
