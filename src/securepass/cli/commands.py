"""
CLI Command Handlers Module

Implements the logic for each CLI command:
- check: Interactive password analysis
- generate: Secure password generation
- batch: Batch file analysis
"""

import getpass
import sys
import json
import csv
from typing import List
from argparse import Namespace

from ..core.analyzer import analyze_password
from ..core.generator import generate_password
from ..models.analysis import PasswordAnalysis
from .formatters import format_analysis_text, format_analysis_json, format_batch_summary


def cmd_check(args: Namespace) -> int:
    """
    Handle 'check' command - interactive password analysis.

    Prompts user for password (secure input with no echo),
    analyzes it, and displays formatted results.

    Args:
        args: Parsed command-line arguments
              - no_breach: Skip breach checking
              - verbose: Show additional details

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Secure password input (no echo to terminal)
        print("Enter password to analyze (input hidden):")
        password = getpass.getpass(prompt="Password: ")

        if not password:
            print("Error: No password entered")
            return 1

        # Analyze password
        print("\nAnalyzing password...")
        check_breach_status = not args.no_breach

        result = analyze_password(password, check_breach_status=check_breach_status)

        # Format and display results
        output = format_analysis_text(result, verbose=args.verbose)
        print(output)

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nError during analysis: {e}")
        return 1


def cmd_generate(args: Namespace) -> int:
    """
    Handle 'generate' command - secure password generation.

    Generates a cryptographically secure password with specified
    parameters, then analyzes and displays it.

    Args:
        args: Parsed command-line arguments
              - length: Password length
              - no_symbols: Exclude symbols
              - no_uppercase: Exclude uppercase
              - no_digits: Exclude digits
              - avoid_ambiguous: Avoid ambiguous characters

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Generate password with specified parameters
        password = generate_password(
            length=args.length,
            use_lowercase=True,  # Always include lowercase
            use_uppercase=not args.no_uppercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            avoid_ambiguous=args.avoid_ambiguous,
        )

        # Display generated password prominently
        print("\n" + "=" * 70)
        print("  GENERATED PASSWORD")
        print("=" * 70)
        print(f"\n  {password}\n")
        print("=" * 70)
        print("\n⚠️  Copy this password to a secure location before closing!")
        print()

        # Analyze the generated password
        print("Password Strength Analysis:")
        result = analyze_password(password, check_breach_status=False)

        # Show key metrics only (not full report)
        print(
            f"  Strength Score: {result.strength_score}/100 ({result.strength_rating.upper()})"
        )
        print(f"  Entropy: {result.entropy_bits:.1f} bits")
        print(f"  Character Pool: {result.character_pool_size} characters")
        print()

        return 0

    except ValueError as e:
        print(f"\nError: {e}")
        return 1
    except Exception as e:
        print(f"\nError during password generation: {e}")
        return 1


def cmd_batch(args: Namespace) -> int:
    """
    Handle 'batch' command - analyze passwords from file.

    Reads passwords from file (one per line), analyzes each,
    generates summary report, and optionally exports results.

    Args:
        args: Parsed command-line arguments
              - file: Input file path
              - output: Output format (text/json/csv)
              - export: Export file path
              - no_breach: Skip breach checking

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Read passwords from file
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            return 1
        except PermissionError:
            print(f"Error: Permission denied: {args.file}")
            return 1

        if not passwords:
            print("Error: No passwords found in file")
            return 1

        print(f"\nAnalyzing {len(passwords)} passwords...")
        print("Progress: ", end="", flush=True)

        # Analyze all passwords
        results: List[PasswordAnalysis] = []
        check_breach_status = not args.no_breach

        for i, password in enumerate(passwords, 1):
            try:
                result = analyze_password(
                    password, check_breach_status=check_breach_status
                )
                results.append(result)

                # Progress indicator
                if i % 10 == 0 or i == len(passwords):
                    print(f"{i}/{len(passwords)}", end=" ", flush=True)
            except Exception as e:
                print(f"\nWarning: Failed to analyze password #{i}: {e}")
                continue

        print("\n")

        if not results:
            print("Error: No passwords were successfully analyzed")
            return 1

        # Display summary
        summary = format_batch_summary(results)
        print(summary)

        # Export if requested
        if args.export:
            try:
                if args.output == "json":
                    _export_json(results, args.export)
                    print(f"✓ Results exported to: {args.export} (JSON format)")
                elif args.output == "csv":
                    _export_csv(results, args.export)
                    print(f"✓ Results exported to: {args.export} (CSV format)")
                else:  # text
                    _export_text(results, args.export)
                    print(f"✓ Results exported to: {args.export} (TXT format)")
            except Exception as e:
                print(f"Warning: Failed to export results: {e}")
                return 1

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nError during batch analysis: {e}")
        return 1


def _export_json(results: List[PasswordAnalysis], filepath: str) -> None:
    """Export results to JSON file."""
    data = [result.to_dict() for result in results]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _export_csv(results: List[PasswordAnalysis], filepath: str) -> None:
    """Export results to CSV file."""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(PasswordAnalysis.csv_header())
        for result in results:
            writer.writerow(result.to_csv_row())


def _export_text(results: List[PasswordAnalysis], filepath: str) -> None:
    """Export results to text file."""
    with open(filepath, "w", encoding="utf-8") as f:
        for i, result in enumerate(results, 1):
            f.write(f"Password #{i}\n")
            f.write(format_analysis_text(result, verbose=True))
            f.write("\n" + "=" * 70 + "\n\n")
