# SecurePass Toolkit - Usage Examples

This directory contains example files and demonstrations for SecurePass Toolkit.

## Files

- `sample_passwords.txt` - Sample passwords for batch analysis testing
- `EXAMPLES.md` - This file with detailed usage examples

---

## Example 1: Basic Password Check

Check the strength of a single password interactively:

```bash
$ securepass check

Enter password to analyze (input hidden):
Password: ********

Analyzing password...

======================================================================
  PASSWORD STRENGTH ANALYSIS
======================================================================

Strength Score: 35/100 [WEAK]

Entropy Analysis:
  Entropy: 37.6 bits
  Character Pool: 26 characters
  Password Length: 8 characters

Estimated Crack Time:
  Online Attack (100/sec):  66.2 years
  Offline Attack (10B/sec): 20.9 seconds

Security Criteria:
  ✗ Minimum length (12+ characters)
  ✓ Contains lowercase letters
  ✗ Contains uppercase letters
  ✗ Contains digits
  ✗ Contains symbols
  ✗ No common patterns
  ✗ Not a dictionary word
  ✓ No sequential characters

Breach Database Check:
  ⚠️  FOUND in 3,861,493 data breaches!
      ⚠️  Change this password immediately!

Recommendations:
  • Increase length to at least 12 characters for better security
  • Add uppercase letters (A-Z)
  • Add numbers (0-9)
  • Add symbols (!@#$%^&* etc.)
  • ⚠️ Contains common pattern. Use unique password
  • ⚠️ Contains dictionary word. Avoid common words
  • 🚨 CRITICAL: Password found in 3,861,493 data breaches! Change immediately!

======================================================================
```

---

## Example 2: Generate Secure Password (Default Settings)

Generate a 16-character password with all character types:

```bash
$ securepass generate

======================================================================
  GENERATED PASSWORD
======================================================================

  K7$mP9@nQ2#wX5zT

======================================================================

⚠️  Copy this password to a secure location before closing!

Password Strength Analysis:
  Strength Score: 100/100 (VERY_STRONG)
  Entropy: 104.9 bits
  Character Pool: 94 characters
```

---

## Example 3: Generate Custom Password

Generate a 20-character password without symbols:

```bash
$ securepass generate --length 20 --no-symbols

======================================================================
  GENERATED PASSWORD
======================================================================

  Kd7mPn9QwXz5Yx2TaB3c

======================================================================

⚠️  Copy this password to a secure location before closing!

Password Strength Analysis:
  Strength Score: 100/100 (VERY_STRONG)
  Entropy: 118.3 bits
  Character Pool: 62 characters
```

---

## Example 4: Batch Analysis

Analyze multiple passwords from a file:

```bash
$ securepass batch sample_passwords.txt

Analyzing 10 passwords...
Progress: 10/10 

======================================================================
  BATCH ANALYSIS SUMMARY
======================================================================

Total Passwords Analyzed: 10

Strength Distribution:
  Weak:          4 (40.0%)
  Moderate:      2 (20.0%)
  Strong:        2 (20.0%)
  Very Strong:   2 (20.0%)

Breach Statistics:
  Passwords in breaches: 3 (30.0%)

Weakest Passwords (Top 5):
  1. Score:  10 | Hash: 5baa61e4c9b9...
  2. Score:  15 | Hash: 8d969eef6eca...
  3. Score:  20 | Hash: 8621ffdbc5de...
  4. Score:  35 | Hash: 5f4dcc3b5aa7...
  5. Score:  45 | Hash: e10adc3949ba...

Average Metrics:
  Average Score:   52.5/100
  Average Entropy: 55.3 bits
  Average Length:  12.4 characters

======================================================================
```

---

## Example 5: Batch Analysis with JSON Export

Export results to JSON format:

```bash
$ securepass batch sample_passwords.txt --export results.json --output json

Analyzing 10 passwords...
Progress: 10/10 

[Summary displayed...]

✓ Results exported to: results.json (JSON format)
```

**results.json** (sample):
```json
[
  {
    "password_hash": "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8",
    "timestamp": "2026-02-10T10:30:45.123456",
    "strength_score": 10,
    "strength_rating": "weak",
    "length": 8,
    "entropy_bits": 37.6,
    "character_pool_size": 26,
    "criteria_met": {
      "min_length": false,
      "has_lowercase": true,
      "has_uppercase": false,
      "has_digits": false,
      "has_symbols": false,
      "no_common_patterns": false,
      "no_dictionary_words": false,
      "no_sequential_chars": true
    },
    "breach_status": {
      "checked": true,
      "found": true,
      "occurrence_count": 3861493
    },
    "recommendations": [
      "⚠️ CRITICAL: Password is too short. Use at least 8 characters (12+ recommended)",
      "Add uppercase letters (A-Z)",
      "Add numbers (0-9)",
      "Add symbols (!@#$%^&* etc.)",
      "⚠️ Contains common pattern. Use unique password",
      "⚠️ Contains dictionary word. Avoid common words",
      "🚨 CRITICAL: Password found in 3,861,493 data breaches! Change immediately!"
    ],
    "estimated_crack_time": {
      "online_attack_100_per_second": "66.2 years",
      "offline_attack_10B_per_second": "20.9 seconds"
    }
  }
]
```

---

## Example 6: Offline Mode (No Breach Check)

Skip breach checking for faster analysis or offline use:

```bash
$ securepass check --no-breach

[Analysis runs without checking Have I Been Pwned API]

Breach Database Check:
  ⚠ Breach check skipped
```

---

## Example 7: Generate Password Without Ambiguous Characters

Avoid characters that look similar (0/O, 1/l/I):

```bash
$ securepass generate --length 16 --avoid-ambiguous

======================================================================
  GENERATED PASSWORD
======================================================================

  Kd7mPn9QwXz5Yx2T

======================================================================

[No 0, O, 1, l, or I characters in the password]
```

---

## Example 8: CSV Export for Spreadsheet Analysis

Export batch results to CSV:

```bash
$ securepass batch sample_passwords.txt --export results.csv --output csv

✓ Results exported to: results.csv (CSV format)
```

**results.csv** can be opened in Excel, Google Sheets, etc. for further analysis.

---

## Tips & Best Practices

### For Students
1. Use batch analysis to understand password patterns in datasets
2. Compare entropy between different password types
3. Study the relationship between length and crack time
4. Experiment with different character sets in generation

### For Security Audits
1. Always use `--no-breach` flag for sensitive environments
2. Export results for documentation and reporting
3. Use batch mode for efficiency with large datasets
4. Review the "Weakest Passwords" section first

### For Personal Use
1. Generate passwords with at least 16 characters
2. Include all character types (default settings)
3. Check existing passwords for breaches regularly
4. Don't reuse passwords across services

---

## Common Use Cases

### Use Case 1: Password Policy Compliance
```bash
# Check if passwords meet minimum 12-character requirement
securepass batch employee_passwords.txt | grep "Weak:"
```

### Use Case 2: Generate Passwords for Multiple Accounts
```bash
# Generate 5 different passwords
for i in {1..5}; do
  echo "Password $i:"
  securepass generate --length 20
  echo ""
done
```

### Use Case 3: Security Training Demonstration
```bash
# Show difference between weak and strong passwords
echo "Weak password: password123"
echo "password123" | securepass check

echo ""
echo "Strong password: K7\$mP9@nQ2#wX5"
securepass check  # Then enter the strong password
```

---

## Troubleshooting

### "Command not found: securepass"
**Solution**: Make sure you've run `pip install -e .` in the src/ directory.

### "Network timeout" error
**Solution**: Use `--no-breach` flag to skip online breach checking.

### "File not found" error
**Solution**: Provide the full path to your password file: 
```bash
securepass batch /full/path/to/passwords.txt
```

---

## More Information

For complete documentation, see [README.md](../README.md)

For source code and tests, see the parent directory structure.
