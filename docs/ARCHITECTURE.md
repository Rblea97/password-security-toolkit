# Architecture

## System Overview

```mermaid
graph TD
    A[User] -->|CLI Input| B[Argument Parser]
    B --> C{Command}
    C -->|check| D[Check Handler]
    C -->|generate| E[Generate Handler]
    C -->|batch| F[Batch Handler]
    D --> G[Password Analyzer]
    E --> H[Password Generator]
    F --> G
    H --> G
    G --> I[Entropy Calculator]
    G --> J[Pattern Detector]
    G --> K[Wordlist Checker]
    G --> L[Breach Checker]
    G --> M[PasswordAnalysis Result]
    M --> N[Output Formatter]
    N --> A
```

## Components

### Core Modules

#### `core/analyzer.py` — Password Analyzer
The main orchestrator. Takes a password string, coordinates all analysis sub-components, and returns a `PasswordAnalysis` result object. Computes the overall strength score (0-100) by weighting entropy, character diversity, pattern presence, and breach status.

#### `core/entropy.py` — Entropy Calculator
Computes Shannon entropy in bits using the formula `H = log2(N) * L` where N is the character pool size and L is the password length. Also estimates crack times for online (100 attempts/sec) and offline (10 billion attempts/sec) scenarios.

#### `core/breach.py` — Breach Checker (HIBP)
Integrates with the Have I Been Pwned Passwords API using k-anonymity. Only the first 5 characters of the SHA-1 hash are sent over the network.

#### `core/generator.py` — Password Generator
Generates cryptographically secure passwords using Python's `secrets` module. Supports customizable length, character sets, and ambiguous character exclusion.

### Utility Modules

#### `utils/patterns.py` — Pattern Detector
Detects sequential characters (`abc`, `123`), repeated characters (`aaa`), keyboard patterns (`qwerty`), and other common weak patterns.

#### `utils/wordlist.py` — Wordlist Checker
Checks passwords against a dictionary of common words and known weak passwords.

### Interface

#### `cli/commands.py` — Command Handlers
Implements the `check`, `generate`, and `batch` subcommands. Handles argument parsing, user input (secure via `getpass`), and output coordination.

#### `cli/formatters.py` — Output Formatter
Renders analysis results with colorized output (red/yellow/green) using `colorama`. Formats scores, entropy, crack times, and recommendations.

### Data Models

#### `models/analysis.py` — PasswordAnalysis
A dataclass holding all analysis results: score, entropy, crack times, criteria results, breach status, and recommendations.

## K-Anonymity Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant A as Analyzer
    participant B as Breach Checker
    participant H as HIBP API

    U->>A: password string
    A->>B: check_breach(password)
    B->>B: SHA-1 hash password
    B->>B: Extract first 5 chars (prefix)
    B->>H: GET /range/{prefix}
    H-->>B: All hashes matching prefix
    B->>B: Compare full hash locally
    B-->>A: (found: bool, count: int)
    A-->>U: Breach status in results
```

## Security Design Decisions

| Decision | Rationale |
|----------|-----------|
| `secrets` not `random` | CSPRNG required for password generation |
| K-anonymity for HIBP | Full password hash never leaves the machine |
| `getpass` for input | Passwords not echoed to terminal |
| No plaintext logging | Passwords never written to disk or logs |
| Input length limits | Prevents resource exhaustion |

## Data Flow

```mermaid
graph LR
    A[Raw Password] --> B[SHA-1 Hash]
    B --> C[First 5 Chars]
    C --> D[HIBP API]
    D --> E[Hash Suffix List]
    E --> F{Local Match?}
    F -->|Yes| G[Breached]
    F -->|No| H[Not Breached]

    A --> I[Character Analysis]
    I --> J[Entropy Calculation]
    I --> K[Pattern Detection]
    I --> L[Dictionary Check]
    J --> M[Score Aggregation]
    K --> M
    L --> M
    F --> M
    M --> N[Final Score 0-100]
```
